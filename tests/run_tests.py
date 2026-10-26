"""Unit tests: every method is checked against an independent computation (a loop, a closed formula, another
library function) or against the printed output of version 1. Run from the repository root:
python tests/run_tests.py"""
import sys
from pathlib import Path

import numpy as np
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from usdtrend import basket, centered_ma, exp_trend, load, load_v1, log100, month_effects  # noqa: E402
from usdtrend.methods import f_drift, f_random_walk, f_ses, rolling_forecast_errors  # noqa: E402

FAILED = []


def check(label, ok):
    print(("ok   " if ok else "FAIL ") + label)
    if not ok:
        FAILED.append(label)


df = load()
rates = basket(df)
check("data: 177 consecutive months, January 2012 to September 2026",
      len(df) == 177 and str(df.index[0]) == "2012-01" and str(df.index[-1]) == "2026-09")
check("basket rate is the mean of the buying and selling rate",
      np.allclose(rates["usd"], (df.usd_buying_try + df.usd_selling_try) / 2))

v1 = load_v1()
common = v1.index.intersection(df.index)
same = (np.abs(df.loc[common] - v1.loc[common]) < 1e-6).all(axis=1)
diff = [str(m) for m in common[~same.values]]
check("EVDS file equals version 1's file in every common month except six (listed in NEWS.md)",
      len(common) == 151 and diff == ["2017-08", "2017-09", "2018-01", "2018-04", "2018-05", "2024-10"])

y = np.random.default_rng(1).normal(size=40).cumsum()
cma = centered_ma(y, 12).values
loop = np.full(40, np.nan)
for t in range(6, 34):
    loop[t] = (0.5 * y[t - 6] + y[t - 5:t + 6].sum() + 0.5 * y[t + 6]) / 12
check("2 x 12 centred moving average equals the weighted sum written out", np.allclose(cma, loop, equal_nan=True))
check("odd-period centred average equals the plain 5-month mean",
      np.allclose(centered_ma(y, 5).values[2:-2], [y[t - 2:t + 3].mean() for t in range(2, 38)]))

fit, fitted, dw = exp_trend(y)
b = np.polyfit(np.arange(1, 41), y, 1)
e = y - fitted
check("exponential trend: OLS slope equals numpy.polyfit", np.isclose(fit.params[1], b[0]))
check("Durbin-Watson equals sum of squared changes of residuals over their sum of squares",
      np.isclose(dw, np.sum(np.diff(e) ** 2) / np.sum(e ** 2)))

g = log100(rates["usd"]).diff().dropna()
_, p_f, f, p_kw = month_effects(g.values, g.index.month)
groups = [g.values[g.index.month == k] for k in range(1, 13)]
check("F test of 11 month dummies equals one-way ANOVA", np.isclose(p_f, stats.f_oneway(*groups).pvalue))
check("Kruskal-Wallis p equals scipy.stats.kruskal", np.isclose(p_kw, stats.kruskal(*groups).pvalue))

x = np.array([1.0, 2.0, 4.0, 7.0])
check("random walk and drift forecasts", np.allclose(f_random_walk(x, 2), [7, 7]) and np.allclose(f_drift(x, 2), [9, 11]))
s = np.random.default_rng(2).normal(size=60).cumsum() + 100
from statsmodels.tsa.holtwinters import ExponentialSmoothing  # noqa: E402
m = ExponentialSmoothing(s, trend=None).fit()
a, lvl = m.params["smoothing_level"], m.params["initial_level"]
for v in s:
    lvl = a * v + (1 - a) * lvl
check("simple exponential smoothing forecast equals the level recursion", np.isclose(f_ses(s, 1)[0], lvl))

z = np.arange(50, dtype=float)
e1 = rolling_forecast_errors(z, {"rw": f_random_walk}, (1, 3), 10)
z2 = z.copy()
z2[-1] = 1e6
e2 = rolling_forecast_errors(z2, {"rw": f_random_walk}, (1, 3), 10)
check("out-of-sample: changing the last month changes only the errors for that target month",
      np.allclose(e1["rw"][1][:-1], e2["rw"][1][:-1]) and np.allclose(e1["rw"][3][:-1], e2["rw"][3][:-1])
      and len(e1["rw"][1]) == 10 and len(e1["rw"][3]) == 10)

r1 = basket(v1)["usd"]
fit1 = sm.OLS(np.log(r1.values), sm.add_constant(np.arange(1, len(r1) + 1))).fit()
ma3 = r1.rolling(3).mean()
check("version 1: exponential trend R^2 0.945, last basket rate 34.20, last 3-month average 33.93",
      round(fit1.rsquared, 3) == 0.945 and round(r1.iloc[-1], 2) == 34.20 and round(ma3.iloc[-1], 2) == 33.93)

print(f"\n{len(FAILED)} check(s) failed.")
sys.exit(1 if FAILED else 0)

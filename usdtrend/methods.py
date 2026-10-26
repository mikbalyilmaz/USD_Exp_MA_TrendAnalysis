"""Trend methods of the course week: moving averages, the exponential trend, a test for monthly seasonality and
exponential smoothing, with an out-of-sample comparison of the forecasts.

All series are 100 log of the exchange rate, so differences are monthly changes in per cent (log points).

Author: Muhammed Ikbal Yilmaz
"""

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def centered_ma(y, period=12):
    """Centred moving average. For an even period p it is the 2 x p average: weights 1/(2p) at the two ends and
    1/p inside, over p + 1 months; for an odd period, the plain average of p months centred on t. The first and
    last p/2 values are missing."""
    y = pd.Series(y)
    if period % 2:
        return y.rolling(period, center=True).mean()
    w = np.r_[0.5, np.ones(period - 1), 0.5] / period
    return y.rolling(period + 1, center=True).apply(lambda v: float(np.dot(v, w)), raw=True)


def trailing_ma(y, window=3):
    """Average of the current and the previous window - 1 months (what version 1 computed)."""
    return pd.Series(y).rolling(window).mean()


def exp_trend(y):
    """OLS of y_t = a + b t + u_t, t = 1, ..., n (an exponential trend in the level when y is 100 log).
    Returns the fit, the fitted values and the Durbin-Watson statistic of the residuals."""
    y = np.asarray(y, float)
    t = np.arange(1, len(y) + 1)
    fit = sm.OLS(y, sm.add_constant(t)).fit()
    return fit, fit.fittedvalues, float(sm.stats.stattools.durbin_watson(fit.resid))


def month_effects(growth, months):
    """Monthly seasonality of a growth series: OLS on a constant and 11 month dummies (F test that the 11
    coefficients are zero) and the Kruskal-Wallis test across the 12 months. Returns the mean growth of each
    calendar month with its standard error, and the two p-values."""
    g = np.asarray(growth, float)
    m = np.asarray(months)
    X = sm.add_constant(pd.get_dummies(pd.Categorical(m, categories=range(1, 13)), drop_first=True).astype(float))
    fit = sm.OLS(g, X).fit()
    rows = []
    for k in range(1, 13):
        gk = g[m == k]
        rows.append({"month": k, "n": len(gk), "mean": gk.mean(), "se": gk.std(ddof=1) / np.sqrt(len(gk))})
    kw = stats.kruskal(*[g[m == k] for k in range(1, 13)]).pvalue
    return pd.DataFrame(rows), float(fit.f_pvalue), float(fit.fvalue), float(kw)


# forecasting methods: each takes the history x (100 log) and a horizon h and returns h forecasts
def f_random_walk(x, h):
    return np.full(h, x[-1])


def f_drift(x, h):
    """Random walk with drift: the last value plus h times the mean monthly change of the history."""
    d = (x[-1] - x[0]) / (len(x) - 1)
    return x[-1] + d * np.arange(1, h + 1)


def f_exp_trend(x, h):
    """Exponential trend fitted by OLS to the history, extended h months."""
    b = np.polyfit(np.arange(len(x)), x, 1)
    return np.polyval(b, np.arange(len(x), len(x) + h))


def _es(x, h, **kw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return np.asarray(ExponentialSmoothing(np.asarray(x, float), **kw).fit().forecast(h))


def f_ses(x, h):
    return _es(x, h, trend=None)


def f_holt(x, h):
    return _es(x, h, trend="add")


def f_damped_holt(x, h):
    return _es(x, h, trend="add", damped_trend=True)


def f_holt_winters(x, h):
    return _es(x, h, trend="add", seasonal="add", seasonal_periods=12)


METHODS = {"Random walk": f_random_walk, "Random walk with drift": f_drift, "Exponential trend": f_exp_trend,
           "Simple exponential smoothing": f_ses, "Holt": f_holt, "Damped Holt": f_damped_holt,
           "Holt-Winters (additive seasonal)": f_holt_winters}


def rolling_forecast_errors(y, methods, horizons, test_months):
    """Expanding-window evaluation. For every forecast origin, each method is fitted on the months up to the
    origin only and forecasts h months ahead; errors are collected for the target months among the last
    `test_months` months. Returns {method: {h: array of errors}}."""
    y = np.asarray(y, float)
    n, hmax = len(y), max(horizons)
    first_target = n - test_months
    errors = {m: {h: [] for h in horizons} for m in methods}
    for origin in range(first_target - hmax, n - 1):
        x = y[:origin + 1]
        for name, f in methods.items():
            fc = f(x, hmax)
            for h in horizons:
                target = origin + h
                if first_target <= target < n:
                    errors[name][h].append(y[target] - fc[h - 1])
    return {m: {h: np.array(v) for h, v in d.items()} for m, d in errors.items()}


def rmse(e):
    return float(np.sqrt(np.mean(np.square(e))))

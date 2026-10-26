"""Analysis 1: the trend of the exchange rates, with moving averages and the exponential trend of version 1.

Why: version 1 fitted an exponential trend, log(rate) = a + b t, and judged it by R^2; it also drew a 3-month
moving average and described it as centred. A trend estimate is only useful if what is left over behaves like
noise. This script measures the growth of both rates, compares the trailing average of version 1 with the
centred 2 x 12 average, and checks the residuals of the exponential trend.

Outputs: Table 1 (table1_data.csv), Table 2 (table2_exp_trend.csv), Figure 1 (fig1_trend).
"""
import warnings

import numpy as np
from statsmodels.tsa.stattools import adfuller

from common import LOGS, NAMES, RATES, dates, save_table
from usdtrend import centered_ma, exp_trend
from usdtrend.style import BLUE, INK, MUTED, end_label, fit_axis, free_axis, save_figure, tick_axis, use_style

warnings.filterwarnings("ignore", message="adfuller currently returns")   # newer statsmodels; same numbers
idx = RATES.index
rows = [{"first_month": str(idx[0]), "last_month": str(idx[-1]), "months": len(idx),
         **{f"{c}_first": float(RATES[c].iloc[0]) for c in RATES},
         **{f"{c}_last": float(RATES[c].iloc[-1]) for c in RATES},
         **{f"{c}_ratio": float(RATES[c].iloc[-1] / RATES[c].iloc[0]) for c in RATES},
         **{f"{c}_mean_monthly_change_pct": float(LOGS[c].diff().mean()) for c in RATES}}]
save_table(rows, "table1_data")

trend_rows = []
for c in RATES:
    fit, fitted, dw = exp_trend(LOGS[c].values)
    resid = LOGS[c].values - fitted
    r1 = float(np.corrcoef(resid[1:], resid[:-1])[0, 1])
    cma = centered_ma(LOGS[c].values, 12)
    trend_rows.append({"series": c, "b_pct_per_month": float(fit.params[1]), "se_b": float(fit.bse[1]),
                       "r2": float(fit.rsquared), "durbin_watson": dw, "resid_autocorr_lag1": r1,
                       "resid_min": float(resid.min()), "resid_max": float(resid.max()),
                       "cma_missing_each_end": int(np.isnan(cma.values[:12]).sum()),
                       "adf_p_level_ct": float(adfuller(LOGS[c].values, regression="ct", autolag="AIC")[1]),
                       "adf_p_change_c": float(adfuller(LOGS[c].diff().dropna().values, regression="c", autolag="AIC")[1])})
    print(trend_rows[-1])
save_table(trend_rows, "table2_exp_trend")

use_style()


def draw():
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(4.75, 2.25), constrained_layout=True, gridspec_kw={"width_ratios": [1.1, 1]})
    x = dates(idx)
    ax = axes[0]
    for c, col in (("usd", INK), ("eur", BLUE)):
        ax.plot(x, RATES[c], color=col, lw=1.3)
        end_label(ax, x[-1], RATES[c].iloc[-1], NAMES[c], col, va="bottom" if c == "eur" else "top")
    cma = np.exp(centered_ma(LOGS["usd"].values, 12) / 100)
    ax.plot(x, cma, color=MUTED, lw=1.0, ls="--")
    tick_axis(ax, "y", [1, 2, 5, 10, 20, 50, 100], log=True, fmt="{:g}")
    ax.set_title("(a) TRY per unit, log scale")
    ax = axes[1]
    for c, col in (("usd", INK), ("eur", BLUE)):
        _, fitted, _ = exp_trend(LOGS[c].values)
        ax.plot(x, LOGS[c].values - fitted, color=col, lw=1.3)
    ax.axhline(0, color=INK, lw=0.6)
    fit_axis(ax, "y", [LOGS[c].values - exp_trend(LOGS[c].values)[1] for c in RATES], 20)
    ax.set_title("(b) Deviation from exp. trend, %")
    for a in axes:
        a.xaxis.set_major_locator(mdates.YearLocator(4))
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        free_axis(a, "x")
    return fig


save_figure("fig1_trend", draw, lambda: "Figure 1. The two rates and what an exponential trend leaves over")

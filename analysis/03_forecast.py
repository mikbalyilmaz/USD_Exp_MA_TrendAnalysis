"""Analysis 3: which trend method forecasts the next months best?

Why: the smoothing methods of the course week (simple exponential smoothing, Holt, damped Holt, Holt-Winters) and
the exponential trend of version 1 are all ways of extrapolating a trend. They are compared with the random walk
and the random walk with drift on months they were not fitted on: for every month of the last five years each
method is fitted on the months before it only and forecasts 1, 3 and 12 months ahead (expanding window). The
series is 100 log of the rate, so errors are in per cent (log points).

Outputs: Table 5 (table5_forecast_rmse.csv), Figure 3 (fig3_forecast).
"""
import numpy as np

from common import LOGS, NAMES, RATES, save_table
from usdtrend import METHODS, rmse, rolling_forecast_errors
from usdtrend.style import BLUE, INK, MUTED, free_axis, save_figure, use_style, value_axis

HORIZONS, TEST = (1, 3, 12), 60
first = str(RATES.index[-TEST])
rows = []
for c in LOGS:
    err = rolling_forecast_errors(LOGS[c].values, METHODS, HORIZONS, TEST)
    for m in METHODS:
        rows.append({"series": c, "method": m, "test_first": first, "test_last": str(RATES.index[-1]),
                     **{f"rmse_h{h}": rmse(err[m][h]) for h in HORIZONS},
                     **{f"n_h{h}": len(err[m][h]) for h in HORIZONS}})
        print(rows[-1])
save_table(rows, "table5_forecast_rmse")

use_style()


def draw():
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(4.75, 2.9), constrained_layout=True, sharey=True)
    names = list(METHODS)
    y = np.arange(len(names))[::-1]
    for ax, c in zip(axes, ("usd", "eur")):
        r = {x["method"]: x for x in rows if x["series"] == c}
        for k, (h, col) in enumerate(zip(HORIZONS, (INK, BLUE, MUTED))):
            ax.barh(y + (1 - k) * 0.26, [r[m][f"rmse_h{h}"] for m in names], height=0.24, color=col,
                    label=f"{h} month{'s' if h > 1 else ''} ahead")
        value_axis(ax, "x", 0, 60, 20)
        ax.set_xlabel("RMSE, %")
        ax.set_yticks(y, names)
        free_axis(ax, "y")
        ax.set_title(f"({'ab'[('usd', 'eur').index(c)]}) {NAMES[c]}")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=3, fontsize=6.5, frameon=False)
    return fig


save_figure("fig3_forecast", draw,
            lambda: f"Figure 3. Forecast errors on new months, {first} to {RATES.index[-1]}")

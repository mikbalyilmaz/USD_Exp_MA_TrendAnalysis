"""Analysis 2: is there a monthly seasonal pattern?

Why: version 1's README listed Holt-Winters and a seasonal decomposition. A seasonal component is only worth
estimating if the monthly changes differ systematically by calendar month. The monthly log change is regressed
on 11 month dummies (F test) and compared across months with the Kruskal-Wallis test, which does not assume
normal errors.

Outputs: Table 3 (table3_seasonality.csv), Table 4 (table4_month_means.csv), Figure 2 (fig2_seasonality).
"""
import numpy as np

from common import LOGS, NAMES, save_table
from usdtrend import month_effects
from usdtrend.style import BLUE, INK, free_axis, save_figure, source_note, use_style, value_axis

res, means = [], []
for c in LOGS:
    g = LOGS[c].diff().dropna()
    table, p_f, f, p_kw = month_effects(g.values, g.index.month)
    res.append({"series": c, "months": len(g), "F": f, "p_F": p_f, "p_kruskal_wallis": p_kw,
                "max_month_mean": float(table["mean"].max()), "min_month_mean": float(table["mean"].min())})
    for _, r in table.iterrows():
        means.append({"series": c, "month": int(r["month"]), "n": int(r["n"]), "mean": float(r["mean"]), "se": float(r["se"])})
    print(res[-1])
save_table(res, "table3_seasonality")
save_table(means, "table4_month_means")

use_style()
MONTHS = "JFMAMJJASOND"


def draw():
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(4.75, 2.1), constrained_layout=True, sharey=False)
    lo = min(m["mean"] - 1.96 * m["se"] for m in means)
    hi = max(m["mean"] + 1.96 * m["se"] for m in means)
    for ax, c, col in zip(axes, ("usd", "eur"), (INK, BLUE)):
        rows = [m for m in means if m["series"] == c]
        k = np.arange(1, 13)
        mu = np.array([m["mean"] for m in rows])
        se = np.array([m["se"] for m in rows])
        ax.errorbar(k, mu, yerr=1.96 * se, fmt="o", ms=3, color=col, ecolor=col, elinewidth=0.9, capsize=0)
        ax.axhline(LOGS[c].diff().mean(), color=INK, lw=0.6, ls="--")
        r = next(x for x in res if x["series"] == c)
        source_note(ax, f"F test p = {r['p_F']:.2f}\nKruskal–Wallis p = {r['p_kruskal_wallis']:.2f}", x=0.03, y=0.97, va="top")
        ax.set_xticks(k, list(MONTHS))
        ax.set_xlim(0.3, 12.7)
        free_axis(ax, "x")
        value_axis(ax, "y", -4, 8, 4)
        ax.set_title(f"({'ab'[('usd', 'eur').index(c)]}) {NAMES[c]}, % per month")
    assert lo > -4 and hi < 8, (lo, hi)
    return fig


save_figure("fig2_seasonality", draw,
            lambda: "Figure 2. Mean monthly change by calendar month, with 95% intervals")

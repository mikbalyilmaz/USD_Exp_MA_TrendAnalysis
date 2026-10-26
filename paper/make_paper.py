"""Writes every number of the project note from ../figures/*.csv, so that the text cannot drift away from the
analysis. Run from inside paper/:  python make_paper.py   Output: numbers.tex (one macro per quoted number) and
tab_rmse.tex (body of Table 1)."""
import csv
from pathlib import Path

FIG = Path(__file__).resolve().parents[1] / "figures"
OUT = Path(__file__).resolve().parent


def read(name):
    with open(FIG / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


def d(x, k):
    return f"{float(x):.{k}f}"


data = read("table1_data")[0]
trend = {r["series"]: r for r in read("table2_exp_trend")}
seas = {r["series"]: r for r in read("table3_seasonality")}
rmse = read("table5_forecast_rmse")
m = {"Months": data["months"], "FirstMonth": data["first_month"], "LastMonth": data["last_month"]}
for c, C in (("usd", "Usd"), ("eur", "Eur")):
    m[f"{C}First"] = d(data[f"{c}_first"], 2)
    m[f"{C}Last"] = d(data[f"{c}_last"], 2)
    m[f"{C}Ratio"] = d(data[f"{c}_ratio"], 1)
    m[f"{C}Growth"] = d(data[f"{c}_mean_monthly_change_pct"], 2)
    t = trend[c]
    m[f"{C}TrendB"] = d(t["b_pct_per_month"], 2)
    m[f"{C}RTwo"] = d(t["r2"], 3)
    m[f"{C}DW"] = d(t["durbin_watson"], 3)
    m[f"{C}ResidRho"] = d(t["resid_autocorr_lag1"], 2)
    m[f"{C}ResidMin"] = d(t["resid_min"], 0).replace("-", "$-$")
    m[f"{C}ResidMax"] = d(t["resid_max"], 0)
    m[f"{C}AdfLevel"] = d(t["adf_p_level_ct"], 2)
    s = seas[c]
    m[f"{C}PF"] = d(s["p_F"], 2)
    m[f"{C}PKW"] = d(s["p_kruskal_wallis"], 2)
r = {(x["series"], x["method"]): x for x in rmse}
m["TestFirst"], m["TestLast"] = rmse[0]["test_first"], rmse[0]["test_last"]
for c, C in (("usd", "Usd"), ("eur", "Eur")):
    for meth, M in (("Random walk with drift", "Drift"), ("Exponential trend", "Exp"), ("Random walk", "RW"),
                    ("Damped Holt", "Damped"), ("Holt-Winters (additive seasonal)", "HW")):
        for h in (1, 12):
            m[f"{C}{M}H{'One' if h == 1 else 'Twelve'}"] = d(r[(c, meth)][f"rmse_h{h}"], 1)
with open(OUT / "numbers.tex", "w") as f:
    for k, v in m.items():
        f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
methods = list(dict.fromkeys(x["method"] for x in rmse))
with open(OUT / "tab_rmse.tex", "w") as f:
    for meth in methods:
        cells = [d(r[(c, meth)][f"rmse_h{h}"], 1) for c in ("usd", "eur") for h in (1, 3, 12)]
        f.write(meth.replace("-", "--") + " & " + " & ".join(cells) + r" \\" + "\n")
    f.write("\\bottomrule\n")
print(f"Wrote numbers.tex ({len(m)} macros) and tab_rmse.tex.")

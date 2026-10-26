"""Exchange-rate data: the CBRT buying and selling rates of the US dollar and the euro, monthly averages.

`data/usd_eur_evds_2012_2026.csv` holds the monthly averages of the CBRT indicative buying and selling rates from
EVDS (TP.DK.USD.A.YTL, TP.DK.USD.S.YTL, TP.DK.EUR.A.YTL, TP.DK.EUR.S.YTL; daily series averaged to months by
EVDS), January 2012 to September 2026, downloaded on 26 October 2026. `data/usd_eur_v1.xlsx` is the file of
version 1, unchanged.

Author: Muhammed Ikbal Yilmaz
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "usd_eur_evds_2012_2026.csv"
V1_FILE = ROOT / "data" / "usd_eur_v1.xlsx"


def load():
    """Monthly buying and selling rates (TRY per unit) with a monthly PeriodIndex; checks the file first."""
    df = pd.read_csv(DATA_FILE, index_col="month")
    df.index = pd.PeriodIndex(df.index, freq="M")
    if df.isna().any().any():
        raise ValueError("missing values in the data file")
    if not (df.index == pd.period_range(df.index[0], df.index[-1], freq="M")).all():
        raise ValueError("months are not consecutive")
    for c in ("usd", "eur"):
        if not (df[f"{c}_buying_try"] < df[f"{c}_selling_try"]).all():
            raise ValueError(f"{c}: a buying rate is not below the selling rate")
    return df


def basket(df):
    """Version 1's 'basket' rate: the mean of the buying and the selling rate, for the dollar and the euro."""
    return pd.DataFrame({c: (df[f"{c}_buying_try"] + df[f"{c}_selling_try"]) / 2 for c in ("usd", "eur")})


def log100(s):
    """100 log of a positive series; first differences are then monthly log changes in per cent."""
    return 100 * np.log(s)


def load_v1():
    """The data file of version 1 (April 2012 to October 2024), with the same column names as `load()`."""
    v1 = pd.read_excel(V1_FILE, index_col=0)
    v1.index = pd.PeriodIndex(pd.to_datetime(v1.index), freq="M")
    return v1.rename(columns={"usd_alis": "usd_buying_try", "usd_satis": "usd_selling_try",
                              "eur_alis": "eur_buying_try", "eur_satis": "eur_selling_try"})

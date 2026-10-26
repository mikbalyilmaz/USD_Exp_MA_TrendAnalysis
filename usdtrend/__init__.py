"""usdtrend: trend analysis of the monthly USD/TRY and EUR/TRY rates (moving averages, exponential trend,
seasonality, exponential smoothing)."""

from .data import basket, load, load_v1, log100
from .methods import (METHODS, centered_ma, exp_trend, month_effects, rmse, rolling_forecast_errors,
                      trailing_ma)

__version__ = "2.0.0"

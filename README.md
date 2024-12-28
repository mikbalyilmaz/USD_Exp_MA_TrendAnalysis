# USD_Exp_MA_TrendAnalysis

# Let us now look at two built-in Python libraries. When it comes to financial data management,
# two of the most frequently used Python packages/libraries are Pandas and Numpy. 
# A function can be easily called only after we import the library. 
# This is why the command for importing libraries is always put at the beginning of a script.
# To employ the pandas library, we import it on the notebook. 
# This line means that Jupyter is told to import the pandas library and assigns it a short name, `pd`, for ease of reference. 📚

# One of the first steps of every statistical analysis is importing the dataset to be analyzed into the software.
# Depending on the format of the data, there are different ways of accomplishing this task.
# This study conducts a comprehensive analysis of monthly USD/TRY and EUR/TRY exchange rates from Q1 2012 to October 2024.
# Data, acquired from the Turkish Central Bank’s EVDS database, consists of separate buying and selling rates,
# later averaged into a 'basket' rate for consistency. 🌐

# Initially, the analysis focuses on USD/TRY before moving to EUR/TRY in parallel,
# applying various time series methods to capture both trend and seasonality.
# The primary methodological framework includes Moving Averages and Smoothing Techniques,
# such as centered moving averages, simple exponential smoothing, and the Holt-Winters model. 
# These techniques smooth the data, helping reveal trend and seasonal components effectively. 

# Stationarity of the series is then assessed through the Augmented Dickey-Fuller (ADF) test, 
# which identifies whether transformations, like differencing or logarithmic adjustments, 
# are needed to stabilize mean and variance over time.
# Once stationarity is confirmed, Model Selection and Forecasting proceeds using both additive and multiplicative 
# decompositions to select a model aligned with the data’s structure. ✨

# Further, advanced forecasting models, including Holt's linear (two-parameter) and seasonal (three-parameter) adjustments, 
# as well as exponential trend modeling, are applied. 
# For series with substantial trend and seasonal components, Box-Jenkins ARMA modeling will enhance forecast precision.
# Autocorrelation Analysis through autocorrelation and partial autocorrelation functions (normalized via Bartlett’s correction) 
# assesses whether trend components need to be removed. 
# The theoretical basis for these methods rests on stochastic process principles, where a real-valued time series in probability space
# forms a stochastic process, a sequence of random variables evolving over time.
# Detailed mathematical formulations supporting each step will follow in later sections. 🧮

# Trend Component Analysis distinguishes between linear and nonlinear growth or decline over the long term, 
# as expressed by the trend function. Seasonal Components are addressed by observing recurring patterns in monthly exchange rates. 
# Additionally, Cyclical Components, characterized by longer-term fluctuations influenced by economic policies, are examined.

# ⚠️ Warning: 'alis' means 'buy', 'satis' means 'sale'.

# --- Time Series Components ---
# Additive Structure:
 $Y_t = T_t + M_t + D_t + R_t$
# Multiplicative Structure:
 $Y_t = T_t * M_t * D_t * R_t$

# Stationarity Analysis
# Covariance Stationarity (Weak Stationarity):
 $E(Y_t) = μ$  (Constant mean)
 $Var(Y_t) = σ^2$ (Constant variance)
 $Cov(Y_t, Y_{t-k}) = γ_k$ (Autocovariance depends only on lag k)

# Strong Stationarity:
# If the joint distributions of a time series remain constant over time, it is strongly stationary.

# Empirical Analysis
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Generating time index and calculating log-transformed series
$foreign_dataset['t'] = range(1, len(foreign_dataset) + 1)$
$foreign_dataset['log_usd_sepet'] = np.log(foreign_dataset['usd_sepet'])$

# Preparing the regression model
$X = foreign_dataset[['t']]$
$X = sm.add_constant(X)$
$y = foreign_dataset['log_usd_sepet']$

# Fitting the OLS model
$model = sm.OLS(y, X).fit()$
$print(model.summary())$

# Predicting and reversing the log transformation
$foreign_dataset['usd_sepet_pred'] = np.exp(model.predict(X))$
$print(foreign_dataset[['t', 'usd_sepet', 'usd_sepet_pred']].head())$

# Observed vs Predicted Values
# Observed: Last observed value = 34.20 USD/TRY
# Predicted: Last estimated value = 33.93 USD/TRY

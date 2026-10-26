Bütün haklar saklıdır.

Bu projenin tüm hakları saklıdır. Kodun, tasarımın ve içeriğin izinsiz olarak kopyalanması, dağıtılması, değiştirilmesi veya herhangi bir şekilde kullanılması yasaktır.  
© 2025 mikbalyilmaz

****************************************************************************************************************************************

All rights reserved.

All rights to this project are reserved. The code, design, and content may not be copied, distributed, modified, or used in any way without permission.  
© 2025 mikbalyilmaz

****************************************************************************************************************************************

# USD_Exp_MA_TrendAnalysis  
[![View Project](https://img.shields.io/badge/View_Project-517FF7)](https://github.com/mikbalyilmaz/USD_Exp_MA_TrendAnalysis)  
[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](LICENSE)  

This project presents a comprehensive **time series analysis** of monthly USD/TRY and EUR/TRY exchange rates from Q1 2012 to October 2024. Data is sourced from the Turkish Central Bank’s EVDS database, using buying and selling rates averaged into a consistent basket rate.  

The primary methodological framework includes **Moving Averages** and **Exponential Smoothing Techniques**, such as centered moving averages, simple exponential smoothing, and the Holt-Winters model. These techniques enable decomposition of the series into **trend, seasonal, and cyclical components**, providing deeper insights into underlying dynamics.  

---

## Methodological Framework

- **Data Preparation**  
  Importing datasets via Python’s `pandas` and `numpy` libraries. Initial transformations include basket rate averaging and log-transformations.  

- **Trend and Seasonality Analysis**  
  - Centered Moving Averages  
  - Simple Exponential Smoothing  
  - Holt-Winters Seasonal Model  
  - Decomposition into additive and multiplicative structures  

- **Stationarity and Model Selection**  
  - Augmented Dickey-Fuller (ADF) test  
  - Transformations (log, differencing) applied as needed  
  - Box-Jenkins ARMA modeling for enhanced forecast precision  

- **Autocorrelation Analysis**  
  - Autocorrelation and Partial Autocorrelation Functions (ACF/PACF)  
  - Bartlett’s correction for normalized confidence bounds  

- **Forecasting and Evaluation**  
  - Holt’s Linear and Seasonal Adjustments  
  - Exponential Trend Models  
  - Comparative analysis between observed and predicted values  

---

## Core Equations

**Additive Decomposition:**  
$ Y_t = T_t + M_t + D_t + R_t $  

**Multiplicative Decomposition:**  
$ Y_t = T_t \times M_t \times D_t \times R_t $ 

**Stationarity Conditions:**  
- Weak Stationarity:  
  $ E(Y_t) = \mu, \quad Var(Y_t) = \sigma^2, \quad Cov(Y_t, Y_{t-k}) = \gamma_k $ 
- Strong Stationarity:  
  Joint distributions remain invariant across time.  

---

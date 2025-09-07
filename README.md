
# Stock CAPM App

An end-to-end **CAPM (Capital Asset Pricing Model)** dashboard built using **Python**, **Streamlit**, and **Plotly**. It fetches real-time stock data, performs financial analysis, forecasts (with model modules), and presents interactive visuals, all in a sleek web UI.
 **[Live Demo on Streamlit](https://nzt9yj49or9mzlstqto5bg.streamlit.app/)**  

---

##  Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Setup & Installation](#setup--installation)
- [How It Works](#how-it-works)
- [Key Modules](#key-modules)
- [Deployment](#deployment)
- [Contributing & License](#contributing--license)

---

##  Project Overview

This project delivers a web app to:

- Input stock tickers to fetch historical pricing data via **yfinance**.
- Analyze and visualize price trends, moving averages, RSI, MACD, and candlestick charts.
- Evaluate model forecasts (via utility functions), such as potential forecasts for the next 30 days.
- Present metrics such as RMSE for forecasting models.
- Showcase professional UI using **Streamlit** with responsive design and visual enhancements.

---

##  Features

| Feature | Description |
|--------|-------------|
| **Stock Info Lookup** | Displays company summary and financial metrics (market cap, beta, P/E) using `fast_info` (reliable) and safe fallbacks for `get_info()`. |
| **Pricing Visualizations** | Plot historical close prices, normalize data, present moving average, RSI, MACD, candlestick charts dynamically. |
| **Forecasting** | Use models built in `capm_functions.py` to forecast future prices (e.g., moving average forecast) and calculate errors (RMSE). |
| **Interactive UI** | Clean layout with input checks, chart selections (line vs candle), timeframes (1Y, MAX, etc.), and responsive columns. |
| **Tethered to Python Modules** | Code is modular in `capm_functions.py` to allow independent testing, extension, or integration. |

---

##  Repository Structure

```

CAPM/
├── README.md
├── requirements.txt         # Python dependencies
├── SOURCES.txt              # Data / resource info
├── TradingApp.py            # Main Streamlit app
├── capm\_functions.py        # Core analysis & forecasting functions
├── tickers.txt              # Valid stock ticker list
├── app.jpg                  # Banner image for app UI
├── app.log                  # Application execution log (if any)
├── test.py                  # Prototype/test script

````

---

##  Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Muskan40/CAPM.git
   cd CAPM
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app locally:

   ```bash
   streamlit run TradingApp.py
   ```

4. Open `localhost:8501` in your browser to access the interface.

---

## How It Works

1. **User Input**:

   * User enters a valid ticker (from `tickers.txt`).
   * Selects time frame inputs and chart style.

2. **Data Retrieval**:

   * Fetch historical price data with `yf.download()`.
   * Safely fetch company metrics using `fast_info` and `get_info()` with fallback.

3. **Forecasting**:

   * Pass data to `capm_functions.get_forecast()` and related methods.
   * Compute RMSE to measure forecasting error.

4. **Visual Output**:

   * Generate interactive Plotly charts (line, candlestick, RSI, MACD).
   * Display forecast table using `plotly_table`.

5. **User Experience**:

   * Clean layout, image banner, and modular UI via columns.
   * Button controls for selecting periods (5D, 1Y, MAX, etc.) and chart types.

---

## Key Modules

* **TradingApp.py**: Main Streamlit application orchestrating UI, data fetch, and visuals.
* **capm\_functions.py**: Contains modular functions:

  * `get_forecast()`, `evaluate_model()`, `plotly_table()`, RSI/MACD calculation, etc.
* **tickers.txt**: Predefined ticker list for validation and selection.
* **SOURCES.txt**: References to libraries or external data sources used.

---

## Deployment

To deploy on **Streamlit Cloud**:

1. Ensure `requirements.txt` includes:

   ```
   streamlit
   yfinance
   pandas
   numpy
   plotly
   pandas_ta
   scikit-learn
   statsmodels
   ```
2. Ensure the root directory has `TradingApp.py`, `capm_functions.py`, `tickers.txt`, and `requirements.txt`.
3. Connect the repo in Streamlit Cloud → deploy.
4. If rate-limit errors appear, the app provides safe fallbacks and doesn't crash.

---

## Contributing 

Feedback, issues, and pull requests are welcome.
Please ensure modules remain modular, dependency-safe, and the UI remains responsive.

---



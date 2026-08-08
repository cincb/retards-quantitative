import yfinance as yf
data = yf.download("AAPL", start="2025-08-08", end="2026-08-08")
data.to_csv("sample_data.csv")
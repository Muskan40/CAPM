import pandas as pd

# Nasdaq full ticker list (live updated)
url = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"

# Read file
df = pd.read_csv(url, sep='|')

# Extract only the "Symbol" column
tickers = df['Symbol'].dropna().unique().tolist()

# Save tickers into a file (CSV or TXT)
with open("tickers.txt", "w") as f:
    for t in tickers:
        f.write(f"{t}\n")

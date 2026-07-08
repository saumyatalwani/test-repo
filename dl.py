import yfinance as yf
import pandas as pd

INVESTMENT = 10_000
THRESHOLDS = [0.5,1.0, 1.5, 2.0]

# ----------------------
# Download Nifty Data
# ----------------------
df = yf.download(
    "NIFTYBEES.NS",
    start="2014-01-01",
    end="2026-06-18",
    auto_adjust=True,
    progress=False,
)

# Handle yfinance MultiIndex columns
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.reset_index()

# Remove timezone if present
df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

df = df.sort_values("Date").reset_index(drop=True)

# ----------------------
# Calculate Gap %
# ----------------------
df["PrevClose"] = df["Close"].shift(1)

df["GapPct"] = (
    (df["Open"] - df["PrevClose"])
    / df["PrevClose"]
    * 100
)

latest_close = df["Close"].iloc[-1]

results = []

# ----------------------
# Gap Down Strategies
# ----------------------
for threshold in THRESHOLDS:
    signals = df[df["GapPct"] <= -threshold]

    total_invested = 0
    total_units = 0

    for _, row in signals.iterrows():
        units = INVESTMENT / row["Open"]

        total_units += units
        total_invested += INVESTMENT

    current_value = total_units * latest_close
    profit = current_value - total_invested

    avg_buy_price = (
        total_invested / total_units
        if total_units > 0
        else 0
    )

    results.append({
        "Strategy": f"{threshold}% Gap Down",
        "Buys": len(signals),
        "Invested": round(total_invested),
        "Value": round(current_value),
        "Profit": round(profit),
        "Return %": round(
            profit / total_invested * 100,
            2
        ) if total_invested else 0,
        "Avg Buy": round(avg_buy_price, 2),
    })

# ----------------------
# SIP on 7th of every month
# If market closed, buy on next trading day
# ----------------------

df["YearMonth"] = df["Date"].dt.to_period("M")

sip_rows = []

for _, month_df in df.groupby("YearMonth"):

    target_date = month_df["Date"].iloc[0].replace(day=7)

    buy_row = month_df[month_df["Date"] >= target_date]

    if buy_row.empty:
        continue

    sip_rows.append(buy_row.iloc[0])

sip_df = pd.DataFrame(sip_rows)

sip_units = 0
sip_invested = 0

for _, row in sip_df.iterrows():
    sip_units += INVESTMENT / row["Open"]
    sip_invested += INVESTMENT

sip_value = sip_units * latest_close
sip_profit = sip_value - sip_invested

avg_sip_buy = (
    sip_invested / sip_units
    if sip_units > 0
    else 0
)

results.append({
    "Strategy": "Monthly SIP (7th)",
    "Buys": len(sip_df),
    "Invested": round(sip_invested),
    "Value": round(sip_value),
    "Profit": round(sip_profit),
    "Return %": round(
        sip_profit / sip_invested * 100,
        2
    ),
    "Avg Buy": round(avg_sip_buy, 2),
})

# ----------------------
# Display Results
# ----------------------
results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    "Return %",
    ascending=False
)

print("\n=== NIFTY STRATEGY COMPARISON ===\n")
print(results_df.to_string(index=False))
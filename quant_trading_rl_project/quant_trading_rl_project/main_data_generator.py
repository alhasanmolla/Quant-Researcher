# 📁 main_data_generator.py

import numpy as np
import pandas as pd
import talib

np.random.seed(42)

# Step 1: Generate Simulated Market Data
def generate_synthetic_market_data(days=100):
    close_prices = np.cumsum(np.random.normal(0, 1, days)) + 100
    volumes = np.random.randint(100000, 500000, days)

    df = pd.DataFrame({
        'Close': close_prices,
        'Volume': volumes
    })
    df.to_csv('historical_data.csv', index=False)
    return df

# Step 2: Add TA-Lib Features
def add_ta_features(df):
    df['RSI'] = talib.RSI(df['Close'])
    df['MACD'], _, _ = talib.MACD(df['Close'])
    df['OBV'] = talib.OBV(df['Close'], df['Volume'])
    df.dropna(inplace=True)
    df.to_csv('ta_features.csv', index=False)
    return df

# Step 3: Generate Sentiment Score from Headlines
def get_sentiment_data():
    headlines = [
        "Stocks rally as inflation cools down",
        "Market uncertainty grows amid war tensions",
        "Tech companies show strong quarterly earnings",
        "Investors cautious ahead of Fed decision",
        "AI stocks surge after major breakthrough"
    ]
    # Generate dummy sentiment scores and labels
    sentiment_scores = []
    for _ in headlines:
        label = 'POSITIVE' if np.random.rand() > 0.5 else 'NEGATIVE'
        score = np.random.uniform(0.5, 0.99)
        sentiment_scores.append({'label': label, 'score': score})

    result_df = pd.DataFrame({
        'Headline': headlines,
        'SentimentLabel': [s['label'] for s in sentiment_scores],
        'SentimentScore': [s['score'] if s['label'] == 'POSITIVE' else -s['score'] for s in sentiment_scores]
    })
    result_df.to_csv('sentiment_data.csv', index=False)
    return result_df

# Step 4: Combine All Features
def combine_all_features(ta_df, sentiment_df):
    # Ensure sentiment_df has enough rows for reindexing
    if len(sentiment_df) < len(ta_df):
        # Pad with dummy data if sentiment_df is shorter
        dummy_sentiment = pd.DataFrame({
            'SentimentLabel': ['NEUTRAL'] * (len(ta_df) - len(sentiment_df)),
            'SentimentScore': [0.0] * (len(ta_df) - len(sentiment_df))
        })
        sentiment_df = pd.concat([sentiment_df, dummy_sentiment], ignore_index=True)

    # Reindex sentiment_df to match ta_df's index length
    sentiment_df = sentiment_df.set_index(ta_df.index[-len(sentiment_df):])
    combined_df = ta_df.copy()
    combined_df['SentimentScore'] = sentiment_df['SentimentScore'].values
    combined_df.dropna(inplace=True)
    combined_df.to_csv('final_dataset.csv', index=False)
    return combined_df

# 🚀 Run Full Pipeline
if __name__ == '__main__':
    print("🔧 Generating synthetic historical data...")
    df = generate_synthetic_market_data()

    print("📊 Adding TA-Lib technical indicators...")
    ta_df = add_ta_features(df)

    print("💬 Creating sentiment data...")
    sentiment_df = get_sentiment_data()

    print("🔗 Combining all into final_dataset.csv")
    final_df = combine_all_features(ta_df, sentiment_df)

    print("✅ Done! Final file created: final_dataset.csv")

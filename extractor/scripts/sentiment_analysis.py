import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
from datetime import datetime
from news_scraper import fetch_public_sentiment

# Initialize sentiment analysis pipeline (using Hugging Face model)
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Analyzes sentiment of the provided text."""
    result = sentiment_pipeline(text)
    return result[0]['label'], result[0]['score']

def process_esg_reports(report_folder):
    """Extracts and analyzes sentiment trends from ESG reports."""
    sentiment_data = []
    
    for filename in os.listdir(report_folder):
        if filename.endswith(".txt") or filename.endswith(".pdf"):  # Assuming text extraction is done prior
            filepath = os.path.join(report_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
                sentiment_label, sentiment_score = analyze_sentiment(text)
                fiscal_year = extract_year_from_filename(filename)
                sentiment_data.append({
                    "file": filename,
                    "year": fiscal_year,
                    "sentiment": sentiment_label,
                    "score": sentiment_score
                })
    
    return sentiment_data

def extract_year_from_filename(filename):
    """Extracts fiscal year from filename (assuming YYYY format in name)."""
    years = [int(s) for s in filename.split() if s.isdigit() and len(s) == 4]
    return years[0] if years else "Unknown"

def compare_sentiment_trends(sentiment_data):
    """Compares sentiment trends year-over-year."""
    df = pd.DataFrame(sentiment_data)
    df = df.sort_values(by="year")
    df["sentiment_change"] = df["score"].diff()
    return df

def detect_anomalies(sentiment_data, public_sentiment_data):
    """Detects inconsistencies between corporate ESG sentiment and public perception."""
    df_corp = pd.DataFrame(sentiment_data)
    df_public = pd.DataFrame(public_sentiment_data)
    merged_df = pd.merge(df_corp, df_public, on="year", suffixes=("_corp", "_public"))
    merged_df["sentiment_gap"] = abs(merged_df["score_corp"] - merged_df["score_public"])
    
    anomalies = merged_df[merged_df["sentiment_gap"] > 0.3]  # Threshold for significant difference
    return anomalies

def plot_sentiment_trends(sentiment_data):
    """Visualizes ESG sentiment trends over time."""
    df = pd.DataFrame(sentiment_data)
    plt.figure(figsize=(10,5))
    sns.lineplot(data=df, x="year", y="score", marker="o", label="Corporate Sentiment")
    plt.title("ESG Sentiment Trends Over Time")
    plt.xlabel("Year")
    plt.ylabel("Sentiment Score")
    plt.legend()
    plt.grid()
    plt.show()

def plot_anomaly_heatmap(anomalies):
    """Visualizes sentiment anomalies with a heatmap."""
    df = anomalies.pivot("year", "file", "sentiment_gap")
    plt.figure(figsize=(10,5))
    sns.heatmap(df, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Sentiment Gap Between Corporate ESG Reports and Public Perception")
    plt.xlabel("Report File")
    plt.ylabel("Year")
    plt.show()

# Example usage
if __name__ == "__main__":
    report_folder = "data/reports"
    sentiment_results = process_esg_reports(report_folder)
    public_sentiment_results = fetch_public_sentiment()  # Fetch from external sources
    trend_analysis = compare_sentiment_trends(sentiment_results)
    anomaly_detection = detect_anomalies(sentiment_results, public_sentiment_results)
    plot_sentiment_trends(sentiment_results)
    plot_anomaly_heatmap(anomaly_detection)
    print(trend_analysis)
    print(anomaly_detection)

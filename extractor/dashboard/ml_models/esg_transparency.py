import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load ESG reports & external data
esg_reports = pd.read_csv("data/company_esg_reports.csv")
external_data = pd.read_csv("data/external_esg_sources.csv")

# Merge datasets for comparison
merged = esg_reports.merge(external_data, on="company", suffixes=("_report", "_external"))

# Calculate transparency metrics
merged["disclosure_completeness"] = merged["disclosed_factors"] / merged["total_possible_factors"]
merged["data_consistency"] = 1 - np.abs(merged["esg_score_report"] - merged["esg_score_external"]) / merged["esg_score_external"]
merged["sentiment_alignment"] = merged["sentiment_score_report"] / merged["sentiment_score_external"]

# Normalize scores
scaler = MinMaxScaler()
merged[["disclosure_completeness", "data_consistency", "sentiment_alignment"]] = scaler.fit_transform(
    merged[["disclosure_completeness", "data_consistency", "sentiment_alignment"]]
)

# Compute final ESG Transparency Score (weighted)
merged["transparency_score"] = (
    0.4 * merged["disclosure_completeness"]
    + 0.4 * merged["data_consistency"]
    + 0.2 * merged["sentiment_alignment"]
)

# Save results
merged.to_csv("data/esg_transparency_scores.csv", index=False)
joblib.dump(scaler, "models/transparency_scaler.pkl")

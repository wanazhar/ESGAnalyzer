import pandas as pd

# Load raw ESG data
df = pd.read_csv("data/aggregated_esg_data.csv")

# Remove duplicates
df.drop_duplicates(subset=["company"], keep="last", inplace=True)

# Replace missing values with averages
df.fillna(df.mean(), inplace=True)

# Save cleaned data
df.to_csv("data/cleaned_esg_data.csv", index=False)

import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def load_esg_data(file_path):
    """Loads processed ESG classification results from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_esg_trend_chart(esg_data):
    """Creates a bar chart to visualize ESG category distribution."""
    categories = ["Environmental", "Social", "Governance"]
    values = [len(esg_data.get(cat, [])) for cat in categories]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color=["green", "blue", "purple"])
    plt.xlabel("ESG Categories")
    plt.ylabel("Number of Mentions")
    plt.title("ESG Classification Overview")
    plt.show()

def generate_interactive_esg_comparison(data_dict):
    """Creates an interactive comparison of ESG classifications using Plotly."""
    categories = list(data_dict.keys())
    values = [len(data_dict[cat]) for cat in categories]

    fig = go.Figure(data=[go.Bar(x=categories, y=values, marker_color=["green", "blue", "purple"])])
    fig.update_layout(title="ESG Classification Comparison", xaxis_title="Category", yaxis_title="Count")
    fig.show()

if __name__ == "__main__":
    esg_data = load_esg_data("output/esg_results.json")
    generate_esg_trend_chart(esg_data["classified_esg_content"])
    generate_interactive_esg_comparison(esg_data["classified_esg_content"])

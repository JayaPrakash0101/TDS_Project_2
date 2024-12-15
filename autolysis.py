# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "chardet>=5.2.0",
#   "matplotlib>=3.9.3",
#   "numpy>=2.2.0",
#   "openai>=1.57.2",
#   "pandas>=2.2.3",
#   "python-dotenv>=1.0.1",
#   "requests>=2.32.3",
#   "scikit-learn>=1.6.0",
#   "seaborn>=0.13.2",
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import requests

# Retrieve the AI Proxy token from the environment variable
api_key = os.environ.get("AIPROXY_TOKEN")

# Define the token cost per 1,000 tokens (adjust based on OpenAI pricing)
COST_PER_1000_TOKENS = 0.03  # Replace with the correct rate for GPT-4o-mini

# Global variables to track token usage and cost
total_tokens_used = 0
total_api_calls = 0

import chardet  # To detect encoding (install with pip if not already installed)

# Function to load the dataset with automatic encoding detection
def load_dataset(filename):
    try:
        # Detect encoding
        with open(filename, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            encoding = detected['encoding']
        
        # Load dataset with detected encoding
        data = pd.read_csv(filename, encoding=encoding)
        print(f"File {filename} loaded successfully with {encoding} encoding.")
        return data
    except Exception as e:
        print(f"Error loading file {filename}: {e}")
        sys.exit(1)


# Function to analyze the dataset
def analyze_dataset(data):
    analysis = {}

    # Summary statistics
    try:
        analysis["summary"] = data.describe(include="all").to_dict()
    except Exception as e:
        print(f"Error generating summary statistics: {e}")
        analysis["summary"] = "Error generating summary statistics."

    # Missing values
    analysis["missing_values"] = data.isnull().sum().to_dict()

    # Data types of each column
    analysis["columns"] = {col: str(data[col].dtype) for col in data.columns}

    # Correlation for numeric columns only
    numeric_data = data.select_dtypes(include=['number'])
    if numeric_data.shape[1] > 1:
        try:
            analysis["correlation"] = numeric_data.corr().to_dict()
        except Exception as e:
            print(f"Error calculating correlation: {e}")
            analysis["correlation"] = "Error calculating correlation."
    else:
        analysis["correlation"] = "Not enough numeric columns for correlation."

    return analysis


# Function to visualize the dataset
def visualize_dataset(data):
    visualizations = []

    # Plot 1: Missing values heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
    plt.title('Missing Values Heatmap')
    plt.savefig('missing_values.png')
    visualizations.append('missing_values.png')
    plt.close()

    # Plot 2: Correlation heatmap (numeric columns only)
    numeric_data = data.select_dtypes(include=['number'])
    if numeric_data.shape[1] > 1:
        plt.figure(figsize=(10, 6))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
        plt.savefig('correlation_heatmap.png')
        visualizations.append('correlation_heatmap.png')
        plt.close()
    else:
        print("Not enough numeric columns for correlation heatmap.")

    # Plot 3: Count plot for the first categorical column (if exists)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        plt.figure(figsize=(10, 6))
        sns.countplot(y=categorical_cols[0], data=data, order=data[categorical_cols[0]].value_counts().index)
        plt.title(f'Count Plot for {categorical_cols[0]}')
        plt.savefig('count_plot.png')
        visualizations.append('count_plot.png')
        plt.close()
    else:
        print("No categorical columns for count plot.")

    return visualizations

# Function to interact with the LLM
def interact_with_llm(prompt):
    global total_tokens_used, total_api_calls
    try:
        # Proxy endpoint for OpenAI API
        api_proxy_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        
        # JSON payload for the request
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an assistant helping analyze datasets."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
        }
        
        # Headers for the request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Make the POST request to the proxy API
        response = requests.post(api_proxy_url, headers=headers, json=payload)
        
        # Check for a successful response
        if response.status_code == 200:
            result = response.json()

            # Update token usage and call count
            usage = result.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            total_tokens_used += total_tokens
            total_api_calls += 1

            return result['choices'][0]['message']['content']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            sys.exit(1)

    except Exception as e:
        print(f"Error interacting with LLM: {e}")
        sys.exit(1)

# Function to create the README.md file
def create_readme(data, analysis, visualizations):
    prompt = (
        f"The dataset has the following columns: {list(data.columns)}\n"
        f"Summary statistics: {analysis['summary']}\n"
        f"Missing values: {analysis['missing_values']}\n"
        f"Correlation matrix: {analysis['correlation']}\n"
        "Please write a story describing the dataset, the analysis performed, the insights, and their implications."
    )

    story = interact_with_llm(prompt)

    with open('README.md', 'w') as f:
        f.write("# Automated Dataset Analysis\n\n")
        f.write(story + "\n\n")
        for viz in visualizations:
            f.write(f"![{viz}]({viz})\n\n")

# Function to print usage statistics
def print_usage_statistics():
    global total_tokens_used, total_api_calls

    # Calculate total cost so far
    total_cost = (total_tokens_used / 1000) * COST_PER_1000_TOKENS

    print(f"Total API Calls: {total_api_calls}")
    print(f"Total Tokens Used: {total_tokens_used}")
    print(f"Total Cost (so far): ${total_cost:.2f}")

    # Estimate monthly cost based on current usage
    # Assuming 30 days of similar usage
    daily_cost = total_cost / total_api_calls if total_api_calls else 0
    estimated_monthly_cost = daily_cost * 30
    print(f"Estimated Monthly Cost: ${estimated_monthly_cost:.2f}")
    
# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    print("Using dataset:", dataset_path)

    # Load, analyze, and visualize the dataset
    data = load_dataset(dataset_path)
    analysis = analyze_dataset(data)
    visualizations = visualize_dataset(data)
    
    # Generate README file
    create_readme(data, analysis, visualizations)
    print("Analysis complete. Outputs saved to README.md and PNG files.")
    print_usage_statistics()

if __name__ == "__main__":
    main()

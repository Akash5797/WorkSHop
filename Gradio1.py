import gradio as gr  # For creating the interactive web interface
import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For plotting charts
import seaborn as sns  # For advanced statistical plots
import ollama  # For AI-generated insights using local models

# Function to perform EDA (Exploratory Data Analysis)
def eda_analysis(file):
    # Load dataset from uploaded file
    DS = pd.read_csv(file.name)

    # Fill missing numeric columns with their median
    for col in DS.select_dtypes(include=['number']).columns:
        DS[col].fillna(DS[col].median(), inplace=True)

    # Fill missing categorical columns with their mode (most frequent value)
    for col in DS.select_dtypes(include=['object']).columns:
        DS[col].fillna(DS[col].mode()[0], inplace=True)

    # Generate dataset summary (describe includes all columns)
    summary = DS.describe(include='all').to_string()

    # Find missing values count per column
    missing_values = DS.isnull().sum().to_string()

    # Generate AI insights using the summary
    insights = generate_insights(summary)

    # Generate visualizations and get list of saved plot paths
    plot_paths = generate_visualizations(DS)

    # Return combined output for Gradio interface
    return f'''
    Data Loaded Successfully  
    \nSummary:\n{summary}  
    \nMissing Values:\n{missing_values}  
    \nLLM Insights:\n{insights}  ''', plot_paths


# Function to generate AI insights from dataset summary
def generate_insights(DS_summary):
    prompt = f"Analyze the Dataset Summary and provide key insights:\n\n{DS_summary}"

    # Call Ollama to get AI-generated insights
    response = ollama.chat(
        model='mistral',  # Use 'mistral' model
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']


# Function to generate and save plots
def generate_visualizations(DS):
    plot_paths = []

    # Plot histogram for numeric columns
    for col in DS.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(6, 4))
        sns.histplot(DS[col], bins=30, kde=True, color='blue')
        plt.title(f"Distribution of {col}")
        path = f"{col}_distribution.png"
        plt.savefig(path)  # FIXED: previously used path.savefig(), which would crash
        plot_paths.append(path)
        plt.close()

    # Plot correlation heatmap (only if numeric columns exist)
    numeric_DS = DS.select_dtypes(include=['number'])
    if not numeric_DS.empty:
        plt.figure(figsize=(8, 5))
        sns.heatmap(numeric_DS.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title("Correlation Heatmap")
        path = "correlation_heatmap.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths


# Gradio Interface
GradioApp = gr.Interface(
    fn=eda_analysis,
    inputs=gr.File(type='filepath'),  # FIXED: corrected input type
    outputs=[
        gr.Textbox(label='EDA Report'),
        gr.Gallery(label='Data Visualizations')  # FIXED: proper component name
    ],
    title="LLM-Powered EDA Data Analyzer Created By Akash ",
    description="Upload any CSV dataset to view a detailed EDA report with AI-generated insights and visualizations."
)

# Launch the app
GradioApp.launch(share=True)

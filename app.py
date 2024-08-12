import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os
import openai
import re
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

from layout import create_layout  # Import the layout function

# Load environment variables from a .env file
load_dotenv()

# Ensure your API key is stored securely, ideally in an environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set your OPENAI_API_KEY environment variable.")

# Set the OpenAI API key
openai.api_key = api_key

# Load the cleaned sales data
df = pd.read_csv('../GPT_OPEN_AI_project/df_cleaned.csv')

# Preprocess Data: Convert 'Date' column to datetime format if needed
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the layout using the function from layout.py
app.layout = create_layout(df)

# Callback to update the graph based on selected analysis type and date range


@app.callback(
    Output('sales-graph', 'figure'),
    [Input('analysis-type', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(analysis_type, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if analysis_type == 'sales_over_time':
        fig = px.line(filtered_df, x='date', y='total_value_usd',
                      title='Total Sales Over Time')

    elif analysis_type == 'top_sales_reps':
        if 'sales_rep_name' in df.columns:
            top_reps = filtered_df.groupby('sales_rep_name')['total_value_usd'].sum(
            ).reset_index().sort_values(by='total_value_usd', ascending=False)
            fig = px.bar(top_reps, x='sales_rep_name',
                         y='total_value_usd', title='Sales by Sales Reps')

    return fig

# Callback to handle AI-generated insights based on the query input


@app.callback(
    Output('ai-insights-output', 'children'),
    [Input('ai-query-btn', 'n_clicks')],
    [State('ai-query-input', 'value'),
     State('analysis-type', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')]
)
def generate_ai_insights(n_clicks, query, analysis_type, start_date, end_date):
    if n_clicks > 0 and query:
        # Filter the data based on date range
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        # Generate specific data summaries based on the selected analysis type
        if analysis_type == 'sales_over_time':
            total_sales = filtered_df['total_value_usd'].sum()
            summary = "Total sales over the selected period is " + \
                str(total_sales) + " USD."

        elif analysis_type == 'top_sales_reps':
            top_reps = filtered_df.groupby('sales_rep_name')[
                'total_value_usd'].sum().sort_values(ascending=False)
            summary = "Top sales reps and their sales: " + \
                str(top_reps.head(5).to_dict()) + "."

        # Modify the query to include this summary
        extended_query = f"{query} Here is a summary of the data: {summary}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Replace with the appropriate model version
                messages=[
                    {"role": "system", "content": "You are an assistant specialized in analyzing sales data."},
                    {"role": "user", "content": extended_query}
                ]
            )

            # Process the response to create Dash components
            response_content = response.choices[0]['message']['content']
            response_parts = re.split(r'(\*\*.*?\*\*|###)', response_content)
            formatted_response = []
            for part in response_parts:
                if part.startswith('**') and part.endswith('**'):
                    # Remove the ** and make bold
                    formatted_response.append(html.Strong(part[2:-2]))
                else:
                    formatted_response.append(html.Span(part))

            return html.Div([
                html.H4("AI Insights", style={
                        'font-weight': 'bold', 'font-family': 'Verdana'}),
                html.Div(formatted_response, style={
                         'font-family': 'Verdana', 'font-size': '16px'})
            ])
        except Exception as e:
            return html.Div([
                html.H4("Error", style={
                        'font-weight': 'bold', 'font-family': 'Verdana'}),
                html.P(f"An error occurred: {e}")
            ])
    return ""


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

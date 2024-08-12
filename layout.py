import dash
import re
from dash import html, dcc


def create_layout(df):
    return html.Div([
        # Overall container for consistent width
        html.Div([
            html.H1("Interactive Sales Dashboard with AI Insights", style={
                    'text-align': 'center', 'font-family': 'Verdana', 'margin-bottom': '20px'}),

            # Section for date range and report type selection
            html.Div([
                html.Label("Select date:", style={
                           'font-weight': 'bold', 'font-family': 'Verdana', 'margin-right': '10px'}),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df['date'].min(),
                    end_date=df['date'].max(),
                    style={'margin-right': '40px', 'font-family': 'Verdana'}
                ),
                html.Label("Select report type:", style={
                           'font-weight': 'bold', 'font-family': 'Verdana', 'margin-right': '10px'}),
                dcc.Dropdown(
                    id='analysis-type',
                    options=[
                        {'label': 'Total Sales Over Time',
                            'value': 'sales_over_time'},
                        {'label': 'Sales by Sales Reps', 'value': 'top_sales_reps'}
                    ],
                    value='sales_over_time',
                    style={'width': '300px', 'font-family': 'Verdana'}
                ),
            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),

            # Graph to display the data
            dcc.Graph(id='sales-graph',
                      style={'width': '80%', 'margin': '0 auto', 'font-family': 'Verdana'}),

            # Section for AI query and insights
            html.Div([
                html.Label("Ask about trends:", style={
                           'font-weight': 'bold', 'font-family': 'Verdana', 'margin-right': '10px'}),
                dcc.Input(id='ai-query-input', type='text', placeholder='Type your question here...',
                          style={'width': '70%', 'margin-right': '10px', 'font-family': 'Verdana'}),
                html.Button('Get AI Insights', id='ai-query-btn',
                            n_clicks=0, style={'font-family': 'Verdana'}),
            ], style={'text-align': 'center', 'margin-bottom': '20px'}),

            # Container for displaying AI-generated insights
            html.Div(id='ai-insights-output', style={
                'margin-top': '20px',
                'font-family': 'Verdana',
                'font-size': '16px',
                'text-align': 'left',
                'padding': '20px',
                'border': '1px solid #ddd',
                'border-radius': '5px',
                'background-color': '#f9f9f9',
                'max-width': '100%',
                'white-space': 'pre-wrap',
                'line-height': '1.6'  # Improve readability
            }),
            # Ensures the entire app fits within a consistent width
        ], style={'max-width': '80%', 'margin': '0 auto'})
    ])

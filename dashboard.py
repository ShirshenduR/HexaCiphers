import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import glob
import json
from datetime import datetime, timedelta
import base64
import io
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx

# Import core components
from src.data_collection import TwitterClient
from src.preprocessing import preprocess_dataset, extract_features
from src.sentiment_analysis import SentimentAnalyzer
from src.engagement_analysis import EngagementAnalyzer
from src.network_analysis import NetworkAnalyzer
from src.alert_system import AlertSystem
from src.visualization import Visualizer

# Initialize components
sentiment_analyzer = SentimentAnalyzer()
engagement_analyzer = EngagementAnalyzer()
network_analyzer = NetworkAnalyzer()
alert_system = AlertSystem()
visualizer = Visualizer()

# Make sure directories exist
os.makedirs('./data/processed', exist_ok=True)
os.makedirs('./visualizations', exist_ok=True)
os.makedirs('./alerts', exist_ok=True)

# External stylesheets
external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
]

# Initialize the Dash app
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    title="Anti-India Content Analysis Dashboard",
    suppress_callback_exceptions=True
)

server = app.server  # For production deployment

# Colors
colors = {
    'background': '#f8f9fa',
    'text': '#343a40',
    'accent': '#dc3545',
    'accent_light': '#f8d7da',
    'positive': '#28a745',
    'neutral': '#6c757d',
    'negative': '#dc3545'
}

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #f8f9fa;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            .header {
                background-color: #343a40;
                color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 0 0 10px 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .card {
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .card-header {
                border-radius: 10px 10px 0 0;
                font-weight: bold;
            }
            .alert-card {
                background-color: #f8d7da;
                border-left: 5px solid #dc3545;
            }
            .analysis-card {
                border-left: 5px solid #007bff;
            }
            .tab-selected {
                border-bottom: 3px solid #dc3545 !important;
                color: #dc3545 !important;
                font-weight: bold;
            }
            .stat-card {
                text-align: center;
                padding: 15px;
            }
            .stat-value {
                font-size: 2rem;
                font-weight: bold;
                margin: 10px 0;
            }
            .stat-label {
                font-size: 0.9rem;
                text-transform: uppercase;
                color: #6c757d;
            }
            .trend-up {
                color: #dc3545;
            }
            .trend-down {
                color: #28a745;
            }
            .nav-tabs .nav-link {
                border: none;
                border-bottom: 3px solid transparent;
                color: #343a40;
            }
            .nav-tabs .nav-link:hover {
                border-bottom: 3px solid #f8d7da;
                color: #dc3545;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Twitter Anti-India Content Analysis Dashboard", className="mb-0"),
        html.P("Real-time monitoring and analysis of anti-India campaigns on Twitter", className="text-muted")
    ], className="header"),
    
    # Main content
    html.Div([
        # Tabs for navigation
        dcc.Tabs(id="tabs", value="dashboard", className="nav nav-tabs mb-4", children=[
            dcc.Tab(label="Dashboard", value="dashboard", className="nav-item", selected_className="tab-selected"),
            dcc.Tab(label="Data Collection", value="data-collection", className="nav-item", selected_className="tab-selected"),
            dcc.Tab(label="Sentiment Analysis", value="sentiment", className="nav-item", selected_className="tab-selected"),
            dcc.Tab(label="Engagement Analysis", value="engagement", className="nav-item", selected_className="tab-selected"),
            dcc.Tab(label="Network Analysis", value="network", className="nav-item", selected_className="tab-selected"),
            dcc.Tab(label="Alerts", value="alerts", className="nav-item", selected_className="tab-selected"),
            dcc.Tab(label="Settings", value="settings", className="nav-item", selected_className="tab-selected"),
        ]),
        
        # Tab content
        html.Div(id="tab-content")
    ], className="container-fluid")
])

# Callback to update tab content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab_content(tab):
    if tab == "dashboard":
        return render_dashboard()
    elif tab == "data-collection":
        return render_data_collection()
    elif tab == "sentiment":
        return render_sentiment_analysis()
    elif tab == "engagement":
        return render_engagement_analysis()
    elif tab == "network":
        return render_network_analysis()
    elif tab == "alerts":
        return render_alerts()
    elif tab == "settings":
        return render_settings()
    return html.Div("This tab is under construction")

# Dashboard tab
def render_dashboard():
    # Get list of available datasets
    datasets = glob.glob('./data/processed/*.csv')
    options = [{'label': os.path.basename(file), 'value': file} for file in datasets]
    
    # Get latest dataset if available
    latest_dataset = max(datasets, key=os.path.getctime) if datasets else None
    
    return html.Div([
        # Dataset selector and refresh button
        html.Div([
            html.Div([
                html.Label("Select Dataset:", className="mr-2"),
                dcc.Dropdown(
                    id='dashboard-dataset-dropdown',
                    options=options,
                    value=latest_dataset,
                    className="form-control",
                    style={'width': '100%'}
                ),
            ], className="col-md-10"),
            html.Div([
                html.Button("Refresh", id="refresh-button", className="btn btn-primary btn-block mt-4")
            ], className="col-md-2"),
        ], className="row mb-4"),
        
        # Key metrics cards
        html.Div(id="dashboard-key-metrics", className="row mb-4"),
        
        # Sentiment distribution and anti-India score
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Sentiment Distribution", className="card-header"),
                    html.Div([
                        dcc.Graph(id="dashboard-sentiment-pie")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Anti-India Score Distribution", className="card-header"),
                    html.Div([
                        dcc.Graph(id="dashboard-anti-india-score")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row mb-4"),
        
        # Recent alerts and top tweets
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Recent Alerts", className="card-header"),
                    html.Div(id="dashboard-recent-alerts", className="card-body")
                ], className="card alert-card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Top Flagged Tweets", className="card-header"),
                    html.Div(id="dashboard-top-tweets", className="card-body")
                ], className="card analysis-card")
            ], className="col-md-6"),
        ], className="row"),
        
        # Store for dataset
        dcc.Store(id="dashboard-dataset")
    ])

# Data Collection tab
def render_data_collection():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Twitter Data Collection", className="card-header"),
                    html.Div([
                        html.P("Collect tweets based on keywords and analyze them for anti-India sentiment."),
                        
                        html.Div([
                            html.Div([
                                html.Label("Collection Method:"),
                                dcc.RadioItems(
                                    id='collection-method',
                                    options=[
                                        {'label': 'Use Keywords from Database', 'value': 'keywords'},
                                        {'label': 'Custom Search Query', 'value': 'custom'}
                                    ],
                                    value='keywords',
                                    className="mb-3"
                                ),
                            ], className="col-md-6"),
                            
                            html.Div([
                                html.Label("Custom Query (if selected):"),
                                dcc.Input(
                                    id='custom-query',
                                    type='text',
                                    placeholder='Enter search query',
                                    className="form-control mb-3"
                                ),
                            ], className="col-md-6"),
                        ], className="row"),
                        
                        html.Div([
                            html.Div([
                                html.Label("Tweet Count:"),
                                dcc.Input(
                                    id='tweet-count',
                                    type='number',
                                    value=100,
                                    min=10,
                                    max=1000,
                                    className="form-control mb-3"
                                ),
                            ], className="col-md-6"),
                            
                            html.Div([
                                html.Label("Language:"),
                                dcc.Dropdown(
                                    id='tweet-language',
                                    options=[
                                        {'label': 'English', 'value': 'en'},
                                        {'label': 'Hindi', 'value': 'hi'},
                                        {'label': 'All Languages', 'value': 'all'}
                                    ],
                                    value='en',
                                    className="mb-3"
                                ),
                            ], className="col-md-6"),
                        ], className="row"),
                        
                        html.Button(
                            "Collect Tweets", 
                            id="collect-tweets-button", 
                            className="btn btn-danger mb-3"
                        ),
                        
                        html.Div(id="collection-status")
                    ], className="card-body")
                ], className="card mb-4")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Upload Dataset", className="card-header"),
                    html.Div([
                        html.P("Upload a CSV file with Twitter data for analysis."),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px 0'
                            },
                            multiple=False
                        ),
                        html.Div(id='upload-status'),
                    ], className="card-body")
                ], className="card mb-4"),
                
                html.Div([
                    html.H5("Available Datasets", className="card-header"),
                    html.Div(id="available-datasets", className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row"),
        
        # Sample dataset section
        html.Div([
            html.Div([
                html.H5("Use Sample Dataset", className="card-header"),
                html.Div([
                    html.P("Use our pre-prepared sample dataset to test the system."),
                    html.Button(
                        "Load Sample Dataset", 
                        id="load-sample-button", 
                        className="btn btn-primary"
                    ),
                    html.Div(id="sample-load-status", className="mt-2")
                ], className="card-body")
            ], className="card")
        ], className="row mt-4")
    ])

# Sentiment Analysis tab
def render_sentiment_analysis():
    # Get list of available datasets
    datasets = glob.glob('./data/processed/*.csv')
    options = [{'label': os.path.basename(file), 'value': file} for file in datasets]
    
    # Get latest dataset if available
    latest_dataset = max(datasets, key=os.path.getctime) if datasets else None
    
    return html.Div([
        # Dataset selector
        html.Div([
            html.Div([
                html.Label("Select Dataset:"),
                dcc.Dropdown(
                    id='sentiment-dataset-dropdown',
                    options=options,
                    value=latest_dataset,
                    className="form-control"
                ),
            ], className="col-md-12"),
        ], className="row mb-4"),
        
        # Sentiment charts
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Sentiment Distribution", className="card-header"),
                    html.Div([
                        dcc.Graph(id="sentiment-distribution-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Anti-India Score Distribution", className="card-header"),
                    html.Div([
                        dcc.Graph(id="anti-india-score-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row mb-4"),
        
        # Word cloud and sentiment by time
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Word Cloud of Negative Tweets", className="card-header"),
                    html.Div([
                        html.Img(id="negative-wordcloud", style={'width': '100%'})
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Sentiment Over Time", className="card-header"),
                    html.Div([
                        dcc.Graph(id="sentiment-time-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row mb-4"),
        
        # Top flagged tweets
        html.Div([
            html.Div([
                html.H5("Top Flagged Tweets by Anti-India Score", className="card-header"),
                html.Div(id="flagged-tweets-table", className="card-body")
            ], className="card")
        ], className="row"),
        
        # Store for dataset
        dcc.Store(id="sentiment-dataset")
    ])

# Engagement Analysis tab
def render_engagement_analysis():
    # Get list of available datasets
    datasets = glob.glob('./data/processed/*.csv')
    options = [{'label': os.path.basename(file), 'value': file} for file in datasets]
    
    # Get latest dataset if available
    latest_dataset = max(datasets, key=os.path.getctime) if datasets else None
    
    return html.Div([
        # Dataset selector
        html.Div([
            html.Div([
                html.Label("Select Dataset:"),
                dcc.Dropdown(
                    id='engagement-dataset-dropdown',
                    options=options,
                    value=latest_dataset,
                    className="form-control"
                ),
            ], className="col-md-12"),
        ], className="row mb-4"),
        
        # Engagement charts
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Engagement vs Anti-India Score", className="card-header"),
                    html.Div([
                        dcc.Graph(id="engagement-scatter-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Top Users by Impact Score", className="card-header"),
                    html.Div([
                        dcc.Graph(id="impact-score-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row mb-4"),
        
        # Engagement metrics and viral content
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Engagement Metrics by Sentiment", className="card-header"),
                    html.Div([
                        dcc.Graph(id="engagement-by-sentiment-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Viral Content Analysis", className="card-header"),
                    html.Div([
                        dcc.Graph(id="viral-content-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row mb-4"),
        
        # Influential users table
        html.Div([
            html.Div([
                html.H5("Influential Users", className="card-header"),
                html.Div(id="influential-users-table", className="card-body")
            ], className="card")
        ], className="row"),
        
        # Store for dataset and user metrics
        dcc.Store(id="engagement-dataset"),
        dcc.Store(id="user-metrics-data")
    ])

# Network Analysis tab
def render_network_analysis():
    # Get list of available datasets
    datasets = glob.glob('./data/processed/*.csv')
    options = [{'label': os.path.basename(file), 'value': file} for file in datasets]
    
    # Get latest dataset if available
    latest_dataset = max(datasets, key=os.path.getctime) if datasets else None
    
    return html.Div([
        # Dataset selector
        html.Div([
            html.Div([
                html.Label("Select Dataset:"),
                dcc.Dropdown(
                    id='network-dataset-dropdown',
                    options=options,
                    value=latest_dataset,
                    className="form-control"
                ),
            ], className="col-md-12"),
        ], className="row mb-4"),
        
        # Network graphs
        html.Div([
            html.Div([
                html.Div([
                    html.H5("User Mention Network", className="card-header"),
                    html.Div([
                        html.Img(id="mention-network-graph", style={'width': '100%'})
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("Hashtag Co-occurrence Network", className="card-header"),
                    html.Div([
                        html.Img(id="hashtag-network-graph", style={'width': '100%'})
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row mb-4"),
        
        # Coordinated activity
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Coordinated Activity Analysis", className="card-header"),
                    html.Div([
                        dcc.Graph(id="coordinated-activity-chart")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-12"),
        ], className="row mb-4"),
        
        # Network metrics tables
        html.Div([
            html.Div([
                html.H5("Top Users by Network Centrality", className="card-header"),
                html.Div(id="network-metrics-table", className="card-body")
            ], className="card")
        ], className="row"),
        
        # Store for dataset and network data
        dcc.Store(id="network-dataset"),
        dcc.Store(id="mention-metrics-data"),
        dcc.Store(id="hashtag-metrics-data"),
        dcc.Store(id="coord-data")
    ])

# Alerts tab
def render_alerts():
    # Get list of available alert files
    alert_files = glob.glob('./alerts/*.json')
    options = [{'label': os.path.basename(file), 'value': file} for file in alert_files]
    options.sort(key=lambda x: os.path.getctime(x['value']), reverse=True)
    
    # Get latest alert file if available
    latest_alert = options[0]['value'] if options else None
    
    return html.Div([
        # Alert file selector
        html.Div([
            html.Div([
                html.Label("Select Alert File:"),
                dcc.Dropdown(
                    id='alert-file-dropdown',
                    options=options,
                    value=latest_alert,
                    className="form-control"
                ),
            ], className="col-md-10"),
            html.Div([
                html.Button("Refresh", id="refresh-alerts-button", className="btn btn-primary btn-block mt-4")
            ], className="col-md-2"),
        ], className="row mb-4"),
        
        # Alert summary
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Alert Summary", className="card-header"),
                    html.Div(id="alert-summary", className="card-body")
                ], className="card alert-card")
            ], className="col-md-12"),
        ], className="row mb-4"),
        
        # Alert details by type
        html.Div([
            html.Div([
                html.Div([
                    html.H5("High Anti-India Score Alerts", className="card-header"),
                    html.Div(id="anti-india-alerts", className="card-body")
                ], className="card")
            ], className="col-md-4"),
            
            html.Div([
                html.Div([
                    html.H5("Influential User Alerts", className="card-header"),
                    html.Div(id="influential-user-alerts", className="card-body")
                ], className="card")
            ], className="col-md-4"),
            
            html.Div([
                html.Div([
                    html.H5("Coordinated Activity Alerts", className="card-header"),
                    html.Div(id="coordinated-activity-alerts", className="card-body")
                ], className="card")
            ], className="col-md-4"),
        ], className="row"),
        
        # Store for alert data
        dcc.Store(id="alert-data")
    ])

# Settings tab
def render_settings():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Keyword Database Management", className="card-header"),
                    html.Div([
                        html.P("Update the keywords, hashtags, and phrases used for detecting anti-India content."),
                        
                        html.Div([
                            html.Div([
                                html.Label("Keywords:"),
                                dcc.Textarea(
                                    id='keywords-textarea',
                                    placeholder='Enter keywords, one per line',
                                    style={'width': '100%', 'height': 150},
                                    className="form-control mb-3"
                                ),
                            ], className="col-md-6"),
                            
                            html.Div([
                                html.Label("Hashtags:"),
                                dcc.Textarea(
                                    id='hashtags-textarea',
                                    placeholder='Enter hashtags, one per line',
                                    style={'width': '100%', 'height': 150},
                                    className="form-control mb-3"
                                ),
                            ], className="col-md-6"),
                        ], className="row"),
                        
                        html.Div([
                            html.Div([
                                html.Label("Phrases:"),
                                dcc.Textarea(
                                    id='phrases-textarea',
                                    placeholder='Enter phrases, one per line',
                                    style={'width': '100%', 'height': 150},
                                    className="form-control mb-3"
                                ),
                            ], className="col-md-6"),
                            
                            html.Div([
                                html.Label("Contexts:"),
                                dcc.Textarea(
                                    id='contexts-textarea',
                                    placeholder='Enter context terms, one per line',
                                    style={'width': '100%', 'height': 150},
                                    className="form-control mb-3"
                                ),
                            ], className="col-md-6"),
                        ], className="row"),
                        
                        html.Button(
                            "Load Current Keywords", 
                            id="load-keywords-button", 
                            className="btn btn-secondary mr-2"
                        ),
                        html.Button(
                            "Save Keywords", 
                            id="save-keywords-button", 
                            className="btn btn-primary"
                        ),
                        html.Div(id="keywords-status", className="mt-2")
                    ], className="card-body")
                ], className="card mb-4")
            ], className="col-md-6"),
            
            html.Div([
                html.Div([
                    html.H5("System Settings", className="card-header"),
                    html.Div([
                        html.P("Configure system parameters for data collection and analysis."),
                        
                        html.Div([
                            html.Label("Alert Threshold:"),
                            dcc.Slider(
                                id='alert-threshold-slider',
                                min=5,
                                max=20,
                                step=1,
                                value=10,
                                marks={i: str(i) for i in range(5, 21, 5)},
                                className="mb-4"
                            ),
                        ]),
                        
                        html.Div([
                            html.Label("Engagement Threshold:"),
                            dcc.Slider(
                                id='engagement-threshold-slider',
                                min=50,
                                max=500,
                                step=50,
                                value=100,
                                marks={i: str(i) for i in range(50, 501, 100)},
                                className="mb-4"
                            ),
                        ]),
                        
                        html.Div([
                            html.Label("Scan Interval (seconds):"),
                            dcc.Slider(
                                id='scan-interval-slider',
                                min=60,
                                max=600,
                                step=60,
                                value=300,
                                marks={i: str(i) for i in range(60, 601, 120)},
                                className="mb-4"
                            ),
                        ]),
                        
                        html.Button(
                            "Save Settings", 
                            id="save-settings-button", 
                            className="btn btn-primary"
                        ),
                        html.Div(id="settings-status", className="mt-2")
                    ], className="card-body")
                ], className="card")
            ], className="col-md-6"),
        ], className="row")
    ])

# Callback for the dashboard key metrics
@app.callback(
    [Output("dashboard-key-metrics", "children"),
     Output("dashboard-sentiment-pie", "figure"),
     Output("dashboard-anti-india-score", "figure"),
     Output("dashboard-recent-alerts", "children"),
     Output("dashboard-top-tweets", "children"),
     Output("dashboard-dataset", "data")],
    [Input("dashboard-dataset-dropdown", "value"),
     Input("refresh-button", "n_clicks")]
)
def update_dashboard(selected_file, n_clicks):
    if not selected_file:
        return html.Div("No dataset selected"), {}, {}, "No alerts available", "No tweets available", None
    
    try:
        # Load and process the dataset
        df = pd.read_csv(selected_file)
        
        # Check if the dataset has already been processed
        if 'anti_india_score' not in df.columns:
            df = preprocess_dataset(df)
            df = extract_features(df)
            df = sentiment_analyzer.analyze_tweets(df)
            df = engagement_analyzer.calculate_engagement_metrics(df)
            
            # Save the processed dataset
            processed_path = selected_file.replace('.csv', '_processed.csv')
            df.to_csv(processed_path, index=False)
        
        # Key metrics
        total_tweets = len(df)
        flagged_tweets = sum(df['flagged']) if 'flagged' in df.columns else 0
        flagged_pct = (flagged_tweets / total_tweets * 100) if total_tweets > 0 else 0
        
        avg_score = df['anti_india_score'].mean() if 'anti_india_score' in df.columns else 0
        
        # Engagement metrics
        if 'total_engagement' in df.columns:
            total_engagement = df['total_engagement'].sum()
            avg_engagement = df['total_engagement'].mean()
        else:
            total_engagement = 0
            avg_engagement = 0
        
        # Create key metrics cards
        key_metrics = html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(f"{total_tweets:,}", className="stat-value"),
                        html.Div("Total Tweets", className="stat-label")
                    ], className="stat-card card")
                ], className="col-md-3"),
                
                html.Div([
                    html.Div([
                        html.Div([
                            f"{flagged_tweets:,}",
                            html.Small(f" ({flagged_pct:.1f}%)", className="text-muted")
                        ], className="stat-value"),
                        html.Div("Flagged Tweets", className="stat-label")
                    ], className="stat-card card alert-card")
                ], className="col-md-3"),
                
                html.Div([
                    html.Div([
                        html.Div(f"{avg_score:.3f}", className="stat-value"),
                        html.Div("Avg Anti-India Score", className="stat-label")
                    ], className="stat-card card")
                ], className="col-md-3"),
                
                html.Div([
                    html.Div([
                        html.Div(f"{total_engagement:,}", className="stat-value"),
                        html.Div("Total Engagement", className="stat-label")
                    ], className="stat-card card")
                ], className="col-md-3"),
            ], className="row")
        ])
        
        # Sentiment pie chart
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            sentiment_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                color=sentiment_counts.index,
                color_discrete_map={
                    'positive': colors['positive'],
                    'neutral': colors['neutral'],
                    'negative': colors['negative']
                }
            )
            sentiment_pie.update_traces(textposition='inside', textinfo='percent+label')
        else:
            sentiment_pie = {}
        
        # Anti-India score histogram
        if 'anti_india_score' in df.columns:
            anti_india_fig = px.histogram(
                df, 
                x='anti_india_score',
                nbins=20,
                title="Anti-India Score Distribution",
                color_discrete_sequence=[colors['accent']]
            )
            anti_india_fig.add_vline(x=0.6, line_dash="dash", line_color="red")
            anti_india_fig.update_layout(showlegend=False)
        else:
            anti_india_fig = {}
        
        # Recent alerts
        alert_files = glob.glob('./alerts/*.json')
        if alert_files:
            latest_alert = max(alert_files, key=os.path.getctime)
            with open(latest_alert, 'r') as f:
                alert_data = json.load(f)
            
            # Display recent alerts
            alerts_html = []
            for alert in alert_data.get('alerts', [])[:5]:
                alert_type = alert.get('type', '')
                severity = alert.get('severity', 'medium')
                
                if alert_type == 'high_anti_india_score':
                    alerts_html.append(html.Div([
                        html.Strong(f"High Anti-India Score: {alert.get('score', 0):.2f}"),
                        html.Br(),
                        f"User: @{alert.get('username', 'unknown')}",
                        html.Br(),
                        f"Tweet: {alert.get('text', '')[:100]}...",
                        html.Hr()
                    ]))
                elif alert_type == 'influential_user':
                    alerts_html.append(html.Div([
                        html.Strong("Influential User Detected"),
                        html.Br(),
                        f"User: @{alert.get('username', 'unknown')}",
                        html.Br(),
                        f"Followers: {alert.get('followers', 0):,}",
                        html.Br(),
                        f"Impact Score: {alert.get('impact_score', 0):.2f}",
                        html.Hr()
                    ]))
                elif alert_type == 'coordinated_activity':
                    alerts_html.append(html.Div([
                        html.Strong("Coordinated Activity Detected"),
                        html.Br(),
                        f"Hashtag: #{alert.get('hashtag', '')}",
                        html.Br(),
                        f"Users: {alert.get('user_count', 0)}",
                        html.Br(),
                        f"Tweets: {alert.get('tweet_count', 0)}",
                        html.Hr()
                    ]))
            
            if not alerts_html:
                alerts_html = ["No recent alerts"]
        else:
            alerts_html = ["No alerts generated yet"]
        
        # Top tweets
        if 'flagged' in df.columns:
            flagged_df = df[df['flagged'] == True].sort_values(
                by='anti_india_score', ascending=False
            ).head(5)
            
            tweets_html = []
            for _, tweet in flagged_df.iterrows():
                tweets_html.append(html.Div([
                    html.Div([
                        html.Strong(f"@{tweet.get('username', 'unknown')}"),
                        html.Small(f" ({tweet.get('user_followers', 0):,} followers)", className="text-muted")
                    ]),
                    html.P(tweet.get('text', '')[:200] + "..."),
                    html.Div([
                        html.Span(f"Anti-India Score: {tweet.get('anti_india_score', 0):.2f}", 
                                 className="badge badge-danger mr-2"),
                        html.Span(f"Engagement: {tweet.get('total_engagement', 0):,}", 
                                 className="badge badge-secondary")
                    ]),
                    html.Hr()
                ]))
            
            if not tweets_html:
                tweets_html = ["No flagged tweets found"]
        else:
            tweets_html = ["No flagged tweets found"]
        
        return key_metrics, sentiment_pie, anti_india_fig, alerts_html, tweets_html, df.to_json(date_format='iso', orient='split')
    
    except Exception as e:
        return html.Div(f"Error: {str(e)}"), {}, {}, "Error loading alerts", "Error loading tweets", None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
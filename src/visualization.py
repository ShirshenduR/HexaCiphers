import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Visualizer:
    def __init__(self, output_dir='./visualizations'):
        """Initialize visualizer"""
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set(style="whitegrid")
        logger.info(f"Initialized Visualizer with output directory: {output_dir}")
    
    def save_figure(self, fig, filename):
        """Save figure to file"""
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close(fig)
        logger.info(f"Saved figure to {filepath}")
        return filepath
    
    def save_plotly(self, fig, filename):
        """Save Plotly figure to HTML file"""
        filepath = os.path.join(self.output_dir, filename)
        fig.write_html(filepath)
        logger.info(f"Saved Plotly figure to {filepath}")
        return filepath
    
    def plot_sentiment_distribution(self, df):
        """Plot sentiment distribution"""
        logger.info("Plotting sentiment distribution")
        
        if 'sentiment' not in df.columns:
            logger.warning("Sentiment column not found in dataframe")
            return None
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot sentiment counts
        sns.countplot(data=df, x='sentiment', ax=ax, palette='RdBu_r')
        
        # Add title and labels
        ax.set_title('Distribution of Sentiment in Analyzed Tweets', fontsize=16)
        ax.set_xlabel('Sentiment Category', fontsize=12)
        ax.set_ylabel('Number of Tweets', fontsize=12)
        
        # Add count labels
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'bottom', fontsize=12)
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_distribution_{timestamp}.png"
        return self.save_figure(fig, filename)
    
    def plot_anti_india_score_distribution(self, df):
        """Plot anti-India score distribution"""
        logger.info("Plotting anti-India score distribution")
        
        if 'anti_india_score' not in df.columns:
            logger.warning("Anti-India score column not found in dataframe")
            return None
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Plot histogram with KDE
        sns.histplot(data=df, x='anti_india_score', kde=True, bins=30, 
                    color='darkred', ax=ax, alpha=0.7)
        
        # Add title and labels
        ax.set_title('Distribution of Anti-India Scores', fontsize=16)
        ax.set_xlabel('Anti-India Score', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        
        # Add vertical line at threshold
        ax.axvline(x=0.6, color='red', linestyle='--', alpha=0.7, 
                  label='Flagging Threshold (0.6)')
        
        # Add legend
        ax.legend(fontsize=12)
        
        # Add annotation
        flagged_count = sum(df['anti_india_score'] > 0.6)
        ax.annotate(f'Flagged Tweets: {flagged_count} ({flagged_count/len(df)*100:.1f}%)', 
                   xy=(0.7, 0.9), xycoords='axes fraction', fontsize=12,
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", alpha=0.8))
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"anti_india_score_distribution_{timestamp}.png"
        return self.save_figure(fig, filename)
    
    def plot_engagement_vs_sentiment(self, df):
        """Plot engagement vs sentiment"""
        logger.info("Plotting engagement vs sentiment")
        
        if 'total_engagement' not in df.columns or 'anti_india_score' not in df.columns:
            logger.warning("Required columns not found in dataframe")
            return None
        
        # Create Plotly figure
        fig = px.scatter(
            df, 
            x='anti_india_score', 
            y='total_engagement',
            color='flagged',
            size='user_followers',
            hover_name='username',
            hover_data=['text', 'sentiment_score', 'keyword_match_score'],
            title='Engagement vs Anti-India Score',
            labels={
                'anti_india_score': 'Anti-India Score',
                'total_engagement': 'Total Engagement (RT + Likes + Replies)',
                'flagged': 'Flagged Content',
                'user_followers': 'Follower Count'
            },
            color_discrete_map={True: 'red', False: 'blue'},
            opacity=0.7
        )
        
        # Add threshold line
        fig.add_shape(
            type='line',
            x0=0.6, y0=0, x1=0.6, y1=df['total_engagement'].max(),
            line=dict(color='red', width=2, dash='dash')
        )
        
        # Update layout
        fig.update_layout(
            xaxis=dict(range=[0, 1]),
            height=600,
            width=900
        )
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"engagement_vs_sentiment_{timestamp}.html"
        return self.save_plotly(fig, filename)
    
    def plot_influential_users(self, user_metrics):
        """Plot top influential users"""
        logger.info("Plotting influential users")
        
        if user_metrics is None or user_metrics.empty:
            logger.warning("User metrics dataframe is empty")
            return None
        
        # Get top users
        top_users = user_metrics.sort_values(by='impact_score', ascending=False).head(20)
        
        # Create figure
        fig = px.bar(
            top_users,
            x='username',
            y='impact_score',
            color='is_influential',
            hover_data=['user_followers', 'tweet_count', 'total_engagement', 'anti_india_score'],
            title='Top 20 Users by Impact Score',
            labels={
                'username': 'Twitter Username',
                'impact_score': 'Impact Score',
                'is_influential': 'Flagged as Influential'
            },
            color_discrete_map={True: 'red', False: 'blue'},
            height=600
        )
        
        # Update layout
        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            xaxis_tickangle=-45
        )
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"influential_users_{timestamp}.html"
        return self.save_plotly(fig, filename)
    
    def plot_network_graph(self, G, metrics, title, is_mention_network=True):
        """Plot network graph using networkx"""
        logger.info(f"Plotting network graph: {title}")
        
        if G.number_of_nodes() == 0:
            logger.warning("Graph has no nodes")
            return None
        
        # Create figure
        plt.figure(figsize=(14, 14))
        
        # Set node size based on metric
        if is_mention_network:
            size_metric = 'in_degree'
            color_metric = 'pagerank'
        else:
            size_metric = 'degree'
            color_metric = 'betweenness_centrality'
        
        # Create node size mapping
        if size_metric in metrics.columns:
            node_size = [metrics[metrics['node'] == node][size_metric].values[0] * 100 
                        if node in metrics['node'].values else 100 
                        for node in G.nodes()]
        else:
            node_size = 300
        
        # Create node color mapping
        if color_metric in metrics.columns:
            node_color = [metrics[metrics['node'] == node][color_metric].values[0]
                         if node in metrics['node'].values else 0
                         for node in G.nodes()]
        else:
            node_color = 'red'
        
        # Set edge width based on weight
        edge_width = [G[u][v]['weight'] * 0.5 for u, v in G.edges()]
        
        # Use spring layout for graph
        pos = nx.spring_layout(G, k=0.3, iterations=50)
        
        # Draw graph
        nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, 
                              cmap=plt.cm.Reds, alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.3, edge_color='gray')
        nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
        
        # Add title
        plt.title(title, fontsize=16)
        plt.axis('off')
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.lower().replace(' ', '_')}_{timestamp}.png"
        return self.save_figure(plt.gcf(), filename)
    
    def plot_coordinated_activity(self, coord_df):
        """Plot coordinated activity"""
        logger.info("Plotting coordinated activity")
        
        if coord_df is None or coord_df.empty:
            logger.warning("Coordinated activity dataframe is empty")
            return None
        
        # Group by hashtag
        hashtag_summary = coord_df.groupby('common_hashtag').agg({
            'tweet_id': 'count',
            'user_id': 'nunique',
            'time_window': 'nunique'
        }).reset_index()
        
        hashtag_summary.columns = ['hashtag', 'tweet_count', 'user_count', 'time_window_count']
        hashtag_summary = hashtag_summary.sort_values(by='user_count', ascending=False)
        
        # Create figure
        fig = px.scatter(
            hashtag_summary,
            x='user_count',
            y='tweet_count',
            size='time_window_count',
            color='user_count',
            hover_name='hashtag',
            text='hashtag',
            title='Coordinated Activity by Hashtag',
            labels={
                'user_count': 'Number of Unique Users',
                'tweet_count': 'Number of Tweets',
                'time_window_count': 'Number of Time Windows'
            },
            color_continuous_scale='Reds',
            height=600
        )
        
        # Update layout
        fig.update_traces(textposition='top center')
        fig.update_layout(
            xaxis_title='Number of Unique Users',
            yaxis_title='Number of Tweets'
        )
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"coordinated_activity_{timestamp}.html"
        return self.save_plotly(fig, filename)
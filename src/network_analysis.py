import pandas as pd
import networkx as nx
import community as community_louvain
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkAnalyzer:
    def __init__(self):
        """Initialize network analyzer"""
        logger.info("Initializing NetworkAnalyzer")
    
    def build_mention_network(self, df):
        """Build a network graph based on user mentions"""
        logger.info("Building mention network")
        
        # Initialize graph
        G = nx.DiGraph()
        
        # Get mentions data
        if 'mentions' not in df.columns or 'username' not in df.columns:
            logger.warning("Required columns 'mentions' or 'username' not found in dataframe")
            return G, pd.DataFrame()
        
        # Add nodes and edges
        for _, row in df.iterrows():
            source = row['username']
            
            # Skip if no mentions
            if not isinstance(row['mentions'], list) and pd.isna(row['mentions']):
                continue
            
            # Convert string representation of list to actual list if needed
            mentions = row['mentions']
            if isinstance(mentions, str):
                # Try to convert string representation to list
                try:
                    mentions = eval(mentions)
                except:
                    mentions = []
            
            # Add edges for each mention
            for target in mentions:
                if G.has_edge(source, target):
                    G[source][target]['weight'] += 1
                else:
                    G.add_edge(source, target, weight=1)
        
        logger.info(f"Built mention network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Calculate network metrics
        if G.number_of_nodes() > 0:
            metrics = self.calculate_network_metrics(G)
        else:
            metrics = pd.DataFrame()
        
        return G, metrics
    
    def build_hashtag_network(self, df):
        """Build a network graph based on hashtag co-occurrence"""
        logger.info("Building hashtag network")
        
        # Initialize graph
        G = nx.Graph()
        
        # Get hashtags data
        if 'hashtags' not in df.columns:
            logger.warning("Required column 'hashtags' not found in dataframe")
            return G, pd.DataFrame()
        
        # Group hashtags by tweet
        for _, row in df.iterrows():
            # Skip if no hashtags
            if not isinstance(row['hashtags'], list) and pd.isna(row['hashtags']):
                continue
            
            # Convert string representation of list to actual list if needed
            hashtags = row['hashtags']
            if isinstance(hashtags, str):
                # Try to convert string representation to list
                try:
                    hashtags = eval(hashtags)
                except:
                    hashtags = []
            
            # Add edges for each co-occurring hashtag pair
            for i, h1 in enumerate(hashtags):
                for h2 in hashtags[i+1:]:
                    if G.has_edge(h1, h2):
                        G[h1][h2]['weight'] += 1
                    else:
                        G.add_edge(h1, h2, weight=1)
        
        logger.info(f"Built hashtag network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Calculate network metrics
        if G.number_of_nodes() > 0:
            metrics = self.calculate_network_metrics(G, is_directed=False)
        else:
            metrics = pd.DataFrame()
        
        return G, metrics
    
    def calculate_network_metrics(self, G, is_directed=True):
        """Calculate network metrics for nodes in the graph"""
        logger.info("Calculating network metrics")
        
        metrics = {}
        
        # Degree centrality
        if is_directed:
            metrics['in_degree'] = dict(G.in_degree())
            metrics['out_degree'] = dict(G.out_degree())
            
            # Convert to centrality (normalized)
            in_degree_cent = nx.in_degree_centrality(G)
            out_degree_cent = nx.out_degree_centrality(G)
            metrics['in_degree_centrality'] = in_degree_cent
            metrics['out_degree_centrality'] = out_degree_cent
        else:
            metrics['degree'] = dict(G.degree())
            metrics['degree_centrality'] = nx.degree_centrality(G)
        
        # Betweenness centrality (identifies bridge nodes)
        try:
            metrics['betweenness_centrality'] = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
        except:
            logger.warning("Failed to calculate betweenness centrality")
            metrics['betweenness_centrality'] = {}
        
        # Pagerank (identifies influential nodes)
        try:
            metrics['pagerank'] = nx.pagerank(G)
        except:
            logger.warning("Failed to calculate pagerank")
            metrics['pagerank'] = {}
        
        # Community detection
        try:
            if not is_directed:
                # Convert to undirected if needed
                G_undirected = G if not is_directed else G.to_undirected()
                
                # Detect communities
                partition = community_louvain.best_partition(G_undirected)
                metrics['community'] = partition
        except:
            logger.warning("Failed to detect communities")
            metrics['community'] = {}
        
        # Convert metrics to dataframe
        metrics_df = pd.DataFrame(metrics).reset_index().rename(columns={'index': 'node'})
        
        return metrics_df
    
    def detect_coordinated_activity(self, df, time_window=1):
        """Detect potentially coordinated activity based on timing and content similarity"""
        logger.info(f"Detecting coordinated activity with time window: {time_window} hour(s)")
        
        if 'created_at' not in df.columns:
            logger.warning("Required column 'created_at' not found in dataframe")
            return df, pd.DataFrame()
        
        # Ensure datetime format
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Sort by creation time
        df_sorted = df.sort_values('created_at')
        
        # Group tweets by time windows
        df_sorted['time_window'] = df_sorted['created_at'].dt.floor(f'{time_window}H')
        
        # Count tweets per user per time window
        user_activity = df_sorted.groupby(['time_window', 'user_id']).size().reset_index(name='tweet_count')
        
        # Find windows with high activity
        window_counts = user_activity.groupby('time_window').size().reset_index(name='user_count')
        high_activity_windows = window_counts[window_counts['user_count'] > window_counts['user_count'].median() * 2]
        
        # Identify coordinated users
        coordinated_activity = []
        
        for _, window_row in high_activity_windows.iterrows():
            window = window_row['time_window']
            
            # Get tweets in this window
            window_tweets = df_sorted[df_sorted['time_window'] == window]
            
            # Look for similar content or hashtags
            if 'hashtags' in window_tweets.columns:
                hashtag_counts = {}
                
                for _, tweet in window_tweets.iterrows():
                    # Skip if no hashtags
                    if not isinstance(tweet['hashtags'], list) and pd.isna(tweet['hashtags']):
                        continue
                    
                    # Convert string representation of list to actual list if needed
                    hashtags = tweet['hashtags']
                    if isinstance(hashtags, str):
                        try:
                            hashtags = eval(hashtags)
                        except:
                            hashtags = []
                    
                    # Count hashtags
                    for tag in hashtags:
                        if tag in hashtag_counts:
                            hashtag_counts[tag] += 1
                        else:
                            hashtag_counts[tag] = 1
                
                # Find commonly used hashtags
                common_hashtags = [tag for tag, count in hashtag_counts.items() 
                                  if count > len(window_tweets) * 0.2]
                
                # Mark tweets using common hashtags
                for tag in common_hashtags:
                    tag_tweets = window_tweets[window_tweets['hashtags'].apply(
                        lambda x: isinstance(x, list) and tag in x or 
                                  isinstance(x, str) and tag in eval(x)
                    )]
                    
                    if len(tag_tweets) >= 3:  # At least 3 users using same hashtag in time window
                        for _, tweet in tag_tweets.iterrows():
                            coordinated_activity.append({
                                'tweet_id': tweet['id'],
                                'user_id': tweet['user_id'],
                                'username': tweet['username'],
                                'time_window': window,
                                'common_hashtag': tag,
                                'tweet_count': len(tag_tweets)
                            })
        
        # Create dataframe of coordinated activity
        coord_df = pd.DataFrame(coordinated_activity)
        
        if not coord_df.empty:
            # Flag coordinated tweets in original dataframe
            coordinated_ids = coord_df['tweet_id'].unique()
            df['is_coordinated'] = df['id'].isin(coordinated_ids)
            
            logger.info(f"Detected {len(coordinated_ids)} potentially coordinated tweets")
        else:
            df['is_coordinated'] = False
            logger.info("No coordinated activity detected")
        
        return df, coord_df
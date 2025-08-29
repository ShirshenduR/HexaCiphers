from src.data_collection import TwitterClient, continuous_collection
from src.preprocessing import preprocess_dataset, extract_features
from src.sentiment_analysis import SentimentAnalyzer
from src.engagement_analysis import EngagementAnalyzer
from src.network_analysis import NetworkAnalyzer
from src.alert_system import AlertSystem
from src.visualization import Visualizer
from utils.generate_sample_data import create_sample_dataset
import os
import pandas as pd
import argparse

# Set up directories
os.makedirs('./data/processed', exist_ok=True)
os.makedirs('./visualizations', exist_ok=True)
os.makedirs('./alerts', exist_ok=True)

def analyze_dataset(file_path):
    """Analyze a Twitter dataset and generate visualizations and alerts"""
    print(f"Analyzing dataset: {file_path}")
    
    # Load data
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} tweets")
    
    # Preprocess
    print("Preprocessing data...")
    df = preprocess_dataset(df)
    df = extract_features(df)
    
    # Analyze sentiment
    print("Analyzing sentiment...")
    sentiment_analyzer = SentimentAnalyzer()
    df = sentiment_analyzer.analyze_tweets(df)
    
    # Analyze engagement
    print("Analyzing engagement...")
    engagement_analyzer = EngagementAnalyzer()
    df = engagement_analyzer.calculate_engagement_metrics(df)
    df, influential_content = engagement_analyzer.identify_influential_content(df)
    df, user_metrics = engagement_analyzer.analyze_user_engagement(df)
    
    # Network analysis
    print("Performing network analysis...")
    network_analyzer = NetworkAnalyzer()
    mention_graph, mention_metrics = network_analyzer.build_mention_network(df)
    hashtag_graph, hashtag_metrics = network_analyzer.build_hashtag_network(df)
    df, coord_df = network_analyzer.detect_coordinated_activity(df)
    
    # Generate alerts
    print("Generating alerts...")
    alert_system = AlertSystem()
    alerts = alert_system.generate_alerts(df, user_metrics, coord_df)
    
    # Create visualizations
    print("Creating visualizations...")
    visualizer = Visualizer()
    visualizer.plot_sentiment_distribution(df)
    visualizer.plot_anti_india_score_distribution(df)
    visualizer.plot_engagement_vs_sentiment(df)
    visualizer.plot_influential_users(user_metrics)
    
    if mention_graph.number_of_nodes() > 0:
        visualizer.plot_network_graph(mention_graph, mention_metrics, "User Mention Network")
    
    if hashtag_graph.number_of_nodes() > 0:
        visualizer.plot_network_graph(hashtag_graph, hashtag_metrics, "Hashtag Co-occurrence Network", False)
    
    if not coord_df.empty:
        visualizer.plot_coordinated_activity(coord_df)
    
    # Save processed dataset
    output_path = file_path.replace('.csv', '_analyzed.csv')
    df.to_csv(output_path, index=False)
    print(f"Analysis complete. Results saved to {output_path}")
    
    return df, alerts

def main():
    parser = argparse.ArgumentParser(description='Twitter Anti-India Content Analysis')
    parser.add_argument('--collect', action='store_true', help='Collect tweets from Twitter API')
    parser.add_argument('--analyze', type=str, help='Analyze an existing dataset (provide CSV file path)')
    parser.add_argument('--sample', action='store_true', help='Generate and analyze a sample dataset')
    parser.add_argument('--count', type=int, default=100, help='Number of tweets to collect (default: 100)')
    parser.add_argument('--duration', type=int, default=0, help='Collection duration in minutes (0 for single batch)')
    
    args = parser.parse_args()
    
    if args.collect:
        print("Collecting tweets from Twitter API...")
        client = TwitterClient()
        output_path = './data/processed'
        
        if args.duration > 0:
            continuous_collection(output_path, args.duration)
        else:
            filepath = client.collect_data(output_path)
            if filepath:
                analyze_dataset(filepath)
                print(f"Analysis complete. Check ./visualizations and ./alerts folders.")
    
    elif args.analyze:
        if os.path.exists(args.analyze):
            analyze_dataset(args.analyze)
            print(f"Analysis complete. Check ./visualizations and ./alerts folders.")
        else:
            print(f"Error: File not found - {args.analyze}")
    
    elif args.sample:
        print("Generating sample dataset...")
        sample_path = create_sample_dataset()
        analyze_dataset(sample_path)
        print(f"Sample analysis complete. Check ./visualizations and ./alerts folders.")
    
    else:
        print("No action specified. Use --collect, --analyze, or --sample.")
        print("Run 'python app.py --help' for more information.")

if __name__ == "__main__":
    main()
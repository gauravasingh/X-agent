#!/usr/bin/env python3
"""
Main X Agent - Reads 10,000+ posts/day from X and generates daily insights
"""
import sys
import argparse
from x_handler import XPostFetcher
from llm_analyzer import PostAnalyzer
from report_generator import ReportGenerator
from config import POSTS_PER_RUN, MAX_POSTS_PER_DAY


def main():
    parser = argparse.ArgumentParser(
        description="X Agent - Analyze trending posts and generate daily reports"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "trending", "keywords", "demo"],
        default="trending",
        help="Agent mode: full analysis, trending posts, keyword search, or demo"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        help="Keywords to search (for keyword mode)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=POSTS_PER_RUN,
        help=f"Number of posts to fetch (default: {POSTS_PER_RUN})"
    )
    
    args = parser.parse_args()
    
    print("🚀 X Agent Starting...")
    print(f"   Mode: {args.mode}")
    print(f"   Limit: {args.limit} posts")
    print()
    
    try:
        # 1. Fetch posts from X
        print("📡 Fetching posts from X...")
        fetcher = XPostFetcher()
        
        if args.mode == "trending":
            posts = fetcher.fetch_trending_posts(limit=args.limit)
        elif args.mode == "keywords":
            keywords = args.keywords or ["tech", "AI", "crypto"]
            posts = fetcher.fetch_by_keywords(keywords, limit=args.limit)
        elif args.mode == "full":
            trending = fetcher.fetch_trending_posts(limit=args.limit // 2)
            keyword_posts = fetcher.fetch_by_keywords(
                ["tech", "AI", "business"], 
                limit=args.limit // 2
            )
            posts = trending + keyword_posts
        elif args.mode == "demo":
            print("   (Using demo data - no API calls)")
            posts = generate_demo_posts()
        
        print(f"✓ Fetched {len(posts)} posts")
        
        if not posts:
            print("⚠️  No posts fetched. Check your API credentials.")
            return
        
        # 2. Analyze posts with LLM
        print("\n🤖 Analyzing posts with LLM...")
        analyzer = PostAnalyzer()
        analysis = analyzer.summarize_posts(posts, max_posts=min(len(posts), 100))
        print("✓ Analysis complete")
        
        # 3. Extract insights
        print("\n💡 Extracting insights...")
        insights = analyzer.extract_insights(posts)
        print("✓ Insights extracted")
        
        # 4. Generate report
        print("\n📊 Generating report...")
        generator = ReportGenerator()
        report_path = generator.generate_daily_report(posts, analysis, insights)
        
        print("\n" + "=" * 60)
        print("✅ AGENT COMPLETE")
        print("=" * 60)
        print(f"Report saved to: {report_path}")
        print(f"Total posts processed: {len(posts)}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def generate_demo_posts():
    """Generate demo posts for testing without API"""
    return [
        {
            "id": f"demo_{i}",
            "text": f"This is demo post #{i}. Great things happening in tech!",
            "author": f"user_{i}",
            "author_verified": i % 3 == 0,
            "author_followers": 1000 + (i * 1000),
            "likes": 100 + (i * 50),
            "retweets": 20 + (i * 10),
            "replies": 5 + i,
            "quotes": 2 + (i % 5)
        }
        for i in range(1, 11)
    ]


if __name__ == "__main__":
    main()

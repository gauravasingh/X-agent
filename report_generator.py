"""
Generate daily reports from analyzed posts
"""
from typing import List, Dict, Any
from datetime import datetime
from config import REPORT_OUTPUT_DIR
import json
import os


class ReportGenerator:
    def __init__(self):
        self.output_dir = REPORT_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_daily_report(
        self, 
        posts: List[Dict],
        analysis: Dict[str, Any],
        insights: Dict[str, Any]
    ) -> str:
        """
        Generate comprehensive daily report
        
        Args:
            posts: List of fetched posts
            analysis: Analysis from LLM
            insights: Extracted insights
            
        Returns:
            Report filename
        """
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H:%M:%S")
        
        # Create report
        report = {
            "generated_at": timestamp.isoformat(),
            "date": date_str,
            "time": time_str,
            "posts_analyzed": len(posts),
            "analysis": analysis,
            "insights": insights,
            "top_posts": self._get_top_posts(posts, limit=10),
            "statistics": self._gather_statistics(posts)
        }
        
        # Save as JSON
        json_filename = f"report_{date_str}_{timestamp.strftime('%H%M%S')}.json"
        json_path = os.path.join(self.output_dir, json_filename)
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save as readable text
        text_filename = f"report_{date_str}.txt"
        text_path = os.path.join(self.output_dir, text_filename)
        self._write_text_report(text_path, report)
        
        print(f"✓ Report saved: {json_path}")
        print(f"✓ Report saved: {text_path}")
        
        return json_path
    
    def _get_top_posts(self, posts: List[Dict], limit: int = 10) -> List[Dict]:
        """Get most engaging posts"""
        sorted_posts = sorted(
            posts,
            key=lambda p: p.get('likes', 0) + p.get('retweets', 0) * 2 + p.get('quotes', 0) * 3,
            reverse=True
        )
        return sorted_posts[:limit]
    
    def _gather_statistics(self, posts: List[Dict]) -> Dict[str, Any]:
        """Gather statistics about posts"""
        if not posts:
            return {}
        
        total_likes = sum(p.get('likes', 0) for p in posts)
        total_retweets = sum(p.get('retweets', 0) for p in posts)
        total_replies = sum(p.get('replies', 0) for p in posts)
        total_engagement = total_likes + total_retweets + total_replies
        
        verified_authors = sum(1 for p in posts if p.get('author_verified', False))
        avg_followers = sum(p.get('author_followers', 0) for p in posts) / len(posts) if posts else 0
        
        return {
            "total_posts": len(posts),
            "total_likes": total_likes,
            "total_retweets": total_retweets,
            "total_replies": total_replies,
            "total_engagement": total_engagement,
            "avg_engagement_per_post": total_engagement / len(posts) if posts else 0,
            "verified_authors": verified_authors,
            "avg_author_followers": int(avg_followers),
            "unique_authors": len(set(p.get('author') for p in posts))
        }
    
    def _write_text_report(self, filepath: str, report: Dict[str, Any]):
        """Write readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"DAILY X (TWITTER) AGENT REPORT\n")
            f.write(f"Generated: {report['generated_at']}\n")
            f.write("=" * 80 + "\n\n")
            
            # Statistics
            f.write("STATISTICS\n")
            f.write("-" * 40 + "\n")
            stats = report.get('statistics', {})
            for key, value in stats.items():
                f.write(f"{key.replace('_', ' ').title()}: {value:,}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("ANALYSIS & INSIGHTS\n")
            f.write("-" * 40 + "\n")
            
            analysis = report.get('analysis', {})
            if isinstance(analysis, dict):
                for key, value in analysis.items():
                    f.write(f"\n{key.upper()}:\n")
                    if isinstance(value, list):
                        for item in value:
                            f.write(f"  • {item}\n")
                    else:
                        f.write(f"{value}\n")
            else:
                f.write(str(analysis) + "\n")
            
            insights = report.get('insights', {})
            if insights:
                f.write("\n" + "=" * 80 + "\n")
                f.write("KEY INSIGHTS\n")
                f.write("-" * 40 + "\n")
                f.write(insights.get('raw_insights', '') + "\n")
            
            # Top posts
            f.write("\n" + "=" * 80 + "\n")
            f.write("TOP POSTS\n")
            f.write("-" * 40 + "\n")
            for i, post in enumerate(report.get('top_posts', []), 1):
                f.write(f"\n{i}. @{post.get('author', 'Unknown')}\n")
                f.write(f"   ❤️ {post.get('likes', 0)} | 🔄 {post.get('retweets', 0)} | "
                       f"💬 {post.get('replies', 0)}\n")
                f.write(f"   {post.get('text', '')[:200]}...\n")
            
            f.write("\n" + "=" * 80 + "\n")

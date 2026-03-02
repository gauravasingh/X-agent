"""
LLM-based analyzer for posts using Claude or OpenAI
"""
from typing import List, Dict, Any
from config import LLM_PROVIDER, ANTHROPIC_API_KEY, OPENAI_API_KEY
import anthropic
import openai
import json


class PostAnalyzer:
    def __init__(self):
        """Initialize LLM client based on provider"""
        self.provider = LLM_PROVIDER
        
        if self.provider == "claude":
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        elif self.provider == "openai":
            openai.api_key = OPENAI_API_KEY
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    def summarize_posts(self, posts: List[Dict], max_posts: int = 100) -> Dict[str, Any]:
        """
        Summarize and analyze posts using LLM
        
        Args:
            posts: List of post dictionaries
            max_posts: Maximum posts to analyze (recent ones prioritized)
            
        Returns:
            Analysis including summary, insights, and trending topics
        """
        # Use most recent posts
        posts_to_analyze = posts[:max_posts]
        
        # Format posts for analysis
        posts_text = self._format_posts_for_analysis(posts_to_analyze)
        
        prompt = f"""Analyze these X (Twitter) posts and provide:
1. Key trending topics and themes
2. Overall sentiment analysis
3. Most important/influential posts
4. Predictions about what's going on in the world

Posts to analyze:
{posts_text}

Provide your analysis in structured JSON format."""
        
        analysis = self._call_llm(prompt)
        return self._parse_analysis(analysis)
    
    def extract_insights(self, posts: List[Dict]) -> Dict[str, Any]:
        """
        Extract deep insights from posts
        
        Args:
            posts: List of posts
            
        Returns:
            Dictionary with insights
        """
        posts_text = self._format_posts_for_analysis(posts[:200])
        
        prompt = f"""From these X posts, identify and explain:
1. What major events or news are people discussing?
2. What's the sentiment around these topics?
3. Who are the key influencers driving these conversations?
4. What predictions can you make about what's really happening?
5. What should someone know about today's important events?

Posts:
{posts_text}

Be concise but insightful."""
        
        insights = self._call_llm(prompt)
        return {"raw_insights": insights}
    
    def _format_posts_for_analysis(self, posts: List[Dict]) -> str:
        """Format posts into a readable string for LLM analysis"""
        formatted = []
        for i, post in enumerate(posts, 1):
            formatted.append(
                f"{i}. [@{post.get('author', 'Unknown')}] "
                f"({post.get('likes', 0)} likes, {post.get('retweets', 0)} retweets)\n"
                f"   {post.get('text', '')[:300]}..."
            )
        return "\n".join(formatted)
    
    def _call_llm(self, prompt: str) -> str:
        """Call appropriate LLM with prompt"""
        try:
            if self.provider == "claude":
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2048,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text
            
            elif self.provider == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                return response['choices'][0]['message']['content']
        
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return f"Error: {str(e)}"
    
    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Try to parse analysis as JSON, fallback to raw text"""
        try:
            # Try to extract JSON from response
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = analysis_text[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
        
        return {"analysis": analysis_text}

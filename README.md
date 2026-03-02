# X Agent - Read 10,000+ Posts/Day from X and Generate Insights

A powerful AI agent that reads and analyzes thousands of X (Twitter) posts daily, identifying trends, key insights, and what's really happening in the world.

## Features

- **📡 X API Integration**: Fetches trending posts and searches by keywords
- **🤖 LLM-Powered Analysis**: Uses Claude or OpenAI to analyze and summarize posts
- **📊 Daily Reports**: Generates comprehensive daily reports with insights
- **📅 Scheduled Execution**: Can run automatically at set times each day
- **🎯 Multiple Modes**: Trending, keyword search, or full analysis
- **📈 Engagement Metrics**: Tracks likes, retweets, replies, and author influence

## Setup

### 1. Prerequisites

- Python 3.8+
- X (Twitter) API credentials (API v2)
- Claude or OpenAI API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get API Credentials

#### X API Credentials
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create/select your app
3. Go to Keys and Tokens
4. Generate/copy:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

#### LLM API Key
- **Claude**: Get from [Anthropic Console](https://console.anthropic.com/)
- **OpenAI**: Get from [OpenAI API Keys](https://platform.openai.com/api-keys)

### 4. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
X_BEARER_TOKEN=your_bearer_token_here
ANTHROPIC_API_KEY=your_anthropic_key_here
LLM_PROVIDER=claude
```

## Usage

### Run Immediately

#### Trending Posts Analysis
```bash
python main.py --mode trending --limit 1000
```

#### Keyword Search
```bash
python main.py --mode keywords --keywords "AI" "crypto" "tech" --limit 1000
```

#### Full Analysis (Trending + Keywords)
```bash
python main.py --mode full --limit 1000
```

#### Demo Mode (No API calls)
```bash
python main.py --mode demo
```

### Schedule Daily Runs

Run agent every day at 9:00 AM:
```bash
python scheduler.py --time 09:00 --mode trending
```

Run at a different time:
```bash
python scheduler.py --time 14:30 --mode full
```

## How It Works

1. **Fetch Posts**: Connects to X API and retrieves trending posts or keyword matches
2. **Process**: Filters for high-engagement, original content
3. **Analyze**: Sends posts to Claude/OpenAI for analysis
   - Identifies trending topics
   - Determines sentiment
   - Extracts key insights
   - Predicts emerging trends
4. **Report**: Generates JSON and readable reports saved to `./reports/`

## Output

Reports are saved in two formats:

- **JSON**: `report_YYYY-MM-DD_HHMMSS.json` - Structured data for programmatic use
- **Text**: `report_YYYY-MM-DD.txt` - Human-readable format

Reports include:
- Post statistics (total engagement, unique authors, etc.)
- LLM analysis (trends, sentiment, key topics)
- Top posts by engagement
- Author influence metrics

## Architecture

```
main.py              ← Entry point
├── x_handler.py     ← X API integration
├── llm_analyzer.py  ← LLM-powered analysis
├── report_generator.py ← Report creation
├── config.py        ← Configuration
├── scheduler.py     ← Daily scheduling
└── requirements.txt ← Dependencies
```

## Example Output

```
Report generated for: 2024-01-15

STATISTICS
Total posts: 1000
Total engagement: 245,892
Avg engagement per post: 245.89
Unique authors: 412
Verified authors: 48

ANALYSIS & INSIGHTS
Key Topics:
 • Artificial Intelligence regulation debate
 • Climate tech innovations
 • Fed monetary policy impact

Sentiment: 62% positive, 28% neutral, 10% negative

TOP POSTS
1. @influential_user
   ❤️ 1,234 | 🔄 456 | 💬 89
   Major breakthrough in quantum computing announced today...
```

## Advanced Configuration

### Adjust post limits
Edit `config.py`:
```python
POSTS_PER_RUN = 2000  # Posts per run
MAX_POSTS_PER_DAY = 10000  # Daily limit
```

### Change LLM provider
Edit `.env`:
```
LLM_PROVIDER=openai
```

### Custom keyword searches
Modify `main.py` keyword lists or pass via CLI:
```bash
python main.py --mode keywords --keywords "startup" "venture" "vc"
```

## Troubleshooting

- **API Rate Limits**: Agent automatically handles rate limiting with `wait_on_rate_limit=True`
- **No Posts Fetched**: Verify X Bearer token is valid and has v2 API access
- **LLM Errors**: Check your API key and rate limits for Claude/OpenAI

## Notes

- Fetches most recent and high-engagement posts
- Filters out retweets and replies for original content focus
- English language posts only
- Tracks author verification status and follower count
- Perfect for market research, trend monitoring, or staying informed

## License

MIT

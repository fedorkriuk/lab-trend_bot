# Tech Trend Bot

An automated system that monitors developer communities (GitHub, Reddit) for trending topics and generates platform-specific social media posts using AI.

## Features

- 🔍 **Multi-source ingestion**: Monitors GitHub trending repos and Reddit developer communities
- 📊 **Smart ranking**: Calculates trend scores based on activity and engagement
- 🤖 **AI-powered content**: Uses LLMs to generate platform-specific posts
- 🚀 **Multi-platform posting**: Supports X (Twitter) and LinkedIn
- ⏸️ **Pause/Resume control**: Multiple ways to pause operations safely
- 🧪 **Dry-run mode**: Test everything without actually posting
- 🐳 **Dockerized**: Easy deployment with Docker Compose

## Architecture

- **FastAPI**: Web server for control endpoints
- **Celery + Redis**: Distributed task queue and scheduling
- **PostgreSQL**: Persistent storage for events, trends, and posts
- **OpenAI API**: Content generation (configurable)

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/fedorkriuk/lab-trend_bot.git
cd lab-trend_bot/tech-trend-bot
cp .env.example .env
# Edit .env with your API keys
```

### 2. Configure Environment

Required variables in `.env`:
- `OPENAI_API_KEY`: For content generation
- `GITHUB_TOKEN`: For GitHub API access (optional initially)
- `REDDIT_CLIENT_ID/SECRET`: For Reddit API (optional initially)
- Platform tokens when ready to post

### 3. Run with Docker

```bash
docker compose up --build
```

### 4. Check Health

```bash
curl http://localhost:8000/health
```

## Control Commands

### Pause/Resume Operations

```bash
# Pause
curl -X POST http://localhost:8000/control/pause \
  -H "Content-Type: application/json" \
  -d '{"paused": true, "reason": "maintenance"}'

# Resume
curl -X POST http://localhost:8000/control/pause \
  -H "Content-Type: application/json" \
  -d '{"paused": false}'

# Check status
curl http://localhost:8000/control/status
```

### CLI Control (inside container)

```bash
docker compose exec web python -m src.scripts.ttbctl status
docker compose exec web python -m src.scripts.ttbctl pause
docker compose exec web python -m src.scripts.ttbctl resume
```

### Emergency Kill Switch

```bash
# Create kill file to pause immediately
docker compose exec web python -m src.scripts.ttbctl killswitch --on

# Remove to resume
docker compose exec web python -m src.scripts.ttbctl killswitch --off
```

## Development

### Monitor Logs

```bash
# All services
docker compose logs -f

# Specific services
docker compose logs -f worker beat web
```

### Database Access

```bash
docker compose exec postgres psql -U postgres -d ttb
```

### Common Queries

```sql
-- View recent events
SELECT * FROM events ORDER BY created_at DESC LIMIT 10;

-- View top trends
SELECT * FROM trends ORDER BY score DESC LIMIT 10;

-- View post drafts
SELECT * FROM post_drafts ORDER BY created_at DESC;
```

## Configuration

### Dry Run Mode

By default, `DRY_RUN=true` in `.env`. The bot will:
- Ingest data normally
- Calculate trends
- Generate post drafts
- Log what would be posted (without actually posting)

### Posting Configuration

To enable real posting:
1. Set `DRY_RUN=false`
2. Enable platforms individually:
   - `TWITTER_POSTING_ENABLED=true`
   - `LINKEDIN_POSTING_ENABLED=true`
3. Implement the TODOs in `src/tasks/post.py` for actual API calls

### Task Schedule

Edit `src/celery_app.py` to adjust timing:
- GitHub ingestion: 60s
- Reddit ingestion: 120s
- Trend ranking: 5m
- Post generation: 10m
- Publishing: 10m

## Deployment

### Production Checklist

1. **Environment**: Set `ENV=production`
2. **Secrets**: Use proper secret management
3. **SSL/TLS**: Set up HTTPS for API endpoints
4. **Monitoring**: Add Prometheus/Grafana
5. **Backups**: Automated PostgreSQL backups
6. **Rate Limiting**: Configure API rate limits
7. **Logging**: Centralized log collection

### Deployment Options

- **VPS**: Ubuntu + Docker Compose
- **Kubernetes**: Helm charts for scalability
- **Managed Services**: 
  - AWS ECS for containers
  - RDS for PostgreSQL
  - ElastiCache for Redis
- **Serverless**: Lambda functions + EventBridge

## API Documentation

### Endpoints

- `GET /health` - System health check
- `GET /control/status` - Current pause status
- `POST /control/pause` - Pause/resume operations

### Response Format

```json
{
  "status": "ok",
  "paused": false,
  "dry_run": true
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Issues: [GitHub Issues](https://github.com/fedorkriuk/lab-trend_bot/issues)
- Discussions: [GitHub Discussions](https://github.com/fedorkriuk/lab-trend_bot/discussions)

## Roadmap

- [ ] Real GitHub trending API integration
- [ ] Reddit subreddit monitoring
- [ ] X (Twitter) reading for signals
- [ ] Advanced trend scoring algorithms
- [ ] A/B testing for post performance
- [ ] Analytics dashboard
- [ ] Multiple LLM provider support
- [ ] Webhook notifications
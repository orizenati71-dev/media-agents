# media-agents

AI agents for media management - Hebrew Content Quality + Publishing Agent

## Hebrew Content Agent

A specialized AI agent for preparing Hebrew (or mixed Hebrew-English) video content for publishing with perfect natural Israeli Hebrew across social media platforms.

### Features

- **Hebrew QA**: Fixes spelling, grammar, and converts formal/robotic Hebrew into natural Israeli social Hebrew
- **Caption Generation**: Creates short punchy and longer captions with hooks and soft CTAs
- **Hashtag Generation**: Provides Israeli broad reach and niche-specific hashtag sets
- **Platform Adaptation**: Adjusts tone for TikTok, Instagram, and YouTube Shorts

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd media-agents

# Install with pip
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### CLI Usage

#### Full Content Processing

```bash
hebrew-agent process "הנה טיפ מדהים באפשרותך ליישם אותו מיד" \
    --topic "טיפים לפרודוקטיביות" \
    --audience "יזמים צעירים" \
    --vibe casual \
    --platforms "tiktok,instagram"
```

#### Quick Hebrew QA

```bash
hebrew-agent qa "באפשרותך לראות את התוצאות המדהימות"
```

#### Generate Hashtags

```bash
hebrew-agent hashtags "יזמות וטכנולוגיה" --platform instagram
```

#### Interactive Mode

```bash
hebrew-agent interactive
```

### Python API Usage

```python
from media_agents.agents import HebrewContentAgent
from media_agents.models import ContentInput, ClientVibe, Platform

# Create agent
agent = HebrewContentAgent()

# Prepare input
content = ContentInput(
    raw_caption="באפשרותך לראות תוצאות מדהימות כאשר תיישם את הטיפ הזה",
    video_topic="טיפים לפרודוקטיביות",
    target_audience="יזמים ובעלי עסקים",
    client_vibe=ClientVibe.EDUCATIONAL,
    platforms=[Platform.TIKTOK, Platform.INSTAGRAM],
)

# Process content
package = agent.process(content)

# Display formatted output
print(agent.format_output(package))

# Or access structured data
for platform_pkg in package.platforms:
    print(f"Platform: {platform_pkg.platform}")
    print(f"Caption A: {platform_pkg.caption_a}")
    print(f"Caption B: {platform_pkg.caption_b}")
    print(f"Hashtags: {platform_pkg.hashtags}")
```

### Client Vibes

- `casual` - קז'ואל, שפה יומיומית, אנרגטי
- `educational` - לימודי, ברור, מקצועי
- `motivational` - מוטיבציוני, השראתי, אמיתי
- `sales` - מכירתי רך, לא אגרסיבי

### Platform Tones

- **TikTok**: Fast + Casual - קצר, קליט, אנרגיה גבוהה
- **Instagram**: Emotional + Clean - רגשי, נקי, אסתטי
- **YouTube Shorts**: Authority + Clarity - סמכותי, ברור, ערך מוסף

### Hebrew QA Rules

The agent automatically:

1. Converts formal Hebrew to spoken Israeli Hebrew
2. Removes/replaces cringe marketing phrases
3. Fixes common spelling errors
4. Cleans up text structure

**Avoided phrases:**
- "הזדמנות אחרונה"
- "מדהים" / "מהפכני"
- "לא תאמינו"
- Other generic marketing language

**Formal to casual conversions:**
- "באפשרותך" → "אתה יכול"
- "ניתן ל" → "אפשר ל"
- "על מנת ש" → "כדי ש"
- And many more...

### Output Format

The agent produces a complete publishing package including:

```
PLATFORM: [TikTok/Instagram/YouTube Shorts]
Caption A: [Short punchy caption]
Caption B: [Longer caption with more context]
Hashtags: [Platform-optimized hashtag set]
Posting suggestion: [Best times and strategies]
Tone notes: [Platform-specific tone guidance]
```

### Project Structure

```
media-agents/
├── src/
│   └── media_agents/
│       ├── __init__.py
│       ├── cli.py              # CLI interface
│       ├── models.py           # Pydantic data models
│       ├── agents/
│       │   ├── __init__.py
│       │   └── hebrew_content_agent.py  # Main agent
│       └── utils/
│           ├── __init__.py
│           ├── hebrew_qa.py    # Hebrew QA processor
│           ├── captions.py     # Caption generator
│           ├── hashtags.py     # Hashtag generator
│           └── platform_adapter.py  # Platform adaptation
├── pyproject.toml
└── README.md
```

### Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

## License

MIT

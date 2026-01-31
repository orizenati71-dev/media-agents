"""Hashtag generation module for Hebrew social media content."""

from dataclasses import dataclass, field

from ..models import HashtagSet, Platform


@dataclass
class HashtagGenerator:
    """Generate Hebrew hashtag sets for social media publishing."""

    # Israeli broad reach hashtags
    broad_reach_base: list[str] = field(default_factory=lambda: [
        "#ישראל",
        "#תלאביב",
        "#ישראלי",
        "#עברית",
        "#חיים",
        "#יזמות",
        "#השראה",
        "#טיפים",
        "#לייף",
        "#ישראלים",
        "#תוכן",
        "#קריירה",
        "#פיתוחאישי",
        "#מוטיבציה",
        "#הצלחה",
        "#יומיום",
        "#fyp",
        "#foryou",
        "#viral",
        "#trending",
    ])

    # Niche hashtags by category
    niche_categories: dict[str, list[str]] = field(default_factory=lambda: {
        "business": [
            "#עסקים",
            "#יזמות",
            "#עסקיםקטנים",
            "#מיתוג",
            "#שיווק",
            "#דיגיטל",
            "#סושיאל",
            "#פרילנס",
            "#עצמאים",
            "#סטארטאפ",
            "#ביזנס",
            "#כסף",
            "#הכנסה",
            "#השקעות",
        ],
        "lifestyle": [
            "#לייפסטייל",
            "#שגרה",
            "#יומיומי",
            "#בית",
            "#משפחה",
            "#זוגיות",
            "#הורות",
            "#ילדים",
            "#אמא",
            "#אבא",
            "#חיידקהסדר",
            "#ארגון",
        ],
        "fitness": [
            "#כושר",
            "#אימון",
            "#בריאות",
            "#תזונה",
            "#ספורט",
            "#חדרכושר",
            "#דיאטה",
            "#גוף",
            "#פיטנס",
            "#אימוןבית",
            "#ירידהבמשקל",
        ],
        "food": [
            "#אוכל",
            "#מתכון",
            "#בישול",
            "#מטבח",
            "#טעים",
            "#אוכלביתי",
            "#מתכונים",
            "#שף",
            "#בריא",
            "#טבעוני",
            "#צמחוני",
        ],
        "tech": [
            "#טכנולוגיה",
            "#הייטק",
            "#תכנות",
            "#קוד",
            "#סטארטאפ",
            "#אפליקציה",
            "#דיגיטל",
            "#AI",
            "#בינהמלאכותית",
            "#חדשנות",
        ],
        "beauty": [
            "#יופי",
            "#איפור",
            "#טיפוח",
            "#עור",
            "#שיער",
            "#ביוטי",
            "#סקינקר",
            "#מייקאפ",
            "#טיפוחפנים",
            "#קוסמטיקה",
        ],
        "fashion": [
            "#אופנה",
            "#סטייל",
            "#לבוש",
            "#אאוטפיט",
            "#ootd",
            "#fashionisrael",
            "#בגדים",
            "#נעליים",
            "#תיקים",
            "#אקססוריז",
        ],
        "education": [
            "#לימודים",
            "#למידה",
            "#השכלה",
            "#קורס",
            "#הכשרה",
            "#מקצוע",
            "#תואר",
            "#סטודנטים",
            "#ידע",
            "#מיומנויות",
        ],
        "travel": [
            "#טיול",
            "#נסיעה",
            "#תיירות",
            "#חופש",
            "#מטייל",
            "#ישראל",
            "#חול",
            "#יעדים",
            "#טיסה",
            "#מלון",
        ],
        "content": [
            "#יוצרתוכן",
            "#קריאייטור",
            "#קונטנט",
            "#סושיאלמדיה",
            "#אינסטגרם",
            "#טיקטוק",
            "#יוטיוב",
            "#ריילס",
            "#וידאו",
            "#עריכה",
        ],
        "motivation": [
            "#מוטיבציה",
            "#השראה",
            "#פיתוחאישי",
            "#הצלחה",
            "#חלומות",
            "#מטרות",
            "#אמונה",
            "#כוח",
            "#צמיחה",
            "#שינוי",
        ],
    })

    # Platform-specific tags
    platform_tags: dict[Platform, list[str]] = field(default_factory=lambda: {
        Platform.TIKTOK: [
            "#טיקטוק",
            "#טיקטוקישראל",
            "#tiktokisrael",
            "#fyp",
            "#foryoupage",
            "#viral",
            "#trending",
            "#ויראלי",
        ],
        Platform.INSTAGRAM: [
            "#אינסטגרם",
            "#instaisrael",
            "#igisrael",
            "#reels",
            "#reelsisrael",
            "#explorepage",
            "#instagood",
        ],
        Platform.YOUTUBE_SHORTS: [
            "#shorts",
            "#youtubeshorts",
            "#יוטיוב",
            "#youtube",
            "#shortsisrael",
            "#ytshorts",
        ],
    })

    def generate(
        self,
        topic: str,
        platform: Platform,
        max_hashtags: int = 15,
    ) -> HashtagSet:
        """Generate hashtag sets for broad reach and niche targeting."""
        # Detect relevant niche categories from topic
        relevant_niches = self._detect_niches(topic)

        # Build broad reach set
        broad_reach = self._build_broad_reach(platform, max_hashtags // 2)

        # Build niche specific set
        niche_specific = self._build_niche_set(relevant_niches, platform, max_hashtags // 2)

        return HashtagSet(broad_reach=broad_reach, niche_specific=niche_specific)

    def _detect_niches(self, topic: str) -> list[str]:
        """Detect relevant niche categories from topic text."""
        topic_lower = topic.lower()
        detected = []

        # Keyword mapping to categories
        keyword_to_niche = {
            "business": ["עסק", "כסף", "מכירות", "שיווק", "לקוחות", "יזמות", "עצמאי", "פרילנס"],
            "lifestyle": ["חיים", "בית", "משפחה", "יומיום", "שגרה", "זוגיות", "ילדים"],
            "fitness": ["כושר", "אימון", "בריאות", "ספורט", "דיאטה", "משקל", "גוף"],
            "food": ["אוכל", "מתכון", "בישול", "מטבח", "אכילה", "ארוחה", "טעים"],
            "tech": ["טכנולוגיה", "אפליקציה", "קוד", "תכנות", "הייטק", "מחשב", "AI"],
            "beauty": ["יופי", "איפור", "טיפוח", "עור", "שיער", "פנים"],
            "fashion": ["אופנה", "בגדים", "סטייל", "לבוש", "נעליים"],
            "education": ["לימודים", "קורס", "למידה", "הכשרה", "ידע"],
            "travel": ["טיול", "נסיעה", "חופש", "מלון", "טיסה", "יעד"],
            "content": ["תוכן", "קריאייטור", "וידאו", "עריכה", "סושיאל"],
            "motivation": ["מוטיבציה", "השראה", "הצלחה", "חלומות", "מטרות", "שינוי"],
        }

        for niche, keywords in keyword_to_niche.items():
            for keyword in keywords:
                if keyword in topic_lower:
                    if niche not in detected:
                        detected.append(niche)
                    break

        # Default to content + motivation if nothing detected
        if not detected:
            detected = ["content", "motivation"]

        return detected[:3]  # Max 3 niches

    def _build_broad_reach(self, platform: Platform, count: int) -> list[str]:
        """Build broad reach hashtag set."""
        tags = []

        # Add platform-specific tags first
        platform_specific = self.platform_tags.get(platform, [])
        tags.extend(platform_specific[:3])

        # Fill with broad reach tags
        remaining = count - len(tags)
        tags.extend(self.broad_reach_base[:remaining])

        return tags[:count]

    def _build_niche_set(
        self, niches: list[str], platform: Platform, count: int
    ) -> list[str]:
        """Build niche-specific hashtag set."""
        tags = []

        # Collect tags from relevant niches
        for niche in niches:
            if niche in self.niche_categories:
                niche_tags = self.niche_categories[niche]
                # Take a portion from each niche
                per_niche = max(3, count // len(niches))
                tags.extend(niche_tags[:per_niche])

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return unique_tags[:count]

    def combine_hashtags(
        self, hashtag_set: HashtagSet, platform: Platform
    ) -> list[str]:
        """Combine hashtag sets with platform-appropriate count."""
        # Platform hashtag limits (recommended, not enforced)
        limits = {
            Platform.TIKTOK: 8,
            Platform.INSTAGRAM: 20,
            Platform.YOUTUBE_SHORTS: 10,
        }

        limit = limits.get(platform, 15)

        # Combine: broad reach first, then niche
        combined = []
        combined.extend(hashtag_set.broad_reach)
        combined.extend(hashtag_set.niche_specific)

        # Remove duplicates
        seen = set()
        unique = []
        for tag in combined:
            if tag not in seen:
                seen.add(tag)
                unique.append(tag)

        return unique[:limit]

    def format_hashtags(self, hashtags: list[str], inline: bool = False) -> str:
        """Format hashtags for display."""
        if inline:
            return " ".join(hashtags)
        else:
            return "\n".join(hashtags)

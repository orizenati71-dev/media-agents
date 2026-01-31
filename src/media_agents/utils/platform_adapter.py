"""Platform adaptation module for social media content optimization."""

from dataclasses import dataclass, field

from ..models import CaptionSet, ClientVibe, Platform, PlatformPackage


@dataclass
class PlatformAdapter:
    """Adapt content for specific social media platforms."""

    # Platform characteristics
    platform_profiles: dict[Platform, dict] = field(default_factory=lambda: {
        Platform.TIKTOK: {
            "name": "TikTok",
            "name_hebrew": "טיקטוק",
            "tone": "fast + casual",
            "max_caption_length": 150,
            "characteristics": [
                "קצר וקליט",
                "אנרגיה גבוהה",
                "שפה צעירה",
                "טרנדי",
            ],
            "best_posting_times": [
                "19:00-22:00 ימי חול",
                "12:00-15:00 סופ״ש",
            ],
            "emoji_style": "minimal",
        },
        Platform.INSTAGRAM: {
            "name": "Instagram",
            "name_hebrew": "אינסטגרם",
            "tone": "emotional + clean",
            "max_caption_length": 500,
            "characteristics": [
                "רגשי ומחובר",
                "ויזואלי",
                "נקי ומסודר",
                "אסתטי",
            ],
            "best_posting_times": [
                "11:00-13:00 ימי חול",
                "19:00-21:00 ערב",
                "10:00-12:00 שישי",
            ],
            "emoji_style": "moderate",
        },
        Platform.YOUTUBE_SHORTS: {
            "name": "YouTube Shorts",
            "name_hebrew": "יוטיוב שורטס",
            "tone": "authority + clarity",
            "max_caption_length": 100,
            "characteristics": [
                "סמכותי",
                "ברור",
                "ערך מוסף",
                "מקצועי",
            ],
            "best_posting_times": [
                "15:00-18:00 ימי חול",
                "20:00-22:00 ערב",
            ],
            "emoji_style": "minimal",
        },
    })

    # Tone adjustments by platform
    tone_adjustments: dict[Platform, dict[str, str]] = field(default_factory=lambda: {
        Platform.TIKTOK: {
            "אני רוצה": "אני חייב",
            "כדאי ל": "חייבים ל",
            "חשוב ש": "שימו לב",
            "בואו נדבר": "נו אז",
            "הנה": "זהו",
        },
        Platform.INSTAGRAM: {
            "נו": "",
            "יאללה": "הנה",
            "סבבה": "מושלם",
            "אחלה": "נפלא",
        },
        Platform.YOUTUBE_SHORTS: {
            "נו": "",
            "יאללה": "בואו",
            "סבבה": "טוב",
            "אחלה": "מצוין",
            "מגניב": "יעיל",
        },
    })

    def adapt(
        self,
        caption_set: CaptionSet,
        platform: Platform,
        vibe: ClientVibe,
        hashtags: list[str],
        topic: str,
    ) -> PlatformPackage:
        """Adapt content for a specific platform."""
        profile = self.platform_profiles[platform]

        # Adapt captions
        adapted_short = self._adapt_caption(
            caption_set.caption_short, platform, profile["max_caption_length"]
        )
        adapted_long = self._adapt_caption(
            caption_set.caption_long, platform, profile["max_caption_length"] + 200
        )

        # Generate posting suggestion
        posting_suggestion = self._generate_posting_suggestion(platform, vibe, topic)

        # Generate tone notes
        tone_notes = self._generate_tone_notes(platform, vibe)

        return PlatformPackage(
            platform=platform,
            caption_a=adapted_short,
            caption_b=adapted_long,
            hashtags=hashtags,
            posting_suggestion=posting_suggestion,
            tone_notes=tone_notes,
        )

    def _adapt_caption(
        self, caption: str, platform: Platform, max_length: int
    ) -> str:
        """Adapt caption text for platform."""
        adapted = caption

        # Apply platform-specific tone adjustments
        adjustments = self.tone_adjustments.get(platform, {})
        for original, replacement in adjustments.items():
            adapted = adapted.replace(original, replacement)

        # Clean up any double spaces from replacements
        while "  " in adapted:
            adapted = adapted.replace("  ", " ")

        # Trim if too long
        if len(adapted) > max_length:
            # Find last complete sentence within limit
            sentences = adapted.split(". ")
            trimmed = ""
            for sentence in sentences:
                if len(trimmed) + len(sentence) + 2 <= max_length - 3:
                    trimmed += sentence + ". "
                else:
                    break
            if trimmed:
                adapted = trimmed.strip()
            else:
                # Just truncate with ellipsis
                adapted = adapted[: max_length - 3] + "..."

        return adapted.strip()

    def _generate_posting_suggestion(
        self, platform: Platform, vibe: ClientVibe, topic: str
    ) -> str:
        """Generate posting time/strategy suggestions."""
        profile = self.platform_profiles[platform]
        times = profile["best_posting_times"]

        suggestions = []

        # Base timing suggestion
        suggestions.append(f"זמנים מומלצים: {', '.join(times)}")

        # Vibe-specific suggestions
        if vibe == ClientVibe.EDUCATIONAL:
            suggestions.append("תוכן לימודי עובד טוב בבוקר כשאנשים פתוחים ללמוד")
        elif vibe == ClientVibe.MOTIVATIONAL:
            suggestions.append("תוכן מוטיבציוני עובד טוב בתחילת שבוע או בבוקר")
        elif vibe == ClientVibe.SALES:
            suggestions.append("תוכן מכירתי עובד טוב בסוף שבוע כשיש יותר זמן פנוי")
        elif vibe == ClientVibe.CASUAL:
            suggestions.append("תוכן קז׳ואל עובד טוב בשעות הערב")

        # Platform-specific
        if platform == Platform.TIKTOK:
            suggestions.append("בטיקטוק חשוב להעלות בתדירות גבוהה - לפחות פעם ביום")
        elif platform == Platform.INSTAGRAM:
            suggestions.append("באינסטגרם כדאי להיות אקטיבי בסטוריז לפני ואחרי הפוסט")
        elif platform == Platform.YOUTUBE_SHORTS:
            suggestions.append("ביוטיוב שורטס חשוב הכותרת והתיאור ל-SEO")

        return " | ".join(suggestions)

    def _generate_tone_notes(self, platform: Platform, vibe: ClientVibe) -> str:
        """Generate notes about tone adaptation."""
        profile = self.platform_profiles[platform]

        notes = []

        # Platform tone
        notes.append(f"טון {profile['name_hebrew']}: {profile['tone']}")

        # Characteristics
        chars = ", ".join(profile["characteristics"][:3])
        notes.append(f"מאפיינים: {chars}")

        # Vibe alignment
        vibe_notes = {
            ClientVibe.CASUAL: "מתאים מאוד לטון הפלטפורמה",
            ClientVibe.EDUCATIONAL: "שמור על בהירות בלי להיות מורה",
            ClientVibe.MOTIVATIONAL: "אמיתי ולא גנרי",
            ClientVibe.SALES: "רך ולא אגרסיבי",
        }
        notes.append(vibe_notes.get(vibe, ""))

        # Emoji guidance
        notes.append(f"אימוג׳י: {profile['emoji_style']}")

        return " | ".join(note for note in notes if note)

    def get_platform_summary(self, platform: Platform) -> str:
        """Get a summary of platform characteristics."""
        profile = self.platform_profiles[platform]

        lines = [
            f"פלטפורמה: {profile['name_hebrew']}",
            f"טון: {profile['tone']}",
            f"אורך מומלץ: עד {profile['max_caption_length']} תווים",
            f"מאפיינים: {', '.join(profile['characteristics'])}",
            f"זמני פרסום: {', '.join(profile['best_posting_times'])}",
        ]

        return "\n".join(lines)

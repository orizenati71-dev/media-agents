"""Caption generation module for Hebrew social media content."""

from dataclasses import dataclass, field

from ..models import CaptionSet, ClientVibe, Platform


@dataclass
class CaptionGenerator:
    """Generate Hebrew captions optimized for social media platforms."""

    # Hook starters by vibe
    hook_starters: dict[ClientVibe, list[str]] = field(default_factory=lambda: {
        ClientVibe.CASUAL: [
            "אוקיי אז",
            "שימו לב לזה",
            "רגע,",
            "בואו נדבר על",
            "אז ככה",
            "יאללה",
            "נו טוב",
        ],
        ClientVibe.EDUCATIONAL: [
            "הנה משהו שלא ידעתם:",
            "טיפ מהיר:",
            "עובדה:",
            "דבר אחד שחשוב להבין:",
            "שאלה:",
            "בואו נבין משהו:",
        ],
        ClientVibe.MOTIVATIONAL: [
            "זה הזמן שלך",
            "מה שאתם צריכים לשמוע:",
            "האמת?",
            "קחו את זה:",
            "הדבר הזה שינה לי הכל:",
            "תזכרו:",
        ],
        ClientVibe.SALES: [
            "חיכיתם לזה:",
            "סוף סוף:",
            "הנה מה שעובד:",
            "גיליתי משהו:",
            "עצרו הכל.",
            "זהו.",
        ],
    })

    # Soft CTA phrases
    soft_ctas: dict[ClientVibe, list[str]] = field(default_factory=lambda: {
        ClientVibe.CASUAL: [
            "מה אתם אומרים?",
            "ספרו לי בתגובות",
            "שתפו אם הזדהיתם",
            "תייגו מישהו שצריך לראות את זה",
            "שמרו לאחר כך",
        ],
        ClientVibe.EDUCATIONAL: [
            "שמרו את הפוסט הזה",
            "עקבו לעוד טיפים",
            "יש לכם שאלות? כתבו לי",
            "רוצים לדעת עוד?",
            "שתפו עם מישהו שזה רלוונטי לו",
        ],
        ClientVibe.MOTIVATIONAL: [
            "מי איתי?",
            "תייגו מישהו שצריך לשמוע את זה",
            "שלחו למישהו שאתם אוהבים",
            "שמרו והחזיקו חזק",
        ],
        ClientVibe.SALES: [
            "קישור בביו",
            "שלחו הודעה ל",
            "כתבו לי בפרטי",
            "תייגו מישהו שזה רלוונטי לו",
            "רוצים פרטים? כתבו",
        ],
    })

    def generate(
        self,
        corrected_text: str,
        topic: str,
        vibe: ClientVibe,
        platform: Platform,
    ) -> CaptionSet:
        """Generate short and long caption versions."""
        hooks = self.hook_starters.get(vibe, self.hook_starters[ClientVibe.CASUAL])
        ctas = self.soft_ctas.get(vibe, self.soft_ctas[ClientVibe.CASUAL])

        # Select hook and CTA based on content
        hook = self._select_best_hook(hooks, topic)
        cta = self._select_best_cta(ctas, platform)

        # Generate short caption (punchy)
        caption_short = self._create_short_caption(corrected_text, hook, cta, platform)

        # Generate longer caption
        caption_long = self._create_long_caption(corrected_text, hook, cta, platform, topic)

        return CaptionSet(caption_short=caption_short, caption_long=caption_long)

    def _select_best_hook(self, hooks: list[str], topic: str) -> str:
        """Select the most appropriate hook based on topic."""
        # Simple selection - in production, could use more sophisticated matching
        topic_lower = topic.lower()

        # Question-based topics get question hooks
        if "?" in topic or "למה" in topic or "איך" in topic:
            question_hooks = [h for h in hooks if h.endswith("?") or h.endswith(":")]
            if question_hooks:
                return question_hooks[0]

        return hooks[0]

    def _select_best_cta(self, ctas: list[str], platform: Platform) -> str:
        """Select CTA based on platform."""
        if platform == Platform.TIKTOK:
            # TikTok prefers engagement CTAs
            engagement_ctas = [c for c in ctas if "תגובות" in c or "תייגו" in c or "?" in c]
            if engagement_ctas:
                return engagement_ctas[0]
        elif platform == Platform.INSTAGRAM:
            # Instagram - save and share focused
            save_ctas = [c for c in ctas if "שמרו" in c or "שתפו" in c]
            if save_ctas:
                return save_ctas[0]
        elif platform == Platform.YOUTUBE_SHORTS:
            # YouTube - follow focused
            follow_ctas = [c for c in ctas if "עקבו" in c or "עוד" in c]
            if follow_ctas:
                return follow_ctas[0]

        return ctas[0]

    def _create_short_caption(
        self, text: str, hook: str, cta: str, platform: Platform
    ) -> str:
        """Create short, punchy caption."""
        # Extract key message from text (first sentence or key phrase)
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

        if not sentences:
            key_message = text[:100]
        else:
            key_message = sentences[0]
            # Keep it short
            if len(key_message) > 80:
                words = key_message.split()
                key_message = " ".join(words[:12])
                if not key_message.endswith((".", "!", "?")):
                    key_message += "..."

        # Compose caption
        caption = f"{hook} {key_message}"

        # Add CTA for non-TikTok (TikTok captions should be minimal)
        if platform != Platform.TIKTOK:
            caption += f"\n\n{cta}"

        return caption.strip()

    def _create_long_caption(
        self, text: str, hook: str, cta: str, platform: Platform, topic: str
    ) -> str:
        """Create longer, more detailed caption."""
        # For long caption, include more context
        caption_parts = []

        # Hook
        caption_parts.append(hook)

        # Main content (cleaned and condensed)
        main_content = text.strip()
        if len(main_content) > 300:
            # Condense if too long
            sentences = [s.strip() for s in main_content.replace("!", ".").replace("?", ".").split(".") if s.strip()]
            main_content = ". ".join(sentences[:4]) + "."

        caption_parts.append(main_content)

        # Platform-specific additions
        if platform == Platform.INSTAGRAM:
            # Instagram likes line breaks
            caption_parts.append("")  # Empty line for spacing

        # CTA
        caption_parts.append(cta)

        # Join with appropriate spacing
        if platform == Platform.TIKTOK:
            return " ".join(part for part in caption_parts if part)
        else:
            return "\n\n".join(part for part in caption_parts if part)

    def add_emojis(self, caption: str, max_emojis: int = 2) -> str:
        """Optionally add relevant emojis (max 2 as per rules)."""
        # Common social media emojis that work well
        emoji_map = {
            "טיפ": "💡",
            "חשוב": "⚡",
            "אהבה": "❤️",
            "כסף": "💰",
            "עבודה": "💼",
            "בריאות": "🏃",
            "אוכל": "🍽️",
            "נסיעה": "✈️",
            "לימוד": "📚",
            "הצלחה": "🎯",
            "שאלה": "🤔",
            "רעיון": "💡",
        }

        added = 0
        for keyword, emoji in emoji_map.items():
            if keyword in caption and added < max_emojis:
                # Add emoji at the end of the line containing the keyword
                lines = caption.split("\n")
                for i, line in enumerate(lines):
                    if keyword in line and emoji not in line:
                        lines[i] = line + f" {emoji}"
                        added += 1
                        break
                caption = "\n".join(lines)

            if added >= max_emojis:
                break

        return caption

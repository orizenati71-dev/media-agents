"""Short Form Hook Agent.

This agent generates compelling hooks (attention-grabbing openings) for short-form
video content across TikTok, Instagram Reels, and YouTube Shorts.
"""

from dataclasses import dataclass, field

from ..models import (
    ClientVibe,
    Hook,
    HookInput,
    HookOutput,
    HookPackage,
    HookType,
    HookVariation,
    Platform,
)


@dataclass
class HookTemplates:
    """Templates and patterns for generating hooks by type."""

    # Hebrew hook templates by type and vibe
    templates: dict[HookType, dict[ClientVibe, list[str]]] = field(
        default_factory=lambda: {
            HookType.QUESTION: {
                ClientVibe.CASUAL: [
                    "מה אם אגיד לכם ש{topic}?",
                    "רגע, אתם באמת חושבים ש{topic}?",
                    "למה אף אחד לא מדבר על {topic}?",
                ],
                ClientVibe.EDUCATIONAL: [
                    "ידעתם ש{topic}?",
                    "מה ההבדל בין {topic}?",
                    "איך בעצם עובד {topic}?",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "מה מונע ממך {topic}?",
                    "למה אתם עדיין לא {topic}?",
                    "מוכנים לשנות את {topic}?",
                ],
                ClientVibe.SALES: [
                    "רוצים לדעת איך {topic}?",
                    "מחפשים פתרון ל{topic}?",
                    "נמאס לכם מ{topic}?",
                ],
            },
            HookType.BOLD_STATEMENT: {
                ClientVibe.CASUAL: [
                    "{topic} - וזהו, נקודה.",
                    "אני אומר את זה - {topic}.",
                    "בואו נדבר על {topic}.",
                ],
                ClientVibe.EDUCATIONAL: [
                    "הנה האמת על {topic}.",
                    "{topic} - ומדע מוכיח את זה.",
                    "זה מה שאף אחד לא מספר לכם על {topic}.",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "אתם יכולים {topic}.",
                    "{topic} - ואני הולך להוכיח לכם.",
                    "היום זה היום ש{topic}.",
                ],
                ClientVibe.SALES: [
                    "זה הסוד ל{topic}.",
                    "{topic} - והנה איך.",
                    "תעצרו הכל - {topic}.",
                ],
            },
            HookType.STORY: {
                ClientVibe.CASUAL: [
                    "אז לפני שבוע קרה לי משהו מטורף עם {topic}...",
                    "סיפור קצר על {topic}...",
                    "הייתי בדיוק באמצע {topic} כש...",
                ],
                ClientVibe.EDUCATIONAL: [
                    "בשנת 2023 גיליתי משהו על {topic}...",
                    "כשהתחלתי לחקור {topic}, גיליתי ש...",
                    "הנה מה שלמדתי על {topic}...",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "לפני שנה הייתי במקום אחר לגמרי עם {topic}...",
                    "כשהכל התחיל להתפרק, {topic}...",
                    "הרגע שהכל השתנה עם {topic}...",
                ],
                ClientVibe.SALES: [
                    "לקוח שלי בא אליי עם בעיה של {topic}...",
                    "קיבלתי הודעה שאמרה {topic}...",
                    "מישהו שאל אותי על {topic} ו...",
                ],
            },
            HookType.STATISTIC: {
                ClientVibe.CASUAL: [
                    "90% מהאנשים לא יודעים את זה על {topic}.",
                    "רק 3% מצליחים ב{topic}.",
                    "8 מתוך 10 אנשים טועים לגבי {topic}.",
                ],
                ClientVibe.EDUCATIONAL: [
                    "מחקרים מראים ש{topic}.",
                    "הנתונים מדברים - {topic}.",
                    "לפי המספרים, {topic}.",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "אתם חלק מה-1% אם {topic}.",
                    "רק 5% מהאנשים באמת {topic}.",
                    "הסטטיסטיקה נגדכם, אבל {topic}.",
                ],
                ClientVibe.SALES: [
                    "הלקוחות שלנו ראו עלייה של 300% ב{topic}.",
                    "בממוצע, אנשים חוסכים 50% על {topic}.",
                    "97% ממי שניסה {topic}.",
                ],
            },
            HookType.CONTROVERSIAL: {
                ClientVibe.CASUAL: [
                    "אני הולך לעצבן אנשים עכשיו - {topic}.",
                    "דעה לא פופולרית: {topic}.",
                    "אני יודע שזה שנוי במחלוקת, אבל {topic}.",
                ],
                ClientVibe.EDUCATIONAL: [
                    "כולם טועים לגבי {topic}.",
                    "הנה למה המומחים לא צודקים על {topic}.",
                    "בניגוד למה שלימדו אתכם, {topic}.",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "תפסיקו להאמין שאתם לא יכולים {topic}.",
                    "כולם אמרו לי שזה בלתי אפשרי, אבל {topic}.",
                    "הגיע הזמן לשבור את המיתוס על {topic}.",
                ],
                ClientVibe.SALES: [
                    "המתחרים לא רוצים שתדעו על {topic}.",
                    "הסוד ששומרים ממכם על {topic}.",
                    "למה כולם משלמים יותר מדי על {topic}?",
                ],
            },
            HookType.CURIOSITY_GAP: {
                ClientVibe.CASUAL: [
                    "זה הדבר שאף אחד לא מספר לכם על {topic}...",
                    "חכו לסוף כדי לראות מה קורה עם {topic}.",
                    "מה שאני עומד לחשוף על {topic}...",
                ],
                ClientVibe.EDUCATIONAL: [
                    "יש סיבה נסתרת למה {topic}...",
                    "הנה מה שחסר לכם על {topic}...",
                    "הפרט הזה על {topic} ישנה הכל...",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "הטריק הזה שינה לי את החיים עם {topic}...",
                    "גיליתי משהו שכולם צריכים לדעת על {topic}...",
                    "אחרי שתראו את זה, {topic} לעולם לא יהיה אותו דבר.",
                ],
                ClientVibe.SALES: [
                    "הנה למה הלקוחות שלנו לא חוזרים לשיטה הישנה של {topic}...",
                    "יש דבר אחד שמבדיל אותנו בנושא {topic}...",
                    "השינוי הקטן הזה ב{topic} עשה את כל ההבדל...",
                ],
            },
            HookType.DIRECT_ADDRESS: {
                ClientVibe.CASUAL: [
                    "אם אתם מתמודדים עם {topic}, תשמעו.",
                    "זה בשבילכם אם {topic}.",
                    "עצרו - אם {topic}, אתם חייבים לראות את זה.",
                ],
                ClientVibe.EDUCATIONAL: [
                    "אם אתם רוצים להבין {topic}, הנה המדריך.",
                    "למי שמחפש ללמוד על {topic}.",
                    "בשבילכם שרוצים לדעת יותר על {topic}.",
                ],
                ClientVibe.MOTIVATIONAL: [
                    "אם נמאס לכם מ{topic}, הנה הפתרון.",
                    "לכל מי שחולם על {topic} - זה הזמן.",
                    "אם אתם מוכנים לשנות את {topic}, תתחילו כאן.",
                ],
                ClientVibe.SALES: [
                    "אם אתם עדיין סובלים מ{topic}, יש פתרון.",
                    "למי ששואל איך {topic} - הנה התשובה.",
                    "אם אתם מחפשים {topic}, מצאתם.",
                ],
            },
        }
    )

    def get_template(
        self, hook_type: HookType, vibe: ClientVibe, index: int = 0
    ) -> str:
        """Get a template for the given hook type and vibe."""
        templates = self.templates.get(hook_type, {}).get(vibe, [])
        if not templates:
            return "{topic}"
        return templates[index % len(templates)]


@dataclass
class PlatformOptimizer:
    """Optimizes hooks for specific platforms."""

    platform_guidelines: dict[Platform, dict] = field(
        default_factory=lambda: {
            Platform.TIKTOK: {
                "max_duration": "3 seconds",
                "style": "punchy, trendy, direct",
                "visual_focus": "face close-up or action",
                "text_overlay": True,
            },
            Platform.INSTAGRAM: {
                "max_duration": "4 seconds",
                "style": "polished, aesthetic, engaging",
                "visual_focus": "visually appealing composition",
                "text_overlay": True,
            },
            Platform.YOUTUBE_SHORTS: {
                "max_duration": "5 seconds",
                "style": "informative, value-driven, clear",
                "visual_focus": "clear and professional",
                "text_overlay": True,
            },
        }
    )

    def optimize_for_platform(
        self, hook_text: str, platform: Platform, topic: str
    ) -> HookVariation:
        """Optimize a hook for a specific platform."""
        guidelines = self.platform_guidelines.get(platform, {})

        # Platform-specific adjustments
        optimized_text = hook_text
        if platform == Platform.TIKTOK:
            # TikTok prefers shorter, more direct hooks
            optimized_text = self._make_punchier(hook_text)
        elif platform == Platform.YOUTUBE_SHORTS:
            # YouTube Shorts can be slightly more informative
            optimized_text = self._add_value_hint(hook_text)

        visual_suggestions = {
            Platform.TIKTOK: f"תקריב פנים עם אנרגיה גבוהה, תנועת ידיים דינמית",
            Platform.INSTAGRAM: f"קומפוזיציה אסתטית, תאורה טובה, מבט ישיר למצלמה",
            Platform.YOUTUBE_SHORTS: f"מסגור ברור, רקע נקי, הבעת פנים מסקרנת",
        }

        text_overlays = {
            Platform.TIKTOK: self._generate_text_overlay(topic, short=True),
            Platform.INSTAGRAM: self._generate_text_overlay(topic, short=True),
            Platform.YOUTUBE_SHORTS: self._generate_text_overlay(topic, short=False),
        }

        return HookVariation(
            platform=platform,
            hook_text=optimized_text,
            visual_suggestion=visual_suggestions.get(
                platform, "הקפידו על איכות תמונה גבוהה"
            ),
            text_overlay=text_overlays.get(platform),
        )

    def _make_punchier(self, text: str) -> str:
        """Make text more punchy for TikTok."""
        # Remove filler words and make more direct
        fillers = ["בעצם", "כאילו", "אז", "נו"]
        result = text
        for filler in fillers:
            result = result.replace(f" {filler} ", " ")
        return result.strip()

    def _add_value_hint(self, text: str) -> str:
        """Add value proposition hint for YouTube."""
        return text

    def _generate_text_overlay(self, topic: str, short: bool = True) -> str:
        """Generate suggested text overlay."""
        if short:
            return f"#{topic.replace(' ', '')}"
        return f"חייבים לדעת על {topic}"


@dataclass
class ShortFormHookAgent:
    """Short Form Hook Agent for generating video hooks.

    Specializes in:
    - Creating attention-grabbing hooks for short-form video
    - Multiple hook types (question, statement, story, etc.)
    - Platform-specific optimization (TikTok, Instagram, YouTube Shorts)
    - Hebrew content with natural tone
    """

    hook_templates: HookTemplates = field(default_factory=HookTemplates)
    platform_optimizer: PlatformOptimizer = field(default_factory=PlatformOptimizer)

    # Engagement tips by vibe
    engagement_tips: dict[ClientVibe, list[str]] = field(
        default_factory=lambda: {
            ClientVibe.CASUAL: [
                "דברו בגובה העיניים, כאילו לחבר",
                "השתמשו בשפה יומיומית ואותנטית",
                "אל תפחדו מהומור קליל",
            ],
            ClientVibe.EDUCATIONAL: [
                "התחילו עם הנקודה החשובה ביותר",
                "השתמשו במספרים ועובדות",
                "הבטיחו ערך ברור תוך שניות",
            ],
            ClientVibe.MOTIVATIONAL: [
                "דברו באנרגיה ובביטחון",
                "השתמשו בשפת גוף פתוחה",
                "צרו קשר עין עם המצלמה",
            ],
            ClientVibe.SALES: [
                "התמקדו בבעיה לפני הפתרון",
                "צרו תחושת דחיפות",
                "הציגו תוצאות, לא תכונות",
            ],
        }
    )

    def process(self, input_data: HookInput) -> HookOutput:
        """Process input and generate complete hook package.

        Args:
            input_data: The hook input with topic, audience, vibe, and platforms.

        Returns:
            Complete hook output with multiple hook types and platform variations.
        """
        # Determine which hook types to generate
        hook_types = input_data.hook_types or list(HookType)

        # Generate hooks for each type
        hook_packages = []
        all_hooks = []

        for hook_type in hook_types:
            package = self._generate_hook_package(
                hook_type=hook_type,
                topic=input_data.video_topic,
                key_message=input_data.key_message,
                vibe=input_data.client_vibe,
                platforms=input_data.platforms,
            )
            hook_packages.append(package)
            all_hooks.append(package.base_hook)

        # Select recommended hook
        recommended_hook = self._select_best_hook(all_hooks, input_data)

        # Generate script starters
        script_starters = self._generate_script_starters(
            hooks=all_hooks,
            key_message=input_data.key_message,
        )

        # Get tips for the vibe
        tips = self.engagement_tips.get(input_data.client_vibe, [])

        # Create input summary
        input_summary = self._create_input_summary(input_data)

        return HookOutput(
            input_summary=input_summary,
            hooks=hook_packages,
            recommended_hook=recommended_hook,
            script_starters=script_starters,
            general_tips=tips,
        )

    def _generate_hook_package(
        self,
        hook_type: HookType,
        topic: str,
        key_message: str,
        vibe: ClientVibe,
        platforms: list[Platform],
    ) -> HookPackage:
        """Generate a complete hook package for a single hook type."""
        # Get template and create base hook
        template = self.hook_templates.get_template(hook_type, vibe)
        hook_text = template.format(topic=topic)

        # Determine platform fit based on hook type
        platform_fit = self._determine_platform_fit(hook_type)

        base_hook = Hook(
            hook_type=hook_type,
            text=hook_text,
            duration_estimate=self._estimate_duration(hook_text),
            platform_fit=platform_fit,
            engagement_notes=self._get_engagement_notes(hook_type, vibe),
        )

        # Generate platform variations
        platform_variations = [
            self.platform_optimizer.optimize_for_platform(hook_text, platform, topic)
            for platform in platforms
        ]

        # Generate A/B test variant
        alt_template = self.hook_templates.get_template(hook_type, vibe, index=1)
        ab_variant = alt_template.format(topic=topic) if alt_template != template else None

        return HookPackage(
            hook_type=hook_type,
            base_hook=base_hook,
            platform_variations=platform_variations,
            a_b_test_variant=ab_variant,
        )

    def _determine_platform_fit(self, hook_type: HookType) -> list[Platform]:
        """Determine which platforms a hook type works best for."""
        platform_fit_map = {
            HookType.QUESTION: [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE_SHORTS],
            HookType.BOLD_STATEMENT: [Platform.TIKTOK, Platform.INSTAGRAM],
            HookType.STORY: [Platform.YOUTUBE_SHORTS, Platform.INSTAGRAM],
            HookType.STATISTIC: [Platform.YOUTUBE_SHORTS, Platform.INSTAGRAM],
            HookType.CONTROVERSIAL: [Platform.TIKTOK],
            HookType.CURIOSITY_GAP: [Platform.TIKTOK, Platform.YOUTUBE_SHORTS],
            HookType.DIRECT_ADDRESS: [Platform.INSTAGRAM, Platform.YOUTUBE_SHORTS],
        }
        return platform_fit_map.get(hook_type, list(Platform))

    def _estimate_duration(self, text: str) -> str:
        """Estimate spoken duration of hook text."""
        # Rough estimate: ~3 words per second for Hebrew
        word_count = len(text.split())
        seconds = max(2, min(5, word_count // 3 + 1))
        return f"{seconds}-{seconds + 1} שניות"

    def _get_engagement_notes(self, hook_type: HookType, vibe: ClientVibe) -> str:
        """Get engagement notes for a hook type."""
        notes_map = {
            HookType.QUESTION: "שאלות מעוררות סקרנות ומושכות תגובות בקומנטס",
            HookType.BOLD_STATEMENT: "טענות נועזות מושכות תשומת לב ומייצרות שיתופים",
            HookType.STORY: "סיפורים יוצרים חיבור רגשי ומגדילים צפייה עד הסוף",
            HookType.STATISTIC: "מספרים מוסיפים אמינות ומשכנעים צופים להישאר",
            HookType.CONTROVERSIAL: "תוכן שנוי במחלוקת מייצר דיון ומגביר אינטראקציה",
            HookType.CURIOSITY_GAP: "פער סקרנות מבטיח צפייה מלאה בסרטון",
            HookType.DIRECT_ADDRESS: "פנייה ישירה יוצרת תחושת רלוונטיות אישית",
        }
        return notes_map.get(hook_type, "הוק אפקטיבי למשיכת תשומת לב")

    def _select_best_hook(
        self, hooks: list[Hook], input_data: HookInput
    ) -> Hook:
        """Select the best hook based on input criteria."""
        # Priority by vibe
        vibe_priority = {
            ClientVibe.CASUAL: [HookType.QUESTION, HookType.BOLD_STATEMENT],
            ClientVibe.EDUCATIONAL: [HookType.STATISTIC, HookType.CURIOSITY_GAP],
            ClientVibe.MOTIVATIONAL: [HookType.DIRECT_ADDRESS, HookType.STORY],
            ClientVibe.SALES: [HookType.CURIOSITY_GAP, HookType.DIRECT_ADDRESS],
        }

        priority = vibe_priority.get(input_data.client_vibe, [])

        for preferred_type in priority:
            for hook in hooks:
                if hook.hook_type == preferred_type:
                    return hook

        return hooks[0] if hooks else hooks[0]

    def _generate_script_starters(
        self, hooks: list[Hook], key_message: str
    ) -> list[str]:
        """Generate full opening lines that follow each hook."""
        starters = []
        for hook in hooks[:3]:  # Top 3 hooks
            starter = f"{hook.text} {key_message}"
            starters.append(starter)
        return starters

    def _create_input_summary(self, input_data: HookInput) -> str:
        """Create a summary of the input parameters."""
        platforms = ", ".join([p.value for p in input_data.platforms])
        return (
            f"נושא: {input_data.video_topic} | "
            f"קהל יעד: {input_data.target_audience} | "
            f"טון: {input_data.client_vibe.value} | "
            f"פלטפורמות: {platforms}"
        )

    def format_output(self, output: HookOutput) -> str:
        """Format the hook output as a readable string."""
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("Short Form Hook Agent - חבילת הוקים")
        lines.append("=" * 60)
        lines.append("")

        # Input summary
        lines.append(f"קלט: {output.input_summary}")
        lines.append("")

        # Recommended hook
        lines.append("ההוק המומלץ")
        lines.append("-" * 40)
        lines.append(f"סוג: {output.recommended_hook.hook_type.value}")
        lines.append(f"טקסט: {output.recommended_hook.text}")
        lines.append(f"משך: {output.recommended_hook.duration_estimate}")
        lines.append(f"הערות: {output.recommended_hook.engagement_notes}")
        lines.append("")

        # All hooks
        lines.append("כל ההוקים")
        lines.append("-" * 40)
        for package in output.hooks:
            lines.append(f"\n[{package.hook_type.value}]")
            lines.append(f"  {package.base_hook.text}")
            if package.a_b_test_variant:
                lines.append(f"  A/B: {package.a_b_test_variant}")
        lines.append("")

        # Script starters
        lines.append("פתיחות מומלצות לתסריט")
        lines.append("-" * 40)
        for i, starter in enumerate(output.script_starters, 1):
            lines.append(f"{i}. {starter}")
        lines.append("")

        # Tips
        lines.append("טיפים למסירה אפקטיבית")
        lines.append("-" * 40)
        for tip in output.general_tips:
            lines.append(f"  {tip}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def create_agent() -> ShortFormHookAgent:
    """Factory function to create a configured Short Form Hook Agent."""
    return ShortFormHookAgent()

"""Short-Form Viral Video Hook Agent.

This agent takes any topic and generates compelling short-form video hooks
and complete video structures optimized for virality on TikTok, Reels, and Shorts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from ..models import ClientVibe, Platform


class HookStyle(str, Enum):
    """Hook style options for video openings."""

    QUESTION = "question"
    BOLD_CLAIM = "bold_claim"
    CONTROVERSY = "controversy"
    STORY = "story"
    CURIOSITY_GAP = "curiosity_gap"
    PATTERN_INTERRUPT = "pattern_interrupt"


class VideoLength(str, Enum):
    """Target video length categories."""

    MICRO = "micro"  # 15-30 seconds
    SHORT = "short"  # 30-60 seconds
    MEDIUM = "medium"  # 60-90 seconds


class HookInput(BaseModel):
    """Input for generating short-form video hooks."""

    topic: str = Field(..., description="The topic or subject to create hooks for")
    target_audience: str = Field(..., description="Target audience description")
    vibe: ClientVibe = Field(
        default=ClientVibe.CASUAL, description="Desired tone/vibe"
    )
    video_length: VideoLength = Field(
        default=VideoLength.SHORT, description="Target video length"
    )
    platforms: list[Platform] = Field(
        default_factory=lambda: [
            Platform.TIKTOK,
            Platform.INSTAGRAM,
            Platform.YOUTUBE_SHORTS,
        ],
        description="Target platforms",
    )
    hook_styles: Optional[list[HookStyle]] = Field(
        default=None, description="Preferred hook styles (None = all styles)"
    )


class Hook(BaseModel):
    """A single video hook."""

    style: HookStyle
    text: str = Field(..., description="The hook text/script")
    visual_suggestion: str = Field(..., description="Visual suggestion for the hook")
    attention_score: int = Field(
        ..., ge=1, le=10, description="Predicted attention score (1-10)"
    )


class VideoSection(BaseModel):
    """A section of the video structure."""

    name: str = Field(..., description="Section name (e.g., 'hook', 'body', 'cta')")
    duration_seconds: int = Field(..., description="Suggested duration in seconds")
    content: str = Field(..., description="Content/script for this section")
    visual_notes: str = Field(..., description="Visual/editing notes")


class VideoStructure(BaseModel):
    """Complete video structure with all sections."""

    total_duration: int = Field(..., description="Total video duration in seconds")
    sections: list[VideoSection] = Field(..., description="Ordered list of sections")
    music_suggestion: str = Field(..., description="Music/audio suggestion")
    editing_style: str = Field(..., description="Recommended editing style")


class HookPackage(BaseModel):
    """Complete package of hooks and structure for a video."""

    topic: str
    hooks: list[Hook] = Field(..., description="Generated hooks (multiple options)")
    recommended_hook: Hook = Field(..., description="Top recommended hook")
    video_structure: VideoStructure = Field(..., description="Complete video structure")
    viral_tips: list[str] = Field(..., description="Tips for maximizing virality")
    platform_adaptations: dict[str, str] = Field(
        ..., description="Platform-specific adaptation notes"
    )


@dataclass
class ShortFormHookAgent:
    """Short-Form Viral Video Hook Agent.

    Specializes in:
    - Creating attention-grabbing hooks for short-form content
    - Structuring videos for maximum retention
    - Platform-specific optimization
    - Viral content patterns and psychology
    """

    hook_templates: dict[HookStyle, list[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize hook templates."""
        if not self.hook_templates:
            self.hook_templates = self._default_hook_templates()

    def _default_hook_templates(self) -> dict[HookStyle, list[str]]:
        """Get default hook templates by style."""
        return {
            HookStyle.QUESTION: [
                "Did you know {topic}?",
                "Why does nobody talk about {topic}?",
                "What if I told you {topic}?",
                "Want to know the secret to {topic}?",
            ],
            HookStyle.BOLD_CLAIM: [
                "This changed everything about {topic}",
                "{topic} is a lie - here's the truth",
                "I discovered something crazy about {topic}",
                "Stop doing {topic} wrong",
            ],
            HookStyle.CONTROVERSY: [
                "Unpopular opinion: {topic}",
                "Everyone's wrong about {topic}",
                "I'm going to say what no one will about {topic}",
                "The {topic} industry doesn't want you to know this",
            ],
            HookStyle.STORY: [
                "So this happened with {topic}...",
                "I never expected this from {topic}",
                "3 years ago I knew nothing about {topic}",
                "The moment I realized {topic} changed my life",
            ],
            HookStyle.CURIOSITY_GAP: [
                "This one thing about {topic}...",
                "The {topic} trick that went viral",
                "Watch until the end for {topic}",
                "You won't believe what happens with {topic}",
            ],
            HookStyle.PATTERN_INTERRUPT: [
                "WAIT - before you scroll, {topic}",
                "POV: You just discovered {topic}",
                "🚨 {topic} alert 🚨",
                "This is your sign to learn about {topic}",
            ],
        }

    def process(self, input_data: HookInput) -> HookPackage:
        """Process input and generate complete hook package.

        Args:
            input_data: The input with topic, audience, vibe, and preferences.

        Returns:
            Complete hook package with multiple hooks and video structure.
        """
        # Step 1: Generate hooks for each style
        hooks = self._generate_hooks(input_data)

        # Step 2: Rank and select best hook
        recommended_hook = self._select_best_hook(hooks, input_data)

        # Step 3: Generate video structure
        video_structure = self._generate_video_structure(
            recommended_hook, input_data
        )

        # Step 4: Generate viral tips
        viral_tips = self._generate_viral_tips(input_data)

        # Step 5: Generate platform adaptations
        platform_adaptations = self._generate_platform_adaptations(input_data)

        return HookPackage(
            topic=input_data.topic,
            hooks=hooks,
            recommended_hook=recommended_hook,
            video_structure=video_structure,
            viral_tips=viral_tips,
            platform_adaptations=platform_adaptations,
        )

    def _generate_hooks(self, input_data: HookInput) -> list[Hook]:
        """Generate hooks for all requested styles."""
        hooks = []
        styles = input_data.hook_styles or list(HookStyle)

        for style in styles:
            hook = self._generate_hook_for_style(style, input_data)
            hooks.append(hook)

        return hooks

    def _generate_hook_for_style(
        self, style: HookStyle, input_data: HookInput
    ) -> Hook:
        """Generate a single hook for a specific style."""
        templates = self.hook_templates.get(style, [])
        template = templates[0] if templates else "{topic}"

        # Apply vibe modifications
        text = self._apply_vibe_to_hook(
            template.format(topic=input_data.topic),
            input_data.vibe,
        )

        visual = self._generate_visual_suggestion(style, input_data.vibe)
        score = self._calculate_attention_score(style, input_data)

        return Hook(
            style=style,
            text=text,
            visual_suggestion=visual,
            attention_score=score,
        )

    def _apply_vibe_to_hook(self, text: str, vibe: ClientVibe) -> str:
        """Apply vibe/tone modifications to hook text."""
        vibe_modifiers = {
            ClientVibe.CASUAL: lambda t: t.replace(".", "..."),
            ClientVibe.EDUCATIONAL: lambda t: f"📚 {t}",
            ClientVibe.MOTIVATIONAL: lambda t: f"💪 {t}",
            ClientVibe.SALES: lambda t: f"🔥 {t}",
        }
        modifier = vibe_modifiers.get(vibe, lambda t: t)
        return modifier(text)

    def _generate_visual_suggestion(
        self, style: HookStyle, vibe: ClientVibe
    ) -> str:
        """Generate visual suggestion based on hook style."""
        visual_suggestions = {
            HookStyle.QUESTION: "Close-up face, raised eyebrow, direct eye contact",
            HookStyle.BOLD_CLAIM: "Text overlay with bold font, dynamic zoom",
            HookStyle.CONTROVERSY: "Reaction face, split screen comparison",
            HookStyle.STORY: "Casual setting, storytelling hand gestures",
            HookStyle.CURIOSITY_GAP: "Partial reveal, blur effect, pointing gesture",
            HookStyle.PATTERN_INTERRUPT: "Quick cuts, flash effect, breaking fourth wall",
        }
        return visual_suggestions.get(style, "Standard talking head setup")

    def _calculate_attention_score(
        self, style: HookStyle, input_data: HookInput
    ) -> int:
        """Calculate predicted attention score for hook style."""
        # Base scores by style (pattern interrupt and curiosity gap typically perform best)
        base_scores = {
            HookStyle.QUESTION: 7,
            HookStyle.BOLD_CLAIM: 8,
            HookStyle.CONTROVERSY: 9,
            HookStyle.STORY: 7,
            HookStyle.CURIOSITY_GAP: 9,
            HookStyle.PATTERN_INTERRUPT: 8,
        }

        score = base_scores.get(style, 6)

        # Adjust for vibe
        if input_data.vibe == ClientVibe.MOTIVATIONAL:
            score = min(10, score + 1)

        return score

    def _select_best_hook(
        self, hooks: list[Hook], input_data: HookInput
    ) -> Hook:
        """Select the best hook from generated options."""
        # Sort by attention score and return highest
        sorted_hooks = sorted(hooks, key=lambda h: h.attention_score, reverse=True)
        return sorted_hooks[0]

    def _generate_video_structure(
        self, hook: Hook, input_data: HookInput
    ) -> VideoStructure:
        """Generate complete video structure based on hook and length."""
        duration_map = {
            VideoLength.MICRO: 20,
            VideoLength.SHORT: 45,
            VideoLength.MEDIUM: 75,
        }
        total_duration = duration_map.get(input_data.video_length, 45)

        sections = self._build_sections(hook, input_data, total_duration)
        music = self._suggest_music(input_data.vibe)
        editing_style = self._suggest_editing_style(input_data.vibe)

        return VideoStructure(
            total_duration=total_duration,
            sections=sections,
            music_suggestion=music,
            editing_style=editing_style,
        )

    def _build_sections(
        self, hook: Hook, input_data: HookInput, total_duration: int
    ) -> list[VideoSection]:
        """Build video sections based on duration and content."""
        sections = []

        # Hook section (first 3-5 seconds are crucial)
        hook_duration = 4 if total_duration <= 30 else 5
        sections.append(
            VideoSection(
                name="Hook",
                duration_seconds=hook_duration,
                content=hook.text,
                visual_notes=hook.visual_suggestion,
            )
        )

        # Body section
        cta_duration = 5
        body_duration = total_duration - hook_duration - cta_duration
        sections.append(
            VideoSection(
                name="Body",
                duration_seconds=body_duration,
                content=f"Deliver value on {input_data.topic} - keep energy high, use quick cuts",
                visual_notes="B-roll, screen recordings, or demonstrations. Keep visual variety high.",
            )
        )

        # CTA section
        cta_text = self._generate_cta(input_data.vibe)
        sections.append(
            VideoSection(
                name="CTA",
                duration_seconds=cta_duration,
                content=cta_text,
                visual_notes="Direct to camera, pointing gesture, text overlay with action",
            )
        )

        return sections

    def _generate_cta(self, vibe: ClientVibe) -> str:
        """Generate call-to-action based on vibe."""
        ctas = {
            ClientVibe.CASUAL: "Follow for more! Drop a comment if this helped.",
            ClientVibe.EDUCATIONAL: "Save this for later. Follow for daily tips!",
            ClientVibe.MOTIVATIONAL: "You got this! Share with someone who needs to hear this.",
            ClientVibe.SALES: "Link in bio. Limited time only - don't miss out!",
        }
        return ctas.get(vibe, "Follow for more content like this!")

    def _suggest_music(self, vibe: ClientVibe) -> str:
        """Suggest music style based on vibe."""
        music_suggestions = {
            ClientVibe.CASUAL: "Trending audio or chill lo-fi beat",
            ClientVibe.EDUCATIONAL: "Upbeat instrumental, moderate tempo",
            ClientVibe.MOTIVATIONAL: "Epic orchestral or pump-up electronic",
            ClientVibe.SALES: "High-energy trending sound, urgency-inducing",
        }
        return music_suggestions.get(vibe, "Trending platform audio")

    def _suggest_editing_style(self, vibe: ClientVibe) -> str:
        """Suggest editing style based on vibe."""
        editing_styles = {
            ClientVibe.CASUAL: "Natural cuts, minimal effects, authentic feel",
            ClientVibe.EDUCATIONAL: "Clean transitions, text overlays, highlight key points",
            ClientVibe.MOTIVATIONAL: "Dynamic cuts, zoom effects, impactful text",
            ClientVibe.SALES: "Fast-paced, urgency overlays, countdown elements",
        }
        return editing_styles.get(vibe, "Standard quick-cut style")

    def _generate_viral_tips(self, input_data: HookInput) -> list[str]:
        """Generate tips for maximizing virality."""
        tips = [
            "Post during peak hours (12-1pm, 7-9pm local time)",
            "First 3 seconds determine 90% of retention - nail the hook",
            "Use trending sounds when available for algorithm boost",
            "Reply to comments quickly to boost engagement",
            "Create a loop - end connects to beginning for rewatches",
        ]

        # Add vibe-specific tips
        vibe_tips = {
            ClientVibe.CASUAL: "Show personality - authenticity beats polish",
            ClientVibe.EDUCATIONAL: "Deliver one clear takeaway - less is more",
            ClientVibe.MOTIVATIONAL: "Include emotional peaks - make them feel something",
            ClientVibe.SALES: "Create urgency without being pushy - scarcity works",
        }
        if input_data.vibe in vibe_tips:
            tips.append(vibe_tips[input_data.vibe])

        return tips

    def _generate_platform_adaptations(
        self, input_data: HookInput
    ) -> dict[str, str]:
        """Generate platform-specific adaptation notes."""
        adaptations = {}

        for platform in input_data.platforms:
            if platform == Platform.TIKTOK:
                adaptations["TikTok"] = (
                    "Use trending sounds, engage with duets/stitches, "
                    "vertical 9:16, captions on-screen"
                )
            elif platform == Platform.INSTAGRAM:
                adaptations["Instagram"] = (
                    "Cross-post to Stories, use Reels-specific features, "
                    "strong thumbnail, hashtags in caption"
                )
            elif platform == Platform.YOUTUBE_SHORTS:
                adaptations["YouTube Shorts"] = (
                    "Focus on retention, add subscribe CTA, "
                    "consider long-form connection, optimize title"
                )

        return adaptations

    def format_output(self, package: HookPackage) -> str:
        """Format the hook package as a readable output."""
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("🎬 Short-Form Hook Package")
        lines.append("=" * 60)
        lines.append(f"Topic: {package.topic}")
        lines.append("")

        # Recommended Hook
        lines.append("⭐ RECOMMENDED HOOK")
        lines.append("-" * 40)
        lines.append(f"Style: {package.recommended_hook.style.value}")
        lines.append(f"Text: \"{package.recommended_hook.text}\"")
        lines.append(f"Visual: {package.recommended_hook.visual_suggestion}")
        lines.append(f"Attention Score: {package.recommended_hook.attention_score}/10")
        lines.append("")

        # All Hooks
        lines.append("🎣 ALL HOOK OPTIONS")
        lines.append("-" * 40)
        for hook in package.hooks:
            lines.append(f"  [{hook.style.value}] \"{hook.text}\" (Score: {hook.attention_score})")
        lines.append("")

        # Video Structure
        lines.append("📐 VIDEO STRUCTURE")
        lines.append("-" * 40)
        lines.append(f"Total Duration: {package.video_structure.total_duration}s")
        lines.append(f"Music: {package.video_structure.music_suggestion}")
        lines.append(f"Editing: {package.video_structure.editing_style}")
        lines.append("")
        for section in package.video_structure.sections:
            lines.append(f"  [{section.duration_seconds}s] {section.name}")
            lines.append(f"      Content: {section.content}")
            lines.append(f"      Visual: {section.visual_notes}")
        lines.append("")

        # Viral Tips
        lines.append("🚀 VIRAL TIPS")
        lines.append("-" * 40)
        for tip in package.viral_tips:
            lines.append(f"  • {tip}")
        lines.append("")

        # Platform Adaptations
        lines.append("📱 PLATFORM ADAPTATIONS")
        lines.append("-" * 40)
        for platform, notes in package.platform_adaptations.items():
            lines.append(f"  {platform}: {notes}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def create_agent() -> ShortFormHookAgent:
    """Factory function to create a configured Short-Form Hook Agent."""
    return ShortFormHookAgent()

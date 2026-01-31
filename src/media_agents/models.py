"""Data models for Hebrew Content Quality Agent."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Platform(str, Enum):
    """Supported social media platforms."""

    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE_SHORTS = "youtube_shorts"


class ClientVibe(str, Enum):
    """Client content vibe/tone options."""

    CASUAL = "casual"
    EDUCATIONAL = "educational"
    MOTIVATIONAL = "motivational"
    SALES = "sales"


class HookType(str, Enum):
    """Types of hooks for short-form content."""

    QUESTION = "question"  # Start with a compelling question
    BOLD_STATEMENT = "bold_statement"  # Make a provocative claim
    STORY = "story"  # Begin with a mini story/scenario
    STATISTIC = "statistic"  # Lead with a surprising stat
    CONTROVERSIAL = "controversial"  # Challenge common beliefs
    CURIOSITY_GAP = "curiosity_gap"  # Tease info that makes viewers stay
    DIRECT_ADDRESS = "direct_address"  # Speak directly to viewer's problem


class ContentInput(BaseModel):
    """Input content for processing."""

    raw_caption: str = Field(..., description="Raw caption or script (Hebrew or mixed)")
    video_topic: str = Field(..., description="Topic of the video content")
    target_audience: str = Field(..., description="Target audience description")
    client_vibe: ClientVibe = Field(..., description="Client's desired tone/vibe")
    platforms: list[Platform] = Field(
        default_factory=lambda: [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE_SHORTS],
        description="Target platforms for publishing",
    )


class QAResult(BaseModel):
    """Result of Hebrew QA processing."""

    original_text: str = Field(..., description="Original input text")
    corrected_text: str = Field(..., description="Corrected and natural Hebrew text")
    corrections: list[str] = Field(default_factory=list, description="List of corrections made")
    notes: list[str] = Field(default_factory=list, description="Notes about the text")


class CaptionSet(BaseModel):
    """Generated captions for a platform."""

    caption_short: str = Field(..., description="Short punchy caption")
    caption_long: str = Field(..., description="Slightly longer caption with more context")


class HashtagSet(BaseModel):
    """Hashtag sets for publishing."""

    broad_reach: list[str] = Field(..., description="Israeli broad reach hashtags")
    niche_specific: list[str] = Field(..., description="Niche-specific hashtags")


class PlatformPackage(BaseModel):
    """Complete publishing package for a single platform."""

    platform: Platform
    caption_a: str = Field(..., description="Short punchy caption")
    caption_b: str = Field(..., description="Longer caption")
    hashtags: list[str] = Field(..., description="Combined hashtag list")
    posting_suggestion: str = Field(..., description="Posting timing/strategy suggestion")
    tone_notes: str = Field(..., description="Notes about tone adaptation")


class PublishingPackage(BaseModel):
    """Complete publishing package across all platforms."""

    qa_result: QAResult
    platforms: list[PlatformPackage]
    general_notes: Optional[str] = None


# Short Form Hook Agent Models


class HookInput(BaseModel):
    """Input for generating short-form video hooks."""

    video_topic: str = Field(..., description="Main topic or subject of the video")
    target_audience: str = Field(..., description="Target audience description")
    key_message: str = Field(..., description="The main message or takeaway of the video")
    client_vibe: ClientVibe = Field(..., description="Client's desired tone/vibe")
    platforms: list[Platform] = Field(
        default_factory=lambda: [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE_SHORTS],
        description="Target platforms for publishing",
    )
    hook_types: Optional[list[HookType]] = Field(
        default=None,
        description="Specific hook types to generate (if None, generates all types)",
    )
    language: str = Field(default="hebrew", description="Primary language for hooks")


class Hook(BaseModel):
    """A single generated hook."""

    hook_type: HookType
    text: str = Field(..., description="The hook text")
    duration_estimate: str = Field(..., description="Estimated spoken duration (e.g., '2-3 seconds')")
    platform_fit: list[Platform] = Field(..., description="Platforms this hook works best for")
    engagement_notes: str = Field(..., description="Notes on why this hook works")


class HookVariation(BaseModel):
    """Hook variation optimized for a specific platform."""

    platform: Platform
    hook_text: str = Field(..., description="Platform-optimized hook text")
    visual_suggestion: str = Field(..., description="Suggested visual to pair with hook")
    text_overlay: Optional[str] = Field(None, description="Suggested text overlay for the video")


class HookPackage(BaseModel):
    """Complete hook package for a single hook type."""

    hook_type: HookType
    base_hook: Hook
    platform_variations: list[HookVariation]
    a_b_test_variant: Optional[str] = Field(None, description="Alternative hook version for testing")


class HookOutput(BaseModel):
    """Complete output from the ShortFormHookAgent."""

    input_summary: str = Field(..., description="Summary of the input parameters")
    hooks: list[HookPackage] = Field(..., description="Generated hook packages by type")
    recommended_hook: Hook = Field(..., description="Top recommended hook based on input")
    script_starters: list[str] = Field(
        ..., description="Full opening lines that follow each hook"
    )
    general_tips: list[str] = Field(..., description="Tips for delivering hooks effectively")

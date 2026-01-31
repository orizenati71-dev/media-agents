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

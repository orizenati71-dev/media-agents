"""Hebrew Content Quality + Publishing AI Agent.

This agent takes Hebrew (or mixed Hebrew-English) video content and prepares it
for publishing with perfect natural Hebrew across multiple social media platforms.
"""

from dataclasses import dataclass, field

from ..models import (
    ClientVibe,
    ContentInput,
    Platform,
    PlatformPackage,
    PublishingPackage,
    QAResult,
)
from ..utils.captions import CaptionGenerator
from ..utils.hashtags import HashtagGenerator
from ..utils.hebrew_qa import HebrewQA
from ..utils.platform_adapter import PlatformAdapter


@dataclass
class HebrewContentAgent:
    """Hebrew Content Quality + Publishing AI Agent.

    Specializes in:
    - Israeli spoken Hebrew
    - Social media tone
    - Correcting robotic or formal language
    - Making captions sound human, current, and native
    """

    qa_processor: HebrewQA = field(default_factory=HebrewQA)
    caption_generator: CaptionGenerator = field(default_factory=CaptionGenerator)
    hashtag_generator: HashtagGenerator = field(default_factory=HashtagGenerator)
    platform_adapter: PlatformAdapter = field(default_factory=PlatformAdapter)

    def process(self, content: ContentInput) -> PublishingPackage:
        """Process content and generate complete publishing package.

        Args:
            content: The input content with raw caption, topic, audience, vibe, and platforms.

        Returns:
            Complete publishing package with QA results and platform-specific packages.
        """
        # Step 1: Hebrew QA
        qa_result = self._perform_qa(content.raw_caption)

        # Step 2-5: Generate platform packages
        platform_packages = []
        for platform in content.platforms:
            package = self._generate_platform_package(
                qa_result=qa_result,
                topic=content.video_topic,
                audience=content.target_audience,
                vibe=content.client_vibe,
                platform=platform,
            )
            platform_packages.append(package)

        # Generate general notes
        general_notes = self._generate_general_notes(content, qa_result)

        return PublishingPackage(
            qa_result=qa_result,
            platforms=platform_packages,
            general_notes=general_notes,
        )

    def _perform_qa(self, raw_caption: str) -> QAResult:
        """Perform Hebrew QA on raw caption."""
        return self.qa_processor.process(raw_caption)

    def _generate_platform_package(
        self,
        qa_result: QAResult,
        topic: str,
        audience: str,
        vibe: ClientVibe,
        platform: Platform,
    ) -> PlatformPackage:
        """Generate complete package for a single platform."""
        # Generate captions
        caption_set = self.caption_generator.generate(
            corrected_text=qa_result.corrected_text,
            topic=topic,
            vibe=vibe,
            platform=platform,
        )

        # Generate hashtags
        hashtag_set = self.hashtag_generator.generate(
            topic=topic,
            platform=platform,
        )

        # Combine hashtags for platform
        combined_hashtags = self.hashtag_generator.combine_hashtags(
            hashtag_set, platform
        )

        # Adapt for platform
        platform_package = self.platform_adapter.adapt(
            caption_set=caption_set,
            platform=platform,
            vibe=vibe,
            hashtags=combined_hashtags,
            topic=topic,
        )

        return platform_package

    def _generate_general_notes(
        self, content: ContentInput, qa_result: QAResult
    ) -> str:
        """Generate general notes about the content."""
        notes = []

        # QA summary
        if qa_result.corrections:
            notes.append(f"בוצעו {len(qa_result.corrections)} תיקונים בטקסט המקורי")

        # Audience note
        notes.append(f"קהל יעד: {content.target_audience}")

        # Vibe note
        vibe_names = {
            ClientVibe.CASUAL: "קז׳ואל",
            ClientVibe.EDUCATIONAL: "לימודי",
            ClientVibe.MOTIVATIONAL: "מוטיבציוני",
            ClientVibe.SALES: "מכירתי",
        }
        notes.append(f"טון: {vibe_names.get(content.client_vibe, content.client_vibe)}")

        # Platforms
        platform_names = [p.value for p in content.platforms]
        notes.append(f"פלטפורמות: {', '.join(platform_names)}")

        return " | ".join(notes)

    def format_output(self, package: PublishingPackage) -> str:
        """Format the publishing package as a readable output."""
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("📦 חבילת פרסום - Hebrew Content Agent")
        lines.append("=" * 60)
        lines.append("")

        # QA Section
        lines.append("📝 בדיקת איכות עברית (QA)")
        lines.append("-" * 40)
        lines.append(f"טקסט מקורי: {package.qa_result.original_text[:100]}...")
        lines.append(f"טקסט מתוקן: {package.qa_result.corrected_text[:100]}...")
        if package.qa_result.corrections:
            lines.append(f"תיקונים ({len(package.qa_result.corrections)}):")
            for correction in package.qa_result.corrections[:5]:
                lines.append(f"  • {correction}")
        if package.qa_result.notes:
            lines.append("הערות:")
            for note in package.qa_result.notes:
                lines.append(f"  • {note}")
        lines.append("")

        # Platform Packages
        for platform_pkg in package.platforms:
            lines.append(self._format_platform_package(platform_pkg))
            lines.append("")

        # General Notes
        if package.general_notes:
            lines.append("📋 הערות כלליות")
            lines.append("-" * 40)
            lines.append(package.general_notes)

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _format_platform_package(self, pkg: PlatformPackage) -> str:
        """Format a single platform package."""
        platform_emojis = {
            Platform.TIKTOK: "🎵",
            Platform.INSTAGRAM: "📸",
            Platform.YOUTUBE_SHORTS: "▶️",
        }
        emoji = platform_emojis.get(pkg.platform, "📱")

        lines = []
        lines.append(f"{emoji} {pkg.platform.value.upper()}")
        lines.append("-" * 40)
        lines.append(f"Caption A (קצר):\n{pkg.caption_a}")
        lines.append("")
        lines.append(f"Caption B (ארוך):\n{pkg.caption_b}")
        lines.append("")
        lines.append(f"Hashtags:\n{' '.join(pkg.hashtags)}")
        lines.append("")
        lines.append(f"המלצת פרסום: {pkg.posting_suggestion}")
        lines.append(f"הערות טון: {pkg.tone_notes}")

        return "\n".join(lines)


def create_agent() -> HebrewContentAgent:
    """Factory function to create a configured Hebrew Content Agent."""
    return HebrewContentAgent()

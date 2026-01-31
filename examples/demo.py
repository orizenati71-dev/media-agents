#!/usr/bin/env python3
"""Demo script for Hebrew Content Agent.

This script demonstrates the agent's capabilities with sample content.
"""

import sys
from pathlib import Path

# Add src to path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from media_agents.agents import HebrewContentAgent
from media_agents.models import ClientVibe, ContentInput, Platform


def main():
    """Run demo with sample content."""
    # Create agent
    agent = HebrewContentAgent()

    # Sample content - formal/robotic Hebrew that needs to be naturalized
    sample_content = ContentInput(
        raw_caption="""
        באפשרותכם לראות תוצאות מדהימות בעסק שלכם על מנת להגיע להצלחה מסחררת.
        יש לציין כי השיטה הזו היא פורצת דרך וייחודית במינה.
        ניתן ליישם את הטיפים הללו באופן מיידי.
        הזדמנות אחרונה לשנות את החיים שלכם!
        """,
        video_topic="טיפים לצמיחה עסקית",
        target_audience="יזמים ובעלי עסקים קטנים בישראל",
        client_vibe=ClientVibe.EDUCATIONAL,
        platforms=[Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE_SHORTS],
    )

    print("=" * 60)
    print("Hebrew Content Agent - Demo")
    print("=" * 60)
    print()

    # Process content
    print("מעבד תוכן...")
    package = agent.process(sample_content)

    # Display QA results
    print("\n📝 בדיקת איכות עברית (QA)")
    print("-" * 50)
    print(f"מקור:\n{package.qa_result.original_text.strip()}")
    print(f"\nמתוקן:\n{package.qa_result.corrected_text}")

    if package.qa_result.corrections:
        print(f"\nתיקונים ({len(package.qa_result.corrections)}):")
        for correction in package.qa_result.corrections:
            print(f"  • {correction}")

    # Display platform packages
    for platform_pkg in package.platforms:
        print(f"\n{'=' * 60}")
        print(f"📱 {platform_pkg.platform.value.upper()}")
        print("=" * 60)

        print(f"\nCaption A (קצר):")
        print(platform_pkg.caption_a)

        print(f"\nCaption B (ארוך):")
        print(platform_pkg.caption_b)

        print(f"\nHashtags:")
        print(" ".join(platform_pkg.hashtags))

        print(f"\nהמלצת פרסום:")
        print(platform_pkg.posting_suggestion)

        print(f"\nהערות טון:")
        print(platform_pkg.tone_notes)

    # General notes
    print(f"\n{'=' * 60}")
    print("📋 הערות כלליות")
    print("-" * 50)
    print(package.general_notes)


def demo_qa_only():
    """Demo just the QA functionality."""
    agent = HebrewContentAgent()

    samples = [
        "באפשרותך לראות את התוצאות המדהימות",
        "ניתן להשיג הצלחה מסחררת על מנת לשנות את חייכם",
        "יש לציין כי הטיפ הזה הוא פורץ דרך ומהפכני",
        "אנו מציעים לכם הזדמנות אחרונה לא תאמינו מה יקרה",
    ]

    print("\n📝 Hebrew QA Demo")
    print("=" * 60)

    for sample in samples:
        result = agent.qa_processor.process(sample)
        print(f"\nמקור: {result.original_text}")
        print(f"מתוקן: {result.corrected_text}")
        if result.corrections:
            print(f"  תיקונים: {len(result.corrections)}")


def demo_hashtags():
    """Demo hashtag generation."""
    agent = HebrewContentAgent()

    topics = [
        "עסקים ויזמות",
        "כושר ובריאות",
        "אוכל ומתכונים",
        "טכנולוגיה והייטק",
    ]

    print("\n# Hashtag Generation Demo")
    print("=" * 60)

    for topic in topics:
        hashtag_set = agent.hashtag_generator.generate(topic, Platform.INSTAGRAM)
        combined = agent.hashtag_generator.combine_hashtags(hashtag_set, Platform.INSTAGRAM)

        print(f"\nנושא: {topic}")
        print(f"Broad: {' '.join(hashtag_set.broad_reach[:5])}")
        print(f"Niche: {' '.join(hashtag_set.niche_specific[:5])}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hebrew Content Agent Demo")
    parser.add_argument(
        "--mode",
        choices=["full", "qa", "hashtags"],
        default="full",
        help="Demo mode to run",
    )
    args = parser.parse_args()

    if args.mode == "full":
        main()
    elif args.mode == "qa":
        demo_qa_only()
    elif args.mode == "hashtags":
        demo_hashtags()

"""Command-line interface for Hebrew Content Agent."""

import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .agents.hebrew_content_agent import HebrewContentAgent, create_agent
from .models import ClientVibe, ContentInput, Platform, PublishingPackage

app = typer.Typer(
    name="hebrew-agent",
    help="Hebrew Content Quality + Publishing AI Agent",
    add_completion=False,
)
console = Console()


def parse_platforms(platforms_str: str) -> list[Platform]:
    """Parse comma-separated platform string."""
    platform_map = {
        "tiktok": Platform.TIKTOK,
        "instagram": Platform.INSTAGRAM,
        "ig": Platform.INSTAGRAM,
        "youtube": Platform.YOUTUBE_SHORTS,
        "yt": Platform.YOUTUBE_SHORTS,
        "shorts": Platform.YOUTUBE_SHORTS,
    }

    platforms = []
    for p in platforms_str.lower().split(","):
        p = p.strip()
        if p in platform_map:
            platforms.append(platform_map[p])

    return platforms if platforms else [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE_SHORTS]


def parse_vibe(vibe_str: str) -> ClientVibe:
    """Parse vibe string."""
    vibe_map = {
        "casual": ClientVibe.CASUAL,
        "קזואל": ClientVibe.CASUAL,
        "educational": ClientVibe.EDUCATIONAL,
        "לימודי": ClientVibe.EDUCATIONAL,
        "motivational": ClientVibe.MOTIVATIONAL,
        "מוטיבציוני": ClientVibe.MOTIVATIONAL,
        "sales": ClientVibe.SALES,
        "מכירות": ClientVibe.SALES,
    }
    return vibe_map.get(vibe_str.lower(), ClientVibe.CASUAL)


def display_package(package: PublishingPackage) -> None:
    """Display publishing package with rich formatting."""
    # Header
    console.print()
    console.print(Panel.fit(
        "[bold blue]📦 חבילת פרסום - Hebrew Content Agent[/bold blue]",
        border_style="blue"
    ))
    console.print()

    # QA Section
    console.print("[bold yellow]📝 בדיקת איכות עברית (QA)[/bold yellow]")
    console.print("-" * 50)

    qa_table = Table(show_header=False, box=None, padding=(0, 2))
    qa_table.add_column("Label", style="cyan")
    qa_table.add_column("Content")

    original_preview = package.qa_result.original_text[:80] + "..." if len(package.qa_result.original_text) > 80 else package.qa_result.original_text
    corrected_preview = package.qa_result.corrected_text[:80] + "..." if len(package.qa_result.corrected_text) > 80 else package.qa_result.corrected_text

    qa_table.add_row("מקור:", original_preview)
    qa_table.add_row("מתוקן:", corrected_preview)
    console.print(qa_table)

    if package.qa_result.corrections:
        console.print(f"\n[dim]תיקונים ({len(package.qa_result.corrections)}):[/dim]")
        for correction in package.qa_result.corrections[:5]:
            console.print(f"  [dim]• {correction}[/dim]")

    console.print()

    # Platform Packages
    platform_colors = {
        Platform.TIKTOK: "magenta",
        Platform.INSTAGRAM: "red",
        Platform.YOUTUBE_SHORTS: "red",
    }
    platform_emojis = {
        Platform.TIKTOK: "🎵",
        Platform.INSTAGRAM: "📸",
        Platform.YOUTUBE_SHORTS: "▶️",
    }

    for pkg in package.platforms:
        color = platform_colors.get(pkg.platform, "white")
        emoji = platform_emojis.get(pkg.platform, "📱")

        console.print(Panel(
            f"[bold]{emoji} {pkg.platform.value.upper()}[/bold]",
            border_style=color,
            expand=False
        ))

        console.print(f"[bold cyan]Caption A (קצר):[/bold cyan]")
        console.print(pkg.caption_a)
        console.print()

        console.print(f"[bold cyan]Caption B (ארוך):[/bold cyan]")
        console.print(pkg.caption_b)
        console.print()

        console.print(f"[bold cyan]Hashtags:[/bold cyan]")
        console.print(" ".join(pkg.hashtags))
        console.print()

        console.print(f"[dim]המלצת פרסום: {pkg.posting_suggestion}[/dim]")
        console.print(f"[dim]הערות טון: {pkg.tone_notes}[/dim]")
        console.print()

    # General Notes
    if package.general_notes:
        console.print("[bold yellow]📋 הערות כלליות[/bold yellow]")
        console.print("-" * 50)
        console.print(package.general_notes)
        console.print()


@app.command()
def process(
    caption: str = typer.Argument(..., help="Raw caption/script in Hebrew or mixed Hebrew-English"),
    topic: str = typer.Option(..., "--topic", "-t", help="Video topic"),
    audience: str = typer.Option(..., "--audience", "-a", help="Target audience description"),
    vibe: str = typer.Option("casual", "--vibe", "-v", help="Client vibe: casual/educational/motivational/sales"),
    platforms: str = typer.Option(
        "tiktok,instagram,youtube",
        "--platforms", "-p",
        help="Comma-separated platforms: tiktok,instagram,youtube"
    ),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save output to file"),
) -> None:
    """Process Hebrew content and generate publishing package.

    Example:
        hebrew-agent process "הנה טיפ מדהים שישנה לכם את החיים" \\
            --topic "טיפים לפרודוקטיביות" \\
            --audience "יזמים צעירים" \\
            --vibe casual \\
            --platforms "tiktok,instagram"
    """
    # Create agent
    agent = create_agent()

    # Parse inputs
    content = ContentInput(
        raw_caption=caption,
        video_topic=topic,
        target_audience=audience,
        client_vibe=parse_vibe(vibe),
        platforms=parse_platforms(platforms),
    )

    # Process
    console.print("[dim]מעבד תוכן...[/dim]")
    package = agent.process(content)

    # Output
    if output_json:
        output = package.model_dump_json(indent=2)
        if output_file:
            output_file.write_text(output, encoding="utf-8")
            console.print(f"[green]נשמר ל: {output_file}[/green]")
        else:
            print(output)
    else:
        if output_file:
            output = agent.format_output(package)
            output_file.write_text(output, encoding="utf-8")
            console.print(f"[green]נשמר ל: {output_file}[/green]")
        else:
            display_package(package)


@app.command()
def interactive() -> None:
    """Start interactive mode for processing content."""
    console.print(Panel.fit(
        "[bold blue]Hebrew Content Quality + Publishing Agent[/bold blue]\n"
        "[dim]Interactive Mode[/dim]",
        border_style="blue"
    ))

    agent = create_agent()

    while True:
        console.print()
        caption = typer.prompt("📝 הכנס טקסט (או 'exit' ליציאה)")
        if caption.lower() == "exit":
            console.print("[dim]להתראות![/dim]")
            break

        topic = typer.prompt("📌 נושא הסרטון")
        audience = typer.prompt("👥 קהל יעד")
        vibe = typer.prompt("🎭 טון (casual/educational/motivational/sales)", default="casual")
        platforms = typer.prompt("📱 פלטפורמות (tiktok,instagram,youtube)", default="tiktok,instagram,youtube")

        content = ContentInput(
            raw_caption=caption,
            video_topic=topic,
            target_audience=audience,
            client_vibe=parse_vibe(vibe),
            platforms=parse_platforms(platforms),
        )

        console.print("[dim]מעבד...[/dim]")
        package = agent.process(content)
        display_package(package)

        console.print("-" * 50)


@app.command()
def qa(
    text: str = typer.Argument(..., help="Hebrew text to check and correct"),
) -> None:
    """Quick Hebrew QA check without full publishing package.

    Example:
        hebrew-agent qa "באפשרותך לראות את התוצאות המדהימות"
    """
    agent = create_agent()
    result = agent.qa_processor.process(text)

    console.print()
    console.print("[bold yellow]📝 בדיקת איכות עברית[/bold yellow]")
    console.print("-" * 50)
    console.print(f"[cyan]מקור:[/cyan] {result.original_text}")
    console.print(f"[green]מתוקן:[/green] {result.corrected_text}")

    if result.corrections:
        console.print(f"\n[dim]תיקונים ({len(result.corrections)}):[/dim]")
        for correction in result.corrections:
            console.print(f"  [dim]• {correction}[/dim]")

    if result.notes:
        console.print("\n[dim]הערות:[/dim]")
        for note in result.notes:
            console.print(f"  [dim]• {note}[/dim]")


@app.command()
def hashtags(
    topic: str = typer.Argument(..., help="Topic for hashtag generation"),
    platform: str = typer.Option("instagram", "--platform", "-p", help="Target platform"),
) -> None:
    """Generate hashtags for a topic.

    Example:
        hebrew-agent hashtags "יזמות וטכנולוגיה" --platform instagram
    """
    agent = create_agent()
    platforms = parse_platforms(platform)
    target_platform = platforms[0] if platforms else Platform.INSTAGRAM

    hashtag_set = agent.hashtag_generator.generate(topic, target_platform)
    combined = agent.hashtag_generator.combine_hashtags(hashtag_set, target_platform)

    console.print()
    console.print(f"[bold yellow]# האשטאגים ל: {topic}[/bold yellow]")
    console.print(f"[dim]פלטפורמה: {target_platform.value}[/dim]")
    console.print("-" * 50)

    console.print("\n[cyan]Broad Reach:[/cyan]")
    console.print(" ".join(hashtag_set.broad_reach))

    console.print("\n[cyan]Niche Specific:[/cyan]")
    console.print(" ".join(hashtag_set.niche_specific))

    console.print("\n[green]Combined (copy-paste):[/green]")
    console.print(" ".join(combined))


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()

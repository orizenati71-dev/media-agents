"""Hebrew Quality Assurance module for natural Israeli Hebrew."""

import re
from dataclasses import dataclass, field

from ..models import QAResult


@dataclass
class HebrewQA:
    """Hebrew QA processor for converting formal/robotic Hebrew to natural Israeli Hebrew."""

    # Formal to casual replacements
    formal_to_casual: dict[str, str] = field(default_factory=lambda: {
        # Formal verbs and phrases to casual
        "אנו": "אנחנו",
        "הנכם": "אתם",
        "הננו": "אנחנו",
        "באפשרותך": "אתה יכול",
        "באפשרותכם": "אתם יכולים",
        "ניתן ל": "אפשר ל",
        "בהתאם ל": "לפי",
        "במידה ו": "אם",
        "לאור העובדה ש": "כי",
        "על מנת ש": "כדי ש",
        "על מנת ל": "כדי ל",
        "בגין": "בגלל",
        "לצורך": "בשביל",
        "אודות": "על",
        "הללו": "האלה",
        "לעיל": "למעלה",
        "להלן": "למטה",
        "בהמשך": "אחר כך",
        "לחילופין": "או",
        "כאמור": "כמו שאמרתי",
        "יצוין כי": "",
        "יש לציין כי": "",
        "ראוי לציין כי": "",
        "חשוב לציין כי": "חשוב ש",
        "אך ורק": "רק",
        "בלבד": "רק",
        "כלל וכלל": "בכלל",
        "מן הראוי": "כדאי",
        "עקב": "בגלל",
        "הואיל ו": "כי",
        "כפי ש": "כמו ש",
        "אשר": "ש",
        "מאחר ו": "כי",
        "לפיכך": "אז",
        "אי לכך": "לכן",
        "עם זאת": "אבל",
        "יחד עם זאת": "אבל",
        "למרות זאת": "אבל בכל זאת",
        "כמו כן": "וגם",
        "בנוסף לכך": "וגם",
        "בנוסף": "וגם",
        "לסיכום": "בקיצור",
    })

    # AI/Marketing cringe phrases to avoid or replace
    cringe_phrases: dict[str, str] = field(default_factory=lambda: {
        "הזדמנות אחרונה": "עכשיו זה הזמן",
        "מדהים": "מגניב",
        "מהפכני": "חדש",
        "חוויה יוצאת דופן": "חוויה טובה",
        "פורץ דרך": "חדשני",
        "ייחודי במינו": "מיוחד",
        "משנה חיים": "עוזר ברצינות",
        "הצלחה מסחררת": "הצלחה",
        "תוצאות מטורפות": "תוצאות טובות",
        "לא תאמינו": "",
        "מה שקורה אחר כך יפתיע אתכם": "",
        "הסוד ש": "",
        "הטריק ש": "הדרך ש",
        "שיטה סודית": "שיטה",
        "טיפ זהב": "טיפ טוב",
        "חייבים לדעת": "כדאי לדעת",
        "משהו ענק": "משהו טוב",
        "בום": "",
        "וואו": "",
    })

    # Common spelling corrections
    spelling_fixes: dict[str, str] = field(default_factory=lambda: {
        # Common typos and errors
        "פה": "פה",  # context-dependent
        "פא": "פה",
        "לבדוק": "לבדוק",
        "אחלה": "אחלה",
        "סבבה": "סבבה",
        "יאללה": "יאללה",
        "באמת": "באמת",
        "בטוח": "בטוח",
        "כאילו": "כאילו",
        "ממש": "ממש",
        "סתם": "סתם",
        "רצינו": "רצינו",
    })

    # Patterns for detecting overly formal structures
    formal_patterns: list[tuple[str, str]] = field(default_factory=lambda: [
        # Future passive constructions to active
        (r"יבוצע על ידי", "יעשה"),
        (r"יתבצע על ידי", "יעשה"),
        (r"בוצע על ידי", "עשה"),
        (r"נעשה על ידי", "עשה"),
        # Remove unnecessary hedging
        (r"למעשה,?\s*", ""),
        (r"בעצם,?\s*", ""),
        (r"כביכול,?\s*", ""),
        (r"אם כך,?\s*", "אז "),
        # Simplify connectors
        (r"\s+אולם\s+", " אבל "),
        (r"\s+אך\s+", " אבל "),
        (r"\s+כי אם\s+", " אלא "),
    ])

    def process(self, text: str) -> QAResult:
        """Process Hebrew text for quality and naturalness."""
        corrections = []
        corrected = text

        # Apply formal to casual replacements
        for formal, casual in self.formal_to_casual.items():
            if formal in corrected:
                corrected = corrected.replace(formal, casual)
                corrections.append(f"'{formal}' → '{casual}'")

        # Remove/replace cringe marketing phrases
        for cringe, replacement in self.cringe_phrases.items():
            if cringe in corrected:
                corrected = corrected.replace(cringe, replacement)
                corrections.append(f"הוסר/הוחלף: '{cringe}'")

        # Apply pattern-based corrections
        for pattern, replacement in self.formal_patterns:
            if re.search(pattern, corrected):
                corrected = re.sub(pattern, replacement, corrected)
                corrections.append(f"תיקון תבנית: {pattern}")

        # Clean up multiple spaces and punctuation issues
        corrected = re.sub(r"\s+", " ", corrected)
        corrected = re.sub(r"\s+([.,!?])", r"\1", corrected)
        corrected = corrected.strip()

        # Generate notes
        notes = self._generate_notes(text, corrected)

        return QAResult(
            original_text=text,
            corrected_text=corrected,
            corrections=corrections,
            notes=notes,
        )

    def _generate_notes(self, original: str, corrected: str) -> list[str]:
        """Generate helpful notes about the text."""
        notes = []

        # Check text length
        if len(original) > 300:
            notes.append("הטקסט ארוך - שקול לקצר לפורמט סושיאל")

        # Check for English words
        english_pattern = r"[a-zA-Z]{3,}"
        english_words = re.findall(english_pattern, original)
        if english_words:
            notes.append(f"מילים באנגלית: {', '.join(set(english_words)[:5])}")

        # Check for potential formality issues
        if "הנכם" in original or "הננו" in original or "באפשרותך" in original:
            notes.append("הטקסט המקורי היה פורמלי מדי - הותאם לעברית מדוברת")

        # Check for hashtags already in text
        if "#" in original:
            notes.append("הטקסט כולל האשטאגים - יופרדו בפלט")

        return notes

    def validate_hebrew(self, text: str) -> bool:
        """Check if text contains Hebrew characters."""
        hebrew_pattern = r"[\u0590-\u05FF]"
        return bool(re.search(hebrew_pattern, text))

    def get_hebrew_word_count(self, text: str) -> int:
        """Count Hebrew words in text."""
        # Split by whitespace and filter Hebrew words
        words = text.split()
        hebrew_pattern = r"[\u0590-\u05FF]"
        hebrew_words = [w for w in words if re.search(hebrew_pattern, w)]
        return len(hebrew_words)

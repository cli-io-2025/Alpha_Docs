"""
document_presets.py — Enterprise Document Presets Engine
Defines layout, typography, margins, and spacing presets for academic and corporate standards
(APA 7th Edition, MLA 9th Edition, IEEE Paper, Corporate Business Report).
"""

from dataclasses import dataclass
from PySide6.QtGui import QFont, QTextBlockFormat, QTextCharFormat, QColor
from PySide6.QtCore import Qt
from resume_layouts import RESUME_HTML_EXECUTIVE, RESUME_HTML_EDITORIAL, RESUME_HTML_SAGE, RESUME_HTML_TERRACOTTA
from brochure_layouts import (
    BROCHURE_HTML_BIFOLD,
    BROCHURE_HTML_TRIFOLD_TECH,
    BROCHURE_HTML_EDITORIAL_TERRACOTTA,
    BROCHURE_HTML_EMERALD_GOLD,
)


@dataclass
class DocumentPreset:
    name: str
    font_family: str
    font_size: int
    line_spacing: float
    paragraph_indent_pts: float
    margin_top_mm: float
    margin_bottom_mm: float
    margin_left_mm: float
    margin_right_mm: float
    space_after_pts: float = 0.0


RESUME_TEMPLATES_CATALOG: dict[str, dict] = {
    "Resume - Strategic Marketing": {
        "title": "Strategic Marketing",
        "badge": "MARKETING & BRAND LEADERSHIP",
        "description": "Midnight navy sidebar, terracotta copper accents, segmented progress meters, and multi-channel campaign impact.",
        "image_file": "resume_template_4_terracotta.jpg",
        "key": "Resume - Strategic Marketing",
    },
    "Resume - Executive Corporate": {
        "title": "Executive Corporate",
        "badge": "LEADERSHIP & ENTERPRISE",
        "description": "Structured Navy & Slate layout with 2-column balance, clear executive metrics, and credentials.",
        "image_file": "resume_template_1_executive.jpg",
        "key": "Resume - Executive Corporate",
    },
    "Resume - Creative Editorial": {
        "title": "Creative Editorial",
        "badge": "DESIGN & VISUAL ARTS",
        "description": "Warm ivory tones, elegant typography, designer avatar profile, dot skill ratings, and interests.",
        "image_file": "resume_template_2_creative.jpg",
        "key": "Resume - Creative Editorial",
    },
    "Resume - Modern Sage": {
        "title": "Modern Sage Geometric",
        "badge": "STRATEGY & INNOVATION",
        "description": "Sage green sidebar, contemporary badges, geometric progress meters, and industry awards.",
        "image_file": "resume_template_3_sage.jpg",
        "key": "Resume - Modern Sage",
    },
}


BROCHURE_TEMPLATES_CATALOG: dict[str, dict] = {
    "Brochure - Bi-Fold Spread": {
        "title": "Bi-Fold Spread",
        "badge": "EARTH-TONED OPEN SPREAD",
        "description": "Natural forest green, sage, and warm gold open spread featuring 'Who We Are', structured service highlights, inspirational quote box, and contact details.",
        "image_file": "brochure_template_1_bifold.jpg",
        "key": "Brochure - Bi-Fold Spread",
    },
    "Brochure - Modern Tech Tri-Fold": {
        "title": "Modern Tech Tri-Fold",
        "badge": "GEOMETRIC & TECH",
        "description": "Dynamic navy, vibrant orange, and electric teal tri-fold featuring 3-panel workflow, 'What We Do', 'Who We Are', and 'Your Future'.",
        "image_file": "brochure_template_2_trifold_tech.jpg",
        "key": "Brochure - Modern Tech Tri-Fold",
    },
    "Brochure - Editorial Studio": {
        "title": "Editorial Studio",
        "badge": "DESIGN & CREATIVE STUDIO",
        "description": "Warm terracotta, midnight navy, and soft sand open spread featuring 'Our Approach', 3-step creative process, and 'The Future of Design'.",
        "image_file": "brochure_template_3_bifold_terracotta.jpg",
        "key": "Brochure - Editorial Studio",
    },
    "Brochure - Emerald Enterprise": {
        "title": "Emerald Enterprise",
        "badge": "CORPORATE & CONSULTING",
        "description": "Deep emerald teal, charcoal slate, and olive gold tri-fold spread featuring 'About Us', 'What We Offer', and leadership highlights.",
        "image_file": "brochure_template_4_trifold_emerald.jpg",
        "key": "Brochure - Emerald Enterprise",
    },
}


SAMPLE_TEMPLATES: dict[str, str] = {
    "Essay": """# The Impact of Autonomous Systems on Modern Software Engineering

## Abstract
This study explores the systemic integration of autonomous AI agents in software development lifecycles. We evaluate quantitative shifts in developer productivity and code safety.

## 1. Introduction
Modern software engineering has reached an inflection point where procedural automation transitions into autonomous synthesis. The deployment of contextual language models empowers development teams to compress planning and execution cadences.

## 2. Methodology & Analytical Framework
We analyzed cross-functional development cohorts across 12 enterprise repositories over a six-month evaluation period. Primary metrics included compilation pass-rates, static analysis security density, and issue resolution velocities.

## 3. Findings & Discussion
Empirical results substantiate a 38% reduction in regression turnaround times when real-time AI assistance is coupled with continuous static inspection.

## 4. Conclusion
Systematic human-agent collaboration represents a durable paradigm shift that enhances software quality while preserving developer autonomy.
""",
    "Report": """# Q3 Strategic Performance & Technology Roadmap

## Executive Summary
Alpha Tech's third-quarter operations demonstrated strong growth across all core document intelligence vectors, with overall platform throughput exceeding benchmarks by 24%.

## 1. Key Performance Indicators
- **System Availability:** 99.98% uptime across all cluster regions.
- **Processing Velocity:** Mean response latency reduced from 420ms to 160ms.
- **Client Retention:** Enterprise cohort retention rose to 97.4%.

## 2. Technology Upgrades & Milestones
During this cycle, we deployed the unified document processing engine, high-fidelity PDF rasterization, and inline AST markdown compilation.

## 3. Financial Summary & Resource Allocation
Capital expenditure remained strictly aligned with the FY26 technology strategy, prioritizing edge inference infrastructure.

## 4. Next Steps
Phase 4 will focus on multi-modal model integrations and real-time collaborative document synchronization.
""",
    "Resume - Strategic Marketing": RESUME_HTML_TERRACOTTA,
    "Resume - Executive Corporate": RESUME_HTML_EXECUTIVE,
    "Resume - Creative Editorial": RESUME_HTML_EDITORIAL,
    "Resume - Modern Sage": RESUME_HTML_SAGE,
    "Resume - Professional": RESUME_HTML_TERRACOTTA,
    "Resume": RESUME_HTML_TERRACOTTA,
    "Brochure - Bi-Fold Spread": BROCHURE_HTML_BIFOLD,
    "Brochure - Modern Tech Tri-Fold": BROCHURE_HTML_TRIFOLD_TECH,
    "Brochure - Editorial Studio": BROCHURE_HTML_EDITORIAL_TERRACOTTA,
    "Brochure - Emerald Enterprise": BROCHURE_HTML_EMERALD_GOLD,
    "Brochure": BROCHURE_HTML_BIFOLD,
    "Brochure - Modern Corporate": BROCHURE_HTML_TRIFOLD_TECH,
    "Brochure - Creative Portfolio": BROCHURE_HTML_EDITORIAL_TERRACOTTA,
    "Brochure - Travel": BROCHURE_HTML_BIFOLD,
    "Brochure - Product": BROCHURE_HTML_EMERALD_GOLD,
    "Cover Letter": """Alex Morgan
124 Innovation Way
San Francisco, CA 94105
alex.morgan@alphatech.io

November 7, 2026

Hiring Committee
Alpha Tech Innovations
500 Technology Parkway
San Francisco, CA 94107

Dear Hiring Committee,

I am writing to express my enthusiastic interest in the Principal AI Systems Engineer role at Alpha Tech. Having closely followed your recent advancements in native desktop document intelligence and autonomous developer workflows, I am eager to contribute my expertise in high-performance software architecture and LLM integration to your mission.

Over the past decade, I have led the architecture of mission-critical systems that unite rigorous software design with modern AI capabilities. At my previous venture, I designed an offline-first desktop suite that reduced developer documentation turnaround times by 40% while preserving absolute data sovereignty.

What excites me most about Alpha Tech is your dedication to uncompromising UI polish, architectural integrity, and developer empowerment. I welcome the opportunity to discuss how my background can accelerate your upcoming milestones.

Thank you for your time and consideration.

Sincerely,

Alex Morgan
""",
    "Article": """# The Rise of Local-First Desktop AI Environments

By **Alpha Tech Editorial**

In an era dominated by centralized cloud services, a silent renaissance is taking place on the developer desktop. Local-first architectures, powered by optimized on-device language models, are redefining what it means to build truly responsive, secure productivity tools.

### Why Latency and Privacy Trump the Cloud
When editing critical contracts, intellectual property, or confidential codebases, data custody is paramount. Cloud roundtrips not only introduce network latency that breaks creative flow, but they also expose sensitive text to external compliance risks.

### The Power of Native Canvas Engineering
Modern toolkits like PySide6 enable software to bypass the memory bloat of web-wrapped containers. With native sub-millisecond event loops and custom paged viewports, desktop suites deliver tactile responsiveness that browser tabs cannot match.

### Looking Ahead
As desktop silicon continues to incorporate dedicated neural accelerators, the boundary between developer intent and intelligent synthesis will dissolve entirely.
""",
    "Guide": """# User Guide & Reference Manual: Alpha Tech Suite

## Getting Started
Welcome to the Alpha Tech Enterprise Document Suite. This guide outlines standard workflows for drafting, formatting, auditing, and exporting enterprise documents.

### 1. Document Creation & Templates
- Click **New Document** from the left navigation panel to start a clean canvas.
- To use an industry preset (APA 7th, MLA 9th, IEEE), open the **Page Layout** ribbon tab and select your standard.

### 2. Search & Replace (Ctrl + F)
- Press **Ctrl + F** to open the inline Find & Replace bar.
- Toggle **Match Case** or **Whole Word** to filter search results with live counter badges.

### 3. AI Writing Copilot
- Select any paragraph or phrase, then click **Summarize**, **Polish**, or **Expand** on the **AI Assistant** ribbon tab.
- Click **Insert at Cursor** or **Replace Selection** in the side panel to apply changes.

### 4. Multi-Format Export (Ctrl + E)
- Press **Ctrl + E** or click **Export File** to generate PDF, Markdown, HTML5, or Plain Text files.
"""
}

PRESETS: dict[str, DocumentPreset] = {
    "APA 7th Edition (Academic)": DocumentPreset(
        name="APA 7th Edition",
        font_family="Times New Roman",
        font_size=12,
        line_spacing=2.0,
        paragraph_indent_pts=36.0, # 0.5 inch
        margin_top_mm=25.4,
        margin_bottom_mm=25.4,
        margin_left_mm=25.4,
        margin_right_mm=25.4,
        space_after_pts=0.0
    ),
    "MLA 9th Edition": DocumentPreset(
        name="MLA 9th Edition",
        font_family="Times New Roman",
        font_size=12,
        line_spacing=2.0,
        paragraph_indent_pts=36.0,
        margin_top_mm=25.4,
        margin_bottom_mm=25.4,
        margin_left_mm=25.4,
        margin_right_mm=25.4,
        space_after_pts=0.0
    ),
    "IEEE Academic Paper": DocumentPreset(
        name="IEEE Paper",
        font_family="Times New Roman",
        font_size=10,
        line_spacing=1.15,
        paragraph_indent_pts=12.0,
        margin_top_mm=19.1,
        margin_bottom_mm=19.1,
        margin_left_mm=19.1,
        margin_right_mm=19.1,
        space_after_pts=2.0
    ),
    "Corporate Business Report": DocumentPreset(
        name="Corporate Business Report",
        font_family="Arial",
        font_size=11,
        line_spacing=1.15,
        paragraph_indent_pts=0.0,
        margin_top_mm=25.4,
        margin_bottom_mm=25.4,
        margin_left_mm=25.4,
        margin_right_mm=25.4,
        space_after_pts=6.0
    )
}


def apply_preset_to_editor(preset_name: str, editor_page):
    """Applies a named preset to a DocumentEditorPage instance."""
    preset = PRESETS.get(preset_name)
    if not preset:
        return

    # 1. Update Page Engine Margins & Sizes
    editor_page.editor.setMarginsMM(
        preset.margin_top_mm,
        preset.margin_bottom_mm,
        preset.margin_left_mm,
        preset.margin_right_mm
    )

    # 2. Typography & Block Format
    font = QFont(preset.font_family, preset.font_size)
    doc = editor_page.editor.document()
    doc.setDefaultFont(font)

    block_fmt = QTextBlockFormat()
    block_fmt.setLineHeight(preset.line_spacing * 100.0, QTextBlockFormat.LineHeightTypes.ProportionalHeight.value)
    block_fmt.setTextIndent(preset.paragraph_indent_pts)
    block_fmt.setBottomMargin(preset.space_after_pts)

    char_fmt = QTextCharFormat()
    char_fmt.setFont(font)
    char_fmt.setForeground(Qt.GlobalColor.black)

    cursor = editor_page.editor.cursor()
    cursor.setBlockFormat(block_fmt)
    cursor.setCharFormat(char_fmt)
    editor_page.editor._set_cursor(cursor)

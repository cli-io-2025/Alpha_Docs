# Alpha_Docs Studio

![Status](https://img.shields.io/badge/Status-Phase%201%20Prototype-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![PySide6](https://img.shields.io/badge/GUI-PySide6%20%2F%20Qt-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Alpha_Docs Studio is a high-performance desktop productivity environment designed exclusively for **Windows 10 / 11**. It unifies an interactive paged word processor, a syntax-highlighted code editor, and a dual-mode AI assistant within a responsive, hardware-accelerated interface.

---

## Key Features

### Paged Document Engine
- Paginated document layout with dynamic margin rulers.
- Real-time page thumbnails and visual filmstrip jump navigation.
- Integrated spellchecking and custom caret styles.
- Export pipeline for AST-driven Markdown, HTML5, and PDF document publishing.

### Multi-Tab Code Workspace
- Code editing powered by syntax highlighting across Python, JavaScript, C++, Rust, JSON, and HTML.
- Contrast-guarded dark and light display modes.
- Code reformatting, tab indentation management, and inline line numbering.

### Dual-Mode AI Copilot
- Collapsible contextual assistant pane featuring Document and Code modes.
- Configurable prompt directives and quick-insert buffer actions.

### Alpha Telemetry & Focus Audio Engine
- Embedded procedural focus audio generator (ambient white noise, rain, and binaural soundscapes).
- Dynamic 44-bar audio frequency visualizer.
- Live typing velocity tracking (WPM), word counters, and active page metrics.

### Theme Engine & Personalization
- 8 preconfigured dark/light palettes.
- Integrated Theme Studio for custom background tints, accent glows, and surface styling.

---

## System Requirements

- **Operating System:** Windows 10 (version 21H2 or later) or Windows 11 (64-bit)
- **Processor:** 64-bit multi-core CPU
- **Memory:** 4 GB RAM minimum (8 GB recommended)
- **Python:** Version 3.10 or newer

---

## Dependencies & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/cli-io-2025/Alpha_Docs.git
   cd Alpha_Docs
   ```

2. **Install Required Libraries**
   ```bash
   pip install PySide6 pygments pyspellchecker
   ```

3. **Launch Application**
   ```bash
   python Alpha_Docs/main.py
   ```

---

## License

This software is released under the **MIT License**.

Developed by the Architect behind [TechGarden.Online](https://techgarden.online).

# Beyond Vibe Coding (Russian Translation)

> **За гранью вайб-кодинга: Разработка софта с ИИ-саппортом**

This repository hosts the Russian translation of the book **"Beyond Vibe Coding"** by **Addy Osmani**.

The translation was performed using a custom automated pipeline designed to maintain a specific **"Vibe Coding" persona**: ironic, humorous, faithful to the tech-savvy spirit of the original, and tailored for a modern developer audience.

## 📖 About the Project

"Beyond Vibe Coding" explores the shift from traditional coding to AI-assisted engineering. This translation aims to capture not just the technical content but the *vibe* of this new era.

- **Original Author**: Addy Osmani
- **Language**: Russian (Professional/Slang/Irony mix)
- **Format**: Static Documentation Site

## 🛠 Tech Stack

- **Framework**: [VitePress](https://vitepress.dev/) - for a fast, content-centric website.
- **Content**: Markdown
- **Translation Engine**: Custom Node.js script using OpenRouter (Gemini 1.5 Pro) with context-aware chunking and persona-based prompting.

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or pnpm

### Installation

```bash
npm install
```

### Running Locally

Start the development server to read the book locally:

```bash
npm run dev
```

The site will be available at `http://localhost:5173/beyond-vibe-coding/`.

### Building for Production

To build the static site:

```bash
npm run build
```

The output will be generated in `docs/.vitepress/dist`.

## 📂 Project Structure

- `docs/` - Markdown source files for chapters.
- `docs/.vitepress/` - VitePress configuration and theme customization.
- `docs/public/` - Static assets.

## 🤖 Translation Process

The translation was executed using an AI agentic workflow:
1.  **Conversion**: Original text converted to structured Markdown.
2.  **Chunking**: Large chapters split into context-aware chunks for processing.
3.  **Translation**: Processed through a sophisticated prompting system to ensure consistent terminology and tone ("dirty realism" style).
4.  **Verification**: Manual and automated checks for formatting and build integrity.

---

*Verified and Built with Vibe* ✨

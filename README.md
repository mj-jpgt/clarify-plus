﻿# Clarify+

> **A lightweight, open-source “decision-aid compiler” that makes any medical PDF or webpage *clearer, fairer, and easier to trust*—in one click.**

---

## ✨ What Clarify+ Does
1. **EquiCheck — Cultural-Equity & Readability Audit**  
   * Runs SMOG & Gunning-Fog on the fly.  
   * Flags jargon, idioms, and images that clash with the Cultural Tailoring Score (CTS) rubric.  
   * Generates a live radar badge so authors can watch their equity score rise as they edit.

2. **NumiCraft — Interactive Risk Literacy Engine**  
   * Detects every percentage, “1 in N,” or relative-risk statement.  
   * Auto-builds colour-blind-safe icon arrays or bar charts.  
   * Embeds 30-second “micro-quests” that teach users how to read the graphic and raise Berlin Numeracy scores.

3. **Plain-Language Rewriter**  
   * One-tap GPT-3.5 rewrite to 6-8ᵗʰ-grade English (Spanish toggle optional).  

4. **Drop-In Widget**  
   * `<clarify-widget>` web component that can be pasted into any EHR viewer, patient portal, or static site.  
   * Netlify-hosted demo at **https://clarifyplus.app**.

---

## 🔥 Why It Matters
* **Equity Gap:** <6 % of 200+ PtDA trials analyze outcomes by race or education.  
* **Numeracy Gap:** Icon arrays alone can *mislead*—shifting perceived risk by 22 % if colors are wrong.  
* **Integration Gap:** No published tool tackles cultural tailoring *and* risk-numeracy training in the same pipeline.  
Clarify+ closes all three gaps with ~200 lines of Python + React and zero proprietary dependencies.

---

## 🛠 Tech Stack
| Layer | Choice | Rationale |
|-------|--------|-----------|
| Back end | **Python 3.11 + FastAPI** | Simple REST; easy `pytest` coverage |
| Parsing | **PyMuPDF, BeautifulSoup** | Fast PDF & HTML scrape |
| Readability & CTS | **textstat + custom keyword rules** | 100 % offline |
| Risk graphics | **Matplotlib** | No seaborn colors → WCAG AA safe |
| Front end | **React 18 + Tailwind CSS** | Accessible by default, keyboard-friendly |
| AI Rewrite | **OpenAI GPT-3.5** (free-tier caching) | Cheap, deterministic prompts |
| CI / CD | **GitHub Actions + Netlify** | Green checks on every push |

---

## 🚀 Quick Start (Local)

```bash
# 1. clone & install
git clone https://github.com/<your-handle>/clarify-plus.git
cd clarify-plus
pip install -r backend/requirements.txt
cd frontend && npm ci && npm run dev
# 2. process a PDF
cd ../backend
python riskify.py sample_docs/flu_shot.pdf --out build/
# 3. open localhost:3000?file=flu_shot.json


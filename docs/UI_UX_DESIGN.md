# 🎨 DarkShield AI — UI/UX Design Specification

**Design System:** Sentinel Amber (Carbon Gunmetal & Vigilant Amber)  
**Target Environments:** Web Dashboard (Desktop & Mobile), Chromium Extension Popup (340px width)  
**Document Version:** 2.0.0  

---

## 1. Design Philosophy & Creative Direction

Early prototypes often suffer from overly flashy "cyberpunk" aesthetics (bright neon magentas, harsh cyan glows, distracting particle animations) that feel like video games rather than serious enterprise or academic tools. 

DarkShield AI uses the **Sentinel Amber** design system:
- **Restrained & Authoritative:** Uses deep slate gunmetal (`#08090d`, `#0f1118`) inspired by intelligence and cybersecurity dashboards.
- **Vigilant Amber Accent:** Employs warm amber/gold (`#f59e0b`, `#d97706`) as a symbol of caution, inspection, and illumination, avoiding aggressive eye fatigue.
- **Clear Threat Triaging:** High-contrast threat indicators (Coral Red `#f43f5e` for deceptive patterns, Emerald Mint `#10b981` for clean pages) provide instant situational awareness.
- **Data-Dense Yet Legible:** Combines modern sans-serif typography for content with monospaced figures for metrics, model parameters, and token scores.

---

## 2. Color Palette & Design Tokens

### 2.1 Core Palette

| Token Name | Hex Value | Purpose & Application |
| :--- | :---: | :--- |
| `--bg-primary` | `#08090d` | Root application background |
| `--bg-secondary` | `#0f1118` | Sub-panels, header bands, extension container |
| `--bg-card` | `#151821` | Elevated component cards, inspector decks |
| `--bg-card-hover` | `#1b1f2b` | Hover state for interactive cards |
| `--bg-input` | `#0c0e14` | Recessed input fields, code blocks |
| `--border-subtle` | `#212534` | Dividers, card outlines, subtle structural borders |
| `--border-card` | `#2c3246` | Active card borders |
| `--border-focus` | `#f59e0b` | Input and button focus rings |
| `--text-primary` | `#f8fafc` | Primary headings and high-contrast body text |
| `--text-secondary` | `#94a3b8` | Subtitles, labels, descriptions |
| `--text-muted` | `#64748b` | Timestamps, secondary metadata |

### 2.2 Functional Accents

| Token Name | Hex Value | Semantic Role |
| :--- | :---: | :--- |
| `--accent-primary` | `#f59e0b` | Primary action button, active tab, vigilant brand |
| `--accent-hover` | `#d97706` | Hover state for primary buttons |
| `--accent-bg` | `rgba(245, 158, 11, 0.10)` | Token chips, badge backings, highlight fills |
| `--danger-primary` | `#f43f5e` | Deceptive pattern detection alert, critical risk |
| `--danger-bg` | `rgba(244, 63, 94, 0.10)` | Threat badge background |
| `--success-primary` | `#10b981` | Verified clean element, non-deceptive status |
| `--success-bg` | `rgba(16, 185, 129, 0.10)` | Safe badge background |

---

## 3. Typography System

DarkShield AI pairs two modern Google Fonts:
1. **`Plus Jakarta Sans`:** Clean, geometric sans-serif for UI labels, buttons, navigation, and body copy.
2. **`JetBrains Mono`:** Technical monospaced font for confidence percentages, token scores, SHAP contribution weights, and raw DOM text.

```css
--font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```

### Hierarchy Scale

- **H1 (Hero Heading):** 36px / 44px line-height, Weight 800 (Bold tracking)
- **H2 (Card Headers):** 20px / 26px line-height, Weight 700
- **H3 (Sub-sections):** 16px / 22px line-height, Weight 600
- **Body Regular:** 14px / 20px line-height, Weight 400
- **Small / Metadata:** 12px / 16px line-height, Weight 500
- **Mono Score:** 13px / 18px line-height, Weight 600

---

## 4. Key Component Anatomy (Web Dashboard)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [🛡] DarkShield AI                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│               Detect & Expose Dark Patterns on Any Web Page                 │
│         Audit e-commerce pages for hidden costs, drip pricing, etc.         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ [🔗] https://www.amazon.in/item/...                 [⚡ Run Audit]    │  │
│  │ Model Focus: [LR] [SVM] [LSTM] [GRU]     [🔘 Benchmark All 4: ON]     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────┐   ┌─────────────────────────────────┐  │
│  │ ⚠️ DECEPTIVE PATTERN DETECTED    │   │ Key Indicators (SHAP Weights)   │  │
│  │ Confidence: 99.5%               │   │ [left +1.97]  [stock +1.09]     │  │
│  │ Risk Level: CRITICAL            │   │ [items +1.06] [order +0.87]     │  │
│  └─────────────────────────────────┘   └─────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 4-Model Comparative Benchmark Table                                   │  │
│  │ LR: 99.5% | SVM: 99.2% | LSTM: 99.9% | GRU: 99.8%                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Scanned DOM Text Extract                           [📋 Copy Text]     │  │
│  │ "FLASH SALE! Limited time only. Only 2 items left in stock..."        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Navigation Bar:** Minimalist top bar with custom vector Sentinel Shield favicon and application title.
2. **Search & Control Deck:** Integrated URL input field with sample e-commerce presets, model focus selectors, and single/multi-model toggles.
3. **Primary Threat Assessment Card:** High-impact status indicator dynamically colored according to model confidence.
4. **SHAP Key Indicators Deck:** Displays detected manipulative tokens with quantitative contribution badges (`+1.973`, `+1.091`).
5. **Multi-Model Benchmark Grid:** Side-by-side comparison across all 4 machine learning models showing agreement and variance.
6. **DOM Text Inspector:** Monospaced terminal-style card displaying extracted visible page text with one-click clipboard copying.

---

## 5. Chrome Extension Popup Anatomy (340px)

```
┌────────────────────────────────────────┐
│ [🛡] DarkShield AI          (🟢 Online) │
│      Pattern Inspector                 │
├────────────────────────────────────────┤
│ Detection Engine:                      │
│ [ Support Vector Machine (Margin)    ▼]│
│                                        │
│ [      Audit Current Web Page         ]│
├────────────────────────────────────────┤
│ ⚠️ DARK PATTERN DETECTED                │
│ Confidence: 99.5%                      │
│                                        │
│ Manipulative Indicators (SHAP):        │
│ [left] [stock] [items] [order] [sale]  │
│                                        │
│ Scanned Text Sample:                   │
│ "FLASH SALE! Only 2 items left..."     │
└────────────────────────────────────────┘
```

- **Width:** Fixed 340px viewport optimized for Chromium extension drawers.
- **One-Click Audit:** Automatically queries active tab via `chrome.tabs.query` and posts directly to the local or remote FastAPI backend.
- **Offline/Online Sentinel Dot:** Green pulsing indicator confirms backend connectivity.

---

## 6. Accessibility & Responsiveness (WCAG 2.1 AA)

- **Color Contrast:** All body text meets or exceeds a $4.5:1$ contrast ratio against dark backgrounds (`#f8fafc` on `#08090d` = $18.4:1$).
- **Reduced Motion:** Interactive buttons and loaders respect `@media (prefers-reduced-motion: reduce)`.
- **Keyboard Navigation:** Full focus ring outline (`--border-focus: #f59e0b`) on all interactive inputs, buttons, and dropdowns.
- **Fluid Layouts:** Uses CSS Grid and Flexbox with responsive breakpoints (`@media (max-width: 768px)` and `@media (max-width: 480px)`).

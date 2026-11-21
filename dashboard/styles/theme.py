
"""AEGIS — Royal Rajasthani-inspired Design System.

Visual styling for the AEGIS Streamlit dashboard.
Does not modify backend security or authorization logic.
"""

import streamlit as st


# ==========================================
# 1. COLOR PALETTES
# ==========================================

THEMES = {
    "Light": {
        "background": "#FFF7ED", "surface": "#FFFDF8",
        "soft": "#F8DFCA", "border": "#DDBCA2",
        "text": "#271C1B", "muted": "#70544A",
        "accent": "#801D32", "accent_hover": "#5E1427",
        "button_text": "#FFF8EB", "success": "#27664D",
        "success_bg": "#E0EBDD", "danger": "#AB3033",
        "danger_bg": "#F9DDDA", "violet": "#935769",
        "gold": "#AC6D12", "gold_soft": "#FFE4A1",
        "rose": "#F3C9C6", "terracotta": "#DF6238",
        "sage": "#DCEAD9", "input_bg": "#FFFDF9",
        "input_text": "#271C1B", "input_hint": "#805F53",
    },
    "Dark": {
        "background": "#171314", "surface": "#282021",
        "soft": "#43292A", "border": "#6E4B40",
        "text": "#FFF1DD", "muted": "#E0C4AC",
        "accent": "#FFA16C", "accent_hover": "#FFC28A",
        "button_text": "#251515", "success": "#A5D1A9",
        "success_bg": "#284435", "danger": "#FF9A89",
        "danger_bg": "#51292C", "violet": "#DBA3A5",
        "gold": "#F6C76B", "gold_soft": "#574023",
        "rose": "#5D3038", "terracotta": "#F49359",
        "sage": "#304737", "input_bg": "#342728",
        "input_text": "#FFF1DD", "input_hint": "#D4B29C",
    },
}


# ==========================================
# 2. CUSTOM AEGIS SHIELD
# ==========================================

SHIELD_SVG = """
<svg
    class="aegis-mark"
    viewBox="0 0 56 64"
    width="40"
    height="46"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
>
    <path
        d="M28 3 50 11v18c0 15-9.4 25.4-22 32C15.4 54.4 6 44 6 29V11L28 3Z"
        fill="currentColor"
        fill-opacity=".10"
        stroke="currentColor"
        stroke-width="2.6"
        stroke-linejoin="round"
    />
    <path
        d="M28 12 40 17v12c0 9-4.5 15.6-12 20.4C20.5 44.6 16 38 16 29V17l12-5Z"
        stroke="currentColor"
        stroke-opacity=".5"
        stroke-width="1.5"
    />
    <path
        d="m18 30 7 7 15-16"
        stroke="currentColor"
        stroke-width="3.4"
        stroke-linecap="round"
        stroke-linejoin="round"
    />
    <circle
        cx="28"
        cy="5"
        r="2.4"
        fill="currentColor"
    />
</svg>
"""


# ==========================================
# 3. APPLY THEME
# ==========================================

def apply_theme(mode):

    t = THEMES.get(mode, THEMES["Light"])

    color_scheme = (
        "dark" if mode == "Dark" else "light"
    )

    # Streamlit versions differ in how the sidebar icon is rendered.
    # Scoped to Dark mode to avoid affecting the Light mode toggle.
    sidebar_arrow_css = ""
    if mode == "Dark":
        sidebar_arrow_css = """
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        button[aria-label="Open sidebar"],
        button[aria-label="Close sidebar"] {
            color: #F8EDF1 !important;
        }
        [data-testid="stSidebarCollapsedControl"] *,
        [data-testid="stSidebarCollapseButton"] *,
        [data-testid="collapsedControl"] *,
        button[aria-label="Open sidebar"] *,
        button[aria-label="Close sidebar"] * {
            color: #F8EDF1 !important;
            -webkit-text-fill-color: #F8EDF1 !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="collapsedControl"] svg,
        button[aria-label="Open sidebar"] svg,
        button[aria-label="Close sidebar"] svg {
            color: #F8EDF1 !important;
            fill: currentColor !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg path,
        [data-testid="stSidebarCollapseButton"] svg path,
        [data-testid="collapsedControl"] svg path {
            fill: currentColor !important;
            stroke: currentColor !important;
        }
        [data-testid="stSidebarCollapsedControl"]:hover,
        [data-testid="stSidebarCollapseButton"]:hover {
            background: #493347 !important;
            border-radius: 9px;
        }
        """

    st.markdown(
        f"""
<style>

/* ==========================================
   FONT IMPORTS
   ========================================== */

@import url(
    'https://fonts.cdnfonts.com/css/anaktoria'
);


/* ==========================================
   GLOBAL THEME
   ========================================== */

:root {{
    color-scheme: {color_scheme};
}}

html,
body,
.stApp,
[data-testid="stWidgetLabel"] {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Helvetica Neue",
        Arial,
        sans-serif !important;
}}


/* ==========================================
   APPLICATION BACKGROUND
   ========================================== */

.stApp {{
    background: {t["background"]};
    color: {t["text"]};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    max-width: 1190px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}}


/* ==========================================
   APPLE SYSTEM TYPOGRAPHY
   ========================================== */

h1, h2, h3, h4, h5, h6 {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Helvetica Neue",
        sans-serif !important;

    color: {t["text"]};
    font-weight: 650 !important;
    letter-spacing: -0.035em !important;
    line-height: 1.2 !important;
}}

h1 {{
    font-size: clamp(2rem, 4vw, 3rem) !important;
}}

h2 {{
    font-size: 1.65rem !important;
}}

h3 {{
    font-size: 1.35rem !important;
}}

p,
li,
label,
button,
input,
textarea,
select {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Helvetica Neue",
        Arial,
        sans-serif !important;
}}


/* ==========================================
   SECONDARY TEXT
   ========================================== */

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
.aegis-tagline,
.aegis-muted,
.aegis-mini-card-caption {{
    color: {t["muted"]} !important;
    font-size: 0.92rem;
    font-weight: 500 !important;
    line-height: 1.65 !important;
    letter-spacing: -0.012em;
}}


/* ==========================================
   SIDEBAR
   ========================================== */

[data-testid="stSidebar"] {{
    background: {t["surface"]};
    border-right: 1px solid {t["border"]};

    /* Allow Streamlit to control width when sidebar collapses. */
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.2rem;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {{
    color: {t["text"]} !important;
}}

[data-testid="stSidebar"] img {{
    max-width: 48px !important;
    height: auto !important;
}}

[data-testid="stSidebar"]
[role="radiogroup"] label {{
    border-radius: 11px;
    padding: 6px 8px;

    transition: background 0.18s ease;
}}

[data-testid="stSidebar"]
[role="radiogroup"] label:hover {{
    background: {t["soft"]};
}}


/* ==========================================
   AEGIS BRANDING
   ========================================== */

.aegis-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.aegis-mark {{
    color: {t["accent"]};

    width: 39px !important;
    height: 45px !important;

    max-width: 39px !important;
    max-height: 45px !important;

    flex-shrink: 0;
}}

.aegis-wordmark {{
    font-family:
        "Anaktoria",
        Georgia,
        serif !important;

    font-size: 3.2rem;
    font-weight: 400 !important;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: {t["text"]};
}}

.aegis-sideword {{
    font-family:
        "Anaktoria",
        Georgia,
        serif !important;

    font-size: 2.3rem;
    font-weight: 400 !important;
    line-height: 1.1;
    color: {t["text"]};
}}


/* ==========================================
   HERO SECTION
   ========================================== */

.aegis-hero {{
    padding: 22px 0 24px;
}}

.aegis-hero h1 {{
    margin: 0 0 9px;
}}

.aegis-eyebrow {{
    font-size: 0.69rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    font-weight: 700;
    color: {t["accent"]};
    margin-bottom: 8px;
}}

.aegis-tagline {{
    max-width: 730px;
}}


/* ==========================================
   DASHBOARD SECTIONS
   ========================================== */

.aegis-section {{
    margin: 24px 0 10px;

    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
}}

.aegis-section-title {{
    font-size: 1.23rem;
    font-weight: 700;
    letter-spacing: -0.035em;
    color: {t["text"]};
}}

.aegis-muted {{
    color: {t["muted"]};
    font-size: 0.86rem;
}}


/* ==========================================
   METRIC CARDS
   ========================================== */

div[data-testid="stMetric"] {{
    background: {t["surface"]};

    border: 1px solid {t["border"]};
    border-radius: 18px;

    padding: 20px 22px;
    min-height: 132px;

    box-shadow:
        0 6px 25px rgba(25, 12, 27, 0.025);

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        box-shadow 0.18s ease;
}}

div[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    border-color: {t["accent"]};

    box-shadow:
        0 8px 25px rgba(25, 12, 27, 0.07);
}}

[data-testid="stMetricValue"] {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Helvetica Neue",
        sans-serif !important;

    color: {t["text"]};
    font-weight: 700;
    letter-spacing: -0.04em;
}}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {{
    color: {t["muted"]} !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
}}


/* ==========================================
   GENERAL CARDS
   ========================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {t["surface"]};
    border-color: {t["border"]} !important;
    border-radius: 20px !important;
}}

div[data-testid="stVerticalBlockBorderWrapper"]
> div[data-testid="stVerticalBlock"] {{
    gap: 0.95rem;
}}

.aegis-mini-card {{
    padding: 18px;
    border-radius: 16px;

    border: 1px solid {t["border"]};
    background: {t["surface"]};

    height: 100%;
}}

.aegis-mini-card-title {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    font-weight: 700;

    color: {t["muted"]};
}}

.aegis-mini-card-value {{
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.035em;

    color: {t["text"]};
    margin-top: 7px;
}}

.aegis-mini-card-caption {{
    margin-top: 7px;
}}


/* ==========================================
   BUTTONS
   ========================================== */

div.stButton > button {{
    border-radius: 11px;
    border: 1px solid {t["border"]};

    background: {t["surface"]};
    color: {t["text"]};

    padding: 0.62rem 1rem;
    font-weight: 600;

    transition:
        transform 0.16s ease,
        box-shadow 0.16s ease,
        border-color 0.16s ease;
}}

div.stButton > button:hover {{
    color: {t["accent"]};
    border-color: {t["accent"]};

    transform: translateY(-1px);

    box-shadow:
        0 5px 16px rgba(40, 15, 37, 0.09);
}}

div.stButton > button[kind="primary"] {{
    background: {t["accent"]};
    border-color: {t["accent"]};
    color: {t["button_text"]};
}}

div.stButton > button[kind="primary"]:hover {{
    background: {t["accent_hover"]};
    color: {t["button_text"]};
}}


/* ==========================================
   INPUTS AND TABS
   ========================================== */

[data-baseweb="textarea"] > div,
[data-baseweb="input"] > div,
[data-baseweb="select"] > div {{
    border-radius: 12px;
    background: {t["surface"]};
    border-color: {t["border"]};
}}

button[data-baseweb="tab"] {{
    font-weight: 600;
    border-radius: 10px 10px 0 0;
}}


/* ==========================================
   TABLES
   ========================================== */

[data-testid="stDataFrame"],
[data-testid="stTable"] {{
    border-radius: 14px;
    overflow: hidden;
}}


/* ==========================================
   TECHNICAL DATA
   ========================================== */

[data-testid="stJson"] *,
pre,
code {{
    font-family:
        "SFMono-Regular",
        "SF Mono",
        Menlo,
        monospace !important;
}}


/* ==========================================
   STATUS ELEMENTS
   ========================================== */

.aegis-pill {{
    display: inline-block;
    padding: 5px 11px;
    border-radius: 999px;

    background: {t["soft"]};
    color: {t["accent"]};

    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}}

[data-testid="stAlert"] {{
    border-radius: 14px;
}}


/* ==========================================
   DIVIDERS & FOOTER
   ========================================== */

hr {{
    border-color: {t["border"]};
    opacity: 0.65;
}}

.aegis-rule {{
    border-top: 1px solid {t["border"]};
    margin: 8px 0 15px;
}}

.aegis-footer {{
    padding-top: 25px;
    color: {t["muted"]};

    font-size: 0.75rem;
    letter-spacing: 0.02em;
}}


/* ==========================================
   ANIMATIONS
   ========================================== */

.aegis-entrance {{
    animation: aegisIn 0.42s ease both;
}}

@keyframes aegisIn {{

    from {{
        opacity: 0;
        transform: translateY(8px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}


/* ==========================================
   ACCESSIBILITY
   ========================================== */

@media (prefers-reduced-motion: reduce) {{

    *,
    *::before,
    *::after {{
        animation: none !important;
        transition: none !important;
    }}
}}


/* ==========================================
   RESPONSIVE DESIGN
   ========================================== */

@media (max-width: 720px) {{

    .block-container {{
        padding: 1.1rem 0.75rem 2rem;
    }}

    .aegis-wordmark {{
        font-size: 2.6rem;
    }}

    div[data-testid="stMetric"] {{
        padding: 12px;
        min-height: 105px;
    }}
}}


/* ==========================================
   DARK-MODE SIDEBAR ARROWS
   ========================================== */

{sidebar_arrow_css}


/* ==========================================
   RETRO-FUTURIST OBSERVATORY — INTERACTION
   ========================================== */

/* The Anaktoria wordmark remains untouched. */
.aegis-wordmark, .aegis-sideword {{
    font-family: "Anaktoria", Georgia, serif !important;
}}

/* Warm multi-accent color language. */
.aegis-eyebrow {{ color: {t["gold"]} !important; }}
.aegis-pill {{ background: {t["soft"]}; color: {t["accent"]}; }}
.aegis-tagline, .aegis-muted, .aegis-mini-card-caption,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    color: {t["muted"]} !important;
    opacity: 1 !important;
    font-weight: 540 !important;
}}

/* Input contrast: make entered text at least as legible as placeholder. */
[data-testid="stTextArea"] textarea,
[data-baseweb="textarea"] textarea,
[data-testid="stTextInput"] input,
[data-baseweb="input"] input {{
    background: {t["input_bg"]} !important;
    color: {t["input_text"]} !important;
    -webkit-text-fill-color: {t["input_text"]} !important;
    caret-color: {t["accent"]} !important;
    opacity: 1 !important;
}}
[data-testid="stTextArea"] textarea::placeholder,
[data-baseweb="textarea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder {{
    color: {t["input_hint"]} !important;
    -webkit-text-fill-color: {t["input_hint"]} !important;
    opacity: 1 !important;
}}
[data-baseweb="textarea"] > div,
[data-baseweb="input"] > div {{
    background: {t["input_bg"]} !important;
    border: 1px solid {t["border"]} !important;
}}
[data-testid="stTextArea"] label,
[data-testid="stTextInput"] label {{
    color: {t["text"]} !important;
    font-weight: 650 !important;
}}

/* Make inactive tabs legible, and reserve the accent for active ones. */
button[data-baseweb="tab"] {{ color: {t["muted"]} !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {t["accent"]} !important;
}}
[data-baseweb="tab-highlight"] {{ background: {t["accent"]} !important; }}

/* Editorial entrances and card interactions. */
.aegis-hero {{ animation: aegisRise 680ms cubic-bezier(.18,.7,.2,1) both; }}
@keyframes aegisRise {{
    from {{ transform: translateY(15px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
}}
.aegis-mini-card,
div[data-testid="stMetric"] {{
    transition: transform 230ms ease, border-color 230ms ease,
                box-shadow 230ms ease !important;
}}
.aegis-mini-card:hover,
div[data-testid="stMetric"]:hover {{
    transform: translateY(-3px);
    border-color: {t["gold"]} !important;
    box-shadow: 0 13px 32px rgba(12,8,6,.14) !important;
}}

/* Decorative orb around the existing shield — reusable in any page. */
.aegis-orbit {{
    width: 118px; height: 118px; border-radius: 50%;
    border: 1px solid {t["border"]};
    background: radial-gradient(circle, {t["surface"]} 0%, {t["soft"]} 100%);
    display: grid; place-items: center;
    position: relative; isolation: isolate;
}}
.aegis-orbit::before {{
    content: ""; position: absolute; inset: 8px;
    border: 2px solid transparent; border-top-color: {t["accent"]};
    border-right-color: {t["gold"]}; border-radius: 50%;
    animation: aegisRotate 13s linear infinite;
}}
.aegis-orbit::after {{
    content: ""; position: absolute; inset: 21px;
    border: 1px dashed {t["violet"]}; border-radius: 50%;
    animation: aegisRotate 24s linear infinite reverse;
}}
.aegis-orbit span {{ color: {t["text"]}; font-weight: 750; font-size: 0.82rem; }}
@keyframes aegisRotate {{ to {{ transform: rotate(360deg); }} }}

/* A short typing treatment, usable beside a heading. */
.aegis-typing {{
    display: inline-block; overflow: hidden; white-space: nowrap;
    max-width: 100%; width: 0; border-right: 2px solid {t["accent"]};
    color: {t["accent"]}; font-size: .8rem;
    letter-spacing: .08em; font-weight: 750;
    animation: aegisType 2.4s steps(23,end) forwards,
               aegisBlink .7s steps(1,end) 5;
}}
@keyframes aegisType {{ to {{ width: 24ch; }} }}
@keyframes aegisBlink {{ 50% {{ border-right-color: transparent; }} }}

/* Footer styles used by show_aegis_footer(). */
.aegis-footer-panel {{
    border-top: 1px solid {t["border"]};
    margin-top: 3rem; padding-top: 1.5rem; padding-bottom: .8rem;
}}
.aegis-footer-title {{ font-size: 1.05rem; font-weight: 750; color: {t["text"]}; }}
.aegis-footer-panel a {{ color: {t["accent"]} !important; font-weight: 650; }}
.aegis-footer-panel a:hover {{ color: {t["gold"]} !important; }}

@media (prefers-reduced-motion: reduce) {{
    .aegis-hero, .aegis-orbit::before, .aegis-orbit::after,
    .aegis-typing {{ animation: none !important; }}
    .aegis-typing {{ width: auto; border: none; }}
    .aegis-mini-card:hover, div[data-testid="stMetric"]:hover {{ transform: none; }}
}}


/* ==========================================
   AEGIS — PLUM, GOLD & ROSE REFINEMENT
   Keep Anaktoria wordmark and system body fonts.
   ========================================== */
:root {{
    --aegis-gold: {t["gold"]};
    --aegis-rose: {t["rose"]};
    --aegis-sage: {t["sage"]};
    --aegis-terracotta: {t["terracotta"]};
}}

/* A quieter editorial canvas, with stronger spacing and hierarchy. */
.block-container {{ max-width: 1240px; }}
.aegis-hero {{ padding: 22px 0 30px; }}
.aegis-hero h1 {{ font-size: clamp(2.2rem, 4vw, 3.25rem) !important; }}
.aegis-tagline {{ font-size: 1.02rem !important; line-height: 1.75 !important; }}
.aegis-eyebrow {{ color: {t["gold"]} !important; letter-spacing: .15em; }}
.aegis-section {{ margin: 28px 0 13px; border-bottom: 1px solid {t["border"]}; padding-bottom: 10px; }}
.aegis-section-title {{ font-size: 1.28rem; }}
.aegis-section .aegis-muted {{ font-size: .7rem !important; letter-spacing: .09em; text-transform: uppercase; }}
.aegis-section::before {{ content: ''; width: 4px; height: 19px; align-self: center; background: {t["gold"]}; border-radius: 4px; flex: 0 0 4px; }}
.aegis-section-title {{ margin-right: auto; }}

/* Small cards have an accent stripe and clear individual roles. */
.aegis-mini-card {{
    position: relative; overflow: hidden;
    background: {t["surface"]};
    border-color: {t["border"]};
    border-radius: 17px;
    padding: 18px 19px 20px;
    min-height: 118px;
    box-shadow: 0 5px 18px rgba(67, 28, 51, .035);
}}
.aegis-mini-card::before {{
    content: ''; display: block; width: 37px; height: 4px; border-radius: 5px;
    background: {t["gold"]}; margin-bottom: 14px;
}}
.aegis-mini-card--gold {{ background: {t["gold_soft"]}; }}
.aegis-mini-card--rose {{ background: {t["rose"]}; }}
.aegis-mini-card--sage {{ background: {t["sage"]}; }}
.aegis-mini-card--rose .aegis-mini-card-title,
.aegis-mini-card--sage .aegis-mini-card-title,
.aegis-mini-card--gold .aegis-mini-card-title {{ color: {t["text"]}; }}
.aegis-mini-card--rose::before {{ background: {t["accent"]}; }}
.aegis-mini-card--sage::before {{ background: {t["success"]}; }}
.aegis-mini-card-title {{ font-size: .69rem; letter-spacing: .12em; }}
.aegis-mini-card-value {{ font-size: clamp(1.08rem, 1.7vw, 1.36rem); overflow-wrap: anywhere; line-height: 1.35; }}
.aegis-mini-card-caption {{ font-size: .84rem !important; line-height: 1.65 !important; }}
.aegis-mini-card:hover {{ transform: translateY(-3px); box-shadow: 0 12px 26px rgba(67, 28, 51, .10); }}

/* Metrics retain native Streamlit behavior but feel like compact cards. */
div[data-testid="stMetric"] {{
    border-top: 4px solid {t["gold"]};
    min-height: 117px; padding: 17px 20px;
    background: {t["surface"]};
}}
[data-testid="stMetricValue"] {{ font-size: clamp(1.8rem, 2.8vw, 2.5rem) !important; color: {t["accent"]} !important; }}
[data-testid="stMetricLabel"] * {{ font-size: .81rem !important; }}

/* Cards, form controls, and tables — unified proportions. */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    box-shadow: 0 4px 18px rgba(67,28,51,.035);
    transition: border-color .2s ease, box-shadow .2s ease;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: {t["gold"]} !important;
    box-shadow: 0 8px 24px rgba(67,28,51,.07);
}}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {t["accent"]} !important; }}
[data-baseweb="tab-highlight"] {{ background: {t["gold"]} !important; height: 3px !important; }}
div.stButton > button:focus-visible,
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {{ outline: 2px solid {t["gold"]}; outline-offset: 2px; }}
div.stButton > button[kind="primary"] {{ box-shadow: 0 4px 14px rgba(67, 28, 51, .13); }}
div.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); }}

/* Security messages use meaningful status colours, not generic bright blue. */
[data-testid="stAlert"] {{ border-radius: 13px !important; }}
[data-testid="stAlert"][data-baseweb="notification"] {{ border-left-width: 4px; }}
.aegis-footer-panel {{ border-top: 2px solid {t["gold"]}; }}
.aegis-footer-panel a {{ text-decoration-color: {t["gold"]}; text-underline-offset: 3px; }}

/* Gentle staggered reveal, accessible with reduced motion. */
@keyframes aegisCardReveal {{ from {{ opacity: 0; transform: translateY(9px); }} to {{ opacity: 1; transform: translateY(0); }} }}
.aegis-mini-card {{ animation: aegisCardReveal 480ms ease-out both; }}
@media (max-width: 720px) {{
    .aegis-section {{ align-items: flex-start; flex-wrap: wrap; }}
    .aegis-section .aegis-muted {{ flex-basis: 100%; margin-left: 16px; }}
    .aegis-mini-card {{ min-height: 0; }}
}}
@media (prefers-reduced-motion: reduce) {{
    .aegis-mini-card {{ animation: none !important; transform: none !important; }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{ transition: none !important; }}
}}


/* ==========================================
   REFINED CONTRAST — CARD-LED COLOUR, NOT VISUAL NOISE
   ========================================== */
.block-container {{ max-width: 1390px; padding-left: clamp(1rem, 3vw, 2.6rem); padding-right: clamp(1rem, 3vw, 2.6rem); }}
.aegis-hero h1 {{ font-size: clamp(2.45rem, 4.3vw, 3.65rem) !important; letter-spacing: -.045em !important; }}
.aegis-tagline {{ font-size: 1.045rem !important; max-width: 800px; }}
.aegis-eyebrow {{ color: {t["gold"]} !important; font-size: .76rem; }}
.aegis-section-title {{ font-size: 1.36rem; }}
.aegis-section::before {{ height: 22px; width: 5px; flex-basis: 5px; }}
.aegis-mini-card {{ min-height: 143px; border-width: 1.5px; padding: 21px 22px 23px; }}
.aegis-mini-card--gold {{ border-color: {t["gold"]}; }}
.aegis-mini-card--rose {{ border-color: {t["accent"]}; }}
.aegis-mini-card--sage {{ border-color: {t["success"]}; }}
.aegis-mini-card-value {{ font-size: clamp(1.19rem, 1.9vw, 1.53rem); }}
.aegis-mini-card-caption {{ font-size: .96rem !important; line-height: 1.55 !important; }}
.aegis-mini-card-title {{ font-size: .76rem; }}
/* New compact, colour-coded metrics retain actual backend values. */
.aegis-stat {{
   border: 1.5px solid {t["border"]}; border-radius: 18px;
   padding: 20px 22px 19px; min-height: 133px;
   box-shadow: 0 6px 18px rgba(56,24,44,.06);
   transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}}
.aegis-stat:hover {{ transform: translateY(-4px); box-shadow: 0 13px 29px rgba(56,24,44,.13); }}
.aegis-stat--total {{ background: {t["gold_soft"]}; border-color: {t["gold"]}; }}
.aegis-stat--allowed {{ background: {t["sage"]}; border-color: {t["success"]}; }}
.aegis-stat--blocked {{ background: {t["rose"]}; border-color: {t["accent"]}; }}
.aegis-stat-label {{ font-size: .87rem; font-weight: 700; color: {t["text"]}; letter-spacing: .01em; }}
.aegis-stat-value {{ font-size: clamp(2rem,3vw,2.8rem); font-weight: 800; letter-spacing: -.055em; line-height: 1.19; margin-top: 9px; color: {t["text"]}; font-variant-numeric: tabular-nums; }}
.aegis-stat--total .aegis-stat-value {{ color: {t["gold"]}; }}
.aegis-stat--allowed .aegis-stat-value {{ color: {t["success"]}; }}
.aegis-stat--blocked .aegis-stat-value {{ color: {t["accent"]}; }}
/* Richer neutral containers with warm highlights; keep all widgets functional. */
div[data-testid="stVerticalBlockBorderWrapper"] {{ border-width: 1.5px !important; }}
div[data-testid="stVerticalBlockBorderWrapper"] h3 {{ font-size: 1.42rem !important; }}
[data-testid="stCaptionContainer"] p {{ font-size: .91rem !important; }}
[data-testid="stAlert"] {{ border: 1px solid {t["border"]}; }}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{ background: {t["soft"]}; }}
.aegis-footer-panel {{ margin-top: 3.3rem; padding-top: 1.9rem; }}
.aegis-footer-title {{ font-size: 1.14rem; }}
.aegis-footer-panel p {{ font-size: .94rem; line-height: 1.6; }}
@media (max-width: 720px) {{
 .aegis-stat {{ min-height: 104px; padding: 15px; }}
 .aegis-mini-card {{ min-height: 0; }}
 .aegis-hero h1 {{ font-size: 2.25rem !important; }}
}}
@media (prefers-reduced-motion: reduce) {{
 .aegis-stat, .aegis-stat:hover {{ animation: none !important; transition: none !important; transform: none !important; }}
}}


/* ==========================================
   ROYAL RAJASTHANI — SUNSET / MAROON / GOLD
   Traditional-inspired detailing, modern usability.
   ========================================== */
:root {{
    --royal-maroon: {t["accent"]};
    --royal-sunset: {t["terracotta"]};
    --royal-gold: {t["gold"]};
}}
/* Warm sandstone canvas: restrained jharokha-like framing, no busy wallpaper. */
.stApp {{
    background-color: {t["background"]};
    background-image: radial-gradient(circle at 98% 0%, {t["soft"]} 0, transparent 33%);
    background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
    background: {t["surface"]};
    border-right: 2px solid {t["gold"]};
}}
.aegis-sideword, .aegis-wordmark {{ color: {t["accent"]} !important; }}
.aegis-hero {{ border-bottom: 1px solid {t["border"]}; margin-bottom: 20px; }}
.aegis-hero h1 {{ color: {t["text"]} !important; }}
.aegis-eyebrow {{ color: {t["terracotta"]} !important; font-weight: 800; }}
.aegis-section {{ border-bottom-color: {t["border"]}; }}
.aegis-section::before {{
    background: linear-gradient(180deg, {t["terracotta"]}, {t["gold"]});
    border-radius: 3px 3px 0 0;
}}
/* Slender golden bands evoke royal textile trim, not literal motifs. */
.aegis-mini-card, .aegis-stat,
div[data-testid="stVerticalBlockBorderWrapper"] {{
    box-shadow: 0 5px 21px rgba(45, 19, 17, .065);
}}
.aegis-mini-card {{
    border-color: {t["border"]};
    border-top: 3px solid {t["gold"]};
    border-radius: 17px 17px 15px 15px;
}}
.aegis-mini-card::before {{
    background: linear-gradient(90deg, {t["gold"]} 0 55%, {t["terracotta"]} 55%);
}}
.aegis-mini-card--gold, .aegis-stat--total {{
    background: {t["gold_soft"]}; border-color: {t["gold"]};
}}
.aegis-mini-card--rose, .aegis-stat--blocked {{
    background: {t["rose"]}; border-color: {t["danger"]};
}}
.aegis-mini-card--sage, .aegis-stat--allowed {{
    background: {t["sage"]}; border-color: {t["success"]};
}}
.aegis-stat {{ border-top: 4px solid {t["gold"]}; }}
.aegis-stat--blocked {{ border-top-color: {t["danger"]}; }}
.aegis-stat--allowed {{ border-top-color: {t["success"]}; }}
.aegis-stat--total .aegis-stat-value {{ color: {t["accent"]}; }}
.aegis-stat--blocked .aegis-stat-value {{ color: {t["danger"]}; }}
.aegis-mini-card--rose .aegis-mini-card-value {{ color: {t["danger"]}; }}
.aegis-mini-card--gold .aegis-mini-card-value {{ color: {t["accent"]}; }}
.aegis-mini-card-caption {{ color: {t["muted"]} !important; }}
/* Buttons and selected navigation use maroon/orange; gold remains focus affordance. */
div.stButton > button[kind="primary"] {{
    background: {t["accent"]}; border: 1px solid {t["accent"]};
    color: {t["button_text"]};
}}
div.stButton > button[kind="primary"]:hover {{
    background: {t["accent_hover"]}; border-color: {t["gold"]};
}}
div.stButton > button:not([kind="primary"]):hover {{
    color: {t["accent"]}; border-color: {t["gold"]};
}}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {t["accent"]} !important; }}
[data-baseweb="tab-highlight"] {{ background: {t["terracotta"]} !important; }}
.aegis-footer-panel {{ border-top: 2px solid {t["gold"]}; }}
.aegis-footer-panel a {{ color: {t["accent"]} !important; }}
.aegis-footer-panel a:hover {{ color: {t["terracotta"]} !important; }}
/* Animations are decorative only; preserve reduced motion. */
.aegis-mini-card:hover, .aegis-stat:hover {{
    border-color: {t["gold"]};
    box-shadow: 0 14px 28px rgba(55, 22, 18, .13);
}}
@media (prefers-reduced-motion: reduce) {{
    .aegis-mini-card, .aegis-stat {{ animation: none !important; transition: none !important; }}
    .aegis-mini-card:hover, .aegis-stat:hover {{ transform: none !important; }}
}}


/* ============================================================
   ROYAL MOTION PASS — editorial typography + restrained delight
   Existing palette, brand and Streamlit functionality stay intact.
   ============================================================ */
/* AEGIS text in the rotating seal uses the SAME face as the wordmark. */
.aegis-orbit {{
    width: 128px; height: 128px;
    background: radial-gradient(circle at 37% 27%, {t["surface"]}, {t["soft"]});
    box-shadow: 0 8px 26px rgba(65, 22, 26, .12), inset 0 0 0 1px {t["gold"]};
    transition: transform .35s ease, box-shadow .35s ease;
}}
.aegis-orbit span {{
    position: relative; z-index: 2;
    font-family: "Anaktoria", Georgia, serif !important;
    color: {t["accent"]} !important;
    font-size: 1.8rem !important;
    font-weight: 400 !important;
    letter-spacing: -.025em !important;
    line-height: 1;
}}
.aegis-orbit::before {{
    border-width: 3px;
    border-top-color: {t["terracotta"]};
    border-right-color: {t["gold"]};
    animation-duration: 18s;
}}
.aegis-orbit::after {{ border-style: dotted; border-color: {t["gold"]}; opacity: .8; animation-duration: 30s; }}
.aegis-orbit:hover {{ transform: translateY(-3px) scale(1.035); box-shadow: 0 12px 32px rgba(65,22,26,.2); }}
.aegis-orbit:hover::before, .aegis-orbit:hover::after {{ animation-play-state: paused; }}

/* A distinctive royal heading, with a fine gold baseline and reveal. */
.aegis-hero {{ position: relative; isolation: isolate; overflow: visible; }}
.aegis-hero h1 {{
    font-family: Georgia, "Times New Roman", serif !important;
    font-size: clamp(2.55rem, 4.5vw, 4.3rem) !important;
    font-weight: 800 !important;
    letter-spacing: -.045em !important;
    line-height: 1.12 !important;
    text-wrap: balance;
    animation: aegisHeadline .75s cubic-bezier(.16,.82,.2,1) both;
}}
.aegis-hero h1::after {{
    content: ""; display: block; width: min(160px, 30%); height: 4px;
    margin: 16px 0 0; border-radius: 8px;
    background: linear-gradient(90deg, {t["accent"]}, {t["terracotta"]}, {t["gold"]});
    transform-origin: left center;
    animation: aegisDrawLine .9s .35s ease-out both;
}}
.aegis-tagline {{ font-size: 1.04rem !important; line-height: 1.75 !important; max-width: 790px; }}
/* Reusable typing mask: the full text stays in the DOM for accessibility. */
.aegis-hero .aegis-eyebrow {{
    display: table; max-width: 100%;
    overflow: hidden; white-space: nowrap;
    font-family: "SFMono-Regular", Menlo, monospace !important;
    font-weight: 800 !important;
    letter-spacing: .15em;
    border-right: 2px solid {t["gold"]};
    animation: aegisTypeReveal 1.25s steps(26,end) both,
               aegisCaret .55s step-end 3;
}}
@keyframes aegisTypeReveal {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
@keyframes aegisCaret {{ 50% {{ border-right-color: transparent; }} }}
@keyframes aegisHeadline {{ from {{ opacity: 0; transform: translateY(16px); filter: blur(5px); }} to {{ opacity: 1; transform: translateY(0); filter: blur(0); }} }}
@keyframes aegisDrawLine {{ from {{ transform: scaleX(0); opacity: 0; }} to {{ transform: scaleX(1); opacity: 1; }} }}

/* Section labels: high-contrast type, a gold flourish and sweeping underline. */
.aegis-section {{ position: relative; overflow: hidden; padding-bottom: 13px; }}
.aegis-section-title {{
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif !important;
    font-size: clamp(1.25rem, 1.9vw, 1.48rem) !important;
    font-weight: 850 !important; letter-spacing: -.045em !important;
    color: {t["text"]};
}}
.aegis-section-title::after {{
    content: "✦"; display: inline-block; font-family: Georgia, serif;
    font-size: .72em; padding-left: .6em; color: {t["gold"]};
    vertical-align: 3px; transition: transform .3s ease, color .3s ease;
}}
.aegis-section:hover .aegis-section-title::after {{ transform: rotate(75deg) scale(1.15); color: {t["terracotta"]}; }}
.aegis-section::after {{
    content: ""; position: absolute; bottom: 0; left: 0;
    height: 2px; width: 100%; transform: scaleX(0); transform-origin: left;
    background: linear-gradient(90deg,{t["gold"]}, {t["terracotta"]}, transparent);
    transition: transform .6s cubic-bezier(.16,.8,.2,1);
}}
.aegis-section:hover::after {{ transform: scaleX(1); }}
.aegis-section .aegis-muted {{ font-family: "SFMono-Regular", Menlo, monospace !important; font-weight: 650 !important; }}
/* Three font personalities only: Anaktoria brand, serif display, system body. */
.aegis-mini-card-value {{ font-weight: 800 !important; letter-spacing: -.035em; }}
.aegis-mini-card-title {{ font-family: "SFMono-Regular", Menlo, monospace !important; font-weight: 800 !important; }}
.aegis-footer-title {{ font-weight: 850 !important; }}

/* Microinteractions: polished but not constant motion. */
.aegis-mini-card {{ transition: transform .28s cubic-bezier(.2,.8,.2,1), box-shadow .28s ease, border-color .28s ease !important; }}
.aegis-mini-card::before {{ transition: width .35s ease, background .35s ease; }}
.aegis-mini-card:hover::before {{ width: 70px; }}
.aegis-stat {{ animation: aegisCardReveal .55s cubic-bezier(.2,.8,.2,1) both; }}
.aegis-stat--allowed {{ animation-delay: 80ms; }}
.aegis-stat--blocked {{ animation-delay: 150ms; }}
.aegis-stat-value {{ transition: transform .25s ease; }}
.aegis-stat:hover .aegis-stat-value {{ transform: translateY(-2px); }}
div.stButton > button {{ transition: transform .2s ease, background .2s ease, box-shadow .2s ease, border-color .2s ease !important; }}
div.stButton > button:active {{ transform: scale(.98) !important; }}
[data-testid="stAlert"] {{ animation: aegisMessageIn .4s ease both; }}
@keyframes aegisMessageIn {{ from {{ opacity: 0; transform: translateY(7px); }} to {{ opacity: 1; transform: translateY(0); }} }}
button[data-baseweb="tab"] {{ transition: color .2s ease, background-color .2s ease !important; }}
button[data-baseweb="tab"]:hover {{ background: {t["soft"]} !important; }}

@media (max-width: 720px) {{
    .aegis-hero h1 {{ font-size: clamp(2.1rem, 8vw, 3rem) !important; }}
    .aegis-orbit {{ width: 105px; height: 105px; }}
    .aegis-orbit span {{ font-size: 1.45rem !important; }}
    .aegis-section-title::after {{ padding-left: .3em; }}
}}
@media (prefers-reduced-motion: reduce) {{
    .aegis-hero h1, .aegis-hero h1::after, .aegis-hero .aegis-eyebrow,
    .aegis-stat, [data-testid="stAlert"] {{ animation: none !important; filter: none !important; clip-path: none !important; }}
    .aegis-hero .aegis-eyebrow {{ border-right: none !important; }}
    .aegis-section::after {{ display: none !important; }}
    .aegis-orbit, .aegis-mini-card, .aegis-stat-value,
    .aegis-section-title::after {{ transition: none !important; transform: none !important; }}
    .aegis-orbit:hover {{ transform: none !important; }}
}}



/* ============================================================
   ROYAL MOTION REFINEMENT — serif microcopy, looping typing,
   and consistent hover affordances across every dashboard page.
   ============================================================ */
/* Keep the large hero headline and Anaktoria wordmark unchanged. */
.aegis-hero .aegis-eyebrow,
.aegis-hero .aegis-tagline {{
    font-family: "Times New Roman", Times, serif !important;
}}
.aegis-hero .aegis-eyebrow {{
    display: inline-block;
    width: max-content;
    max-width: 100%;
    font-size: clamp(.86rem, 1.3vw, 1rem) !important;
    font-weight: 700 !important;
    letter-spacing: .14em;
    line-height: 1.4;
    white-space: nowrap;
    overflow: hidden;
    border-right: 2px solid {t["gold"]};
    /* 6.8 second loop: type, pause, erase, then restart. */
    animation: aegisRoyalType 6.8s steps(24, end) infinite,
               aegisRoyalCaret .68s step-end infinite !important;
}}
.aegis-hero .aegis-tagline {{
    font-size: clamp(1.07rem, 1.5vw, 1.2rem) !important;
    font-weight: 500 !important;
    line-height: 1.65 !important;
    letter-spacing: .005em !important;
}}
@keyframes aegisRoyalType {{
    0%, 3%   {{ clip-path: inset(0 100% 0 0); }}
    23%, 76% {{ clip-path: inset(0 0 0 0); }}
    93%, 100% {{ clip-path: inset(0 100% 0 0); }}
}}
@keyframes aegisRoyalCaret {{
    0%, 49% {{ border-right-color: {t["gold"]}; }}
    50%, 100% {{ border-right-color: transparent; }}
}}

/* Same gold-edged lift applied to every card, including Streamlit
   bordered containers used in the playground, tickets and logs. */
.aegis-mini-card,
.aegis-stat,
div[data-testid="stMetric"],
div[data-testid="stVerticalBlockBorderWrapper"] {{
    transition: transform 260ms cubic-bezier(.2,.8,.2,1),
                border-color 260ms ease,
                box-shadow 260ms ease,
                background-color 260ms ease !important;
    transform-origin: center top;
}}
.aegis-mini-card:hover,
.aegis-stat:hover,
div[data-testid="stMetric"]:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: translateY(-4px) !important;
    border-color: {t["gold"]} !important;
    box-shadow: 0 15px 31px rgba(70, 28, 22, .20),
                0 0 0 1px {t["gold"]} !important;
}}
/* Panels also gain a quiet decorative glint while hovered. */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    position: relative;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:hover h3 {{
    color: {t["terracotta"]} !important;
    transition: color 260ms ease;
}}
/* Keyboard users see an equally visible focus treatment. */
div[data-testid="stVerticalBlockBorderWrapper"]:focus-within {{
    border-color: {t["gold"]} !important;
}}
@media (prefers-reduced-motion: reduce) {{
    .aegis-hero .aegis-eyebrow {{
        animation: none !important;
        clip-path: none !important;
        border-right: 0 !important;
    }}
    .aegis-mini-card, .aegis-stat,
    div[data-testid="stMetric"],
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        transition: none !important;
    }}
    .aegis-mini-card:hover, .aegis-stat:hover,
    div[data-testid="stMetric"]:hover,
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: none !important;
        box-shadow: none !important;
    }}
}}


/* ============================================================
   TIMES NEW ROMAN — ANALYTICS AND TICKET EXPLORER
   This stylesheet is inside a Python f-string: doubled CSS
   braces are intentional and required.
   ============================================================ */

/* AEGIS uses custom HTML metric cards, not only st.metric. */
.aegis-stat-label,
.aegis-stat-value,
.aegis-stat-label *,
.aegis-stat-value *,
div[data-testid="stMetric"] *,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {{
    font-family: "Times New Roman", Times, serif !important;
}}

.aegis-stat-label,
[data-testid="stMetricLabel"] * {{
    font-size: 1.16rem !important;
    font-weight: 700 !important;
    letter-spacing: .005em !important;
}}

.aegis-stat-value,
[data-testid="stMetricValue"] * {{
    font-size: clamp(2.6rem, 3.6vw, 3.45rem) !important;
    font-weight: 700 !important;
    letter-spacing: -.025em !important;
    line-height: 1.08 !important;
}}

/* Search/filter controls and ticket details inside bordered panels. */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stTextInput"] input,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stWidgetLabel"] {{
    font-family: "Times New Roman", Times, serif !important;
}}

/* Dataframe uses a canvas in many Streamlit releases. These
   variables target the grid font where supported by its renderer. */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] *,
[data-testid="stTable"],
[data-testid="stTable"] * {{
    font-family: "Times New Roman", Times, serif !important;
    --gdg-font-family: "Times New Roman", Times, serif;
    --gdg-header-font-family: "Times New Roman", Times, serif;
    --gdg-editor-font-family: "Times New Roman", Times, serif;
}}

[data-testid="stDataFrame"] {{
    --gdg-font-size: 15px;
}}


/* Royal footer — scoped to the footer's Streamlit keyed container only. */
.st-key-aegis_footer {{
    background: linear-gradient(125deg, #531424 0%, #801D32 55%, #9D412C 100%) !important;
    border: 1px solid #D69B4A !important;
    border-top: 4px solid #F6C76B !important;
    border-radius: 24px !important;
    margin-top: 3rem !important;
    padding: 1.6rem 1.8rem 1.35rem !important;
    box-shadow: 0 15px 36px rgba(60, 21, 21, .16) !important;
    overflow: hidden;
}}
.st-key-aegis_footer, .st-key-aegis_footer p,
.st-key-aegis_footer [data-testid="stCaptionContainer"] p {{
    color: #FFE9CA !important;
}}
.st-key-aegis_footer .aegis-sideword {{
    color: #F6C76B !important;
}}
.st-key-aegis_footer .aegis-footer-panel {{
    display: none !important;
}}
.st-key-aegis_footer a {{
    color: #FFD17D !important;
    text-decoration-color: #FFD17D !important;
    text-underline-offset: 4px;
    transition: color .25s ease, text-shadow .25s ease;
}}
.st-key-aegis_footer a:hover {{
    color: #FFFFFF !important;
    text-shadow: 0 0 10px rgba(255, 210, 115, .55);
}}
/* Old-school typewriter signature — ink on warm archival paper. */
.st-key-aegis_footer .aegis-footer-title {{
    display: inline-block;
    box-sizing: content-box;
    position: relative;
    max-width: 100%;
    width: 0;
    overflow: hidden;
    white-space: nowrap;
    vertical-align: bottom;
    padding: 0 0 .08em;
    border-right: 3px solid #F6C76B;
    font-family: "Times New Roman", Times, serif !important;
    font-weight: 800 !important;
    font-size: clamp(1.12rem, 2.15vw, 1.92rem) !important;
    color: #FFE5AC !important;
    line-height: 1.35 !important;
    letter-spacing: .035em !important;
    text-shadow: 1px 2px 0 #381621, 0 0 12px rgba(246,199,107,.12);
    animation: aegisSignatureType 7.5s steps(24, end) infinite,
               aegisSignatureCaret .72s step-end infinite;
}}
/* A restrained vintage stationery underline gives the signature personality. */
.st-key-aegis_footer .aegis-footer-title + p {{
    margin-top: .8rem;
    border-top: 1px dashed rgba(255,226,160,.38);
    padding-top: .8rem;
    letter-spacing: .025em;
}}
@keyframes aegisSignatureType {{
    0%, 6% {{ width: 0; }}
    43%, 80% {{ width: 27ch; }}
    96%, 100% {{ width: 0; }}
}}
@keyframes aegisSignatureCaret {{
    50% {{ border-right-color: transparent; }}
}}
/* Pixel-art stack: large, cute rectangular bricks with stepped corners. */
.aegis-footer-blocks {{
    width: min(100%, 270px);
    min-height: 250px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    gap: 9px;
    margin: 0 auto;
    padding: 12px 10px 16px;
    position: relative;
    isolation: isolate;
}}
.aegis-footer-block {{
    --tile: #FFE4A5;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    position: relative;
    isolation: isolate;
    height: 48px;
    width: 100%;
    background: var(--tile);
    color: #34181D;
    border: 0;
    border-radius: 0;
    clip-path: polygon(8px 0, calc(100% - 8px) 0, calc(100% - 8px) 4px, calc(100% - 4px) 4px, calc(100% - 4px) 8px, 100% 8px, 100% calc(100% - 8px), calc(100% - 4px) calc(100% - 8px), calc(100% - 4px) calc(100% - 4px), calc(100% - 8px) calc(100% - 4px), calc(100% - 8px) 100%, 8px 100%, 8px calc(100% - 4px), 4px calc(100% - 4px), 4px calc(100% - 8px), 0 calc(100% - 8px), 0 8px, 4px 8px, 4px 4px, 8px 4px);
    font-family: "Times New Roman", Times, serif !important;
    font-size: clamp(1.03rem, 1.4vw, 1.2rem);
    font-weight: 700;
    letter-spacing: .035em;
    text-shadow: 1px 1px 0 rgba(255,255,255,.28);
    opacity: 0;
    transform: translateY(-55px);
    animation: aegisPixelStack 9s steps(6,end) infinite;
    will-change: transform, opacity;
}}
/* Pixel outlines and crisp inset highlights (no gradients or round corners). */
.aegis-footer-block::before {{
    content: "";
    position: absolute;
    inset: 4px;
    border-top: 3px solid rgba(255,255,255,.58);
    border-left: 3px solid rgba(255,255,255,.35);
    border-right: 4px solid rgba(58,19,24,.25);
    border-bottom: 4px solid rgba(58,19,24,.34);
    z-index: -1;
    pointer-events: none;
}}
.aegis-footer-block::after {{
    content: "";
    width: 7px;
    height: 7px;
    position: absolute;
    top: 11px;
    right: 14px;
    background: rgba(255,255,255,.67);
    box-shadow: -7px 7px 0 rgba(255,255,255,.25), 7px 7px 0 rgba(71,28,31,.13);
    pointer-events: none;
}}
.aegis-footer-block:nth-child(1) {{
    --tile: #FFE4A5;
    font-family: "Anaktoria", Georgia, serif !important;
    font-size: 1.75rem;
    animation-delay: 0s;
}}
.aegis-footer-block:nth-child(2) {{ --tile: #F6C76B; animation-delay: .46s; }}
.aegis-footer-block:nth-child(3) {{ --tile: #E97746; animation-delay: .92s; }}
.aegis-footer-block:nth-child(4) {{ --tile: #F5B0A0; animation-delay: 1.38s; }}
@keyframes aegisPixelStack {{
    0%, 5% {{ opacity: 0; transform: translateY(-55px); }}
    11% {{ opacity: 1; transform: translateY(8px); }}
    15%, 78% {{ opacity: 1; transform: translateY(0); }}
    89%, 100% {{ opacity: 0; transform: translateY(12px); }}
}}
@media (max-width: 760px) {{
    .st-key-aegis_footer {{ padding: 1rem !important; }}
    .aegis-footer-blocks {{ width: min(100%, 250px); min-height: 236px; }}
    .aegis-footer-block {{ height: 44px; font-size: 1.03rem; }}
}}
@media (prefers-reduced-motion: reduce) {{
    .st-key-aegis_footer .aegis-footer-title,
    .aegis-footer-block {{ animation: none !important; }}
    .st-key-aegis_footer .aegis-footer-title {{ width: auto !important; border-right: 0 !important; }}
    .aegis-footer-block {{ opacity: 1 !important; transform: none !important; }}
}}

</style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 4. SHARED FOOTER — CALL ONCE AFTER PAGE ROUTING
# ==========================================

def show_aegis_footer():
    """Royal, accessible footer shared by all four dashboard pages."""
    from pathlib import Path

    # Scoped Streamlit container allows the entire footer to have its own
    # background rather than styling only a free-standing HTML divider.
    with st.container(key="aegis_footer"):
        brand, details, ornament = st.columns([1, 2.5, 1.6], gap="medium")
        with brand:
            logo_path = Path(__file__).resolve().parents[1] / "assets" / "aegis-mark.png"
            if logo_path.exists():
                st.image(str(logo_path), width=64)
            st.markdown('<div class="aegis-sideword">aegis.</div>', unsafe_allow_html=True)
        with details:
            st.markdown(
                '<div class="aegis-footer-title">Developed by Rishika Roy</div>'
                '<p>AI action governance · Independent authorization · Responsible AI</p>'
                '<p><a href="mailto:rishika24.roy@gmail.com">rishika24.roy@gmail.com</a>'
                ' &nbsp;·&nbsp; '
                '<a href="https://github.com/rishikaroy24" target="_blank" '
                'rel="noopener noreferrer">GitHub</a></p>',
                unsafe_allow_html=True,
            )
            st.caption("AEGIS · Local security demonstration")
        with ornament:
            st.markdown(
                '<div class="aegis-footer-blocks" aria-label="AEGIS: Automated Security Agent">'
                '<span class="aegis-footer-block">aegis.</span>'
                '<span class="aegis-footer-block">Automated</span>'
                '<span class="aegis-footer-block">Security</span>'
                '<span class="aegis-footer-block">Agent</span>'
                '</div>',
                unsafe_allow_html=True,
            )

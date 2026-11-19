
import streamlit as st

THEMES = {
    "Light": {
        "background": "#FFF9FB",
        "surface": "#FFFFFF",
        "soft": "#FCE7F3",
        "border": "#F2DCE7",
        "text": "#4A1837",
        "muted": "#896C7E",
        "accent": "#BE185D",
        "accent_hover": "#9D174D",
        "button_text": "#FFFFFF",
    },
    "Dark": {
        "background": "#21131E",
        "surface": "#30202C",
        "soft": "#3A2335",
        "border": "#513A49",
        "text": "#FFF1F7",
        "muted": "#C8A8BC",
        "accent": "#F9A8D4",
        "accent_hover": "#FBCFE8",
        "button_text": "#21131E",
    },
}


def apply_theme(mode):
    theme = THEMES[mode]

    st.markdown(
        f"""
        <style>
        /* Main application */
        .stApp {{
            background-color: {theme["background"]};
            color: {theme["text"]};
        }}

        [data-testid="stHeader"] {{
            background-color: {theme["background"]};
        }}

        .block-container {{
            max-width: 1250px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: {theme["text"]};
            letter-spacing: -0.5px;
        }}

        /* Dashboard metrics */
        div[data-testid="stMetric"] {{
            background: {theme["surface"]};
            border: 1px solid {theme["border"]};
            border-radius: 14px;
            padding: 18px;
        }}

        div[data-testid="stMetricValue"] {{
            color: {theme["text"]};
        }}

        /* Buttons */
        div.stButton > button {{
            border-radius: 10px;
            border: 1px solid {theme["border"]};
            background: {theme["surface"]};
            color: {theme["text"]};
            font-weight: 500;
        }}

        div.stButton > button:hover {{
            border-color: {theme["accent"]};
            color: {theme["accent"]};
        }}

        div.stButton > button[kind="primary"] {{
            background: {theme["accent"]};
            border-color: {theme["accent"]};
            color: {theme["button_text"]};
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {theme["surface"]};
            border-right: 1px solid {theme["border"]};
        }}
        
        
        /* Sidebar background */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div {{
            background-color: {theme["surface"]};
        }}

        /* Sidebar headings, labels and radio text */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] [role="radiogroup"] p {{
            color: {theme["text"]} !important;
            opacity: 1 !important;
        }}

        /* Metric labels */
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {{
            color: {theme["muted"]} !important;
            opacity: 1 !important;
        }}

        

        


        /* Dividers */
        hr {{
            border-color: {theme["border"]};
            opacity: 0.6;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

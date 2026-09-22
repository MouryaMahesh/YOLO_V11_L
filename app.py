import os
import tempfile
import uuid
from pathlib import Path

import cv2
import streamlit as st
from PIL import Image
from ultralytics import YOLO

st.set_page_config(
    page_title="AI Smart Waste Detection",
    page_icon="♻️",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_CANDIDATES = [
    BASE_DIR / "Model" / "best.pt",
    BASE_DIR / "model" / "best.pt",
    BASE_DIR / "best.pt",
]


def resolve_model_path():
    for candidate in MODEL_CANDIDATES:
        if candidate.exists():
            return str(candidate)
    return str(MODEL_CANDIDATES[0])


@st.cache_resource
def load_model():
    model_path = resolve_model_path()
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return YOLO(model_path)


def get_theme_css(theme_name):
    if theme_name == "Light":
        bg_top = "#eef7f5"
        bg_bottom = "#dfeeea"
        panel = "rgba(255,255,255,0.78)"
        panel_strong = "rgba(255,255,255,0.92)"
        sidebar_bg = "rgba(240,245,243,0.96)"
        border = "rgba(16, 76, 62, 0.14)"
        text = "#162b2b"
        muted = "#4d6463"
        green = "#14b37c"
        hero = "linear-gradient(135deg, rgba(230,255,247,0.96), rgba(209,243,234,0.9))"
        card = "rgba(255,255,255,0.72)"
        input_bg = "rgba(255,255,255,0.92)"
        pill_bg = "rgba(255,255,255,0.7)"
    else:
        bg_top = "#030d12"
        bg_bottom = "#07151d"
        panel = "rgba(10, 23, 31, 0.9)"
        panel_strong = "rgba(15, 29, 37, 0.82)"
        sidebar_bg = "rgba(6, 15, 19, 0.94)"
        border = "rgba(79, 197, 164, 0.25)"
        text = "#edf7f3"
        muted = "#a9c5bf"
        green = "#39d0a4"
        hero = "linear-gradient(135deg, rgba(10, 32, 30, 0.9), rgba(9, 26, 31, 0.9))"
        card = "rgba(15, 33, 39, 0.88)"
        input_bg = "rgba(12, 27, 34, 0.9)"
        pill_bg = "rgba(255,255,255,0.06)"

    return f"""
    <style>
    :root {{
        --bg-top: {bg_top};
        --bg-bottom: {bg_bottom};
        --panel: {panel};
        --panel-strong: {panel_strong};
        --sidebar-bg: {sidebar_bg};
        --border: {border};
        --text: {text};
        --muted: {muted};
        --green: {green};
        --hero: {hero};
        --card: {card};
        --input-bg: {input_bg};
        --pill-bg: {pill_bg};
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
        color: var(--text);
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1500px !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }}

    .stApp {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00));
    }}

    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg);
        border-right: 1px solid var(--border);
        width: 330px !important;
        min-width: 330px !important;
    }}

    .sidebar-section {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 0.9rem;
        box-shadow: 0 18px 27px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }}

    .sidebar-title {{
        font-size: 0.8rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 700;
        margin-bottom: 0.8rem;
    }}

    .stInfo {{
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}

    .stInfo > div {{
        white-space: nowrap !important;
    }}

    .stRadio label, .stRadio div[data-testid="stVerticalBlock"] {{
        white-space: nowrap !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }}

    .stSlider {{
        margin-top: 0.25rem !important;
    }}

    [data-testid="stSliderThumbValue"] {{
        white-space: nowrap !important;
    }}

    .dashboard-card {{
        background: var(--panel-strong);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 18px 30px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }}

    .hero-card {{
        background: var(--hero);
        border: 1px solid rgba(85, 244, 194, 0.3);
        border-radius: 22px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 16px 36px rgba(6, 16, 22, 0.2);
    }}

    h1 {{
        font-size: clamp(2rem, 2.7vw, 3.1rem) !important;
        line-height: 1.12 !important;
        letter-spacing: -0.04em !important;
        color: var(--text) !important;
        margin-bottom: 0.3rem !important;
    }}

    .subtitle {{
        color: var(--muted);
        font-size: 1rem;
        margin-top: 0.3rem;
    }}

    .pill-row {{
        display: flex;
        flex-wrap: nowrap;
        gap: 0.6rem;
        margin-top: 1rem;
        overflow: hidden;
    }}

    .pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: var(--pill-bg);
        color: var(--text);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        white-space: nowrap;
    }}

    .pill.green {{
        background: rgba(57, 208, 164, 0.15);
        border-color: rgba(57, 208, 164, 0.35);
        color: var(--text);
    }}

    .primary-button > button {{
        background: linear-gradient(135deg, #29d7ab, #12b87d) !important;
        color: #032215 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.2rem !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 25px rgba(18, 184, 125, 0.35) !important;
        width: 100% !important;
    }}

    .primary-button > button:hover {{
        background: linear-gradient(135deg, #34e0b0, #1cc889) !important;
        transform: translateY(-1px) !important;
    }}

    button[kind="secondary"], div[data-testid="stFileUploaderDropzone"] {{
        background: var(--input-bg) !important;
        border-color: rgba(118, 178, 206, 0.45) !important;
        border-width: 1.5px !important;
        border-style: dashed !important;
        border-radius: 16px !important;
        min-height: 80px !important;
        padding: 1rem !important;
        width: 100% !important;
    }}

    [data-testid="stFileUploaderDropzoneHover"] {{
        border-color: rgba(57, 208, 164, 0.7) !important;
        background: rgba(18, 36, 35, 0.85) !important;
    }}

    div[data-testid="stFileUploader"] {{
        width: 100% !important;
    }}

    [data-baseweb="base-input"], .stSelectbox > div, .stSlider > div {{
        background: var(--input-bg) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
    }}

    .metric-box {{
        background: var(--panel-strong);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        min-height: 86px;
    }}

    .metric-label {{
        color: var(--muted);
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .metric-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text);
        margin-top: 0.35rem;
    }}

    .result-box {{
        background: var(--card);
        border: 1px solid rgba(57, 208, 164, 0.25);
        border-radius: 18px;
        padding: 0.8rem;
    }}

    .stAlert {{
        border-radius: 12px !important;
        border: 1px solid rgba(255, 183, 77, 0.25) !important;
        background: rgba(98, 72, 29, 0.18) !important;
    }}
    </style>
    """


if "theme" not in st.session_state:
    st.session_state.theme = "Light"

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero-card">
        <div style="display:flex; justify-content:space-between; align-items:center; gap: 1rem; flex-wrap:wrap;">
            <div>
                <div class='pill green'>♻️ WasteVision AI</div>
                <h1>YOLO11L Waste Detection</h1>
                <div class='subtitle'>Multi-class waste detection with precision-driven visual analysis on the combined dataset.</div>
            </div>
            <div class='pill'>● Model ready</div>
        </div>
        <div class='pill-row'>
            <div class='pill'>Precision: 0.95</div>
            <div class='pill'>YOLO11L</div>
            <div class='pill green'>Multiple dataset</div>
            <div class='pill'>Batch upload enabled</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Configuration</div>', unsafe_allow_html=True)
    st.markdown("<div style='color:#dfeff8; font-size: 1rem; margin-bottom: 0.5rem;'>Detection dataset</div>", unsafe_allow_html=True)
    st.info("Multiple dataset")

    st.session_state.theme = st.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Detection Settings</div>', unsafe_allow_html=True)
    conf = st.slider("Confidence threshold", min_value=0.1, max_value=0.95, value=st.session_state.get("conf_threshold", 0.5), step=0.01)
    st.session_state.conf_threshold = conf
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Validation results</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="metric-box"><div class="metric-label">Dataset</div><div class="metric-value">Multi</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="metric-box"><div class="metric-label">Precision</div><div class="metric-value">95.0</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="metric-box"><div class="metric-label">mAP50</div><div class="metric-value">41.9</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Training Hyperparameters</div>', unsafe_allow_html=True)
    st.table({"HYPERPARAMETER": ["Model", "Dataset"], "VALUE": ["YOLO11L", "Multiple dataset"]})
    st.markdown('</div>', unsafe_allow_html=True)

model = load_model()

uploaded_files = st.file_uploader(
    "Upload images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    help="Drag and drop images here or click to browse. Supported formats: JPG, JPEG, PNG",
    label_visibility="collapsed",
)

if uploaded_files:
    if "detections" not in st.session_state:
        st.session_state.detections = {}
    if "run_detection" not in st.session_state:
        st.session_state.run_detection = False
    if "last_conf_threshold" not in st.session_state:
        st.session_state.last_conf_threshold = conf

    uploaded_names = [f.name for f in uploaded_files]
    if "last_uploaded_files" not in st.session_state or st.session_state.last_uploaded_files != uploaded_names:
        st.session_state.detections = {}
        st.session_state.last_uploaded_files = uploaded_names
        st.session_state.run_detection = False

    if st.session_state.last_conf_threshold != conf:
        st.session_state.detections = {}
        st.session_state.last_conf_threshold = conf
        st.session_state.run_detection = True

    detect_button = st.button("Detect Waste", use_container_width=True, type="primary")
    if detect_button:
        st.session_state.run_detection = True

    tabs = st.tabs([f"{file.name}" for file in uploaded_files])

    for idx, uploaded_file in enumerate(uploaded_files):
        with tabs[idx]:
            image = Image.open(uploaded_file).convert("RGB")
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown('<div class="result-box"><h3 style="margin:0 0 0.8rem 0;">Uploaded Image</h3></div>', unsafe_allow_html=True)
                st.image(image, use_container_width=True)

            if st.session_state.run_detection or uploaded_file.name in st.session_state.detections:
                if uploaded_file.name not in st.session_state.detections:
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        temp_path = BASE_DIR / f"tmp_{uuid.uuid4().hex}.jpg"
                        image.save(temp_path)
                        try:
                            results = model.predict(source=str(temp_path), conf=conf, save=False)
                        finally:
                            if temp_path.exists():
                                temp_path.unlink()

                        result = results[0]
                        plotted = result.plot()
                        plotted = cv2.cvtColor(plotted, cv2.COLOR_BGR2RGB)

                        boxes = []
                        if result.boxes is not None:
                            for box in result.boxes:
                                cls = int(box.cls)
                                conf_score = float(box.conf)
                                boxes.append((cls, conf_score))

                        st.session_state.detections[uploaded_file.name] = {
                            "plotted": plotted,
                            "boxes": boxes,
                        }

                det = st.session_state.detections[uploaded_file.name]

                with col_right:
                    st.markdown('<div class="result-box"><h3 style="margin:0 0 0.8rem 0;">Detection Result</h3></div>', unsafe_allow_html=True)
                    st.image(det["plotted"], use_container_width=True)

                    if not det["boxes"]:
                        st.warning("No waste objects detected in this image.")
                    else:
                        st.markdown("### Detected objects")
                        for cls_idx, conf_score in det["boxes"]:
                            label = model.names.get(cls_idx, f"Class {cls_idx}")
                            st.write(f"✅ {label} — confidence: {conf_score:.2f}")
else:
    st.markdown(
        """
        <div class="dashboard-card" style="text-align:center; padding: 2rem 1rem;">
            <h3 style="margin-bottom: 0.5rem;">No images uploaded yet</h3>
            <p style="color: #a9c5bf; margin: 0;">Select one or more images to begin object detection.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("Prepared for waste classification tasks with YOLO-based detection.")

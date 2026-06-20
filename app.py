import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Car Sale Price Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM STYLES
# Design: dealership dashboard — charcoal body, steel-blue
# section headers, amber accent reserved for the price readout.
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    :root {
        --ink:        #1A1D23;
        --steel:      #2E5266;
        --steel-dark: #1F3A47;
        --amber:      #E8A33D;
        --paper:      #F7F5F2;
        --slate:      #6B7280;
        --line:       #E3E0D8;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background: var(--paper);
    }

    /* Hide default Streamlit chrome */
    #MainMenu, header[data-testid="stHeader"] {
        background: transparent;
    }
    footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 980px;
    }

    /* ---------- Hero ---------- */
    .hero {
        background: linear-gradient(135deg, var(--ink) 0%, var(--steel-dark) 100%);
        border-radius: 18px;
        padding: 2.6rem 2.4rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: "";
        position: absolute;
        top: -40px; right: -40px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(232,163,61,0.18), transparent 70%);
    }
    .hero-eyebrow {
        color: var(--amber);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin: 0 0 0.5rem 0;
    }
    .hero-title {
        color: var(--paper);
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 0.55rem 0;
        line-height: 1.15;
    }
    .hero-sub {
        color: #B9C4CB;
        font-size: 0.98rem;
        margin: 0;
        max-width: 560px;
        line-height: 1.5;
    }

    /* ---------- Section cards ---------- */
    .section-card {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.6rem 1.8rem 0.4rem 1.8rem;
        margin-bottom: 1.4rem;
    }
    .section-head {
        display: flex;
        align-items: baseline;
        gap: 0.55rem;
        margin-bottom: 1.1rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid var(--line);
    }
    .section-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--amber);
        background: var(--ink);
        padding: 0.12rem 0.5rem;
        border-radius: 5px;
        letter-spacing: 0.04em;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--ink);
        letter-spacing: -0.01em;
    }
    .section-caption {
        font-size: 0.84rem;
        color: var(--slate);
        margin: -0.6rem 0 1rem 0;
    }

    /* ---------- Form field labels ---------- */
    label, .stSelectbox label, .stNumberInput label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: var(--ink) !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput input {
        border-radius: 9px !important;
        border-color: var(--line) !important;
    }

    .stNumberInput input {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* ---------- Predict button ---------- */
    div.stButton > button {
        width: 100%;
        background: var(--ink);
        color: var(--paper);
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.02em;
        padding: 0.85rem 0;
        border-radius: 11px;
        border: none;
        margin-top: 0.6rem;
        transition: all 0.15s ease;
    }
    div.stButton > button:hover {
        background: var(--steel-dark);
        color: var(--amber);
        transform: translateY(-1px);
    }

    /* ---------- Result price tag ---------- */
    .price-tag {
        background: var(--ink);
        border-radius: 16px;
        padding: 1.9rem 2rem;
        margin-top: 1.6rem;
        text-align: center;
        position: relative;
        border: 1px solid var(--steel-dark);
    }
    .price-tag-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #9DAAB0;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        margin-bottom: 0.5rem;
    }
    .price-tag-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.6rem;
        font-weight: 700;
        color: var(--amber);
        letter-spacing: -0.01em;
        border-bottom: 3px solid var(--amber);
        display: inline-block;
        padding-bottom: 0.2rem;
    }

    /* ---------- Expander (raw input view) ---------- */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: var(--slate) !important;
    }

    /* ---------- Divider dots in hero ---------- */
    .hero-meta {
        display: flex;
        gap: 1.4rem;
        margin-top: 1.1rem;
    }
    .hero-meta span {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #8FA0A8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LOAD MODEL ARTIFACTS  (unchanged)
# ============================================================
@st.cache_resource
def load_artifacts():
    model = pickle.load(open("Car_sale_price_model.pkl", "rb"))
    ct = pickle.load(open("ct.pkl", "rb"))
    num_imputer = pickle.load(open("num_imputer.pkl", "rb"))
    cat_imputer = pickle.load(open("cat_imputer.pkl", "rb"))

    return model, ct, num_imputer, cat_imputer

model, ct, num_imputer, cat_imputer = load_artifacts()
current_year = datetime.now().year

# ============================================================
# HERO
# ============================================================
st.markdown(
    f"""
    <div class="hero">
        <p class="hero-eyebrow">Resale Valuation Engine</p>
        <p class="hero-title">🚗 Car Sale Price Prediction</p>
        <p class="hero-sub">
            Estimate the resale value of a used car from its specifications,
            usage history, and condition — built on listings data across India.
        </p>
        <div class="hero-meta">
            <span>● MODEL: RANDOM FOREST REGRESSOR</span>
            <span>● COVERAGE: 13 CITIES</span>
            <span>● AS OF: {current_year}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SECTION 1 — VEHICLE IDENTITY
# ============================================================
st.markdown(
    """
    <div class="section-card">
        <div class="section-head">
            <span class="section-num">01</span>
            <span class="section-title">Vehicle Identity</span>
        </div>
        <p class="section-caption">Tell us exactly which car you're valuing.</p>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    make = st.selectbox(
        "Make",
        sorted(['audi', 'bmw', 'chevrolet', 'datsun', 'fiat', 'ford', 'honda', 'hyundai', 'isuzu', 'jaguar', 'jeep', 'kia', 'mahindra', 'mahindra renault', 'maruti', 'mercedes benz', 'mg', 'mitsubishi', 'nissan', 'opel', 'renault', 'skoda', 'ssangyong', 'tata', 'toyota', 'volkswagen', 'volvo']
        )
    )
with col2:
    model_name = st.selectbox(
        "Model",
        sorted(['3 series', '5 series', '800', 'a class', 'a star', 'a3', 'a4', 'a6', 'accent', 'accord', 'alto', 'alto 800', 'alto k10', 'amaze', 'ameo', 'aria', 'astra', 'aura', 'aveo u va', 'b class', 'baleno', 'beat', 'bolero', 'bolt', 'br-v', 'brio', 'c class', 'camry', 'captur', 'celerio', 'celerio x', 'ciaz', 'city', 'city zx', 'civic', 'cla class', 'cls class', 'compass', 'corolla', 'corolla altis', 'creta', 'cross polo', 'cruze', 'crv', 'd-max v cross', 'duster', 'dzire', 'e 20', 'e class', 'ecosport', 'eeco', 'elite i20', 'enjoy', 'eon', 'ertiga', 'esteem', 'etios', 'etios liva', 'evalia', 'fabia', 'fiesta', 'fiesta classic', 'figo', 'figo aspire', 'fluence', 'fortuner', 'freestyle', 'getz prime', 'gla class', 'glanza', 'go', 'go plus', 'grand i10', 'grand i10 nios', 'grand punto', 'harrier', 'hector', 'hexa', 'i10', 'i20', 'i20 active', 'ignis', 'ikon', 'indica ev2', 'indica v2', 'indica vista', 'indigo cs', 'indigo ecs', 'innova', 'innova crysta', 'jazz', 'jetta', 'kicks', 'kuv100', 'kwid', 'laura', 'linea', 'lodgy', 'logan', 'manza', 'marazzo', 'maxximo ', 'micra', 'micra active', 'ml class', 'mobilio', 'mu-7', 'nano', 'new  wagon-r', 'new elantra', 'new figo', 'new santro', 'nexon ', 'nuvosport', 'octavia', 'omni', 'omni e', 'optra', 'optra magnum', 'outlander', 'passat', 'polo', 'prius', 'pulse', 'punto evo', 'punto pure ', 'q3', 'quanto', 'rapid', 'redi go', 'reva', 'rexton', 'ritz', 's cross', 's presso', 's60', 'safari', 'safari storme', 'sail uva', 'santa fe', 'santro', 'santro xing', 'scala', 'scorpio', 'seltos', 'sonata transform', 'spark', 'sumo gold', 'sunny', 'superb', 'swift', 'swift dzire', 'sx4', 'terrano', 'thar', 'tiago', 'tigor', 'triber', 'tucson new', 'tuv300', 'vento', 'venue', 'verito', 'verna', 'vitara brezza', 'wagon r', 'wagon r 1.0', 'wagon r duo', 'wagon r stingray', 'wr-v', 'x1', 'x3', 'xc60', 'xcent', 'xj l', 'xl6', 'xuv 3oo', 'xuv500', 'xylo', 'yaris', 'yeti', 'zen', 'zen estilo', 'zest', 'zs ev']
        )
    )

car_name = st.selectbox(
    "Car Name",
    sorted(['audi a3', 'audi a4', 'audi a6', 'audi q3', 'bmw 3 series', 'bmw 5 series', 'bmw x1', 'bmw x3', 'chevrolet aveo u va', 'chevrolet beat', 'chevrolet cruze', 'chevrolet enjoy', 'chevrolet optra', 'chevrolet optra magnum', 'chevrolet sail uva', 'chevrolet spark', 'datsun go', 'datsun go plus', 'datsun redi go', 'fiat grand punto', 'fiat linea', 'fiat punto evo', 'fiat punto pure', 'ford ecosport', 'ford fiesta', 'ford fiesta classic', 'ford figo', 'ford figo aspire', 'ford freestyle', 'ford ikon', 'ford new figo', 'honda accord', 'honda amaze', 'honda br-v', 'honda brio', 'honda city', 'honda city zx', 'honda civic', 'honda crv', 'honda jazz', 'honda mobilio', 'honda wr-v', 'hyundai accent', 'hyundai aura', 'hyundai creta', 'hyundai elite i20', 'hyundai eon', 'hyundai getz prime', 'hyundai grand i10', 'hyundai grand i10 nios', 'hyundai i10', 'hyundai i20', 'hyundai i20 active', 'hyundai new elantra', 'hyundai new santro', 'hyundai santa fe', 'hyundai santro', 'hyundai santro xing', 'hyundai sonata transform', 'hyundai tucson new', 'hyundai venue', 'hyundai verna', 'hyundai xcent', 'isuzu d-max v cross', 'isuzu mu-7', 'jaguar xj l', 'jeep compass', 'kia seltos', 'mahindra bolero', 'mahindra e2o', 'mahindra kuv100', 'mahindra marazzo', 'mahindra maxximo', 'mahindra nuvosport', 'mahindra quanto', 'mahindra renault logan', 'mahindra reva', 'mahindra scorpio', 'mahindra thar', 'mahindra tuv300', 'mahindra verito', 'mahindra xuv 3oo', 'mahindra xuv500', 'mahindra xylo', 'maruti 800', 'maruti a star', 'maruti alto', 'maruti alto 800', 'maruti alto k10', 'maruti baleno', 'maruti celerio', 'maruti celerio x', 'maruti ciaz', 'maruti dzire', 'maruti eeco', 'maruti ertiga', 'maruti esteem', 'maruti ignis', 'maruti new  wagon-r', 'maruti omni', 'maruti omni e', 'maruti ritz', 'maruti s cross', 'maruti s presso', 'maruti swift', 'maruti swift dzire', 'maruti sx4', 'maruti vitara brezza', 'maruti wagon r', 'maruti wagon r 1.0', 'maruti wagon r duo', 'maruti wagon r stingray', 'maruti xl6', 'maruti zen', 'maruti zen estilo', 'mercedes benz a class', 'mercedes benz b class', 'mercedes benz c class', 'mercedes benz cla class', 'mercedes benz cls class', 'mercedes benz e class', 'mercedes benz gla class', 'mercedes benz ml class', 'mg hector', 'mg zs ev', 'mitsubishi outlander', 'nissan evalia', 'nissan micra', 'nissan micra active', 'nissan nissan kicks', 'nissan sunny', 'nissan terrano', 'opel astra', 'renault captur', 'renault duster', 'renault fluence', 'renault kwid', 'renault lodgy', 'renault pulse', 'renault scala', 'renault triber', 'skoda fabia', 'skoda laura', 'skoda octavia', 'skoda rapid', 'skoda superb', 'skoda yeti', 'ssangyong rexton', 'tata aria', 'tata bolt', 'tata harrier', 'tata hexa', 'tata indica ev2', 'tata indica v2', 'tata indica vista', 'tata indigo cs', 'tata indigo ecs', 'tata manza', 'tata nano', 'tata nexon', 'tata safari', 'tata safari storme', 'tata sumo gold', 'tata tiago', 'tata tigor', 'tata zest', 'toyota camry', 'toyota corolla', 'toyota corolla altis', 'toyota etios', 'toyota etios liva', 'toyota fortuner', 'toyota glanza', 'toyota innova', 'toyota innova crysta', 'toyota prius', 'toyota yaris', 'volkswagen ameo', 'volkswagen cross polo', 'volkswagen jetta', 'volkswagen passat', 'volkswagen polo', 'volkswagen vento', 'volvo s60', 'volvo xc 60']
    )
)

variant = st.selectbox(
    "Variant",
    ['1.0 climber opt amt', '1.0 ecoboost titanium', '1.0 ecoboost titanium opt', '1.0 ecoboost titanium sports(sunroof)', '1.0 lxi (o)', '1.0 rxl', '1.0 rxt', '1.0 rxt opt', '1.0 rxt opt at', '1.0 rxt opt marvel edition', '1.0 rxz', '1.0 s at', '1.0 t(o) at', '1.0 turbo gdi sx+ at', '1.0 vxi (o)', '1.0l turbo gdi sx mt', '1.0l turbo gdi sx(o) mt', '1.1 gvs', '1.1 magna mt', '1.1 sports amt', '1.2', '1.2  asta (o) cvt', '1.2 asta (o) at', '1.2 base i vtec', '1.2 e mt i vtec', '1.2 emt i vtec', '1.2 ex mt i vtec', '1.2 exi duratec', '1.2 exmt i vtec', '1.2 fire', '1.2 i-vtec s mt edge edition', '1.2 i-vtec vx mt', '1.2 ls abs', '1.2 lxi duratec', '1.2 magna plus vtvt', '1.2 s', '1.2 s (o) mt i vtec', '1.2 s (o) mt ivtec', '1.2 s crdi', '1.2 s cvt i vtec', '1.2 s i - vtech  alive edition mt', '1.2 s mt', '1.2 s mt i vtec', '1.2 s vtvt', '1.2 sat i vtec', '1.2 select i vtec', '1.2 smt i vtec', '1.2 sports plus vtvt', '1.2 sports plus vtvt cvt', '1.2 sportz plus dual tone vtvt', '1.2 sv mt', '1.2 sv petrol', '1.2 sx', '1.2 sx mt i vtec', '1.2 titanium', '1.2 titanium duratec', '1.2 titanium petrol', '1.2 trend petrol', '1.2 trend+ petrol', '1.2 v at', '1.2 v cvt i vtec', '1.2 v mt', '1.2 v mt i vtec', '1.2 v mt i-vtec', '1.2 vx at', '1.2 vx at i vtec', '1.2 vx i-vtech', '1.2 vx mt i vtec', '1.2 vxmt i vtec', '1.2 zxi duratec', '1.3 base', '1.3 flair', '1.3 gvs', '1.3 ls 8 str', '1.3 lt 7 str', '1.4 base', '1.4 clxi tdci', '1.4 crdi asta (o)', '1.4 crdi ex mt', '1.4 crdi s mt', '1.4 e plus crdi', '1.4 exi', '1.4 exi duratorq', '1.4 exi tdci', '1.4 gtx+ turbo gdi petrol at', '1.4 ls 8 str', '1.4 lxi duratorq', '1.4 magna plus crdi', '1.4 s', '1.4 s crdi', '1.4 s plus crdi', '1.4 sx', '1.4 sxi tdci abs', '1.4 titanium duratorq', '1.4 vtvt ex', '1.4 zxi duratorq', '1.4 zxi tdci', '1.5 alpha shvs', '1.5 ambiente tdci', '1.5 d2 bs iv', '1.5 e mt petrol', '1.5 e2', '1.5 ecosport titanium sports(sunroof)', '1.5 elegance tdi mt', '1.5 emt i dtec', '1.5 exi', '1.5 exmt i dtec', '1.5 i- dtec s', '1.5 i- dtec v', '1.5 i-dtec s mt', '1.5 i-dtec vx mt', '1.5 i-vtec s', '1.5 i-vtec v cvt', '1.5 i-vtec vx', '1.5 platine diesel', '1.5 s i vtec', '1.5 smt i dtec', '1.5 sv i dtec', '1.5 sx mt i dtec', '1.5 tdci titanium plus', '1.5 tdi at ambition', '1.5 tdi at style plus', '1.5 tdi mt ambition', '1.5 tdi mt elegance', '1.5 titanium', '1.5 titanium plus ti vct at', '1.5 titanium sports edition', '1.5 titanium ti vct', '1.5 titanium ti vct at', '1.5 titaniumtdci opt', '1.5 trend', '1.5 trend diesel', '1.5 trend tdci', '1.5 trend ti vct', '1.5 trend+ tdci', '1.5 v cvt i-dtec', '1.5 v i dtec', '1.5 v i vtec', '1.5 v mt', '1.5 v opt. i vtec', '1.5 vtec plus', '1.5 vxmt i dtec', '1.5ambiente ti vct', '1.5titanium tdci', '1.6', '1.6 base', '1.6 crdi sx', '1.6 crdi sx + at', '1.6 crdi sx plus auto', '1.6 crdi sx(o) executive', '1.6 e + vtvt', '1.6 mpi at ambition plus', '1.6 s', '1.6 sx (o)', '1.6 sx (o) at crdi', '1.6 sx (o) crdi', '1.6 sx (o) crdi mt', '1.6 sx (o) vtvt', '1.6 sx at', '1.6 sx at crdi', '1.6 sx at o', '1.6 sx at petrol', '1.6 sx crdi', '1.6 sx crdi dual tone', '1.6 sx mt', '1.6 sx plus auto petrol', '1.6 sx plus diesel', '1.6 sx plus petrol', '1.6 sx plus se', '1.6 sx plus vtvt', '1.6 sx vtvt', '1.6 sx vtvt (o)', '1.6 sx vtvt at (o)', '1.6 sxi abs', '1.6 tdi mt ambition', '1.6 tdi mt ambition plus', '1.6 zxi', '1.6 zxi abs', '1.8 g', '1.8 gl', '1.8 j', '1.8 tsi lk at', '1.8 tsi style at', '1.8 z3', '1.8s mt', '1.8v at', '1.8v at sun roof', '1.8v mt', '110 ps rxz 8 str', '110 ps rxz diesel opt', '110 ps rxz diesel plus', '2.0 2wd at', '2.0 crdi at', '2.0 limited', '2.0 limited 4*2', '2.0 longitude', '2.0 longitude (o)', '2.0 sport', '2.0 tdi', '2.0 tdi 174bhp', '2.0 tdi 174bhp prm plus', '2.0 tdi cr lk at', '2.0 tdi premium plus', '2.0 tdi quattro', '2.0 tdi quattro mt', '2.0 tdi s line', '2.2 ex 4x2', '2.2 vx 4x2', '2.2 vx 4x4', '2.4 at', '2.4 at 4wd avn', '2.4 at i vtec', '2.4 gx 7 str', '2.4 gx 8 str', '2.4 mivec', '2.4 mt', '2.4 vti l at', '2.4 vx 7 str', '2.4 vx 8 str', '2.4 zx 7 str', '2.5 e', '2.5 g1', '2.5 g1 bs iv', '2.5 g2 7 seater', '2.5 g3', '2.5 g3 8 str', '2.5 g4 7 str', '2.5 g4 8 str', '2.5 gx 7 str bs iv', '2.5 gx 8 str bs iv', '2.5 v 7str', '2.5 v 8 str', '2.5 vx 7 str bs iv', '2.5 vx 8 str bs iv', '2.5 zx 7 str bs iv', '2.8 4x2 at', '2.8 4x2 mt', '2.8 4x4 at', '2.8 gx at 7 str', '2.8 gx at 8 str', '2.8 tfsi technology', '2.8 zx at 7 str', '200 cdi sport', '200 cdi style', '200 cgi avantgarde', '200 cgi spotrs', '200 elegance', '230 avantgarde', '250 cdi', '250 cdi avantgarde', '250 cdi elegance at', '280 cdi elegance', '2wd at gl diesel', '2wd at gls diesel', '2wd at gls petrol', '3.0 at 4x2', '3.0 at 4x4', '3.0 mt 4x2', '3.0 mt 4x4', '3.0 v 6 premium luxury', '30 tdi premium', '30 tdi quattro', '320 d performance edition', '320d', '320d highline', '320d luxuryline', '328i sportline', '35 tdi premium plus', '35 tdi quattro', '35 tdi technology', '350 blue efficiency', '35tdi', '4*4 mt', '40 tfsi premium', '4wd', '4wd at', '4x2 ex dicor 2.2 vtt', '4x2 ex dicor bs iv', '4x2 lx', '4x2 lx dicor 2.2 vtt', '5 seater', '5 str', '5 str cng with ac plushtr', '5 str with ac plus htr', '5 str with ac plushtr', '520d', '520d 2.0', '525d', '525d luxury', '7 seater', '7 str', '8 str', '85 ps rxe', '85 ps rxe diesel adventure', '85 ps rxl', '85 ps rxl opt', 'a', 'a180 cdi style', 'ac', 'active 1.2', 'active 1.3', 'active 2.0 tdi 4x2', 'alpha 1.2 k12', 'alpha 1.2 k12 amt', 'alpha 1.2 k12 dual tone', 'alpha 1.3', 'alpha 1.3 ddis shvs', 'alpha 1.4 vvt', 'alpha 1.4 vvt amt', 'alpha 1.5 at vtvt shvs', 'alpha 1.5 mt vvt shvs', 'alpha ddis 190', 'alpha shvs', 'alpha shvs  mt', 'ambiente', 'ambiente 1.2 mpi', 'ambiente 1.8 tsi', 'ambiente 2.0 tdi cr at', 'ambiente 2.0 tdi cr mt', 'ambition 1.6 mpfi mt', 'ambition 1.6 mpi mt plus', 'ambition 1.6 tdi mt', 'ambition 2.0 tdi 4x2', 'ambition 2.0 tdi cr', 'ambition plus 1.2 tdi', 'aqua safire bs iii', 'asta 1.1 (o) crdi', 'asta 1.1 crdi', 'asta 1.1 crdi opt', 'asta 1.1 mt', 'asta 1.2', 'asta 1.2 (o)', 'asta 1.2 (o) vtvt', 'asta 1.2 at kappa2 with sunroof', 'asta 1.2 at vtvt', 'asta 1.2 at with sunroof', 'asta 1.2 dual tone', 'asta 1.2 kappa vtvt', 'asta 1.2 kappa vtvt opt', 'asta 1.2 kappa2', 'asta 1.2 o with sunroof', 'asta 1.2 vtvt', 'asta 1.4 crdi', 'asta 1.4 crdi 6 speed', 'asta at 1.2 kappa vtvt', 'asta petrol', 'aura 1.3 quadrajet', 'aura abs safire bs iv', 'aura quadrajet bs iv', 'b180', 'c 220 cdi avantgarde', 'c 220 cdi classic', 'c 220 cdi elegance mt', 'c 220 cdi style', 'c200 cgi grand edition', 'c220 cdi grand edition', 'c4', 'c8', 'cla 200 cdi sport', 'climber 1.0', 'climber 1.0 at', 'comfortline 1.0', 'comfortline 1.0 petrol', 'comfortline 1.2', 'comfortline 1.2l diesel', 'comfortline 1.2l petrol', 'comfortline 1.4 tsi mt', 'comfortline 1.5l diesel', 'comfortline 2.0l tdi', 'comfortline diesel', 'comfortline plus 1.0', 'comfortline tdi at', 'comfortline tsi at', 'crde 4x4 bs iv', 'cross 1.2 g', 'cross 1.4 gd', 'cross 1.5 v', 'd 4d g', 'd 4d gd', 'd 4d gd sp', 'd 4d gl', 'd 4d j', 'd 4d vd', 'd lite', 'd lite plus', 'd-4d vxd', 'd2 bs iv', 'delta 1.2 k12', 'delta 1.2 k12 amt', 'delta 1.2 k12 at', 'delta 1.3', 'delta 1.3 ddis shvs', 'delta 1.4 vvt', 'delta 1.5 shvs vvt at', 'delta 1.6', 'delta ddis 190', 'delta shvs', 'dle 1.5 dci', 'dlg bs iii', 'dlg dicor bs iii', 'dls', 'dls 1.5 dci', 'dlx 1.5 dci bs iv', 'dx', 'dynamic 1.3', 'dynamic 1.3 multijet', 'e 1.0', 'e 200 avantgarde', 'e 220 cdi classic', 'e 220 cdi elegance', 'e 250 cdi avantgarde', 'e 250 cdi classic', 'e 250 cdi elegance', 'e mt diesel', 'e plus', 'e20 t2', 'e8 abs bs iv', 'elegance 1.2 mpi', 'elegance 1.6 mpfi at', 'elegance 1.6 mpfi mt', 'elegance 1.6 tdi mt', 'elegance 1.8 tsi at', 'elegance 1.8 tsi mt', 'elegance 2.0 tdi cr at', 'elegance tdi 2.0 at', 'emotion 1.3', 'emotion 1.3 multijet', 'emotion pack 1.3 90 hp', 'emotion pk 1.4', 'era', 'era 1.1 1rde2', 'era 1.1 irde', 'era 1.2', 'era 1.2 kappa vtvt', 'era 1.2 vtvt', 'era 1.4 crdi', 'era plus', 'era plus (o)', 'era plus lpg', 'ex', 'ex quadrajet', 'exclusive', 'executive', 'executive gle', 'fluidic 1.4 crdi', 'fluidic 1.4 crdi cx', 'fluidic 1.4 ex crdi', 'fluidic 1.4 vtvt', 'fluidic 1.4 vtvt cx', 'fluidic 1.6 crdi  s at', 'fluidic 1.6 crdi s', 'fluidic 1.6 crdi sx at', 'fluidic 1.6 crdi sx opt', 'fluidic 1.6 crdi sx opt at', 'fluidic 1.6 ex crdi', 'fluidic 1.6 ex vtvt', 'fluidic 1.6 ex vtvt at', 'fluidic 1.6 sx crdi', 'fluidic 1.6 sx crdi opt', 'fluidic 1.6 sx vtvt', 'fluidic 1.6 sx vtvt opt', 'fluidic 1.6 sx vtvt opt at', 'fluidic 1.6 vtvt s', 'fluidic 1.6 vtvt s (o)  mt', 'fluidic 1.6 vtvt sx at', 'g', 'g at', 'g cvt', 'g sp', 'gd', 'gd exclusive', 'gl', 'gl plus', 'gl plus lpg', 'gle', 'gls', 'gls 1.6 abs', 'gls at', 'gls cng', 'gls lpg', 'glx', 'glx 1.4', 'gt tdi', 'gt tdi 1.6 mt diesel', 'gt tsi', 'gt tsi 1.2 petrol at', 'gtx + at petrol', 'gtx+ 1.4 mt', 'gxi', 'gxi cvt', 'h2 1.8 e', 'h4 abs bs iv', 'h8 abs airbag bs iv', 'he 1.8 j', 'high 4x2 mt', 'high line plus 1.0', 'highline 1.0 petrol', 'highline 1.2', 'highline 1.2 tsi at', 'highline 1.5', 'highline 1.5l at (d)', 'highline 1.6l petrol', 'highline diesel', 'highline dsg', 'highline petrol', 'highline petrol at', 'highline plus dsg 1.5', 'highline tdi at', 'highline1.2l diesel', 'highline1.2l petrol', 'highline1.5l diesel', 'htk 1.5 petrol', 'htk plus 1.5 diesel', 'htx 1.5 diesel', 'hybrid', 'i', 'j cvt', 'j mt', 'k10 vxi at', 'k2 6 str', 'k4 6 str', 'k4+ 6 str', 'k4+ d 6 str', 'k6 d 6 str', 'k6+ 6 str', 'k6+ d 6 str', 'k8 6 str', 'k8 d 5 str', 'k8 d 6 str', 'kinetic d4', 'kraz at petrol', 'l2', 'ldi', 'ldi bs iv', 'ldi o', 'ldi opt', 'le', 'limited (o) 2.0', 'limited 1.4 at', 'ls', 'ls 1.0', 'ls 1.0 lpg', 'ls 1.2', 'ls cr4 bs iv', 'ls diesel', 'ls petrol', 'lt 1.0', 'lt 1.6', 'lt diesel', 'lt opt petrol', 'lt petrol', 'ltz', 'ltz at', 'lx', 'lx bs iv', 'lx special edition', 'lx tdi', 'lx tdi bs iii', 'lxi', 'lxi 1.0 l', 'lxi 1.2 bs iv', 'lxi 1.3', 'lxi cng', 'lxi cng (o)', 'lxi cng 1.0 l', 'lxi cng avance limited edition', 'lxi cng opt', 'lxi krest limited edition', 'lxi lpg', 'lxi minor', 'lxi opt', 'lxi utsav limited addition', 'm8 7 str', 'm8 8 str', 'magna', 'magna 1.1 crdi', 'magna 1.1 irde2', 'magna 1.1 lpg', 'magna 1.2', 'magna 1.2 at', 'magna 1.2 at  vtvt', 'magna 1.2 crdi', 'magna 1.2 kappa vtvt', 'magna 1.2 kappa2', 'magna 1.2 vtvt', 'magna 1.4 crdi', 'magna executive 1.2', 'magna executive diesel', 'magna o', 'magna o 1.2', 'magna o 1.4 crdi', 'magna o with sunroof', 'magna plus', 'magna plus blue drive', 'magna plus optional', 'multijet 1.3 90 hp', 'n6 mhawk', 'neotech 1.0 easyr', 'power+ sle', 'power+ slx', 'power+ zlx', 'ps 1.0', 'ps diesel', 'ps petrol', 'pure 4x2', 'rev 116', 'revotron xt', 'rs 1.0 petrol', 'rx 6', 'rx l petrol', 'rx7', 'rxe petrol 104', 'rxe petrol mt', 'rxl', 'rxl 110 ps adventure', 'rxl 85ps explore', 'rxl amt 110 ps', 'rxl diesel 110', 'rxl pack diesel 85', 'rxl petrol 104', 'rxl plus diesel 85', 'rxl1.0 easy-r at', 'rxs cvt 106 ps', 'rxt', 'rxt 1.0 easy-r  at', 'rxt 1.0 easy-r at option', 'rxt opt', 'rxz', 'rxz 110 4wd', 'rxz amt 110 ps', 'rxz diesel 110', 's', 's 1.0', 's 1.1 crdi', 's 1.1 crdi opt', 's 1.2', 's 1.2 opt', 's 1.6 mt', 's 1.8 mt', 's at', 's mt', 's mt diesel', 's mt petrol', 's10', 's10 7 str', 's10 at', 's11', 's2', 's5', 's5 2wd', 's6 plus', 's6+ intell hybrid', 's8', 's9', 'sdrive 20d', 'sharp 2.0 diesel', 'sharp dct petrol', 'sharp hybird petrol mt', 'shvs vdi', 'sigma 1.2 k12', 'sigma 1.3', 'sigma 1.3 ddis shvs', 'sigma ddis 190', 'sle', 'sle bs iii', 'sle bs iv', 'slx bs iv', 'sport 1.3', 'sport plus petrol', 'sports 1.2 vtvt', 'sportz', 'sportz (o) 1.2', 'sportz (o) 1.2 at vtvt', 'sportz (o) 1.4', 'sportz 1.1', 'sportz 1.1 crdi', 'sportz 1.1 irde2', 'sportz 1.2', 'sportz 1.2 at', 'sportz 1.2 at kappa2', 'sportz 1.2 kappa vtvt', 'sportz 1.2 kappa2', 'sportz 1.2 o', 'sportz 1.2 vtvt', 'sportz 1.4', 'sportz 1.4 crdi', 'sportz 1.4 crdi 6 speed bs iv', 'sportz at 1.2 kappa vtvt', 'sportz o 1.2', 'sportz o 1.4 crdi', 'sportz petrol', 'sportz(o) 1.2 mt', 'sportz1.2 crdi', 'std', 'style 1.5 tdi at', 'style 1.6 mpi mt', 'summum d3', 'summum d4', 'sv cvt petrol', 'sv mt diesel', 'sv mt petrol', 'sx 1.1 crdi', 'sx 1.2', 'sx 1.2 opt', 'sx 1.6 crdi', 'sx 1.8 at', 'sx at 1.2 opt', 'sx o mt 1.2 diesel', 'sx petrol at', 'sx(o) crdi', 't', 't (o)', 't 10 mt dual tone', 't2', 't6', 't6+', 't6+ at', 't8', 't8 at', 't8 dual tone', 'titanium + 1.2 ti-vct', 'titanium 1.2 ti-vct', 'titanium 1.2 ti-vct mt', 'titanium 1.5 tdci', 'titanium plus petrol at', 'tour', 'tour s diesel', 'touring sport diesel at', 'transform 1.6 vtvt', 'trend 1.2 ti-vct', 'trendline 1.0', 'trendline 1.0 l petrol', 'trendline 1.2l diesel', 'trendline 1.2l petrol', 'trendline 1.4 tsi mt', 'trendline 1.5l diesel', 'trendline 1.6', 'trendline 2.0l tdi', 'trendline diesel', 'trendline petrol', 'twist xta', 'v', 'v  limited', 'v at', 'v cvt', 'v mt diesel', 'v mt petrol', 'v mt sunroof', 'varicor 400 xma', 'varicor 400 xt', 'varicor 400 xta', 'vd', 'vd limited edition', 'vd sp', 'vdi', 'vdi (o) shvs hybird', 'vdi abs', 'vdi amt', 'vdi bs iv', 'vdi dual tone', 'vdi elate limited edition', 'vdi glory edition', 'vdi opt', 'vdi plus', 'vdi shvs', 'vdi shvs limited edition', 'vdi+ shvs', 'vgt crdi', 'vgt crdi sx', 'vgt crdi sx 1.5', 'vgt crdi sx abs', 'vl at', 'vlx 2wd airbag bs iv', 'vlx 2wd bs iv', 'vlx airbag bs iv', 'vtec', 'vx', 'vx  1.2', 'vx (o) petrol', 'vx cvt petrol', 'vx d', 'vx dual tone', 'vx mt diesel', 'vx mt o diesel', 'vx mt petrol', 'vx quadrajet', 'vxi', 'vxi (o)', 'vxi (o) amt', 'vxi (o)1.ol ags', 'vxi 1.0', 'vxi 1.2 bs iv', 'vxi 1.2l', 'vxi 1.3', 'vxi 1.3 abs', 'vxi abs', 'vxi abs air bag', 'vxi abs at', 'vxi amt', 'vxi at', 'vxi bs iii', 'vxi bs iv', 'vxi cng', 'vxi cng anniversary edition', 'vxi deca', 'vxi elate limited edition', 'vxi genus', 'vxi limited edition', 'vxi minor', 'vxi musik edition', 'vxi opt', 'vxi opt. mt', 'vxi optional', 'vxi plus', 'vxi plus ags', 'vxi plus amt', 'vxi regal limited edition', 'vxi regalia', 'vxi smart hybrid', 'vxi+ (o) mt', 'w10', 'w10 at', 'w10 at awd', 'w10 at fwd', 'w10 fwd', 'w11 (o)', 'w11 at', 'w4', 'w4 4x2', 'w4 petrol', 'w5 fwd', 'w6 4x2', 'w6 at', 'w7 fwd', 'w8 fwd', 'w8(o)', 'w9', 'xcite', 'xdrive 20d', 'xe', 'xe 1.05 revotorq', 'xe 1.2 revotron', 'xe 2.0l kryotec', 'xe 85 ps deisel', 'xe diesel', 'xe revotron', 'xg', 'xg erlx euro iii', 'xi', 'xl cvt', 'xl cvt (petrol)', 'xl diesel', 'xl erlx euro ii', 'xl erlx euro iii', 'xl p', 'xl petrol', 'xl plus 85 ps deisel', 'xm 1.2', 'xm 1.2 revotron', 'xm 1.5', 'xm quadrajet 75ps', 'xm revotorq', 'xm revotron', 'xm rt', 'xm rt 90 ps abs', 'xma 1.5', 'xms quadrajet 90ps', 'xms rt', 'xo erlx euro ii', 'xo erlx euro iii', 'xp', 'xt 1.05 revotorq', 'xt 1.2 revotron', 'xt revotron', 'xt rt', 'xt twist', 'xv', 'xv 110 diesel', 'xv cvt', 'xv d thp premium 110 ps', 'xv diesel', 'xv petrol', 'xv s', 'xxi', 'xz 1.05 revotorq', 'xz 1.2 revotron', 'xz 1.2 revotron opt', 'xz 2.0l kryotec', 'xz+ 1.2', 'xz+ 1.2 revotron', 'xz+ 1.5', 'xza + 1.2 petrol a/t', 'xza 1.2 revotron', 'xza+ 1.2 rtn', 'xza+ 1.5', 'zdi', 'zdi +', 'zdi + amt', 'zdi amt', 'zdi plus', 'zdi plus 1.5 diesel', 'zdi plus amt', 'zdi plus dual tone', 'zdi plus shvs', 'zdi shvs', 'zdi shvs hybird', 'zdi+ dual tone amt', 'zdi+ shvs', 'zdi+ shvs rs mt', 'zeta 1.2 k12', 'zeta 1.2 k12 amt', 'zeta 1.2 k12 cvt', 'zeta 1.3', 'zeta 1.3 ddis shvs', 'zeta 1.3 shvs', 'zeta 1.4 vvt', 'zeta 1.4 vvt amt', 'zeta 1.5 shvs vvt mt', 'zeta ddis 190', 'zeta shvs', 'zeta shvs petrol', 'zlx', 'zlx special edition', 'zx cvt', 'zx cvt petrol', 'zxi', 'zxi 1.2', 'zxi 1.2 bs iv', 'zxi 1.3', 'zxi abs', 'zxi abs amt', 'zxi amt', 'zxi at', 'zxi leather amt', 'zxi mt bs iv', 'zxi opt', 'zxi opt amt', 'zxi plus', 'zxi plus amt', 'zxi plus shvs', 'zxi smart hybrid', 'zxi smart hybrid at', 'zxi+ bs iv']
)

col3, col4 = st.columns(2)
with col3:
    body_type = st.selectbox(
        "Body Type",
        ["hatchback", "sedan", "suv", "luxury sedan", "luxury suv"]
    )
with col4:
    transmission = st.selectbox(
        "Transmission",
        ["manual", "automatic"]
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SECTION 2 — USAGE & HISTORY
# ============================================================
st.markdown(
    """
    <div class="section-card">
        <div class="section-head">
            <span class="section-num">02</span>
            <span class="section-title">Usage & History</span>
        </div>
        <p class="section-caption">How much road has this car already seen?</p>
    """,
    unsafe_allow_html=True,
)

col5, col6, col7 = st.columns(3)
with col5:
    yr_mfr = st.number_input(
        "Year Manufactured",
        min_value=1990,
        max_value=current_year
    )
with col6:
    kms_run = st.number_input("Kilometers Run", min_value=0)
with col7:
    total_owners = st.number_input(
        "Total Owners",
        min_value=0,
        step=1
    )

col8, col9 = st.columns(2)
with col8:
    city = st.selectbox(
        "City",
        ["noida", "gurgaon", "bengaluru", "new delhi", "mumbai", "pune",
         "hyderabad", "chennai", "kolkata", "ahmedabad",
         "faridabad", "ghaziabad", "lucknow"]
    )
with col9:
    assured_buy = st.selectbox(
        "Assured Buy",
        [True, False]
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SECTION 3 — CONDITION
# ============================================================
st.markdown(
    """
    <div class="section-card">
        <div class="section-head">
            <span class="section-num">03</span>
            <span class="section-title">Condition & Certification</span>
        </div>
        <p class="section-caption">The state the car is in today — this moves the price the most.</p>
    """,
    unsafe_allow_html=True,
)

col10, col11 = st.columns(2)
with col10:
    car_rating = st.selectbox(
        "Car Rating",
        ["great", "good", "fair", "overpriced"]
    )
with col11:
    fitness_certificate = st.selectbox(
        "Fitness Certificate",
        [True, False]
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PREDICT
# ============================================================
predict_clicked = st.button("Predict Resale Price →")

if predict_clicked:

    current_year = datetime.now().year

    car_age = current_year - yr_mfr

    if car_age == 0:
        km_per_year = kms_run
    else:
        km_per_year = kms_run / car_age

    input_df = pd.DataFrame({
        'car_name': [car_name],
        'yr_mfr': [yr_mfr],
        'kms_run': [kms_run],
        'city': [city],
        'body_type': [body_type],
        'transmission': [transmission],
        'variant': [variant],
        'assured_buy': [assured_buy],
        'make': [make],
        'model': [model_name],
        'total_owners': [total_owners],
        'car_rating': [car_rating],
        'fitness_certificate': [fitness_certificate],
        'car_age': [car_age],
        'km_per_year': [km_per_year]
    })

    with st.expander("View raw input passed to the model"):
        st.write(input_df)

    # Numerical columns
    num_cols = [
        'yr_mfr',
        'kms_run',
        'total_owners',
        'car_age',
        'km_per_year'
    ]

    # Categorical columns
    cat_cols = [
        'car_name',
        'city',
        'body_type',
        'transmission',
        'variant',
        'assured_buy',
        'make',
        'model',
        'car_rating',
        'fitness_certificate'
    ]

    # Apply imputers
    input_df[num_cols] = num_imputer.transform(input_df[num_cols])
    input_df[cat_cols] = cat_imputer.transform(input_df[cat_cols])

    # Apply OneHotEncoding
    input_encoded = ct.transform(input_df)

    # Prediction
    prediction = model.predict(input_encoded)

    st.markdown(
        f"""
        <div class="price-tag">
            <div class="price-tag-label">Estimated Resale Value</div>
            <div class="price-tag-value">₹ {prediction[0]:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

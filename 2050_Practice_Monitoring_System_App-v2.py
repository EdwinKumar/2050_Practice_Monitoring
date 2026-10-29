import streamlit as st
import pandas as pd
import sqlite3
import datetime
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="2050 Strategy Practice Monitoring System (v2.0)",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "2050_practice_monitoring.db"

# User Credentials & Role Definitions
USERS_CONFIG = {
    "sysadmin": {
        "password": "admin123",
        "name": "System Administrator",
        "role": "System Admin",
        "tag_id": "ALL",
        "tag_name": "All Thematic Areas (System Admin)",
        "badge": "👑 System Super Admin",
        "color": "#6C5CE7"
    },
    "mel_admin": {
        "password": "mel2050",
        "name": "PIFS MEL Secretariat Coordinator",
        "role": "MEL Admin",
        "tag_id": "ALL",
        "tag_name": "All Thematic Areas (MEL Reviewer)",
        "badge": "🛡️ MEL Admin Coordinator",
        "color": "#1F4E79"
    },
    "ta1_lead": {
        "password": "ta1_pass",
        "name": "TA1 Lead (PIFS Political & Regionalism)",
        "role": "TAG Focal Point",
        "tag_id": "TA01",
        "tag_name": "Political Leadership & Regionalism TAG",
        "badge": "🏛️ TA1 Lead",
        "motto": "Fostering Pacific Solidarity, Sovereignty & High-Level Diplomacy",
        "primary_color": "#1F4E79",
        "secondary_color": "#D4AF37",
        "banner_bg": "linear-gradient(135deg, #1F4E79 0%, #2F5496 50%, #D4AF37 100%)",
        "icon": "🏛️"
    },
    "ta2_lead": {
        "password": "ta2_pass",
        "name": "TA2 Lead (SPC People-Centred Division)",
        "role": "TAG Focal Point",
        "tag_id": "TA02",
        "tag_name": "People-Centred Development TAG",
        "badge": "👥 TA2 Lead",
        "motto": "Inclusivity, Health, Gender Equality, Youth & Cultural Heritage",
        "primary_color": "#E07A5F",
        "secondary_color": "#2A9D8F",
        "banner_bg": "linear-gradient(135deg, #E07A5F 0%, #F4A261 50%, #2A9D8F 100%)",
        "icon": "👥"
    },
    "ta3_lead": {
        "password": "ta3_pass",
        "name": "TA3 Lead (Forum Secretariat Peace & Security)",
        "role": "TAG Focal Point",
        "tag_id": "TA03",
        "tag_name": "Peace & Security TAG",
        "badge": "🛡️ TA3 Lead",
        "motto": "Implementing the Boe Declaration for a Safe & Secure Blue Pacific",
        "primary_color": "#2B4C7E",
        "secondary_color": "#E9C46A",
        "banner_bg": "linear-gradient(135deg, #1A365D 0%, #2B4C7E 50%, #E9C46A 100%)",
        "icon": "🛡️"
    },
    "ta4_lead": {
        "password": "ta4_pass",
        "name": "TA4 Lead (FFA / PIFS Economic Development)",
        "role": "TAG Focal Point",
        "tag_id": "TA04",
        "tag_name": "Resource & Economic Development TAG",
        "badge": "📈 TA4 Lead",
        "motto": "Sustainable Fisheries, Trade Expansion & Blue Economy Growth",
        "primary_color": "#2A9D8F",
        "secondary_color": "#264653",
        "banner_bg": "linear-gradient(135deg, #264653 0%, #2A9D8F 50%, #E9C46A 100%)",
        "icon": "📈"
    },
    "ta5_lead": {
        "password": "ta5_pass",
        "name": "TA5 Lead (SPREP Resilience / Climate Team)",
        "role": "TAG Focal Point",
        "tag_id": "TA05",
        "tag_name": "Climate Change & Disasters TAG",
        "badge": "🌪️ TA5 Lead",
        "motto": "Building Climate Resilience, Loss & Damage & Disaster Mobilisation",
        "primary_color": "#E76F51",
        "secondary_color": "#264653",
        "banner_bg": "linear-gradient(135deg, #264653 0%, #E76F51 50%, #F4A261 100%)",
        "icon": "🌪️"
    },
    "ta6_lead": {
        "password": "ta6_pass",
        "name": "TA6 Lead (SPREP / SPC Ocean Division)",
        "role": "TAG Focal Point",
        "tag_id": "TA06",
        "tag_name": "Ocean & Natural Environment TAG",
        "badge": "🌊 TA6 Lead",
        "motto": "Stewardship of the Ocean Realm, Biodiversity & BBNJ Treaty",
        "primary_color": "#0077B6",
        "secondary_color": "#00B4D8",
        "banner_bg": "linear-gradient(135deg, #03045E 0%, #0077B6 50%, #00B4D8 100%)",
        "icon": "🌊"
    },
    "ta7_lead": {
        "password": "ta7_pass",
        "name": "TA7 Lead (USP / PPA Technology & Connectivity)",
        "role": "TAG Focal Point",
        "tag_id": "TA07",
        "tag_name": "Technology & Connectivity TAG",
        "badge": "⚡ TA7 Lead",
        "motto": "Digital Transformation, Cyber Security & Regional Telecommunications",
        "primary_color": "#6C5CE7",
        "secondary_color": "#0984E3",
        "banner_bg": "linear-gradient(135deg, #2D3436 0%, #6C5CE7 50%, #0984E3 100%)",
        "icon": "⚡"
    }
}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_thematic_areas (
        thematic_area_id TEXT PRIMARY KEY,
        thematic_area_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS national_priorities (
        national_priority_id TEXT PRIMARY KEY,
        national_priority_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_outcomes (
        outcome_id TEXT PRIMARY KEY,
        outcome_name TEXT NOT NULL,
        national_priority_id TEXT,
        FOREIGN KEY (national_priority_id) REFERENCES national_priorities(national_priority_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_leaders_decisions (
        decision_id TEXT PRIMARY KEY,
        decision_name TEXT NOT NULL,
        decision_date TEXT,
        progress_status TEXT,
        outcome_id TEXT,
        FOREIGN KEY (outcome_id) REFERENCES practice_outcomes(outcome_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_rcas (
        rca_id TEXT PRIMARY KEY,
        rca_name TEXT NOT NULL,
        outcome_id TEXT,
        FOREIGN KEY (outcome_id) REFERENCES practice_outcomes(outcome_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_regional_initiatives (
        initiative_id TEXT PRIMARY KEY,
        initiative_name TEXT NOT NULL,
        decision_id TEXT,
        primary_rca_id TEXT,
        contributing_rca_ids TEXT,
        FOREIGN KEY (decision_id) REFERENCES practice_leaders_decisions(decision_id),
        FOREIGN KEY (primary_rca_id) REFERENCES practice_rcas(rca_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_indicators (
        indicator_id TEXT PRIMARY KEY,
        indicator_name TEXT NOT NULL,
        description TEXT,
        unit TEXT,
        reporting_frequency TEXT,
        outcome_id TEXT,
        FOREIGN KEY (outcome_id) REFERENCES practice_outcomes(outcome_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_monitoring_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        result_name TEXT NOT NULL,
        indicator_id TEXT,
        reporting_period TEXT,
        actual_value REAL,
        target_value REAL,
        reporting_date TEXT,
        FOREIGN KEY (indicator_id) REFERENCES practice_indicators(indicator_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_tag_submissions (
        submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_title TEXT NOT NULL,
        tag_name TEXT NOT NULL,
        reporting_period TEXT NOT NULL,
        indicator_id TEXT,
        actual_value REAL,
        narrative_update TEXT NOT NULL,
        evidence_reference TEXT,
        submission_status TEXT DEFAULT 'Draft',
        ai_interpretation TEXT,
        reviewer_comments TEXT,
        review_decision TEXT DEFAULT 'Pending',
        submitted_on TEXT,
        ai_draft_generated_on TEXT,
        reviewed_on TEXT,
        FOREIGN KEY (indicator_id) REFERENCES practice_indicators(indicator_id)
    )
    """)

    # Seed master data if table is empty
    cursor.execute("SELECT COUNT(*) FROM practice_thematic_areas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO practice_thematic_areas VALUES (?, ?)", [
            ("TA01", "Political Leadership & Regionalism TAG"),
            ("TA02", "People-Centred Development TAG"),
            ("TA03", "Peace & Security TAG"),
            ("TA04", "Resource & Economic Development TAG"),
            ("TA05", "Climate Change & Disasters TAG"),
            ("TA06", "Ocean & Natural Environment TAG"),
            ("TA07", "Technology & Connectivity TAG")
        ])

        cursor.executemany("INSERT INTO national_priorities VALUES (?, ?)", [
            ("NP01", "Governance & Political Solidarity Priority"),
            ("NP02", "Human Capital & Social Inclusion Priority"),
            ("NP03", "Regional Peace & Boe Security Priority"),
            ("NP04", "Sustainable Trade & Economic Sovereignty Priority"),
            ("NP05", "Climate Resilience & Loss Damage Priority"),
            ("NP06", "Ocean Conservation & Marine Stewardship Priority"),
            ("NP07", "Digital Infrastructure & Cyber Connectivity Priority")
        ])

        cursor.executemany("INSERT INTO practice_outcomes VALUES (?, ?, ?)", [
            ("OUT01", "Enhanced Regional Diplomacy & Governance", "NP01"),
            ("OUT02", "Universal Access to Education & Health Services", "NP02"),
            ("OUT03", "Safe & Secure Pacific Maritime Boundaries", "NP03"),
            ("OUT04", "Sustainable Fisheries & Economic Resilience", "NP04"),
            ("OUT05", "Operational Pacific Resilience Facility & Climate Finance", "NP05"),
            ("OUT06", "30x30 Protected Marine Areas & BBNJ Ratification", "NP06"),
            ("OUT07", "High-Speed Subsea Fiber Connectivity across FICs", "NP07")
        ])

        cursor.executemany("INSERT INTO practice_indicators VALUES (?, ?, ?, ?, ?, ?)", [
            ("IND01", "Female Parliamentary Representation (%)", "Measures share of female MPs across Pacific parliaments", "Percentage", "Annual", "OUT01"),
            ("IND02", "NCD Intervention & Prevention Coverage (%)", "Percentage of population with access to essential NCD screening", "Percentage", "Quarterly", "OUT02"),
            ("IND03", "Maritime Boundary Treaties Formally Signed", "Number of bilateral/multilateral boundary treaties ratified", "Count", "Annual", "OUT03"),
            ("IND04", "Offshore Tuna Processing & Value Retention (%)", "Share of tuna catch processed within Pacific island states", "Percentage", "Quarterly", "OUT04"),
            ("IND05", "Pacific Resilience Facility (PRF) Capital Pledged ($M)", "Total pledged capital towards the $500M PRF target", "USD Millions", "Quarterly", "OUT05"),
            ("IND06", "Marine Protected Area (MPA) Coverage (% EEEZ)", "Percentage of EEZ under formal protection status", "Percentage", "Annual", "OUT06"),
            ("IND07", "Subsea Fiber Broadband Penetration Rate (%)", "Share of population with high-speed fiber broadband connection", "Percentage", "Quarterly", "OUT07")
        ])

        cursor.executemany("INSERT INTO practice_monitoring_results (result_name, indicator_id, reporting_period, actual_value, target_value, reporting_date) VALUES (?, ?, ?, ?, ?, ?)", [
            ("IND01 – 2026 Result", "IND01", "2026 Q4", 18.5, 30.0, "2026-10-27"),
            ("IND02 – 2026 Result", "IND02", "2026 Q4", 62.0, 75.0, "2026-10-27"),
            ("IND03 – 2026 Result", "IND03", "2026 Q4", 14.0, 18.0, "2026-10-27"),
            ("IND04 – 2026 Result", "IND04", "2026 Q4", 48.0, 60.0, "2026-10-27"),
            ("IND05 – 2026 Result", "IND05", "2026 Q4", 153.0, 500.0, "2026-10-27"),
            ("IND06 – 2026 Result", "IND06", "2026 Q4", 22.4, 30.0, "2026-10-27"),
            ("IND07 – 2026 Result", "IND07", "2026 Q4", 54.0, 70.0, "2026-10-27")
        ])

        # Seed sample submissions for ALL 7 TAGs so every profile has immediate rich data
        sample_subs = [
            ("Political Leadership TAG – Q4 2026 Governance Update", "Political Leadership & Regionalism TAG", "2026 Q4", "IND01", 18.5,
             "Advancement achieved in female political leadership mentorship programs across Melanesia and Polynesia. 18.5% national parliament representation recorded.", "PIFS-POL-2026-Q4", "Approved", "Approved", "2026-10-20 10:00:00"),
            
            ("People-Centred Development TAG – Health & Youth Progress", "People-Centred Development TAG", "2026 Q4", "IND02", 62.0,
             "Universal screening for NCDs expanded across 8 member countries with SPC support. Target reached 62% coverage.", "SPC-PCD-2026-Q4", "Awaiting Human Review", "Pending", "2026-10-22 11:30:00"),
             
            ("Peace & Security TAG – Boe Declaration Maritime Survey", "Peace & Security TAG", "2026 Q4", "IND03", 14.0,
             "Fourteen maritime boundary treaties ratified to date. Two new bilateral treaties between Tuvalu and Kiribati under negotiation.", "SEC-BOE-2026-Q4", "Submitted", "Pending", "2026-10-24 14:15:00"),

            ("Resource & Economic Development TAG – Blue Economy & Tuna Processing", "Resource & Economic Development TAG", "2026 Q4", "IND04", 48.0,
             "Offshore tuna processing facilities in Solomon Islands and PNG expanded capacity. 48% of total catch now processed onshore.", "FFA-RED-2026-Q4", "Approved", "Approved", "2026-10-18 09:00:00"),

            ("Climate Change & Disasters TAG – PRF Capitalisation Update", "Climate Change & Disasters TAG", "2026 Q4", "IND05", 153.0,
             "Pacific Resilience Facility pledged capital reached $153M following Kingdom of Saudi Arabia ($50M) and UK pledges.", "SPREP-PRF-2026-Q4", "Approved", "Approved", "2026-10-15 16:20:00"),

            ("Ocean & Natural Environment TAG – BBNJ Treaty & 30x30 Coral Protection", "Ocean & Natural Environment TAG", "2026 Q4", "IND06", 22.4,
             "Cook Islands and Palau expanded marine sanctuary zones, raising overall EEZ protected coverage to 22.4%.", "SPREP-OCEAN-2026-Q4", "Returned for Clarification", "Returned for Clarification", "2026-10-25 08:45:00"),

            ("Technology & Connectivity TAG – South Pacific Connect Subsea Cables", "Technology & Connectivity TAG", "2026 Q4", "IND07", 54.0,
             "Google South Pacific Connect fiber deployment landed in Fiji and French Polynesia. High-speed penetration reached 54%.", "USP-TECH-2026-Q4", "Awaiting Human Review", "Pending", "2026-10-26 12:00:00")
        ]

        for title, tag, period, ind_id, val, narrative, ev, status, dec, sub_time in sample_subs:
            ai_draft = f"AI-GENERATED DRAFT — HUMAN REVIEW REQUIRED\n\n(1) Progress Summary:\nThe {tag} submitted progress for {period}.\n\n(2) Reported Actual: {val}\n\n(3) Status: {status}"
            cursor.execute("""
                INSERT INTO practice_tag_submissions (
                    submission_title, tag_name, reporting_period, indicator_id, actual_value,
                    narrative_update, evidence_reference, submission_status, review_decision,
                    ai_interpretation, submitted_on, ai_draft_generated_on
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, tag, period, ind_id, val, narrative, ev, status, dec, ai_draft, sub_time, sub_time))

    conn.commit()
    conn.close()

init_db()

def run_ai_interpretation_workflow(submission_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.*, i.indicator_name, i.description as ind_desc, i.unit, r.target_value
        FROM practice_tag_submissions s
        LEFT JOIN practice_indicators i ON s.indicator_id = i.indicator_id
        LEFT JOIN practice_monitoring_results r ON s.indicator_id = r.indicator_id AND s.reporting_period = r.reporting_period
        WHERE s.submission_id = ?
    """, (submission_id,))
    sub = cursor.fetchone()

    if not sub:
        conn.close()
        return False, "Submission not found."

    actual = sub["actual_value"]
    target = sub["target_value"] if sub["target_value"] is not None else "Not specified"
    ind_name = sub["indicator_name"] or "Unlinked Indicator"
    period = sub["reporting_period"]

    ai_interpretation_draft = f"""AI-GENERATED DRAFT — HUMAN REVIEW REQUIRED

(1) Progress Summary:
The {sub['tag_name']} reports progress for {period} regarding '{ind_name}'. Narrative indicates active implementation across member countries.

(2) Reported Performance:
- Reported Actual Value: {actual} ({sub['evidence_reference'] or 'No unit'})
- Target Value Benchmark: {target}
- Reporting Period: {period}

(3) Key Achievements & Gaps:
- Reported Progress: {sub['narrative_update'][:150]}...
- Evidence Verification Status: Reference link provided ({sub['evidence_reference'] or 'None'}). Needs independent audit.

(4) Risks & Strategic Alignment:
- Implementation Risk: Capacity constraints and resource gaps require continuous monitoring.
- Action Required: MEL Reviewer to confirm data alignment with NSO benchmarks before final approval.
"""

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE practice_tag_submissions
        SET ai_interpretation = ?,
            ai_draft_generated_on = ?,
            submission_status = 'Awaiting Human Review',
            submitted_on = COALESCE(submitted_on, ?)
        WHERE submission_id = ?
    """, (ai_interpretation_draft, now_str, now_str, submission_id))

    conn.commit()
    conn.close()
    return True, "AI Workflow executed successfully. Record moved to 'Awaiting Human Review'."

# Session State Initialization for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

# Custom CSS Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; color: #1F4E79; font-weight: 700; margin-bottom: 0px; }
    .sub-title { font-size: 1.0rem; color: #2F5496; font-style: italic; margin-bottom: 20px; }
    .login-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #1F4E79; }
    .tag-banner { padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .card-box { background-color: #F8F9FA; padding: 18px; border-radius: 8px; border-left: 5px solid #1F4E79; margin-bottom: 15px; }
    .status-badge { padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: bold; display: inline-block; }
    .badge-draft { background-color: #E0E0E0; color: #333; }
    .badge-submitted { background-color: #CCE5FF; color: #004085; }
    .badge-review { background-color: #FFF3CD; color: #856404; }
    .badge-approved { background-color: #D4EDDA; color: #155724; }
    .badge-returned { background-color: #F8D7DA; color: #721C24; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LOGIN PAGE FUNCTION
# -----------------------------------------------------------------------------
def render_login_page():
    st.markdown('<p class="main-title">🌊 2050 Strategy Practice Monitoring Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Pacific Islands Forum Secretariat (PIFS) — Authenticated Multi-TAG & MEL Gateway</p>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    
    with col_b:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🔑 Sign In to Your 2050 Portal Account")
        
        username_input = st.text_input("Username:", placeholder="e.g. sysadmin, mel_admin, ta1_lead...")
        password_input = st.text_input("Password:", type="password", placeholder="Enter your password")
        
        login_btn = st.button("🔐 Login to Portal", use_container_width=True)
        
        if login_btn:
            if username_input in USERS_CONFIG and USERS_CONFIG[username_input]["password"] == password_input:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username_input
                st.session_state["user_info"] = USERS_CONFIG[username_input]
                st.success(f"Welcome back, {USERS_CONFIG[username_input]['name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        with st.expander("💡 Quick Demo Credentials & Role Access List"):
            st.markdown("""
            | Role | Username | Password | Access Scope |
            | :--- | :--- | :--- | :--- |
            | **👑 System Admin** | `sysadmin` | `admin123` | **Full System & Role Switcher Access** |
            | **🛡️ MEL Admin** | `mel_admin` | `mel2050` | **Cross-TAG Review & Approval Queue** |
            | **🏛️ TA1 Lead** | `ta1_lead` | `ta1_pass` | Political Leadership & Regionalism TAG |
            | **👥 TA2 Lead** | `ta2_lead` | `ta2_pass` | People-Centred Development TAG |
            | **🛡️ TA3 Lead** | `ta3_lead` | `ta3_pass` | Peace & Security TAG |
            | **📈 TA4 Lead** | `ta4_lead` | `ta4_pass` | Resource & Economic Development TAG |
            | **🌪️ TA5 Lead** | `ta5_lead` | `ta5_pass` | Climate Change & Disasters TAG |
            | **🌊 TA6 Lead** | `ta6_lead` | `ta6_pass` | Ocean & Natural Environment TAG |
            | **⚡ TA7 Lead** | `ta7_lead` | `ta7_pass` | Technology & Connectivity TAG |
            """)

# -----------------------------------------------------------------------------
# MAIN APPLICATION AFTER AUTHENTICATION
# -----------------------------------------------------------------------------
if not st.session_state["authenticated"]:
    render_login_page()
else:
    user = st.session_state["user_info"]
    role = user["role"]
    username = st.session_state["username"]

    # System Admin Impersonation / View Override Option
    view_as_tag = user["tag_name"]
    active_role = role
    
    # Sidebar Navigation & User Profile Block
    st.sidebar.markdown(f"### 👤 Logged in as:")
    st.sidebar.info(f"**{user['name']}**\n\n**Role:** `{user['badge']}`")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["user_info"] = None
        st.rerun()

    st.sidebar.markdown("---")

    # If System Admin, allow impersonating any TAG or MEL view
    if role == "System Admin":
        st.sidebar.subheader("👑 System Admin Impersonator")
        selected_view_mode = st.sidebar.selectbox("Switch View Profile:", [
            "System Admin (Global Access)",
            "MEL Secretariat Admin View",
            "Political Leadership & Regionalism TAG (TA1)",
            "People-Centred Development TAG (TA2)",
            "Peace & Security TAG (TA3)",
            "Resource & Economic Development TAG (TA4)",
            "Climate Change & Disasters TAG (TA5)",
            "Ocean & Natural Environment TAG (TA6)",
            "Technology & Connectivity TAG (TA7)"
        ])
        
        if "TA1" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta1_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "TA2" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta2_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "TA3" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta3_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "TA4" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta4_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "TA5" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta5_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "TA6" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta6_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "TA7" in selected_view_mode:
            view_as_tag = USERS_CONFIG["ta7_lead"]["tag_name"]
            active_role = "TAG Focal Point"
        elif "MEL Secretariat" in selected_view_mode:
            view_as_tag = "All Thematic Areas (MEL Reviewer)"
            active_role = "MEL Admin"

    st.sidebar.title("Portal Navigation")
    
    # Navigation module options based on active role
    if active_role == "TAG Focal Point":
        nav_options = [
            "1. My TAG Profile & Mini Dashboard",
            "2. My TAG Submissions History",
            "3. Submit New TAG Progress Update",
            "4. System Architecture & Guide"
        ]
    else:
        nav_options = [
            "1. Executive Monitoring Dashboard V2",
            "2. TAG Submissions & AI Review Queue",
            "3. Submit New TAG Progress Update",
            "4. Indicator & Results Management",
            "5. Strategic Data Model (Dataverse Mirror)",
            "6. System Architecture & Guide"
        ]

    module = st.sidebar.radio("Select Portal Page:", nav_options)

    # -------------------------------------------------------------------------
    # MODULE 1: TAG PROFILE & MINI DASHBOARD (FOR TAG LEADS) OR GLOBAL DASHBOARD
    # -------------------------------------------------------------------------
    if "My TAG Profile" in module or module == "1. Executive Monitoring Dashboard V2":
        
        if active_role == "TAG Focal Point":
            # Find matching tag config
            tag_cfg = None
            for u_k, u_v in USERS_CONFIG.items():
                if u_v.get("tag_name") == view_as_tag:
                    tag_cfg = u_v
                    break
            
            if not tag_cfg:
                tag_cfg = USERS_CONFIG["ta1_lead"] # default fallback

            # Custom Tag Header Banner
            st.markdown(f"""
            <div class="tag-banner" style="background: {tag_cfg['banner_bg']};">
                <h1 style="margin:0; font-size:2.2rem; color:white;">{tag_cfg['icon']} {tag_cfg['tag_name']}</h1>
                <p style="font-size:1.1rem; margin-top:5px; font-style:italic; opacity:0.95;">"{tag_cfg['motto']}"</p>
                <div style="margin-top:15px; font-size:0.95rem;">
                    <span><b>TAG Lead Agency:</b> {tag_cfg['name']}</span> | 
                    <span><b>Security Status:</b> Authenticated TAG Portal</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader(f"📊 {tag_cfg['icon']} My TAG Performance & Submissions Analytics")
            
            conn = get_db_connection()
            
            # Fetch TAG-isolated submissions
            df_my_subs = pd.read_sql_query("""
                SELECT submission_id, submission_title, reporting_period, actual_value, submission_status, review_decision, submitted_on, ai_draft_generated_on
                FROM practice_tag_submissions
                WHERE tag_name = ?
                ORDER BY submission_id DESC
            """, conn, params=(view_as_tag,))

            c1, c2, c3, c4 = st.columns(4)
            total_my_subs = len(df_my_subs)
            approved_count = len(df_my_subs[df_my_subs["submission_status"] == "Approved"])
            review_count = len(df_my_subs[df_my_subs["submission_status"] == "Awaiting Human Review"])
            returned_count = len(df_my_subs[df_my_subs["submission_status"] == "Returned for Clarification"])

            with c1:
                st.metric("Total Submissions Logged", total_my_subs)
            with c2:
                st.metric("Approved Submissions", approved_count, delta="Verified" if approved_count > 0 else None)
            with c3:
                st.metric("Awaiting MEL Review", review_count, delta="In Queue" if review_count > 0 else None)
            with c4:
                st.metric("Returned / Action Needed", returned_count, delta="Action Req" if returned_count > 0 else "Clean")

            st.markdown("---")

            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown("#### 🍩 Submissions Lifecycle Breakdown")
                if not df_my_subs.empty:
                    df_status_cnt = df_my_subs["submission_status"].value_counts().reset_index()
                    df_status_cnt.columns = ["Status", "Count"]
                    fig_donut = px.pie(df_status_cnt, names="Status", values="Count", hole=0.4,
                                       color="Status",
                                       color_discrete_map={
                                           'Draft': '#A0A0A0',
                                           'Submitted': '#2F5496',
                                           'Awaiting Human Review': '#FFC107',
                                           'Approved': '#28A745',
                                           'Returned for Clarification': '#DC3545'
                                       })
                    fig_donut.update_layout(height=320, margin=dict(t=20, b=20, l=20, r=20))
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:
                    st.info("No submission records logged yet for your TAG.")

            with col_chart2:
                st.markdown("#### 📈 Reported Progress vs. Indicator Benchmark")
                # Get related indicator result
                df_ind_res = pd.read_sql_query("""
                    SELECT i.indicator_name, r.actual_value, r.target_value, r.reporting_period
                    FROM practice_indicators i
                    JOIN practice_outcomes o ON i.outcome_id = o.outcome_id
                    JOIN practice_monitoring_results r ON i.indicator_id = r.indicator_id
                    WHERE i.indicator_id = ?
                """, conn, params=(f"IND0{tag_cfg['tag_id'][-1]}",))

                if not df_ind_res.empty:
                    act_val = df_ind_res.iloc[0]['actual_value']
                    tgt_val = df_ind_res.iloc[0]['target_value']
                    ind_lbl = df_ind_res.iloc[0]['indicator_name']

                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = act_val,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': f"{ind_lbl[:30]}..."},
                        delta = {'reference': tgt_val, 'relative': False},
                        gauge = {
                            'axis': {'range': [0, max(tgt_val * 1.2, 100)]},
                            'bar': {'color': tag_cfg['primary_color']},
                            'steps': [
                                {'range': [0, tgt_val * 0.5], 'color': "#F8D7DA"},
                                {'range': [tgt_val * 0.5, tgt_val], 'color': "#FFF3CD"},
                                {'range': [tgt_val, max(tgt_val * 1.2, 100)], 'color': "#D4EDDA"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': tgt_val
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=320, margin=dict(t=30, b=20, l=30, r=30))
                    st.plotly_chart(fig_gauge, use_container_width=True)
                else:
                    st.info("Indicator metrics initializing...")

            conn.close()

        else:
            # Executive Global Dashboard (MEL Admin & System Admin)
            st.header("📊 2050 Executive Monitoring Dashboard V2")
            st.caption("Cross-Cutting Regional Analysis across all 7 Thematic Advisory Groups (TAGs)")

            conn = get_db_connection()

            col1, col2, col3, col4 = st.columns(4)
            total_outcomes = conn.execute("SELECT COUNT(*) FROM practice_outcomes").fetchone()[0]
            total_indicators = conn.execute("SELECT COUNT(*) FROM practice_indicators").fetchone()[0]
            total_submissions = conn.execute("SELECT COUNT(*) FROM practice_tag_submissions").fetchone()[0]
            awaiting_review = conn.execute("SELECT COUNT(*) FROM practice_tag_submissions WHERE submission_status = 'Awaiting Human Review'").fetchone()[0]

            with col1:
                st.metric("Practice Outcomes Tracked", total_outcomes)
            with col2:
                st.metric("Core Regional Indicators", total_indicators)
            with col3:
                st.metric("Total TAG Submissions", total_submissions)
            with col4:
                st.metric("Awaiting Human Review", awaiting_review, delta="Action Required" if awaiting_review > 0 else "Clear")

            st.markdown("---")

            col_left, col_right = st.columns(2)

            with col_left:
                st.subheader("Actual vs Target Performance across Indicators")
                df_results = pd.read_sql_query("""
                    SELECT r.result_name, i.indicator_name, r.actual_value, r.target_value, r.reporting_period
                    FROM practice_monitoring_results r
                    JOIN practice_indicators i ON r.indicator_id = i.indicator_id
                """, conn)

                if not df_results.empty:
                    fig_bar = go.Figure()
                    fig_bar.add_trace(go.Bar(x=df_results['result_name'], y=df_results['actual_value'], name='Actual Value', marker_color='#1F4E79'))
                    fig_bar.add_trace(go.Bar(x=df_results['result_name'], y=df_results['target_value'], name='Target Value', marker_color='#2F5496', opacity=0.4))
                    fig_bar.update_layout(barmode='group', height=380)
                    st.plotly_chart(fig_bar, use_container_width=True)

            with col_right:
                st.subheader("Submissions Status Breakdown across 7 TAGs")
                df_status = pd.read_sql_query("SELECT submission_status, COUNT(*) as count FROM practice_tag_submissions GROUP BY submission_status", conn)
                if not df_status.empty:
                    fig_pie = px.pie(df_status, names='submission_status', values='count', color='submission_status',
                                     color_discrete_map={
                                         'Draft': '#A0A0A0',
                                         'Submitted': '#2F5496',
                                         'Awaiting Human Review': '#FFC107',
                                         'Approved': '#28A745',
                                         'Returned for Clarification': '#DC3545'
                                     })
                    fig_pie.update_layout(height=380)
                    st.plotly_chart(fig_pie, use_container_width=True)

            conn.close()

    # -------------------------------------------------------------------------
    # MODULE 2: SUBMISSIONS HISTORY / AI REVIEW QUEUE
    # -------------------------------------------------------------------------
    elif "Submissions History" in module or module == "2. TAG Submissions & AI Review Queue":
        
        conn = get_db_connection()

        if active_role == "TAG Focal Point":
            st.header(f"📝 My TAG Submissions History")
            st.caption(f"Role-Isolated View: Filtered strictly for {view_as_tag}")

            df_subs = pd.read_sql_query("""
                SELECT submission_id, submission_title, reporting_period, actual_value, submission_status, review_decision, submitted_on
                FROM practice_tag_submissions
                WHERE tag_name = ?
                ORDER BY submission_id DESC
            """, conn, params=(view_as_tag,))

            st.dataframe(df_subs, use_container_width=True)

            st.markdown("---")
            st.subheader("🔍 Inspect Detailed Submission Record")
            
            sub_id_list = df_subs['submission_id'].tolist() if not df_subs.empty else []
            selected_id = st.selectbox("Select Submission to View:", sub_id_list) if sub_id_list else None

            if selected_id:
                sub = conn.execute("SELECT * FROM practice_tag_submissions WHERE submission_id = ?", (selected_id,)).fetchone()

                st.markdown(f"""
                <div class="card-box">
                    <h4>{sub['submission_title']}</h4>
                    <p><b>Reporting Period:</b> {sub['reporting_period']} | <b>Reported Actual:</b> {sub['actual_value']}</p>
                    <p><b>Submission Status:</b> <span class="status-badge badge-submitted">{sub['submission_status']}</span> | <b>Review Decision:</b> {sub['review_decision']}</p>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### 📄 Submitted Source Narrative")
                    st.info(sub["narrative_update"])
                    st.caption(f"**Evidence Link:** {sub['evidence_reference'] or 'None provided'}")
                with col_b:
                    st.markdown("#### 🤖 AI Review & Secretariat Feedback")
                    if sub["ai_interpretation"]:
                        st.warning(sub["ai_interpretation"])
                    else:
                        st.info("Awaiting AI processing / Secretariat review.")
                    if sub["reviewer_comments"]:
                        st.success(f"**MEL Reviewer Comments:** {sub['reviewer_comments']}")

        else:
            # MEL Admin & System Admin Full Review Queue
            st.header("📝 TAG Submissions & AI Review Queue")
            st.caption("Inspect Narrative Submissions across All 7 TAGs, Trigger AI Processing, and Execute Approvals")

            selected_tag_filter = st.selectbox("Filter Queue by TAG:", ["All TAGs"] + [
                "Political Leadership & Regionalism TAG",
                "People-Centred Development TAG",
                "Peace & Security TAG",
                "Resource & Economic Development TAG",
                "Climate Change & Disasters TAG",
                "Ocean & Natural Environment TAG",
                "Technology & Connectivity TAG"
            ])

            if selected_tag_filter == "All TAGs":
                df_subs = pd.read_sql_query("SELECT submission_id, submission_title, tag_name, reporting_period, actual_value, submission_status, review_decision FROM practice_tag_submissions ORDER BY submission_id DESC", conn)
            else:
                df_subs = pd.read_sql_query("SELECT submission_id, submission_title, tag_name, reporting_period, actual_value, submission_status, review_decision FROM practice_tag_submissions WHERE tag_name = ? ORDER BY submission_id DESC", conn, params=(selected_tag_filter,))

            st.dataframe(df_subs, use_container_width=True)

            st.markdown("---")
            st.subheader("🔍 Review & Approval Panel")

            sub_id_list = df_subs['submission_id'].tolist() if not df_subs.empty else []
            selected_id = st.selectbox("Select Record to Review:", sub_id_list) if sub_id_list else None

            if selected_id:
                sub = conn.execute("SELECT * FROM practice_tag_submissions WHERE submission_id = ?", (selected_id,)).fetchone()

                st.markdown(f"""
                <div class="card-box">
                    <h4>{sub['submission_title']}</h4>
                    <p><b>TAG:</b> {sub['tag_name']} | <b>Period:</b> {sub['reporting_period']} | <b>Actual Value:</b> {sub['actual_value']}</p>
                    <p><b>Status:</b> {sub['submission_status']} | <b>Decision:</b> {sub['review_decision']}</p>
                </div>
                """, unsafe_allow_html=True)

                col_nav1, col_nav2 = st.columns(2)

                with col_nav1:
                    st.markdown("### 📄 Submitted Source Narrative")
                    st.info(sub["narrative_update"])
                    st.caption(f"**Evidence:** {sub['evidence_reference'] or 'None provided'}")

                    if sub["submission_status"] in ["Draft", "Submitted"]:
                        if st.button("⚡ Trigger AI Interpretation Workflow"):
                            success, msg = run_ai_interpretation_workflow(selected_id)
                            if success:
                                st.success(msg)
                                st.rerun()

                with col_nav2:
                    st.markdown("### 🤖 AI Draft Interpretation Output")
                    if sub["ai_interpretation"]:
                        st.warning(sub["ai_interpretation"])
                    else:
                        st.info("No AI draft generated yet.")

                st.markdown("---")
                st.markdown("### ✍️ Authorised MEL Reviewer Decision")

                with st.form("human_review_form"):
                    reviewer_comments = st.text_area("Reviewer Audit Comments:", value=sub["reviewer_comments"] or "")
                    new_decision = st.selectbox("Set Review Decision:", ["Pending", "Approved", "Returned for Clarification"],
                                                 index=["Pending", "Approved", "Returned for Clarification"].index(sub["review_decision"] if sub["review_decision"] in ["Pending", "Approved", "Returned for Clarification"] else "Pending"))

                    submit_review = st.form_submit_button("Save Review Decision & Update Status")

                    if submit_review:
                        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        new_status = sub["submission_status"]
                        if new_decision == "Approved":
                            new_status = "Approved"
                        elif new_decision == "Returned for Clarification":
                            new_status = "Returned for Clarification"

                        conn.execute("""
                            UPDATE practice_tag_submissions
                            SET reviewer_comments = ?, review_decision = ?, submission_status = ?, reviewed_on = ?
                            WHERE submission_id = ?
                        """, (reviewer_comments, new_decision, new_status, now_str, selected_id))
                        conn.commit()
                        st.success(f"Decision saved! Record status updated to '{new_status}'.")
                        st.rerun()

        conn.close()

    # -------------------------------------------------------------------------
    # MODULE 3: NEW TAG SUBMISSION ENTRY
    # -------------------------------------------------------------------------
    elif "Submit New TAG" in module:
        st.header("➕ Create New TAG Progress Submission")
        st.caption("Submit new qualitative narrative updates and performance numbers into the MEL pipeline")

        conn = get_db_connection()
        indicators = conn.execute("SELECT indicator_id, indicator_name FROM practice_indicators").fetchall()
        ind_options = {f"{ind['indicator_id']} - {ind['indicator_name']}": ind['indicator_id'] for ind in indicators}

        with st.form("new_submission_form"):
            title = st.text_input("Submission Title:", f"{view_as_tag if active_role == 'TAG Focal Point' else 'Practice'} – Q4 2026 Progress Submission")
            
            if active_role == "TAG Focal Point":
                st.text_input("Assigned TAG Name:", view_as_tag, disabled=True)
                tag_name = view_as_tag
            else:
                tag_name = st.selectbox("Select TAG Name:", [
                    "Political Leadership & Regionalism TAG",
                    "People-Centred Development TAG",
                    "Peace & Security TAG",
                    "Resource & Economic Development TAG",
                    "Climate Change & Disasters TAG",
                    "Ocean & Natural Environment TAG",
                    "Technology & Connectivity TAG"
                ])

            period = st.selectbox("Reporting Period:", ["2026 Q4", "2026 Annual", "2027 Q1"])
            selected_ind_key = st.selectbox("Related Core Indicator:", list(ind_options.keys()) if ind_options else ["None"])
            ind_id = ind_options.get(selected_ind_key) if ind_options else None
            actual_val = st.number_input("Reported Actual Value:", value=65.0, step=0.5)
            narrative = st.text_area("Qualitative Narrative Update (Source Text):",
                                     "During the reporting period, targeted regional actions were accelerated across member countries. Key milestones achieved include expanded technical capacity building and baseline survey completions.")
            evidence_url = st.text_input("Evidence Reference Link / Document Code:", "PIFS-2026-Q4-Sample-Evidence")

            initial_status = st.selectbox("Save Initial Status As:", ["Draft", "Submitted"])

            submit_btn = st.form_submit_button("Save Submission Record")

            if submit_btn:
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                submitted_timestamp = now_str if initial_status == "Submitted" else None

                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO practice_tag_submissions (
                        submission_title, tag_name, reporting_period, indicator_id, actual_value,
                        narrative_update, evidence_reference, submission_status, submitted_on
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (title, tag_name, period, ind_id, actual_val, narrative, evidence_url, initial_status, submitted_timestamp))
                conn.commit()
                new_id = cursor.lastrowid

                st.success(f"Submission created successfully with ID #{new_id}!")

                if initial_status == "Submitted":
                    st.info("Triggering AI workflow equivalent...")
                    success, msg = run_ai_interpretation_workflow(new_id)
                    if success:
                        st.success(f"AI Workflow triggered: {msg}")

                conn.close()

    # -------------------------------------------------------------------------
    # MODULE 4: INDICATOR MANAGEMENT (MEL / SYSTEM ADMIN)
    # -------------------------------------------------------------------------
    elif "Indicator & Results" in module:
        st.header("📈 Practice Indicators & Monitoring Results")
        st.caption("Manage Practice Indicators, Units, Frequencies, and Actual/Target Results")

        conn = get_db_connection()
        tab1, tab2 = st.tabs(["Practice Indicators", "Monitoring Results"])

        with tab1:
            df_ind = pd.read_sql_query("SELECT * FROM practice_indicators", conn)
            st.dataframe(df_ind, use_container_width=True)

        with tab2:
            df_res = pd.read_sql_query("SELECT * FROM practice_monitoring_results", conn)
            st.dataframe(df_res, use_container_width=True)

        conn.close()

    # -------------------------------------------------------------------------
    # MODULE 5: DATA MODEL INSPECTOR (SYSTEM ADMIN)
    # -------------------------------------------------------------------------
    elif "Strategic Data Model" in module:
        st.header("🗄️ Relational Data Model (Dataverse Mirror)")
        st.caption("Inspect the 9 linked Dataverse tables mirroring Strategic Context, Implementation, and Monitoring")

        conn = get_db_connection()
        table_choice = st.selectbox("Select Dataverse Table to Inspect:", [
            "practice_thematic_areas",
            "national_priorities",
            "practice_outcomes",
            "practice_leaders_decisions",
            "practice_rcas",
            "practice_regional_initiatives",
            "practice_indicators",
            "practice_monitoring_results",
            "practice_tag_submissions"
        ])

        df_table = pd.read_sql_query(f"SELECT * FROM {table_choice}", conn)
        st.write(f"**Table Name:** `{table_choice}` | **Total Rows:** {len(df_table)}")
        st.dataframe(df_table, use_container_width=True)
        conn.close()

    # -------------------------------------------------------------------------
    # MODULE 6: ARCHITECTURE & GUIDE
    # -------------------------------------------------------------------------
    elif "System Architecture" in module:
        st.header("📚 System Architecture & Authentication Guide")
        st.markdown("""
        ### Multi-User Role & Security Architecture
        
        | Role | Default User | Access Scope & Capabilities |
        | :--- | :--- | :--- |
        | **System Admin** | `sysadmin` | **Universal Access:** Can view/edit all 7 TAG profiles, switch roles dynamically, manage raw database tables, and run system diagnostics. |
        | **MEL Admin** | `mel_admin` | **Secretariat View:** Access to cross-cutting regional dashboards, AI review queue, submission approvals/returns, and indicator targets. |
        | **TAG Lead (x7)** | `ta1_lead` to `ta7_lead` | **Role-Isolated View:** Restricted strictly to their respective TAG data, custom banner profile, local mini-dashboard, and submission forms. |

        ---

        ### Database & Storage Architecture
        - **Relational Database:** SQLite (`2050_practice_monitoring.db`) hosting 9 Dataverse-mirror core tables.
        - **AI Review Engine:** Automated workflow generating structured 6-section evaluation drafts upon submission while preserving original submitter narratives verbatim.
        - **Session Management:** Streamlit Session State (`st.session_state`) maintaining secure role-based navigation and login state.
        """)

st.sidebar.markdown("---")
st.sidebar.caption("Pacific Islands Forum Secretariat (PIFS) Data & Analytics Advisory")

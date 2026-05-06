import streamlit as st
import json
import random
import sqlite3
import hashlib
import os
import math
import re
from datetime import datetime, timedelta
from collections import defaultdict

st.set_page_config(
    page_title="SecureFlow - Workflow Governance",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #1a1a18;
    color: #f0ebe0;
}

section[data-testid="stSidebar"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.sf-hero {
    background: linear-gradient(135deg, #1a1a18 0%, #2d2d1e 50%, #1a1a18 100%);
    padding: 80px 60px;
    text-align: center;
    border-bottom: 1px solid #3d3d2a;
    position: relative;
    overflow: hidden;
}

.sf-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(180,160,80,0.08) 0%, transparent 60%);
    pointer-events: none;
}

.sf-hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 72px;
    font-weight: 900;
    color: #f0ebe0;
    letter-spacing: -2px;
    line-height: 1.1;
    margin-bottom: 16px;
    text-transform: uppercase;
}

.sf-hero-accent {
    color: #c8a84b;
    font-style: italic;
}

.sf-hero-sub {
    font-size: 16px;
    color: #a09070;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 40px;
}

.sf-topnav {
    background: #111110;
    padding: 18px 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2a2a1a;
    position: sticky;
    top: 0;
    z-index: 999;
}

.sf-topnav-brand {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    color: #f0ebe0;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.sf-topnav-brand span {
    color: #c8a84b;
}

.sf-pill-nav {
    display: flex;
    gap: 4px;
    background: #1a1a18;
    border-radius: 50px;
    padding: 4px;
    border: 1px solid #3d3d2a;
    flex-wrap: wrap;
    justify-content: center;
    margin: 20px auto;
    max-width: 900px;
}

.sf-pill-btn {
    background: transparent;
    border: none;
    color: #a09070;
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.2s;
}

.sf-pill-btn:hover, .sf-pill-btn.active {
    background: #c8a84b;
    color: #1a1a18;
}

.sf-card {
    background: #222218;
    border: 1px solid #3d3d2a;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.sf-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c8a84b, #a07830);
    border-radius: 16px 16px 0 0;
}

.sf-card:hover {
    border-color: #c8a84b;
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(200,168,75,0.1);
}

.sf-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #f0ebe0;
    margin-bottom: 8px;
}

.sf-card-sub {
    font-size: 12px;
    color: #a09070;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
}

.sf-metric {
    background: #1a1a18;
    border: 1px solid #3d3d2a;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.sf-metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 900;
    color: #c8a84b;
    line-height: 1;
    margin-bottom: 6px;
}

.sf-metric-label {
    font-size: 11px;
    color: #a09070;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.sf-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.sf-badge-pass { background: rgba(100,200,100,0.15); color: #6dc86d; border: 1px solid #6dc86d; }
.sf-badge-warn { background: rgba(200,168,75,0.15); color: #c8a84b; border: 1px solid #c8a84b; }
.sf-badge-fail { background: rgba(220,80,80,0.15); color: #dc5050; border: 1px solid #dc5050; }
.sf-badge-pending { background: rgba(100,140,200,0.15); color: #6494c8; border: 1px solid #6494c8; }
.sf-badge-critical { background: rgba(220,50,50,0.2); color: #ff6060; border: 1px solid #ff4040; }
.sf-badge-high { background: rgba(220,120,50,0.2); color: #ff9050; border: 1px solid #ff7030; }
.sf-badge-medium { background: rgba(220,180,50,0.15); color: #c8a84b; border: 1px solid #c8a84b; }
.sf-badge-low { background: rgba(100,200,100,0.15); color: #6dc86d; border: 1px solid #6dc86d; }

.sf-btn-primary {
    background: #c8a84b;
    color: #1a1a18;
    border: none;
    padding: 14px 32px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-block;
}

.sf-btn-primary:hover {
    background: #e0c060;
    transform: translateY(-1px);
}

.sf-section-header {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 900;
    color: #f0ebe0;
    text-align: center;
    margin: 40px 0 8px 0;
    letter-spacing: -1px;
}

.sf-section-sub {
    text-align: center;
    color: #a09070;
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 32px;
}

.sf-divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #c8a84b, #a07830);
    margin: 0 auto 32px auto;
    border-radius: 3px;
}

.sf-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.sf-table th {
    background: #1a1a18;
    color: #a09070;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 11px;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid #3d3d2a;
}

.sf-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #2a2a1a;
    color: #d0c8b0;
    vertical-align: middle;
}

.sf-table tr:hover td {
    background: rgba(200,168,75,0.04);
}

.sf-input-wrapper {
    position: relative;
    margin-bottom: 16px;
}

.sf-alert-box {
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 14px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.sf-alert-success {
    background: rgba(100,200,100,0.08);
    border: 1px solid rgba(100,200,100,0.3);
    color: #6dc86d;
}

.sf-alert-danger {
    background: rgba(220,80,80,0.08);
    border: 1px solid rgba(220,80,80,0.3);
    color: #dc5050;
}

.sf-alert-warning {
    background: rgba(200,168,75,0.08);
    border: 1px solid rgba(200,168,75,0.3);
    color: #c8a84b;
}

.sf-alert-info {
    background: rgba(100,140,200,0.08);
    border: 1px solid rgba(100,140,200,0.3);
    color: #6494c8;
}

.sf-progress-bar {
    height: 8px;
    background: #2a2a1a;
    border-radius: 50px;
    overflow: hidden;
    margin: 8px 0;
}

.sf-progress-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #c8a84b, #e0c060);
    transition: width 0.4s;
}

.sf-tag {
    display: inline-block;
    background: rgba(200,168,75,0.1);
    border: 1px solid rgba(200,168,75,0.3);
    color: #c8a84b;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    margin: 2px;
}

.sf-stat-row {
    display: flex;
    gap: 12px;
    margin: 12px 0;
}

.sf-login-wrap {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1a1a18;
    background-image: radial-gradient(ellipse at 50% 0%, rgba(200,168,75,0.08) 0%, transparent 60%);
    padding: 40px;
}

.sf-login-card {
    background: #222218;
    border: 1px solid #3d3d2a;
    border-radius: 24px;
    padding: 56px 48px;
    width: 100%;
    max-width: 460px;
    text-align: center;
}

.sf-gauge-wrap {
    position: relative;
    display: inline-block;
}

.sf-full-page {
    min-height: 100vh;
    background: #1a1a18;
}

.sf-page-content {
    padding: 32px 48px;
}

.stButton > button {
    background: #c8a84b !important;
    color: #1a1a18 !important;
    border: none !important;
    border-radius: 50px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    width: auto !important;
}

.stButton > button:hover {
    background: #e0c060 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(200,168,75,0.3) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #1a1a18 !important;
    border: 1px solid #3d3d2a !important;
    color: #f0ebe0 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #c8a84b !important;
    box-shadow: 0 0 0 2px rgba(200,168,75,0.2) !important;
}

.stNumberInput > div > div > input {
    background: #1a1a18 !important;
    border: 1px solid #3d3d2a !important;
    color: #f0ebe0 !important;
    border-radius: 12px !important;
}

div[data-testid="stExpander"] {
    background: #222218 !important;
    border: 1px solid #3d3d2a !important;
    border-radius: 12px !important;
}

div[data-testid="stExpander"] summary {
    color: #f0ebe0 !important;
    font-weight: 600 !important;
}

div[data-testid="stExpander"] > div {
    background: #1a1a18 !important;
    border-radius: 0 0 12px 12px !important;
}

.stSlider > div > div > div > div {
    background: #c8a84b !important;
}

.stCheckbox > label > span:first-child {
    border-color: #3d3d2a !important;
}

.stRadio > div > label {
    color: #d0c8b0 !important;
}

.stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label, .stSlider label {
    color: #a09070 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}

div[data-testid="stFileUploader"] {
    background: #1a1a18 !important;
    border: 2px dashed #3d3d2a !important;
    border-radius: 16px !important;
}

div[data-testid="stFileUploader"]:hover {
    border-color: #c8a84b !important;
}

div[data-testid="metric-container"] {
    background: #222218 !important;
    border: 1px solid #3d3d2a !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

div[data-testid="metric-container"] label {
    color: #a09070 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #c8a84b !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 36px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #1a1a18 !important;
    border-radius: 50px !important;
    padding: 4px !important;
    border: 1px solid #3d3d2a !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 50px !important;
    color: #a09070 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    background: #c8a84b !important;
    color: #1a1a18 !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding: 20px 0 !important;
}

.stDataFrame {
    border: 1px solid #3d3d2a !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

.element-container:has(.stDataFrame) {
    background: #222218 !important;
    border-radius: 12px !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #f0ebe0 !important;
    font-family: 'Playfair Display', serif !important;
}

p, li, span, div {
    color: #d0c8b0;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1a1a18; }
::-webkit-scrollbar-thumb { background: #3d3d2a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c8a84b; }

.stAlert { border-radius: 12px !important; }
[data-testid="stMarkdownContainer"] { color: #d0c8b0 !important; }
.stSpinner > div { border-top-color: #c8a84b !important; }

.sf-3d-card {
    background: linear-gradient(145deg, #262618, #1e1e14);
    border: 1px solid #3d3d2a;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 6px 6px 12px rgba(0,0,0,0.4), -2px -2px 6px rgba(200,168,75,0.05);
    transition: all 0.3s;
}

.sf-3d-card:hover {
    transform: perspective(1000px) rotateX(1deg) rotateY(-1deg) translateY(-4px);
    box-shadow: 12px 16px 24px rgba(0,0,0,0.5), -4px -4px 12px rgba(200,168,75,0.08);
}

.sf-risk-ring {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    margin: 0 auto;
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 900;
}

.sf-timeline-item {
    display: flex;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid #2a2a1a;
    align-items: flex-start;
}

.sf-timeline-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #c8a84b;
    margin-top: 5px;
    flex-shrink: 0;
}

.sf-timeline-dot.red { background: #dc5050; }
.sf-timeline-dot.green { background: #6dc86d; }
.sf-timeline-dot.blue { background: #6494c8; }

.sf-flow-node {
    display: inline-block;
    background: #1a1a18;
    border: 2px solid #3d3d2a;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    color: #d0c8b0;
    position: relative;
}

.sf-flow-node.active { border-color: #c8a84b; color: #c8a84b; }
.sf-flow-node.risk { border-color: #dc5050; color: #dc5050; }
.sf-flow-node.pass { border-color: #6dc86d; color: #6dc86d; }

.sf-arrow {
    display: inline-block;
    color: #3d3d2a;
    margin: 0 6px;
    font-size: 18px;
}

.sf-world-map-placeholder {
    background: linear-gradient(135deg, #222218, #1a1a18);
    border: 1px solid #3d3d2a;
    border-radius: 16px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #a09070;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
    position: relative;
    overflow: hidden;
}

[data-testid="stSidebar"] {
    display: none !important;
    width: 0 !important;
}

.css-1d391kg { display: none !important; }
</style>
""", unsafe_allow_html=True)

DB_PATH = "secureflow.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'analyst',
        email TEXT,
        created_at TEXT,
        last_login TEXT,
        is_active INTEGER DEFAULT 1
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS workflows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        owner TEXT,
        trigger_type TEXT,
        frequency TEXT,
        version TEXT DEFAULT '1.0',
        status TEXT DEFAULT 'active',
        step_count INTEGER DEFAULT 0,
        source_format TEXT DEFAULT 'manual',
        created_by INTEGER,
        created_at TEXT,
        updated_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS workflow_steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workflow_id INTEGER,
        step_name TEXT,
        step_type TEXT,
        sequence_num INTEGER,
        owner TEXT,
        dependency TEXT,
        description TEXT,
        FOREIGN KEY(workflow_id) REFERENCES workflows(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS rule_sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        created_by INTEGER,
        created_at TEXT,
        is_active INTEGER DEFAULT 1
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_set_id INTEGER,
        name TEXT,
        category TEXT,
        severity TEXT,
        weight REAL,
        description TEXT,
        threshold TEXT,
        FOREIGN KEY(rule_set_id) REFERENCES rule_sets(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workflow_id INTEGER,
        rule_set_id INTEGER,
        analyst_id INTEGER,
        compliance_result TEXT,
        risk_score REAL,
        violation_count INTEGER,
        executed_at TEXT,
        notes TEXT,
        FOREIGN KEY(workflow_id) REFERENCES workflows(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER,
        step_name TEXT,
        severity TEXT,
        message TEXT,
        mitigation_status TEXT DEFAULT 'unresolved',
        recommendation TEXT,
        FOREIGN KEY(assessment_id) REFERENCES assessments(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        detail TEXT,
        timestamp TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER,
        report_name TEXT,
        created_by INTEGER,
        created_at TEXT,
        report_data TEXT,
        FOREIGN KEY(assessment_id) REFERENCES assessments(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS simulations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workflow_id INTEGER,
        scenario_name TEXT,
        trigger TEXT,
        conditions TEXT,
        result TEXT,
        risk_delta REAL,
        created_by INTEGER,
        created_at TEXT,
        FOREIGN KEY(workflow_id) REFERENCES workflows(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS risk_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER,
        risk_title TEXT,
        category TEXT,
        severity TEXT,
        status TEXT DEFAULT 'open',
        mitigation TEXT,
        accepted_by TEXT,
        updated_at TEXT,
        FOREIGN KEY(assessment_id) REFERENCES assessments(id)
    )""")
    conn.commit()

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        seed_db(conn)
    conn.close()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def seed_db(conn):
    c = conn.cursor()
    users_data = [
        ("admin_sys", hash_pw("Admin@2026"), "System Administrator", "admin", "admin@secureflow.io"),
        ("analyst_chief", hash_pw("Analyst@2026"), "Manideep Gujju", "analyst", "manideep@secureflow.io"),
        ("auditor_lead", hash_pw("Auditor@2026"), "Priya Sharma", "auditor", "priya@secureflow.io"),
        ("owner_ops", hash_pw("Owner@2026"), "Ravi Kumar", "owner", "ravi@secureflow.io"),
    ]
    for u in users_data:
        c.execute("INSERT INTO users (username, password_hash, full_name, role, email, created_at) VALUES (?,?,?,?,?,?)",
                  (u[0], u[1], u[2], u[3], u[4], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    wf_data = [
        ("Invoice Approval Workflow", "Multi-step invoice review and authorization", "Finance Team", "scheduled", "daily", "2.1", "active", 6),
        ("Employee Onboarding Flow", "New hire process automation end-to-end", "HR Department", "trigger", "on-demand", "1.4", "active", 8),
        ("Access Request Handler", "User access provisioning and de-provisioning", "IT Security", "trigger", "on-demand", "3.0", "active", 5),
        ("Customer Escalation Process", "Support ticket escalation routing", "Customer Success", "event", "real-time", "1.1", "active", 7),
        ("Vendor Payment Release", "Payment approval and release workflow", "Finance Team", "scheduled", "weekly", "1.8", "active", 9),
        ("Compliance Audit Trail", "Automated compliance record generation", "Compliance Team", "scheduled", "monthly", "2.5", "active", 4),
        ("Data Backup Verification", "Automated backup integrity checks", "IT Operations", "scheduled", "nightly", "1.2", "active", 3),
        ("Contract Review Process", "Legal contract review and sign-off chain", "Legal Team", "trigger", "on-demand", "1.0", "draft", 6),
    ]
    wf_ids = []
    for w in wf_data:
        c.execute("INSERT INTO workflows (name, description, owner, trigger_type, frequency, version, status, step_count, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,1,?)",
                  (w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        wf_ids.append(c.lastrowid)

    step_types = ["trigger", "approval", "notification", "data-transfer", "conditional", "action", "audit", "transform"]
    for wf_id in wf_ids:
        c.execute("SELECT step_count FROM workflows WHERE id=?", (wf_id,))
        sc = c.fetchone()[0]
        for i in range(sc):
            c.execute("INSERT INTO workflow_steps (workflow_id, step_name, step_type, sequence_num, owner, dependency) VALUES (?,?,?,?,?,?)",
                      (wf_id, f"Step {i+1}", random.choice(step_types), i+1,
                       random.choice(["Finance Team","HR Dept","IT Security","Legal"]),
                       f"Step {i}" if i > 0 else ""))

    c.execute("INSERT INTO rule_sets (name, description, created_by, created_at, is_active) VALUES (?,?,1,?,1)",
              ("Default Governance Policy", "Standard organizational governance rules", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    rs_id = c.lastrowid
    c.execute("INSERT INTO rule_sets (name, description, created_by, created_at, is_active) VALUES (?,?,1,?,1)",
              ("Financial Compliance Rules", "Rules specific to financial workflow processes", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    rs2_id = c.lastrowid

    rules_data = [
        (rs_id, "Ownership Assignment", "ownership", "High", 20, "Every workflow must have an assigned owner"),
        (rs_id, "Minimum Steps", "structure", "Medium", 10, "Workflow must have at least 2 steps"),
        (rs_id, "Approval Gate Required", "compliance", "Critical", 25, "All financial workflows require an approval step"),
        (rs_id, "Sequential Dependencies", "structure", "Medium", 15, "Steps must have properly defined dependencies"),
        (rs_id, "No Duplicate Actions", "structure", "Low", 8, "Workflow should not contain duplicate action steps"),
        (rs_id, "Execution Frequency Defined", "governance", "Medium", 12, "Trigger and frequency must be specified"),
        (rs_id, "Audit Step Present", "compliance", "High", 18, "Audit trail step must be included in sensitive workflows"),
        (rs2_id, "Dual Approval for High Value", "compliance", "Critical", 30, "High-value transactions require dual approval"),
        (rs2_id, "Finance Owner Required", "ownership", "High", 20, "Finance workflows must have finance team owner"),
        (rs2_id, "Payment Cap Threshold", "governance", "High", 22, "Payment workflows must enforce spending limits"),
    ]
    for r in rules_data:
        c.execute("INSERT INTO rules (rule_set_id, name, category, severity, weight, description) VALUES (?,?,?,?,?,?)", r)

    assess_data = []
    for i, wf_id in enumerate(wf_ids[:6]):
        score = random.uniform(55, 98)
        result = "Pass" if score >= 80 else ("Warning" if score >= 60 else "Fail")
        vc = random.randint(0, 5)
        d = (datetime.now() - timedelta(days=random.randint(0,30))).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO assessments (workflow_id, rule_set_id, analyst_id, compliance_result, risk_score, violation_count, executed_at) VALUES (?,?,2,?,?,?,?)",
                  (wf_id, rs_id, result, round(score, 1), vc, d))
        aid = c.lastrowid
        assess_data.append((aid, wf_id, result, score, vc))

        severities = ["Low","Medium","High","Critical"]
        msgs = [
            "Missing approval gate detected in step sequence",
            "Owner assignment not found for critical step",
            "Execution frequency not defined",
            "Duplicate notification actions found",
            "Dependency chain has unresolved reference"
        ]
        for j in range(vc):
            sev = random.choice(severities)
            c.execute("INSERT INTO violations (assessment_id, step_name, severity, message, mitigation_status) VALUES (?,?,?,?,?)",
                      (aid, f"Step {j+1}", sev, random.choice(msgs), random.choice(["unresolved","accepted","mitigated"])))

    log_actions = [
        ("UPLOAD", "Uploaded Invoice Approval Workflow v2.1"),
        ("ASSESSMENT", "Ran governance assessment on Employee Onboarding Flow"),
        ("RULE_UPDATE", "Modified Approval Gate Required rule weight to 25"),
        ("EXPORT", "Exported audit report for Vendor Payment Release"),
        ("USER_CREATED", "Created new auditor account: auditor_lead"),
        ("SIMULATION", "Ran what-if simulation for Access Request Handler"),
    ]
    for action, detail in log_actions:
        c.execute("INSERT INTO audit_logs (user_id, action, detail, timestamp) VALUES (?,?,?,?)",
                  (random.choice([1,2,3]), action, detail,
                   (datetime.now() - timedelta(hours=random.randint(1, 72))).strftime("%Y-%m-%d %H:%M:%S")))

    sim_scenarios = [
        ("Reduced Frequency Scenario", "manual_trigger", '{"frequency":"weekly"}', "Pass", -8.5),
        ("No Approval Gate Test", "automated", '{"skip_approval":true}', "Fail", +22.3),
        ("Parallel Execution Test", "scheduled", '{"parallel":true}', "Warning", +5.1),
    ]
    for wf_id in wf_ids[:3]:
        for sc in sim_scenarios:
            c.execute("INSERT INTO simulations (workflow_id, scenario_name, trigger, conditions, result, risk_delta, created_by, created_at) VALUES (?,?,?,?,?,?,2,?)",
                      (wf_id, sc[0], sc[1], sc[2], sc[3], sc[4], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()

def log_action(user_id, action, detail):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO audit_logs (user_id, action, detail, timestamp) VALUES (?,?,?,?)",
              (user_id, action, detail, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def check_login(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password_hash=? AND is_active=1",
              (username, hash_pw(password)))
    user = c.fetchone()
    if user:
        c.execute("UPDATE users SET last_login=? WHERE id=?",
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user["id"]))
        conn.commit()
    conn.close()
    return dict(user) if user else None

def register_user(username, password, full_name, role, email):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Username already exists"
    c.execute("INSERT INTO users (username, password_hash, full_name, role, email, created_at) VALUES (?,?,?,?,?,?)",
              (username, hash_pw(password), full_name, role, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return True, "Account created successfully"

def get_workflows(status_filter=None):
    conn = get_db()
    c = conn.cursor()
    if status_filter:
        c.execute("SELECT * FROM workflows WHERE status=? ORDER BY created_at DESC", (status_filter,))
    else:
        c.execute("SELECT * FROM workflows ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_workflow(wf_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM workflows WHERE id=?", (wf_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_steps(wf_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM workflow_steps WHERE workflow_id=? ORDER BY sequence_num", (wf_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_rule_sets():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM rule_sets WHERE is_active=1")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_rules(rs_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM rules WHERE rule_set_id=?", (rs_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_assessments(wf_id=None):
    conn = get_db()
    c = conn.cursor()
    if wf_id:
        c.execute("""SELECT a.*, w.name as wf_name FROM assessments a 
                     LEFT JOIN workflows w ON a.workflow_id=w.id 
                     WHERE a.workflow_id=? ORDER BY a.executed_at DESC""", (wf_id,))
    else:
        c.execute("""SELECT a.*, w.name as wf_name FROM assessments a 
                     LEFT JOIN workflows w ON a.workflow_id=w.id 
                     ORDER BY a.executed_at DESC""")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_violations(assessment_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM violations WHERE assessment_id=?", (assessment_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_audit_logs(limit=50):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT al.*, u.full_name, u.username FROM audit_logs al
                 LEFT JOIN users u ON al.user_id=u.id
                 ORDER BY al.timestamp DESC LIMIT ?""", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def run_assessment_engine(workflow_id, rule_set_id, analyst_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM workflows WHERE id=?", (workflow_id,))
    wf = c.fetchone()
    if not wf:
        conn.close()
        return None
    wf = dict(wf)

    c.execute("SELECT * FROM workflow_steps WHERE workflow_id=?", (workflow_id,))
    steps = [dict(s) for s in c.fetchall()]

    c.execute("SELECT * FROM rules WHERE rule_set_id=?", (rule_set_id,))
    rules = [dict(r) for r in c.fetchall()]

    violations = []
    total_deduction = 0.0
    base_score = 100.0

    for rule in rules:
        triggered = False
        msg = ""
        if rule["category"] == "ownership":
            if not wf.get("owner") or wf["owner"].strip() == "":
                triggered = True
                msg = f"Ownership not assigned — violates '{rule['name']}'"
        elif rule["category"] == "structure":
            if "Minimum" in rule["name"] and len(steps) < 2:
                triggered = True
                msg = f"Only {len(steps)} step(s) found — '{rule['name']}' requires at least 2"
            elif "Duplicate" in rule["name"]:
                types = [s["step_type"] for s in steps]
                if len(types) != len(set(types)):
                    triggered = True
                    msg = f"Duplicate step types detected — violates '{rule['name']}'"
        elif rule["category"] == "compliance":
            if "Approval" in rule["name"]:
                has_approval = any(s["step_type"] == "approval" for s in steps)
                if not has_approval:
                    triggered = True
                    msg = f"No approval step found — '{rule['name']}' requires one"
            elif "Audit" in rule["name"]:
                has_audit = any(s["step_type"] == "audit" for s in steps)
                if not has_audit and len(steps) > 4:
                    triggered = True
                    msg = f"Audit trail step missing — violates '{rule['name']}'"
        elif rule["category"] == "governance":
            if not wf.get("trigger_type") or not wf.get("frequency"):
                triggered = True
                msg = f"Execution metadata incomplete — violates '{rule['name']}'"

        if triggered:
            sev = rule["severity"]
            violations.append({"step_name": "Workflow-Level", "severity": sev, "message": msg})
            total_deduction += rule["weight"]

    complexity_penalty = max(0, (len(steps) - 7) * 2)
    total_deduction += complexity_penalty
    if complexity_penalty > 0:
        violations.append({"step_name": "Workflow-Level", "severity": "Medium",
                            "message": f"Complex workflow with {len(steps)} steps (+{complexity_penalty:.0f} complexity penalty)"})

    if not steps:
        total_deduction += 30
        violations.append({"step_name": "Workflow-Level", "severity": "Critical",
                            "message": "Workflow has no defined steps"})

    noise = random.uniform(-2, 2)
    final_score = max(0, min(100, base_score - total_deduction + noise))
    result = "Pass" if final_score >= 80 else ("Warning" if final_score >= 60 else "Fail")

    c.execute("INSERT INTO assessments (workflow_id, rule_set_id, analyst_id, compliance_result, risk_score, violation_count, executed_at) VALUES (?,?,?,?,?,?,?)",
              (workflow_id, rule_set_id, analyst_id, result, round(final_score, 1), len(violations), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    assessment_id = c.lastrowid

    for v in violations:
        rec = "Review and address " + v["message"].split("—")[0].strip().lower()
        c.execute("INSERT INTO violations (assessment_id, step_name, severity, message, mitigation_status, recommendation) VALUES (?,?,?,?,?,?)",
                  (assessment_id, v["step_name"], v["severity"], v["message"], "unresolved", rec))

    conn.commit()
    conn.close()
    log_action(analyst_id, "ASSESSMENT", f"Ran assessment on workflow ID {workflow_id} — Result: {result} ({final_score:.1f})")
    return {"id": assessment_id, "result": result, "score": final_score, "violations": violations}

def get_dashboard_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM workflows"); total_wf = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM assessments"); total_assess = c.fetchone()[0]
    c.execute("SELECT AVG(risk_score) FROM assessments"); avg_score = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM violations WHERE mitigation_status='unresolved'"); open_risks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM rules"); total_rules = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users"); total_users = c.fetchone()[0]
    c.execute("SELECT compliance_result, COUNT(*) FROM assessments GROUP BY compliance_result")
    result_counts = {r[0]: r[1] for r in c.fetchall()}
    c.execute("SELECT workflow_id, risk_score, executed_at FROM assessments ORDER BY executed_at DESC LIMIT 20")
    trend_data = [dict(r) for r in c.fetchall()]
    conn.close()
    return {
        "total_workflows": total_wf,
        "total_assessments": total_assess,
        "avg_score": round(avg_score, 1),
        "open_risks": open_risks,
        "total_rules": total_rules,
        "total_users": total_users,
        "result_counts": result_counts,
        "trend_data": trend_data
    }

def generate_svg_gauge(score, size=160):
    if score >= 80:
        color = "#6dc86d"
    elif score >= 60:
        color = "#c8a84b"
    else:
        color = "#dc5050"

    angle = (score / 100) * 180
    r = 60
    cx, cy = size // 2, size // 2 + 10
    start_x = cx - r
    start_y = cy
    rad = math.radians(180 - angle)
    end_x = cx + r * math.cos(rad)
    end_y = cy - r * math.sin(rad)
    large_arc = 1 if angle > 180 else 0

    svg = f"""<svg width="{size}" height="{size//2 + 30}" viewBox="0 0 {size} {size//2 + 30}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g{int(score)}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:0.6"/>
      <stop offset="100%" style="stop-color:{color};stop-opacity:1"/>
    </linearGradient>
  </defs>
  <path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="#2a2a1a" stroke-width="10" stroke-linecap="round"/>
  <path d="M {cx-r} {cy} A {r} {r} 0 {large_arc} 1 {end_x:.2f} {end_y:.2f}" fill="none" stroke="url(#g{int(score)})" stroke-width="10" stroke-linecap="round"/>
  <text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="Playfair Display,serif" font-size="22" font-weight="900" fill="{color}">{score:.0f}</text>
  <text x="{cx}" y="{cy+18}" text-anchor="middle" font-family="Inter,sans-serif" font-size="9" fill="#a09070" letter-spacing="2">SCORE</text>
</svg>"""
    return svg

def generate_risk_bar_chart(assessments):
    if not assessments:
        return ""
    scores = [a.get("risk_score", 0) for a in assessments[:8]]
    names = [a.get("wf_name", f"WF {i+1}")[:14] for i, a in enumerate(assessments[:8])]
    max_s = max(scores) if scores else 100
    bar_h = 28
    bar_gap = 10
    chart_h = (bar_h + bar_gap) * len(scores) + 40
    chart_w = 420

    bars_svg = ""
    for i, (n, s) in enumerate(zip(names, scores)):
        y = 20 + i * (bar_h + bar_gap)
        bar_w = int((s / 100) * 280)
        color = "#6dc86d" if s >= 80 else ("#c8a84b" if s >= 60 else "#dc5050")
        bars_svg += f"""
  <text x="5" y="{y+18}" font-family="Inter" font-size="10" fill="#a09070">{n}</text>
  <rect x="120" y="{y+4}" width="{bar_w}" height="{bar_h-8}" rx="4" fill="{color}" opacity="0.8"/>
  <text x="{120+bar_w+6}" y="{y+18}" font-family="Inter" font-size="11" font-weight="700" fill="{color}">{s:.0f}</text>"""

    return f"""<svg width="{chart_w}" height="{chart_h}" viewBox="0 0 {chart_w} {chart_h}" xmlns="http://www.w3.org/2000/svg">
  <text x="210" y="14" text-anchor="middle" font-family="Inter" font-size="11" fill="#a09070" letter-spacing="2">RISK SCORES BY WORKFLOW</text>
  {bars_svg}
</svg>"""

def generate_donut_chart(pass_c, warn_c, fail_c):
    total = pass_c + warn_c + fail_c
    if total == 0:
        total = 1
    cx, cy, r, r2 = 80, 80, 65, 45
    def arc(start, end, color, label, val):
        if val == 0:
            return ""
        s_rad = math.radians(start - 90)
        e_rad = math.radians(end - 90)
        sx = cx + r * math.cos(s_rad)
        sy = cy + r * math.sin(s_rad)
        ex = cx + r * math.cos(e_rad)
        ey = cy + r * math.sin(e_rad)
        ix = cx + r2 * math.cos(e_rad)
        iy = cy + r2 * math.sin(e_rad)
        jx = cx + r2 * math.cos(s_rad)
        jy = cy + r2 * math.sin(s_rad)
        large = 1 if (end - start) > 180 else 0
        return f'<path d="M {sx:.1f} {sy:.1f} A {r} {r} 0 {large} 1 {ex:.1f} {ey:.1f} L {ix:.1f} {iy:.1f} A {r2} {r2} 0 {large} 0 {jx:.1f} {jy:.1f} Z" fill="{color}" opacity="0.85"/>'

    p_deg = (pass_c / total) * 360
    w_deg = (warn_c / total) * 360
    f_deg = (fail_c / total) * 360
    seg1 = arc(0, p_deg, "#6dc86d", "Pass", pass_c)
    seg2 = arc(p_deg, p_deg + w_deg, "#c8a84b", "Warn", warn_c)
    seg3 = arc(p_deg + w_deg, 360, "#dc5050", "Fail", fail_c)

    return f"""<svg width="300" height="180" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
  <text x="150" y="14" text-anchor="middle" font-family="Inter" font-size="11" fill="#a09070" letter-spacing="2">COMPLIANCE DISTRIBUTION</text>
  {seg1}{seg2}{seg3}
  <text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="Playfair Display" font-size="18" font-weight="900" fill="#f0ebe0">{total}</text>
  <text x="{cx}" y="{cy+16}" text-anchor="middle" font-family="Inter" font-size="8" fill="#a09070">TOTAL</text>
  <rect x="175" y="40" width="10" height="10" rx="2" fill="#6dc86d"/>
  <text x="190" y="50" font-family="Inter" font-size="11" fill="#d0c8b0">Pass: {pass_c}</text>
  <rect x="175" y="60" width="10" height="10" rx="2" fill="#c8a84b"/>
  <text x="190" y="70" font-family="Inter" font-size="11" fill="#d0c8b0">Warn: {warn_c}</text>
  <rect x="175" y="80" width="10" height="10" rx="2" fill="#dc5050"/>
  <text x="190" y="90" font-family="Inter" font-size="11" fill="#d0c8b0">Fail: {fail_c}</text>
</svg>"""

def generate_trend_line(trend_data):
    if not trend_data:
        return ""
    scores = [d.get("risk_score", 70) for d in reversed(trend_data[:12])]
    w, h = 380, 100
    if len(scores) < 2:
        return ""
    xs = [int(i * (w - 40) / (len(scores)-1)) + 20 for i in range(len(scores))]
    ys = [int(h - 20 - (s / 100) * (h - 30)) for s in scores]
    points = " ".join(f"{x},{y}" for x, y in zip(xs, ys))
    fill_points = f"20,{h-10} " + points + f" {w-20},{h-10}"
    return f"""<svg width="{w}" height="{h+20}" viewBox="0 0 {w} {h+20}" xmlns="http://www.w3.org/2000/svg">
  <text x="{w//2}" y="14" text-anchor="middle" font-family="Inter" font-size="10" fill="#a09070" letter-spacing="2">RISK SCORE TREND</text>
  <polygon points="{fill_points}" fill="rgba(200,168,75,0.1)"/>
  <polyline points="{points}" fill="none" stroke="#c8a84b" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  {''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="#c8a84b"/>' for x, y in zip(xs, ys))}
</svg>"""

def generate_severity_heatmap(violations_all):
    sev_map = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for v in violations_all:
        s = v.get("severity", "Low")
        if s in sev_map:
            sev_map[s] += 1
    total = sum(sev_map.values()) or 1
    colors = {"Critical": "#ff4040", "High": "#ff7030", "Medium": "#c8a84b", "Low": "#6dc86d"}
    w, h = 320, 80
    bar_w = w - 20
    x = 10
    bars = ""
    for sev, cnt in sev_map.items():
        bw = int((cnt / total) * bar_w)
        if bw > 0:
            bars += f'<rect x="{x}" y="30" width="{bw}" height="28" rx="4" fill="{colors[sev]}" opacity="0.85"/>'
            if bw > 30:
                bars += f'<text x="{x+bw//2}" y="48" text-anchor="middle" font-family="Inter" font-size="10" font-weight="700" fill="#1a1a18">{cnt}</text>'
            x += bw + 2

    legend = ""
    lx = 10
    for sev, col in colors.items():
        legend += f'<rect x="{lx}" y="65" width="8" height="8" rx="2" fill="{col}"/>'
        legend += f'<text x="{lx+11}" y="73" font-family="Inter" font-size="9" fill="#a09070">{sev}</text>'
        lx += 72

    return f"""<svg width="{w}" height="{h+10}" viewBox="0 0 {w} {h+10}" xmlns="http://www.w3.org/2000/svg">
  <text x="{w//2}" y="14" text-anchor="middle" font-family="Inter" font-size="10" fill="#a09070" letter-spacing="2">VIOLATION SEVERITY DISTRIBUTION</text>
  {bars}{legend}
</svg>"""

def generate_radar_chart(scores_dict):
    labels = list(scores_dict.keys())
    values = list(scores_dict.values())
    n = len(labels)
    if n < 3:
        return ""
    cx, cy, r = 100, 100, 75
    angles = [math.radians(360 / n * i - 90) for i in range(n)]
    web_points = []
    for level in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{cx + r*level*math.cos(a):.1f},{cy + r*level*math.sin(a):.1f}" for a in angles)
        web_points.append(f'<polygon points="{pts}" fill="none" stroke="#3d3d2a" stroke-width="1"/>')

    data_pts = " ".join(f"{cx + r*(v/100)*math.cos(a):.1f},{cy + r*(v/100)*math.sin(a):.1f}"
                        for v, a in zip(values, angles))
    label_svgs = ""
    for i, (lbl, ang) in enumerate(zip(labels, angles)):
        lx = cx + (r + 18) * math.cos(ang)
        ly = cy + (r + 18) * math.sin(ang)
        label_svgs += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Inter" font-size="9" fill="#a09070">{lbl}</text>'

    return f"""<svg width="220" height="220" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
  <text x="110" y="14" text-anchor="middle" font-family="Inter" font-size="10" fill="#a09070" letter-spacing="2">GOVERNANCE RADAR</text>
  {"".join(web_points)}
  {"".join(f'<line x1="{cx}" y1="{cy}" x2="{cx+r*math.cos(a):.1f}" y2="{cy+r*math.sin(a):.1f}" stroke="#2a2a1a" stroke-width="1"/>' for a in angles)}
  <polygon points="{data_pts}" fill="rgba(200,168,75,0.2)" stroke="#c8a84b" stroke-width="2"/>
  {"".join(f'<circle cx="{cx+r*(v/100)*math.cos(a):.1f}" cy="{cy+r*(v/100)*math.sin(a):.1f}" r="4" fill="#c8a84b"/>' for v, a in zip(values, angles))}
  {label_svgs}
</svg>"""

def render_topnav():
    user = st.session_state.get("user", {})
    role = user.get("role", "").upper()
    name = user.get("full_name", user.get("username", "User"))
    st.markdown(f"""
    <div class="sf-topnav">
        <div class="sf-topnav-brand">SECURE<span>FLOW</span></div>
        <div style="font-size:12px;color:#a09070;letter-spacing:1px;">
            {name} &nbsp;·&nbsp; <span style="color:#c8a84b;">{role}</span>
        </div>
    </div>""", unsafe_allow_html=True)

def page_login():
    st.markdown("""<div class="sf-full-page">""", unsafe_allow_html=True)
    tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        st.markdown("""
        <div style="text-align:center; padding: 40px 0 20px 0;">
            <div style="font-family:'Playfair Display',serif; font-size:52px; font-weight:900; color:#f0ebe0; letter-spacing:-2px;">
                SECURE<span style="color:#c8a84b; font-style:italic;">FLOW</span>
            </div>
            <div style="color:#a09070; font-size:12px; letter-spacing:4px; text-transform:uppercase; margin-top:8px;">
                Workflow Governance & Risk Intelligence
            </div>
        </div>""", unsafe_allow_html=True)

        col_spacer, col_form, col_spacer2 = st.columns([1, 1.2, 1])
        with col_form:
            st.markdown('<div class="sf-card">', unsafe_allow_html=True)
            st.markdown('<div class="sf-card-sub" style="text-align:center;">Authorized Access Only</div>', unsafe_allow_html=True)
            username = st.text_input("Username", key="login_user", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_pw", placeholder="Enter your password")
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("ACCESS PLATFORM", key="btn_login", use_container_width=True):
                if username and password:
                    user = check_login(username, password)
                    if user:
                        st.session_state["user"] = user
                        st.session_state["page"] = "dashboard"
                        log_action(user["id"], "LOGIN", f"User {username} signed in")
                        st.rerun()
                    else:
                        st.markdown('<div class="sf-alert-box sf-alert-danger">Invalid credentials. Please try again.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="sf-alert-box sf-alert-warning">Please enter both username and password.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="text-align:center; margin-top:24px; font-size:12px; color:#a09070; line-height:2;">
                Roles Available: Admin &nbsp;·&nbsp; Analyst &nbsp;·&nbsp; Auditor &nbsp;·&nbsp; Owner<br/>
                <span style="color:#3d3d2a;">─────────────────────────</span><br/>
                All sessions are logged and monitored.
            </div>""", unsafe_allow_html=True)

    with tab_register:
        st.markdown("""
        <div style="text-align:center; padding: 30px 0 20px 0;">
            <div style="font-family:'Playfair Display',serif; font-size:36px; font-weight:900; color:#f0ebe0;">
                Create Account
            </div>
            <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:8px;">
                Register for platform access
            </div>
        </div>""", unsafe_allow_html=True)

        col_s, col_rf, col_s2 = st.columns([1, 1.4, 1])
        with col_rf:
            st.markdown('<div class="sf-card">', unsafe_allow_html=True)
            r_fullname = st.text_input("Full Name", key="reg_name", placeholder="Your full name")
            r_email = st.text_input("Email Address", key="reg_email", placeholder="you@organization.com")
            r_username = st.text_input("Choose Username", key="reg_user", placeholder="unique username")
            r_password = st.text_input("Password", type="password", key="reg_pw", placeholder="Min 8 characters")
            r_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Re-enter password")
            r_role = st.selectbox("Requested Role", ["analyst", "auditor", "owner"], key="reg_role")
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("CREATE ACCOUNT", key="btn_register", use_container_width=True):
                if not all([r_fullname, r_email, r_username, r_password, r_confirm]):
                    st.markdown('<div class="sf-alert-box sf-alert-warning">All fields are required.</div>', unsafe_allow_html=True)
                elif r_password != r_confirm:
                    st.markdown('<div class="sf-alert-box sf-alert-danger">Passwords do not match.</div>', unsafe_allow_html=True)
                elif len(r_password) < 8:
                    st.markdown('<div class="sf-alert-box sf-alert-warning">Password must be at least 8 characters.</div>', unsafe_allow_html=True)
                else:
                    ok, msg = register_user(r_username, r_password, r_fullname, r_role, r_email)
                    if ok:
                        st.markdown(f'<div class="sf-alert-box sf-alert-success">{msg} — Please sign in.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="sf-alert-box sf-alert-danger">{msg}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def page_dashboard():
    render_topnav()
    stats = get_dashboard_stats()
    assessments = get_assessments()
    violations_all = []
    for a in assessments[:20]:
        violations_all.extend(get_violations(a["id"]))

    st.markdown("""
    <div style="padding:40px 48px 20px;">
        <div style="font-family:'Playfair Display',serif; font-size:42px; font-weight:900; color:#f0ebe0; letter-spacing:-1px;">
            Governance <span style="color:#c8a84b; font-style:italic;">Command Center</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:6px;">
            Real-time workflow risk intelligence dashboard
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Workflows", stats["total_workflows"])
    with c2:
        st.metric("Assessments Run", stats["total_assessments"])
    with c3:
        st.metric("Avg Risk Score", f"{stats['avg_score']}")
    with c4:
        st.metric("Open Risks", stats["open_risks"])
    with c5:
        st.metric("Governance Rules", stats["total_rules"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:20px 48px;">', unsafe_allow_html=True)
    col_left, col_mid, col_right = st.columns([1.4, 1, 1])

    with col_left:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        bar_svg = generate_risk_bar_chart(assessments)
        st.markdown(bar_svg, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_mid:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        rc = stats["result_counts"]
        donut_svg = generate_donut_chart(rc.get("Pass", 0), rc.get("Warning", 0), rc.get("Fail", 0))
        st.markdown(donut_svg, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        trend_svg = generate_trend_line(stats["trend_data"])
        st.markdown(trend_svg, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        sev_svg = generate_severity_heatmap(violations_all)
        st.markdown(sev_svg, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px 20px;">', unsafe_allow_html=True)
    col_radar, col_recent = st.columns([1, 1.6])

    with col_radar:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        radar_data = {
            "Ownership": random.randint(70, 95),
            "Compliance": random.randint(60, 90),
            "Structure": random.randint(65, 95),
            "Governance": random.randint(55, 85),
            "Timing": random.randint(70, 92),
            "Security": random.randint(60, 88)
        }
        radar_svg = generate_radar_chart(radar_data)
        st.markdown(radar_svg, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        for k, v in radar_data.items():
            color = "#6dc86d" if v >= 80 else ("#c8a84b" if v >= 65 else "#dc5050")
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin:4px 0;">
                <span style="font-size:12px;color:#a09070;">{k}</span>
                <div style="flex:1;margin:0 12px;height:6px;background:#2a2a1a;border-radius:3px;overflow:hidden;">
                    <div style="width:{v}%;height:100%;background:{color};border-radius:3px;"></div>
                </div>
                <span style="font-size:12px;font-weight:700;color:{color};">{v}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_recent:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Recent Assessments</div>', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Latest governance evaluations</div>', unsafe_allow_html=True)
        for a in assessments[:7]:
            r = a.get("compliance_result", "Pending")
            badge_cls = "sf-badge-pass" if r == "Pass" else ("sf-badge-warn" if r == "Warning" else ("sf-badge-fail" if r == "Fail" else "sf-badge-pending"))
            score = a.get("risk_score", 0)
            gauge = generate_svg_gauge(score, 80)
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #2a2a1a;">
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:600;color:#f0ebe0;">{a.get('wf_name','Unknown')}</div>
                    <div style="font-size:11px;color:#a09070;margin-top:2px;">{a.get('executed_at','')[:16]}</div>
                </div>
                {gauge}
                <div style="margin-left:12px;"><span class="sf-badge {badge_cls}">{r}</span></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_workflows():
    render_topnav()
    user = st.session_state.get("user", {})
    st.markdown("""
    <div style="padding:32px 48px 16px;">
        <div style="font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#f0ebe0;">
            Workflow <span style="color:#c8a84b;font-style:italic;">Repository</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:4px;">
            Upload, manage and configure workflow artifacts
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)

    tab_list, tab_upload, tab_create, tab_steps = st.tabs(["All Workflows", "Upload Artifact", "Create Workflow", "Step Configuration"])

    with tab_list:
        workflows = get_workflows()
        filter_col, search_col = st.columns([1, 2])
        with filter_col:
            status_filter = st.selectbox("Filter by Status", ["All", "active", "draft", "archived"], key="wf_status_filter")
        with search_col:
            search_term = st.text_input("Search workflows", placeholder="Search by name or owner...", key="wf_search")

        filtered = workflows
        if status_filter != "All":
            filtered = [w for w in filtered if w["status"] == status_filter]
        if search_term:
            filtered = [w for w in filtered if search_term.lower() in w["name"].lower() or search_term.lower() in (w["owner"] or "").lower()]

        for wf in filtered:
            assessments = get_assessments(wf["id"])
            last_score = assessments[0]["risk_score"] if assessments else None
            last_result = assessments[0]["compliance_result"] if assessments else "Not Assessed"
            badge_cls = "sf-badge-pass" if last_result == "Pass" else ("sf-badge-warn" if last_result == "Warning" else ("sf-badge-fail" if last_result == "Fail" else "sf-badge-pending"))

            with st.expander(f"{wf['name']}  —  v{wf['version']}  ·  {wf['owner']}"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Steps", wf.get("step_count", 0))
                c2.metric("Trigger", wf.get("trigger_type", "N/A").title())
                c3.metric("Frequency", wf.get("frequency", "N/A").title())
                c4.metric("Last Score", f"{last_score:.0f}" if last_score else "N/A")

                if last_score:
                    gauge_svg = generate_svg_gauge(last_score, 100)
                    col_g, col_info = st.columns([1, 3])
                    with col_g:
                        st.markdown(gauge_svg, unsafe_allow_html=True)
                    with col_info:
                        st.markdown(f"""
                        <div style="padding:12px;">
                            <div style="font-size:13px;color:#a09070;margin-bottom:8px;">COMPLIANCE STATUS</div>
                            <span class="sf-badge {badge_cls}">{last_result}</span>
                            <div style="margin-top:12px;font-size:12px;color:#a09070;">
                                Description: {wf.get('description','N/A')}
                            </div>
                        </div>""", unsafe_allow_html=True)

                steps = get_steps(wf["id"])
                if steps:
                    st.markdown('<div style="margin-top:16px; overflow-x:auto;">', unsafe_allow_html=True)
                    flow_html = '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:8px 0;">'
                    for i, s in enumerate(steps):
                        type_colors = {"approval": "active", "audit": "pass", "trigger": "", "conditional": "risk"}
                        node_cls = type_colors.get(s["step_type"], "")
                        flow_html += f'<span class="sf-flow-node {node_cls}">{s["step_name"]}<br/><span style="font-size:9px;opacity:0.7;">{s["step_type"]}</span></span>'
                        if i < len(steps) - 1:
                            flow_html += '<span class="sf-arrow">→</span>'
                    flow_html += '</div>'
                    st.markdown(flow_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    with tab_upload:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Upload Workflow Artifact</div>', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Supports JSON and XML Power Automate exports</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Select workflow artifact file", type=["json", "xml"], key="wf_upload")

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8", errors="replace")
            st.markdown('<div class="sf-alert-box sf-alert-success">File uploaded successfully. Parsing artifact...</div>', unsafe_allow_html=True)

            if uploaded_file.type == "application/json" or uploaded_file.name.endswith(".json"):
                try:
                    parsed = json.loads(content)
                    wf_name_detected = parsed.get("name", parsed.get("title", uploaded_file.name.replace(".json", "")))
                    steps_detected = len(parsed.get("steps", parsed.get("actions", [])))
                    st.markdown(f"""
                    <div class="sf-card" style="margin-top:16px;">
                        <div class="sf-card-title">Parsed Artifact Preview</div>
                        <div style="display:flex;gap:24px;margin-top:12px;">
                            <div class="sf-metric" style="flex:1;"><div class="sf-metric-val">{wf_name_detected[:12]}</div><div class="sf-metric-label">Detected Name</div></div>
                            <div class="sf-metric" style="flex:1;"><div class="sf-metric-val">{steps_detected}</div><div class="sf-metric-label">Steps Found</div></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    owner_input = st.text_input("Assign Owner", key="upload_owner")
                    if st.button("IMPORT WORKFLOW", key="btn_import"):
                        conn = get_db()
                        c = conn.cursor()
                        c.execute("INSERT INTO workflows (name, owner, source_format, version, step_count, status, trigger_type, frequency, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                                  (wf_name_detected, owner_input or "Unassigned", "json", "1.0", steps_detected, "active", "trigger", "on-demand", user["id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        conn.commit()
                        conn.close()
                        log_action(user["id"], "UPLOAD", f"Imported workflow: {wf_name_detected}")
                        st.markdown('<div class="sf-alert-box sf-alert-success">Workflow imported and stored successfully.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="sf-alert-box sf-alert-danger">Parse error: {str(e)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="sf-alert-box sf-alert-info">XML artifact detected ({len(content)} bytes). Manual review recommended for XML workflows.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_create:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Create New Workflow</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Workflow Name", key="new_wf_name")
            new_owner = st.text_input("Owner / Team", key="new_wf_owner")
            new_trigger = st.selectbox("Trigger Type", ["scheduled", "trigger", "event", "manual"], key="new_wf_trigger")
        with col2:
            new_desc = st.text_area("Description", height=80, key="new_wf_desc")
            new_freq = st.selectbox("Execution Frequency", ["daily", "weekly", "monthly", "on-demand", "real-time", "nightly"], key="new_wf_freq")
            new_version = st.text_input("Version", value="1.0", key="new_wf_ver")

        if st.button("CREATE WORKFLOW", key="btn_create_wf"):
            if new_name and new_owner:
                conn = get_db()
                c = conn.cursor()
                c.execute("INSERT INTO workflows (name, description, owner, trigger_type, frequency, version, status, step_count, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                          (new_name, new_desc, new_owner, new_trigger, new_freq, new_version, "active", 0, user["id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                log_action(user["id"], "CREATE_WORKFLOW", f"Created: {new_name}")
                st.markdown('<div class="sf-alert-box sf-alert-success">Workflow created successfully.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sf-alert-box sf-alert-warning">Name and Owner are required.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_steps:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Configure Workflow Steps</div>', unsafe_allow_html=True)
        workflows = get_workflows()
        if workflows:
            wf_options = {w["name"]: w["id"] for w in workflows}
            selected_wf_name = st.selectbox("Select Workflow", list(wf_options.keys()), key="step_wf_select")
            selected_wf_id = wf_options[selected_wf_name]
            existing_steps = get_steps(selected_wf_id)
            if existing_steps:
                st.markdown(f'<div class="sf-card-sub">{len(existing_steps)} steps configured</div>', unsafe_allow_html=True)
                cols = st.columns([2, 2, 1, 2, 1])
                cols[0].markdown('<div style="font-size:11px;color:#a09070;letter-spacing:1px;text-transform:uppercase;">Step Name</div>', unsafe_allow_html=True)
                cols[1].markdown('<div style="font-size:11px;color:#a09070;letter-spacing:1px;text-transform:uppercase;">Type</div>', unsafe_allow_html=True)
                cols[2].markdown('<div style="font-size:11px;color:#a09070;letter-spacing:1px;text-transform:uppercase;">Seq</div>', unsafe_allow_html=True)
                cols[3].markdown('<div style="font-size:11px;color:#a09070;letter-spacing:1px;text-transform:uppercase;">Owner</div>', unsafe_allow_html=True)
                for step in existing_steps:
                    c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1])
                    type_cls = "sf-badge-pass" if step["step_type"] == "approval" else "sf-badge-pending"
                    c1.markdown(f'<div style="font-size:13px;color:#f0ebe0;padding:6px 0;">{step["step_name"]}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<span class="sf-badge {type_cls}">{step["step_type"]}</span>', unsafe_allow_html=True)
                    c3.markdown(f'<div style="font-size:13px;color:#c8a84b;">{step["sequence_num"]}</div>', unsafe_allow_html=True)
                    c4.markdown(f'<div style="font-size:12px;color:#a09070;">{step["owner"] or "Unassigned"}</div>', unsafe_allow_html=True)

            st.markdown('<div style="margin-top:20px;border-top:1px solid #3d3d2a;padding-top:20px;">', unsafe_allow_html=True)
            st.markdown('<div class="sf-card-sub">Add New Step</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                ns_name = st.text_input("Step Name", key="ns_name")
            with c2:
                ns_type = st.selectbox("Step Type", ["trigger", "approval", "notification", "data-transfer", "conditional", "action", "audit", "transform"], key="ns_type")
            with c3:
                ns_owner = st.text_input("Step Owner", key="ns_owner")
            with c4:
                ns_seq = st.number_input("Sequence #", min_value=1, value=len(existing_steps)+1, key="ns_seq")

            if st.button("ADD STEP", key="btn_add_step"):
                if ns_name:
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("INSERT INTO workflow_steps (workflow_id, step_name, step_type, sequence_num, owner) VALUES (?,?,?,?,?)",
                              (selected_wf_id, ns_name, ns_type, ns_seq, ns_owner))
                    c.execute("UPDATE workflows SET step_count=step_count+1 WHERE id=?", (selected_wf_id,))
                    conn.commit()
                    conn.close()
                    st.markdown('<div class="sf-alert-box sf-alert-success">Step added successfully.</div>', unsafe_allow_html=True)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_governance():
    render_topnav()
    user = st.session_state.get("user", {})
    st.markdown("""
    <div style="padding:32px 48px 16px;">
        <div style="font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#f0ebe0;">
            Governance <span style="color:#c8a84b;font-style:italic;">Rules Engine</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:4px;">
            Define, configure and manage compliance policies
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)
    tab_rulesets, tab_rules, tab_create_rule = st.tabs(["Rule Sets", "Rules Library", "Create Rule"])

    with tab_rulesets:
        rule_sets = get_rule_sets()
        cols = st.columns(min(len(rule_sets), 3))
        for i, rs in enumerate(rule_sets):
            rules = get_rules(rs["id"])
            categories = list(set(r["category"] for r in rules))
            with cols[i % 3]:
                st.markdown(f"""
                <div class="sf-3d-card">
                    <div class="sf-card-title">{rs['name']}</div>
                    <div class="sf-card-sub">{rs.get('description','')[:60]}</div>
                    <div style="margin:16px 0;">
                        <div class="sf-metric-val" style="font-size:36px;">{len(rules)}</div>
                        <div class="sf-metric-label">Active Rules</div>
                    </div>
                    <div style="margin-top:12px;">
                        {"".join(f'<span class="sf-tag">{c.title()}</span>' for c in categories)}
                    </div>
                    <div style="margin-top:16px;font-size:11px;color:#a09070;">Created: {rs.get('created_at','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    with tab_rules:
        rule_sets = get_rule_sets()
        if rule_sets:
            rs_options = {rs["name"]: rs["id"] for rs in rule_sets}
            selected_rs = st.selectbox("Select Rule Set", list(rs_options.keys()), key="view_rules_rs")
            rules = get_rules(rs_options[selected_rs])

            if rules:
                sev_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
                rules_sorted = sorted(rules, key=lambda r: sev_order.get(r["severity"], 4))

                sev_colors = {"Critical": "#ff4040", "High": "#ff7030", "Medium": "#c8a84b", "Low": "#6dc86d"}
                for rule in rules_sorted:
                    sev = rule["severity"]
                    col = sev_colors.get(sev, "#a09070")
                    badge_cls = f"sf-badge-{sev.lower()}" if sev.lower() in ["critical","high","medium","low"] else "sf-badge-pending"
                    w = rule.get("weight", 0)
                    progress = min(100, int(w * 2.5))

                    st.markdown(f"""
                    <div class="sf-card" style="margin-bottom:12px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div>
                                <div class="sf-card-title" style="font-size:16px;">{rule['name']}</div>
                                <div style="font-size:12px;color:#a09070;margin-top:4px;">{rule.get('description','')}</div>
                                <div style="margin-top:8px;">
                                    <span class="sf-tag">{rule['category'].title()}</span>
                                </div>
                            </div>
                            <div style="text-align:right;min-width:120px;">
                                <span class="sf-badge {badge_cls}">{sev}</span>
                                <div style="margin-top:8px;font-size:22px;font-family:'Playfair Display',serif;color:{col};font-weight:900;">{w}</div>
                                <div style="font-size:10px;color:#a09070;letter-spacing:1px;">WEIGHT</div>
                            </div>
                        </div>
                        <div class="sf-progress-bar" style="margin-top:12px;">
                            <div class="sf-progress-fill" style="width:{progress}%;background:{col};"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    with tab_create_rule:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Define New Governance Rule</div>', unsafe_allow_html=True)
        rule_sets = get_rule_sets()
        rs_opts = {rs["name"]: rs["id"] for rs in rule_sets}

        col1, col2 = st.columns(2)
        with col1:
            cr_name = st.text_input("Rule Name", key="cr_name")
            cr_rs = st.selectbox("Assign to Rule Set", list(rs_opts.keys()), key="cr_rs")
            cr_cat = st.selectbox("Category", ["ownership", "structure", "compliance", "governance", "security", "timing"], key="cr_cat")
        with col2:
            cr_sev = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], key="cr_sev")
            cr_weight = st.slider("Rule Weight (Impact)", 1, 40, 15, key="cr_weight")
            cr_desc = st.text_area("Description", height=80, key="cr_desc")

        if st.button("CREATE RULE", key="btn_create_rule"):
            if cr_name:
                conn = get_db()
                c = conn.cursor()
                c.execute("INSERT INTO rules (rule_set_id, name, category, severity, weight, description) VALUES (?,?,?,?,?,?)",
                          (rs_opts[cr_rs], cr_name, cr_cat, cr_sev, cr_weight, cr_desc))
                conn.commit()
                conn.close()
                log_action(user["id"], "RULE_CREATE", f"Created rule: {cr_name} [{cr_sev}]")
                st.markdown('<div class="sf-alert-box sf-alert-success">Rule created and added to rule set.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sf-alert-box sf-alert-warning">Rule name is required.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_assessment():
    render_topnav()
    user = st.session_state.get("user", {})
    st.markdown("""
    <div style="padding:32px 48px 16px;">
        <div style="font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#f0ebe0;">
            Risk <span style="color:#c8a84b;font-style:italic;">Assessment Engine</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:4px;">
            Run governance analysis and evaluate compliance
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)
    tab_run, tab_results, tab_violations = st.tabs(["Run Assessment", "Assessment History", "Violation Tracker"])

    with tab_run:
        col_form, col_info = st.columns([1, 1])
        with col_form:
            st.markdown('<div class="sf-card">', unsafe_allow_html=True)
            st.markdown('<div class="sf-card-title">Configure Assessment</div>', unsafe_allow_html=True)

            workflows = get_workflows("active")
            rule_sets = get_rule_sets()

            if not workflows:
                st.markdown('<div class="sf-alert-box sf-alert-warning">No active workflows found. Please create workflows first.</div>', unsafe_allow_html=True)
            elif not rule_sets:
                st.markdown('<div class="sf-alert-box sf-alert-warning">No rule sets found. Please create governance rules first.</div>', unsafe_allow_html=True)
            else:
                wf_opts = {w["name"]: w["id"] for w in workflows}
                rs_opts = {rs["name"]: rs["id"] for rs in rule_sets}
                sel_wf = st.selectbox("Select Workflow", list(wf_opts.keys()), key="assess_wf")
                sel_rs = st.selectbox("Apply Rule Set", list(rs_opts.keys()), key="assess_rs")
                assess_notes = st.text_area("Assessment Notes (optional)", height=80, key="assess_notes")

                wf_preview = get_workflow(wf_opts[sel_wf])
                if wf_preview:
                    st.markdown(f"""
                    <div style="background:#1a1a18;border:1px solid #3d3d2a;border-radius:10px;padding:14px;margin:12px 0;">
                        <div style="font-size:11px;color:#a09070;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Workflow Preview</div>
                        <div style="display:flex;gap:20px;">
                            <div><div style="font-size:18px;font-weight:900;color:#c8a84b;">{wf_preview.get('step_count',0)}</div><div style="font-size:10px;color:#a09070;">STEPS</div></div>
                            <div><div style="font-size:14px;color:#f0ebe0;">{wf_preview.get('owner','N/A')}</div><div style="font-size:10px;color:#a09070;">OWNER</div></div>
                            <div><div style="font-size:14px;color:#f0ebe0;">{wf_preview.get('trigger_type','N/A').upper()}</div><div style="font-size:10px;color:#a09070;">TRIGGER</div></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                if st.button("RUN ASSESSMENT", key="btn_run_assess"):
                    with st.spinner("Running governance analysis..."):
                        result = run_assessment_engine(wf_opts[sel_wf], rs_opts[sel_rs], user["id"])
                        if result:
                            score = result["score"]
                            res = result["result"]
                            gauge_svg = generate_svg_gauge(score, 140)
                            badge_cls = "sf-badge-pass" if res == "Pass" else ("sf-badge-warn" if res == "Warning" else "sf-badge-fail")
                            st.markdown(f"""
                            <div style="text-align:center;padding:20px;background:#1a1a18;border-radius:12px;margin-top:16px;">
                                {gauge_svg}
                                <div style="margin-top:8px;"><span class="sf-badge {badge_cls}" style="font-size:14px;padding:8px 24px;">{res}</span></div>
                                <div style="margin-top:12px;font-size:13px;color:#a09070;">{len(result['violations'])} violation(s) detected</div>
                            </div>""", unsafe_allow_html=True)
                            if result["violations"]:
                                st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
                                for v in result["violations"]:
                                    sev = v.get("severity", "Low")
                                    bc = f"sf-badge-{sev.lower()}" if sev.lower() in ["critical","high","medium","low"] else "sf-badge-pending"
                                    st.markdown(f"""
                                    <div class="sf-timeline-item">
                                        <div class="sf-timeline-dot {'red' if sev in ['Critical','High'] else ''}"></div>
                                        <div>
                                            <div style="font-size:13px;color:#f0ebe0;">{v['message']}</div>
                                            <span class="sf-badge {bc}" style="margin-top:4px;">{sev}</span>
                                        </div>
                                    </div>""", unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
        with col_info:
            st.markdown("""
            <div class="sf-card">
                <div class="sf-card-title">Assessment Guide</div>
                <div class="sf-card-sub">How scoring works</div>
                <div style="margin-top:16px;">
            """, unsafe_allow_html=True)
            guide_items = [
                ("Pass (80-100)", "#6dc86d", "Workflow meets all governance requirements with minimal violations."),
                ("Warning (60-79)", "#c8a84b", "Some governance concerns detected. Review recommended before deployment."),
                ("Fail (0-59)", "#dc5050", "Significant governance violations found. Workflow requires remediation."),
            ]
            for label, color, desc in guide_items:
                st.markdown(f"""
                <div style="display:flex;gap:12px;margin-bottom:16px;padding:12px;background:#1a1a18;border-radius:10px;border-left:3px solid {color};">
                    <div>
                        <div style="font-size:13px;font-weight:600;color:{color};">{label}</div>
                        <div style="font-size:12px;color:#a09070;margin-top:4px;">{desc}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("""
                </div>
                <div style="margin-top:20px;border-top:1px solid #3d3d2a;padding-top:16px;">
                    <div class="sf-card-sub">Risk Score Factors</div>
            """, unsafe_allow_html=True)
            factors = [("Ownership gaps", 20), ("Missing approval gates", 25), ("No audit steps", 18), ("Complexity penalty", 15), ("Governance metadata", 12)]
            for f, w in factors:
                bar_w = int(w * 2.5)
                st.markdown(f"""
                <div style="margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;font-size:11px;color:#a09070;margin-bottom:3px;">
                        <span>{f}</span><span style="color:#c8a84b;">{w} pts</span>
                    </div>
                    <div class="sf-progress-bar">
                        <div class="sf-progress-fill" style="width:{bar_w}%;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

    with tab_results:
        assessments = get_assessments()
        if assessments:
            summary_cols = st.columns(4)
            pass_c = sum(1 for a in assessments if a["compliance_result"] == "Pass")
            warn_c = sum(1 for a in assessments if a["compliance_result"] == "Warning")
            fail_c = sum(1 for a in assessments if a["compliance_result"] == "Fail")
            avg = sum(a["risk_score"] for a in assessments) / len(assessments)
            summary_cols[0].metric("Total", len(assessments))
            summary_cols[1].metric("Pass", pass_c)
            summary_cols[2].metric("Warning", warn_c)
            summary_cols[3].metric("Fail", fail_c)

            st.markdown("<br/>", unsafe_allow_html=True)
            for a in assessments:
                res = a["compliance_result"]
                score = a["risk_score"]
                badge_cls = "sf-badge-pass" if res == "Pass" else ("sf-badge-warn" if res == "Warning" else ("sf-badge-fail" if res == "Fail" else "sf-badge-pending"))
                gauge = generate_svg_gauge(score, 80)
                violations = get_violations(a["id"])

                with st.expander(f"{a.get('wf_name','Workflow')}  —  {a['executed_at'][:16]}"):
                    c1, c2, c3 = st.columns([2, 1, 1])
                    with c1:
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:16px;">
                            {gauge}
                            <div>
                                <span class="sf-badge {badge_cls}">{res}</span>
                                <div style="font-size:13px;color:#a09070;margin-top:8px;">{a['violation_count']} violation(s)</div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    with c2:
                        st.metric("Risk Score", f"{score:.1f}")
                    with c3:
                        st.metric("Violations", a["violation_count"])

                    if violations:
                        st.markdown('<div style="margin-top:12px;">', unsafe_allow_html=True)
                        for v in violations:
                            sev = v.get("severity","Low")
                            status = v.get("mitigation_status", "unresolved")
                            s_cls = "sf-badge-pass" if status == "mitigated" else ("sf-badge-warn" if status == "accepted" else "sf-badge-fail")
                            bc = f"sf-badge-{sev.lower()}" if sev.lower() in ["critical","high","medium","low"] else "sf-badge-pending"
                            st.markdown(f"""
                            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px;background:#1a1a18;border-radius:8px;margin:4px 0;">
                                <div style="flex:1;">
                                    <div style="font-size:12px;color:#d0c8b0;">{v['message']}</div>
                                </div>
                                <div style="display:flex;gap:8px;margin-left:12px;">
                                    <span class="sf-badge {bc}">{sev}</span>
                                    <span class="sf-badge {s_cls}">{status}</span>
                                </div>
                            </div>""", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sf-alert-box sf-alert-info">No assessments found. Run your first assessment in the Run Assessment tab.</div>', unsafe_allow_html=True)

    with tab_violations:
        assessments = get_assessments()
        all_violations = []
        for a in assessments:
            vs = get_violations(a["id"])
            for v in vs:
                v["wf_name"] = a.get("wf_name", "Unknown")
                v["assessed_at"] = a.get("executed_at","")
            all_violations.extend(vs)

        if all_violations:
            filt_sev = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"], key="viol_sev_filter")
            filt_status = st.selectbox("Filter by Status", ["All", "unresolved", "accepted", "mitigated"], key="viol_status_filter")

            filtered_v = all_violations
            if filt_sev != "All":
                filtered_v = [v for v in filtered_v if v.get("severity") == filt_sev]
            if filt_status != "All":
                filtered_v = [v for v in filtered_v if v.get("mitigation_status") == filt_status]

            stats_cols = st.columns(4)
            for i, sev in enumerate(["Critical","High","Medium","Low"]):
                cnt = sum(1 for v in all_violations if v.get("severity") == sev)
                colors = {"Critical":"#ff4040","High":"#ff7030","Medium":"#c8a84b","Low":"#6dc86d"}
                stats_cols[i].metric(sev, cnt)

            st.markdown("<br/>", unsafe_allow_html=True)
            for v in filtered_v[:30]:
                sev = v.get("severity","Low")
                status = v.get("mitigation_status","unresolved")
                bc = f"sf-badge-{sev.lower()}" if sev.lower() in ["critical","high","medium","low"] else "sf-badge-pending"
                s_cls = "sf-badge-pass" if status == "mitigated" else ("sf-badge-warn" if status == "accepted" else "sf-badge-fail")
                st.markdown(f"""
                <div class="sf-card" style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="flex:1;">
                            <div style="font-size:13px;color:#f0ebe0;font-weight:600;">{v['message']}</div>
                            <div style="font-size:11px;color:#a09070;margin-top:4px;">
                                {v.get('wf_name','')} &nbsp;·&nbsp; Step: {v.get('step_name','')} &nbsp;·&nbsp; {v.get('assessed_at','')[:10]}
                            </div>
                        </div>
                        <div style="display:flex;gap:8px;align-items:center;">
                            <span class="sf-badge {bc}">{sev}</span>
                            <span class="sf-badge {s_cls}">{status}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="sf-alert-box sf-alert-success">No violations found in the system.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_simulation():
    render_topnav()
    user = st.session_state.get("user", {})
    st.markdown("""
    <div style="padding:32px 48px 16px;">
        <div style="font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#f0ebe0;">
            Simulation <span style="color:#c8a84b;font-style:italic;">Laboratory</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:4px;">
            What-if analysis and workflow execution modeling
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)
    tab_sim, tab_whatif, tab_compare = st.tabs(["Run Simulation", "What-If Analysis", "Compare Workflows"])

    with tab_sim:
        col_form, col_result = st.columns([1, 1])
        with col_form:
            st.markdown('<div class="sf-card">', unsafe_allow_html=True)
            st.markdown('<div class="sf-card-title">Configure Simulation</div>', unsafe_allow_html=True)
            workflows = get_workflows("active")
            if workflows:
                wf_opts = {w["name"]: w["id"] for w in workflows}
                sel_wf = st.selectbox("Target Workflow", list(wf_opts.keys()), key="sim_wf")
                sim_name = st.text_input("Scenario Name", placeholder="e.g. Reduced Frequency Test", key="sim_name")
                sim_trigger = st.selectbox("Modified Trigger", ["scheduled", "manual_trigger", "automated", "event_based", "api_call"], key="sim_trigger")
                sim_freq = st.selectbox("Simulated Frequency", ["daily", "twice-daily", "weekly", "monthly", "on-demand", "real-time"], key="sim_freq")
                skip_approval = st.checkbox("Simulate Missing Approval Gate", key="sim_skip_approval")
                parallel = st.checkbox("Test Parallel Execution", key="sim_parallel")
                reduce_steps = st.checkbox("Reduce Workflow to Minimal Steps", key="sim_reduce")

                if st.button("EXECUTE SIMULATION", key="btn_sim"):
                    steps = get_steps(wf_opts[sel_wf])
                    base_assessments = get_assessments(wf_opts[sel_wf])
                    base_score = base_assessments[0]["risk_score"] if base_assessments else 75.0

                    delta = 0.0
                    events = []
                    if skip_approval:
                        delta += 22.3
                        events.append({"type": "risk", "msg": "Approval gate removed — critical compliance gap introduced", "sev": "Critical"})
                    if parallel:
                        delta += 5.1
                        events.append({"type": "warn", "msg": "Parallel execution introduces potential race conditions", "sev": "Medium"})
                    if reduce_steps:
                        delta -= 8.5
                        events.append({"type": "pass", "msg": "Simplified flow reduces complexity penalty", "sev": "Low"})
                    delta += random.uniform(-3, 3)

                    new_score = max(0, min(100, base_score - delta))
                    sim_result = "Pass" if new_score >= 80 else ("Warning" if new_score >= 60 else "Fail")

                    conn = get_db()
                    c = conn.cursor()
                    conditions = json.dumps({"skip_approval": skip_approval, "parallel": parallel, "reduce_steps": reduce_steps})
                    c.execute("INSERT INTO simulations (workflow_id, scenario_name, trigger, conditions, result, risk_delta, created_by, created_at) VALUES (?,?,?,?,?,?,?,?)",
                              (wf_opts[sel_wf], sim_name or "Unnamed Scenario", sim_trigger, conditions, sim_result, round(delta, 2), user["id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    log_action(user["id"], "SIMULATION", f"Ran simulation '{sim_name}' on workflow ID {wf_opts[sel_wf]}")
                    st.session_state["sim_result"] = {"score": new_score, "result": sim_result, "delta": delta, "events": events, "base": base_score}

            st.markdown('</div>', unsafe_allow_html=True)

        with col_result:
            sim_r = st.session_state.get("sim_result")
            if sim_r:
                score = sim_r["score"]
                base = sim_r["base"]
                delta = sim_r["delta"]
                res = sim_r["result"]
                badge_cls = "sf-badge-pass" if res == "Pass" else ("sf-badge-warn" if res == "Warning" else "sf-badge-fail")
                delta_color = "#dc5050" if delta > 0 else "#6dc86d"
                delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"

                st.markdown(f"""
                <div class="sf-card" style="text-align:center;">
                    <div class="sf-card-title">Simulation Result</div>
                    <div style="display:flex;justify-content:center;gap:40px;margin:20px 0;">
                        <div>
                            <div style="font-size:11px;color:#a09070;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Baseline</div>
                            {generate_svg_gauge(base, 120)}
                        </div>
                        <div style="font-size:28px;color:#3d3d2a;align-self:center;">→</div>
                        <div>
                            <div style="font-size:11px;color:#a09070;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Simulated</div>
                            {generate_svg_gauge(score, 120)}
                        </div>
                    </div>
                    <div style="font-size:28px;font-family:'Playfair Display',serif;font-weight:900;color:{delta_color};">
                        {delta_str} pts
                    </div>
                    <div style="font-size:11px;color:#a09070;text-transform:uppercase;letter-spacing:2px;">Risk Delta</div>
                    <div style="margin-top:16px;"><span class="sf-badge {badge_cls}">{res}</span></div>
                </div>""", unsafe_allow_html=True)

                if sim_r.get("events"):
                    st.markdown('<div class="sf-card" style="margin-top:16px;">', unsafe_allow_html=True)
                    st.markdown('<div class="sf-card-title">Simulation Events</div>', unsafe_allow_html=True)
                    for e in sim_r["events"]:
                        dot_cls = "red" if e["type"] == "risk" else ("green" if e["type"] == "pass" else "")
                        st.markdown(f"""
                        <div class="sf-timeline-item">
                            <div class="sf-timeline-dot {dot_cls}"></div>
                            <div>
                                <div style="font-size:13px;color:#d0c8b0;">{e['msg']}</div>
                                <div style="font-size:11px;color:#a09070;margin-top:2px;">{e['sev']} severity</div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="sf-card" style="text-align:center;padding:60px;">
                    <div style="font-size:60px;margin-bottom:16px;color:#3d3d2a;">⬡</div>
                    <div style="font-size:14px;color:#a09070;">Configure and execute a simulation to see results here</div>
                </div>""", unsafe_allow_html=True)

    with tab_whatif:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">What-If Scenario Builder</div>', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Model multiple scenarios and compare outcomes</div>', unsafe_allow_html=True)

        workflows = get_workflows("active")
        if workflows:
            wf_opts = {w["name"]: w["id"] for w in workflows}
            sel_wf_wi = st.selectbox("Workflow for Analysis", list(wf_opts.keys()), key="wi_wf")
            base_assessments = get_assessments(wf_opts[sel_wf_wi])
            base_score = base_assessments[0]["risk_score"] if base_assessments else 75.0

            st.markdown(f"""
            <div style="background:#1a1a18;border-radius:10px;padding:16px;margin:12px 0;display:flex;align-items:center;gap:16px;">
                <div>
                    <div style="font-size:11px;color:#a09070;letter-spacing:2px;text-transform:uppercase;">Current Baseline Score</div>
                    <div style="font-size:32px;font-family:'Playfair Display',serif;font-weight:900;color:#c8a84b;">{base_score:.1f}</div>
                </div>
                <div style="flex:1;">
                    <div class="sf-progress-bar">
                        <div class="sf-progress-fill" style="width:{base_score}%;background:{'#6dc86d' if base_score>=80 else '#c8a84b' if base_score>=60 else '#dc5050'};"></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            scenarios = [
                ("Baseline (Current)", 0),
                ("Add Dual Approval Gate", -12),
                ("Remove Audit Step", +18),
                ("Increase Execution Frequency", +5),
                ("Reduce Step Complexity", -8),
                ("Add Missing Ownership", -15),
                ("Enable Parallel Processing", +7),
            ]

            st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
            for scenario_name, impact in scenarios:
                new_s = max(0, min(100, base_score - impact))
                col_scenario, col_gauge = st.columns([3, 1])
                with col_scenario:
                    color = "#6dc86d" if new_s >= 80 else ("#c8a84b" if new_s >= 60 else "#dc5050")
                    impact_str = (f"+{impact}" if impact > 0 else str(impact)) + " pts risk"
                    i_color = "#dc5050" if impact > 0 else "#6dc86d"
                    st.markdown(f"""
                    <div style="padding:12px;background:#1a1a18;border-radius:10px;margin:4px 0;border-left:3px solid {color};">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div style="font-size:13px;color:#f0ebe0;">{scenario_name}</div>
                            <div style="font-size:12px;color:{i_color};font-weight:700;">{impact_str if impact!=0 else "current"}</div>
                        </div>
                        <div style="margin-top:6px;">
                            <div class="sf-progress-bar">
                                <div class="sf-progress-fill" style="width:{new_s}%;background:{color};"></div>
                            </div>
                            <div style="font-size:11px;color:#a09070;margin-top:2px;">{new_s:.0f}/100</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_compare:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Workflow Comparison</div>', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Compare risk profiles across multiple workflows</div>', unsafe_allow_html=True)

        workflows = get_workflows()
        if len(workflows) >= 2:
            wf_names = [w["name"] for w in workflows]
            selected_wfs = st.multiselect("Select Workflows to Compare (2-4)", wf_names, default=wf_names[:3], key="compare_wfs")

            if len(selected_wfs) >= 2:
                compare_data = []
                for wf in workflows:
                    if wf["name"] in selected_wfs:
                        assessments = get_assessments(wf["id"])
                        score = assessments[0]["risk_score"] if assessments else 0
                        result = assessments[0]["compliance_result"] if assessments else "Not Assessed"
                        compare_data.append({"name": wf["name"], "score": score, "result": result,
                                             "steps": wf.get("step_count", 0), "owner": wf.get("owner", "N/A"),
                                             "trigger": wf.get("trigger_type", "N/A")})

                cols = st.columns(len(compare_data))
                for i, cd in enumerate(compare_data):
                    with cols[i]:
                        score = cd["score"]
                        bc = "sf-badge-pass" if cd["result"] == "Pass" else ("sf-badge-warn" if cd["result"] == "Warning" else ("sf-badge-fail" if cd["result"] == "Fail" else "sf-badge-pending"))
                        st.markdown(f"""
                        <div style="text-align:center;background:#1a1a18;border-radius:12px;padding:20px;border:1px solid #3d3d2a;">
                            <div style="font-size:13px;font-weight:600;color:#f0ebe0;margin-bottom:8px;">{cd['name'][:20]}</div>
                            {generate_svg_gauge(score, 110)}
                            <span class="sf-badge {bc}" style="margin-top:8px;display:inline-block;">{cd['result']}</span>
                            <div style="margin-top:12px;font-size:11px;color:#a09070;">
                                {cd['steps']} steps &nbsp;·&nbsp; {cd['trigger'].title()}
                            </div>
                        </div>""", unsafe_allow_html=True)

                st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
                headers = ["Workflow", "Risk Score", "Result", "Steps", "Owner", "Trigger"]
                table_html = '<table class="sf-table"><thead><tr>'
                for h in headers:
                    table_html += f'<th>{h}</th>'
                table_html += '</tr></thead><tbody>'
                for cd in compare_data:
                    bc = "sf-badge-pass" if cd["result"] == "Pass" else ("sf-badge-warn" if cd["result"] == "Warning" else ("sf-badge-fail" if cd["result"] == "Fail" else "sf-badge-pending"))
                    color = "#6dc86d" if cd["score"] >= 80 else ("#c8a84b" if cd["score"] >= 60 else "#dc5050")
                    table_html += f"""<tr>
                        <td style="color:#f0ebe0;font-weight:600;">{cd['name']}</td>
                        <td style="color:{color};font-weight:700;">{cd['score']:.1f}</td>
                        <td><span class="sf-badge {bc}">{cd['result']}</span></td>
                        <td style="color:#c8a84b;">{cd['steps']}</td>
                        <td style="color:#a09070;">{cd['owner']}</td>
                        <td style="color:#a09070;">{cd['trigger'].title()}</td>
                    </tr>"""
                table_html += '</tbody></table>'
                st.markdown(table_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_audit():
    render_topnav()
    user = st.session_state.get("user", {})
    st.markdown("""
    <div style="padding:32px 48px 16px;">
        <div style="font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#f0ebe0;">
            Audit <span style="color:#c8a84b;font-style:italic;">Trail & Reports</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:4px;">
            Complete traceability, decision logs and compliance reports
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)
    tab_logs, tab_reports, tab_export = st.tabs(["Audit Logs", "Assessment Reports", "Export Center"])

    with tab_logs:
        logs = get_audit_logs(100)
        filter_action = st.selectbox("Filter by Action", ["All", "ASSESSMENT", "UPLOAD", "LOGIN", "RULE_CREATE", "SIMULATION", "CREATE_WORKFLOW", "EXPORT"], key="log_filter")

        filtered_logs = logs
        if filter_action != "All":
            filtered_logs = [l for l in logs if l.get("action") == filter_action]

        action_colors = {
            "ASSESSMENT": "#c8a84b",
            "UPLOAD": "#6494c8",
            "LOGIN": "#6dc86d",
            "RULE_CREATE": "#a070c8",
            "SIMULATION": "#64b4c8",
            "CREATE_WORKFLOW": "#c87070",
            "EXPORT": "#c8a060",
        }

        for log in filtered_logs[:50]:
            col = action_colors.get(log.get("action",""), "#a09070")
            user_name = log.get("full_name") or log.get("username") or "System"
            st.markdown(f"""
            <div class="sf-timeline-item">
                <div class="sf-timeline-dot" style="background:{col};"></div>
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:12px;font-weight:700;color:{col};letter-spacing:1px;">{log.get('action','')}</span>
                            <span style="font-size:13px;color:#d0c8b0;margin-left:12px;">{log.get('detail','')}</span>
                        </div>
                        <div style="font-size:11px;color:#a09070;white-space:nowrap;margin-left:16px;">
                            {user_name} &nbsp;·&nbsp; {log.get('timestamp','')[:16]}
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab_reports:
        assessments = get_assessments()
        for a in assessments[:10]:
            violations = get_violations(a["id"])
            res = a["compliance_result"]
            score = a["risk_score"]
            badge_cls = "sf-badge-pass" if res == "Pass" else ("sf-badge-warn" if res == "Warning" else ("sf-badge-fail" if res == "Fail" else "sf-badge-pending"))

            with st.expander(f"Assessment Report — {a.get('wf_name','Workflow')} [{a['executed_at'][:10]}]"):
                st.markdown(f"""
                <div style="padding:16px;background:#1a1a18;border-radius:12px;margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:22px;font-family:'Playfair Display',serif;font-weight:900;color:#f0ebe0;">{a.get('wf_name','Workflow')}</div>
                            <div style="font-size:12px;color:#a09070;margin-top:4px;">Assessment ID: {a['id']} &nbsp;·&nbsp; Executed: {a['executed_at'][:16]}</div>
                        </div>
                        <div style="text-align:right;">
                            {generate_svg_gauge(score, 100)}
                            <span class="sf-badge {badge_cls}" style="display:block;text-align:center;">{res}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Risk Score", f"{score:.1f}/100")
                col_b.metric("Violations Found", len(violations))
                col_c.metric("Compliance Status", res)

                if violations:
                    st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
                    st.markdown('<div class="sf-card-sub">Detected Violations</div>', unsafe_allow_html=True)
                    crit = [v for v in violations if v["severity"] == "Critical"]
                    high = [v for v in violations if v["severity"] == "High"]
                    med = [v for v in violations if v["severity"] == "Medium"]
                    low = [v for v in violations if v["severity"] == "Low"]
                    for group, label, color in [(crit,"Critical","#ff4040"),(high,"High","#ff7030"),(med,"Medium","#c8a84b"),(low,"Low","#6dc86d")]:
                        for v in group:
                            st.markdown(f"""
                            <div style="display:flex;gap:12px;padding:10px;background:#222218;border-radius:8px;margin:4px 0;border-left:3px solid {color};">
                                <div>
                                    <div style="font-size:12px;color:#d0c8b0;">{v['message']}</div>
                                    <div style="font-size:11px;color:#a09070;margin-top:4px;">Rec: {v.get('recommendation','Review and remediate')}</div>
                                </div>
                            </div>""", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    with tab_export:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Export Governance Report</div>', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Generate and download audit-ready compliance documentation</div>', unsafe_allow_html=True)

        assessments = get_assessments()
        if assessments:
            export_opts = {f"{a.get('wf_name','WF')} [{a['executed_at'][:10]}]": a["id"] for a in assessments}
            sel_report = st.selectbox("Select Assessment for Export", list(export_opts.keys()), key="export_sel")
            export_format = st.selectbox("Export Format", ["JSON Report", "Text Summary", "Markdown Report"], key="export_fmt")

            if st.button("GENERATE EXPORT", key="btn_export"):
                a_id = export_opts[sel_report]
                a = next((x for x in assessments if x["id"] == a_id), None)
                violations = get_violations(a_id)

                if export_format == "JSON Report":
                    report = {
                        "report_type": "SecureFlow Governance Assessment",
                        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "workflow": a.get("wf_name"),
                        "assessment_id": a_id,
                        "executed_at": a.get("executed_at"),
                        "compliance_result": a.get("compliance_result"),
                        "risk_score": a.get("risk_score"),
                        "violation_count": len(violations),
                        "violations": [{"severity": v["severity"], "message": v["message"], "status": v["mitigation_status"]} for v in violations]
                    }
                    report_str = json.dumps(report, indent=2)
                    st.download_button("DOWNLOAD JSON REPORT", data=report_str, file_name=f"secureflow_report_{a_id}.json", mime="application/json")
                    st.code(report_str[:800] + ("..." if len(report_str) > 800 else ""), language="json")

                elif export_format == "Text Summary":
                    lines = [
                        "=" * 60,
                        "SECUREFLOW GOVERNANCE ASSESSMENT REPORT",
                        "=" * 60,
                        f"Workflow:    {a.get('wf_name', 'N/A')}",
                        f"Result:      {a.get('compliance_result', 'N/A')}",
                        f"Risk Score:  {a.get('risk_score', 0):.1f}/100",
                        f"Violations:  {len(violations)}",
                        f"Assessed:    {a.get('executed_at', 'N/A')[:16]}",
                        "",
                        "VIOLATIONS DETAIL:",
                        "-" * 40,
                    ]
                    for v in violations:
                        lines.append(f"[{v['severity']}] {v['message']}")
                        lines.append(f"  Status: {v['mitigation_status']}")
                    lines += ["", "=" * 60, "END OF REPORT"]
                    report_str = "\n".join(lines)
                    st.download_button("DOWNLOAD TEXT REPORT", data=report_str, file_name=f"secureflow_report_{a_id}.txt", mime="text/plain")
                    st.code(report_str, language="text")

                elif export_format == "Markdown Report":
                    lines = [
                        "# SecureFlow Governance Assessment Report",
                        f"**Workflow:** {a.get('wf_name', 'N/A')}  ",
                        f"**Result:** `{a.get('compliance_result', 'N/A')}`  ",
                        f"**Risk Score:** {a.get('risk_score', 0):.1f}/100  ",
                        f"**Assessed:** {a.get('executed_at', 'N/A')[:16]}",
                        "",
                        "## Violations",
                        "| Severity | Message | Status |",
                        "|---------|---------|--------|",
                    ]
                    for v in violations:
                        lines.append(f"| {v['severity']} | {v['message']} | {v['mitigation_status']} |")
                    report_str = "\n".join(lines)
                    st.download_button("DOWNLOAD MD REPORT", data=report_str, file_name=f"secureflow_report_{a_id}.md", mime="text/markdown")
                    st.markdown(report_str)

                log_action(user["id"], "EXPORT", f"Exported report for assessment {a_id}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_admin():
    render_topnav()
    user = st.session_state.get("user", {})
    if user.get("role") != "admin":
        st.markdown("""
        <div style="padding:60px;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:32px;color:#dc5050;">Access Restricted</div>
            <div style="color:#a09070;margin-top:8px;">Administrator privileges required.</div>
        </div>""", unsafe_allow_html=True)
        return

    st.markdown("""
    <div style="padding:32px 48px 16px;">
        <div style="font-family:'Playfair Display',serif; font-size:38px; font-weight:900; color:#f0ebe0;">
            System <span style="color:#c8a84b;font-style:italic;">Administration</span>
        </div>
        <div style="color:#a09070; font-size:12px; letter-spacing:3px; text-transform:uppercase; margin-top:4px;">
            User management, system configuration and synthetic data tools
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 48px;">', unsafe_allow_html=True)
    tab_users, tab_settings, tab_synthetic, tab_archive = st.tabs(["User Management", "System Settings", "Synthetic Workflows", "Archive"])

    with tab_users:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = [dict(u) for u in c.fetchall()]
        conn.close()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Users", len(users))
        c2.metric("Active", sum(1 for u in users if u["is_active"]))
        c3.metric("Roles", len(set(u["role"] for u in users)))

        st.markdown("<br/>", unsafe_allow_html=True)
        role_colors = {"admin": "#ff7030", "analyst": "#c8a84b", "auditor": "#6494c8", "owner": "#6dc86d"}
        for u in users:
            rc = role_colors.get(u["role"], "#a09070")
            active_badge = '<span class="sf-badge sf-badge-pass">Active</span>' if u["is_active"] else '<span class="sf-badge sf-badge-fail">Inactive</span>'
            st.markdown(f"""
            <div class="sf-card" style="margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="display:flex;align-items:center;gap:16px;">
                        <div style="width:42px;height:42px;border-radius:50%;background:{rc}22;border:2px solid {rc};display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-size:16px;font-weight:900;color:{rc};">
                            {(u.get('full_name','?') or '?')[0].upper()}
                        </div>
                        <div>
                            <div style="font-size:14px;font-weight:600;color:#f0ebe0;">{u.get('full_name','N/A')}</div>
                            <div style="font-size:12px;color:#a09070;">@{u['username']} &nbsp;·&nbsp; {u.get('email','')}</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;align-items:center;">
                        <span style="font-size:12px;font-weight:700;color:{rc};letter-spacing:1px;text-transform:uppercase;">{u['role']}</span>
                        {active_badge}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:24px;border-top:1px solid #3d3d2a;padding-top:20px;">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Create New User Account</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            nu_name = st.text_input("Full Name", key="nu_name")
            nu_user = st.text_input("Username", key="nu_user")
        with c2:
            nu_email = st.text_input("Email", key="nu_email")
            nu_pw = st.text_input("Initial Password", type="password", key="nu_pw")
        with c3:
            nu_role = st.selectbox("Role", ["analyst", "auditor", "owner", "admin"], key="nu_role")

        if st.button("CREATE USER ACCOUNT", key="btn_admin_create_user"):
            if nu_name and nu_user and nu_pw:
                ok, msg = register_user(nu_user, nu_pw, nu_name, nu_role, nu_email)
                if ok:
                    log_action(user["id"], "USER_CREATED", f"Admin created user: {nu_user} [{nu_role}]")
                    st.markdown(f'<div class="sf-alert-box sf-alert-success">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="sf-alert-box sf-alert-danger">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sf-alert-box sf-alert-warning">Name, username, and password are required.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_settings:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Global Governance Configuration</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            risk_threshold_pass = st.slider("Pass Threshold (min score)", 70, 95, 80, key="thresh_pass")
            risk_threshold_warn = st.slider("Warning Threshold (min score)", 50, 75, 60, key="thresh_warn")
        with col2:
            max_step_complexity = st.slider("Max Steps Before Complexity Penalty", 3, 15, 7, key="max_steps")
            complexity_penalty = st.slider("Complexity Penalty (per extra step)", 1, 10, 2, key="complexity_pen")

        st.markdown(f"""
        <div style="background:#1a1a18;border-radius:10px;padding:16px;margin-top:16px;">
            <div style="font-size:12px;color:#a09070;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">Score Band Preview</div>
            <div style="display:flex;gap:8px;">
                <div style="flex:1;background:#6dc86d22;border:1px solid #6dc86d;border-radius:8px;padding:10px;text-align:center;">
                    <div style="color:#6dc86d;font-weight:700;">Pass</div>
                    <div style="color:#a09070;font-size:11px;">{risk_threshold_pass}–100</div>
                </div>
                <div style="flex:1;background:#c8a84b22;border:1px solid #c8a84b;border-radius:8px;padding:10px;text-align:center;">
                    <div style="color:#c8a84b;font-weight:700;">Warning</div>
                    <div style="color:#a09070;font-size:11px;">{risk_threshold_warn}–{risk_threshold_pass-1}</div>
                </div>
                <div style="flex:1;background:#dc505022;border:1px solid #dc5050;border-radius:8px;padding:10px;text-align:center;">
                    <div style="color:#dc5050;font-weight:700;">Fail</div>
                    <div style="color:#a09070;font-size:11px;">0–{risk_threshold_warn-1}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button("SAVE CONFIGURATION", key="btn_save_config"):
            log_action(user["id"], "CONFIG_UPDATE", "Updated global governance thresholds")
            st.markdown('<div class="sf-alert-box sf-alert-success">Configuration saved successfully.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_synthetic:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Synthetic Workflow Generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-sub">Generate test workflows conforming to Power Automate schema structure</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            syn_count = st.number_input("Number of Workflows to Generate", min_value=1, max_value=20, value=3, key="syn_count")
            syn_step_min = st.number_input("Min Steps per Workflow", min_value=2, max_value=5, value=3, key="syn_step_min")
        with col2:
            syn_step_max = st.number_input("Max Steps per Workflow", min_value=5, max_value=15, value=8, key="syn_step_max")
            syn_complexity = st.selectbox("Scenario Type", ["Mixed Risk", "High Risk", "Low Risk", "Compliance Edge Cases"], key="syn_complexity")

        if st.button("GENERATE SYNTHETIC WORKFLOWS", key="btn_generate_syn"):
            owners = ["Finance Team", "HR Department", "IT Security", "Legal Team", "Operations", "Compliance Team"]
            step_types = ["trigger", "approval", "notification", "data-transfer", "conditional", "action", "audit", "transform"]
            wf_templates = ["Approval Workflow", "Notification Pipeline", "Data Sync Process", "Escalation Handler", "Review Chain", "Batch Processor", "Alert Manager", "Compliance Checker"]
            triggers = ["scheduled", "trigger", "event", "manual"]
            freqs = ["daily", "weekly", "monthly", "on-demand", "real-time"]

            conn = get_db()
            c = conn.cursor()
            generated = []
            for i in range(int(syn_count)):
                name = f"{random.choice(wf_templates)} - Synthetic {random.randint(1000,9999)}"
                owner = random.choice(owners)
                n_steps = random.randint(int(syn_step_min), int(syn_step_max))
                trig = random.choice(triggers)
                freq = random.choice(freqs)

                if syn_complexity == "High Risk":
                    step_pool = ["trigger", "action", "data-transfer", "notification"]
                elif syn_complexity == "Low Risk":
                    step_pool = ["trigger", "approval", "audit", "notification", "conditional"]
                else:
                    step_pool = step_types

                c.execute("INSERT INTO workflows (name, owner, trigger_type, frequency, version, status, step_count, source_format, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                          (name, owner, trig, freq, "1.0", "active", n_steps, "synthetic", user["id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                wf_id = c.lastrowid
                for j in range(n_steps):
                    c.execute("INSERT INTO workflow_steps (workflow_id, step_name, step_type, sequence_num, owner) VALUES (?,?,?,?,?)",
                              (wf_id, f"Step {j+1}", random.choice(step_pool), j+1, owner))
                generated.append(name)

            conn.commit()
            conn.close()
            log_action(user["id"], "SYNTHETIC_GEN", f"Generated {syn_count} synthetic workflows [{syn_complexity}]")
            st.markdown(f'<div class="sf-alert-box sf-alert-success">{int(syn_count)} synthetic workflows generated successfully.</div>', unsafe_allow_html=True)
            for n in generated:
                st.markdown(f'<div class="sf-timeline-item"><div class="sf-timeline-dot green"></div><div style="font-size:13px;color:#d0c8b0;">{n}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_archive:
        st.markdown('<div class="sf-card">', unsafe_allow_html=True)
        st.markdown('<div class="sf-card-title">Workflow Archive Management</div>', unsafe_allow_html=True)

        col_arc, col_restore = st.columns(2)
        with col_arc:
            st.markdown('<div class="sf-card-sub">Archive Active Workflows</div>', unsafe_allow_html=True)
            active_wfs = get_workflows("active")
            if active_wfs:
                arc_opts = {w["name"]: w["id"] for w in active_wfs}
                sel_arc = st.selectbox("Select Workflow to Archive", list(arc_opts.keys()), key="arc_sel")
                if st.button("ARCHIVE WORKFLOW", key="btn_archive"):
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("UPDATE workflows SET status='archived' WHERE id=?", (arc_opts[sel_arc],))
                    conn.commit()
                    conn.close()
                    log_action(user["id"], "ARCHIVE", f"Archived workflow: {sel_arc}")
                    st.markdown('<div class="sf-alert-box sf-alert-success">Workflow archived successfully.</div>', unsafe_allow_html=True)
                    st.rerun()

        with col_restore:
            st.markdown('<div class="sf-card-sub">Restore Archived Workflows</div>', unsafe_allow_html=True)
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM workflows WHERE status='archived'")
            archived = [dict(r) for r in c.fetchall()]
            conn.close()
            if archived:
                rest_opts = {w["name"]: w["id"] for w in archived}
                sel_rest = st.selectbox("Select Archived Workflow", list(rest_opts.keys()), key="rest_sel")
                if st.button("RESTORE WORKFLOW", key="btn_restore"):
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("UPDATE workflows SET status='active' WHERE id=?", (rest_opts[sel_rest],))
                    conn.commit()
                    conn.close()
                    log_action(user["id"], "RESTORE", f"Restored workflow: {sel_rest}")
                    st.markdown('<div class="sf-alert-box sf-alert-success">Workflow restored successfully.</div>', unsafe_allow_html=True)
                    st.rerun()
            else:
                st.markdown('<div class="sf-alert-box sf-alert-info">No archived workflows found.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_nav_pills():
    user = st.session_state.get("user", {})
    role = user.get("role", "")
    current = st.session_state.get("page", "dashboard")

    pages = [
        ("dashboard", "Dashboard"),
        ("workflows", "Workflows"),
        ("governance", "Rules"),
        ("assessment", "Assessment"),
        ("simulation", "Simulation"),
        ("audit", "Audit"),
    ]
    if role == "admin":
        pages.append(("admin", "Admin"))

    cols = st.columns(len(pages) + 1)
    for i, (page_key, label) in enumerate(pages):
        with cols[i]:
            if st.button(label, key=f"nav_{page_key}"):
                st.session_state["page"] = page_key
                st.rerun()

    with cols[-1]:
        if st.button("Sign Out", key="nav_signout"):
            log_action(user.get("id", 0), "LOGOUT", f"User {user.get('username','')} signed out")
            st.session_state.clear()
            st.rerun()

def main():
    init_db()

    if "user" not in st.session_state:
        page_login()
        return

    if "page" not in st.session_state:
        st.session_state["page"] = "dashboard"

    render_nav_pills()

    page = st.session_state.get("page", "dashboard")
    if page == "dashboard":
        page_dashboard()
    elif page == "workflows":
        page_workflows()
    elif page == "governance":
        page_governance()
    elif page == "assessment":
        page_assessment()
    elif page == "simulation":
        page_simulation()
    elif page == "audit":
        page_audit()
    elif page == "admin":
        page_admin()

if __name__ == "__main__":
    main()
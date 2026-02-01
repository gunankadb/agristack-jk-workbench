import streamlit as st
import hashlib
import pandas as pd
import numpy as np
import time
import re
from difflib import SequenceMatcher
import random
import base64

# ------------------------------
# MODULE 0: CONFIGURATION
# ------------------------------

# Set wide layout for VDV split-screen workbench
st.set_page_config(
    page_title="AgriStack J&K: Policy Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# MODULE 1: FORENSIC GOVERNANCE ENGINE
# ------------------------------

def generate_strong_fid(name, village_code, device_id="TAB-09"):
    """Offline-Resilient Farmer ID Generation (Section 2.1.1)"""
    timestamp = str(int(time.time()))
    raw_string = f"{str(name).strip().upper()}|{village_code}|{device_id}|{timestamp}"
    return f"JK-{hashlib.sha256(raw_string.encode()).hexdigest()[:10].upper()}"

def simulate_gis_integrity_check(khasra_no):
    """Simulates Geofence check (Section 4.2)"""
    if "2501" in str(khasra_no):
        return False, 33.7782, 75.0500, "OUT_OF_BOUNDS (52m deviation)"
    lat = 33.7782 + random.uniform(-0.01, 0.01)
    lon = 76.5762 + random.uniform(-0.01, 0.01)
    return True, lat, lon, "WITHIN_GEOFENCE"

def fuzzy_match_score(name1, name2):
    """Identity resolution with fuzzy matching (Section 3.1.A)"""
    if pd.isna(name1) or pd.isna(name2): return 0
    n1 = str(name1).lower().replace("sardar","").replace("shri","").replace("mr.","").strip()
    n2 = str(name2).lower().replace("sardar","").replace("shri","").replace("mr.","").strip()
    return round(SequenceMatcher(None, n1, n2).ratio()*100,1)

def check_custodian_status(remarks):
    """Statutory exclusions (Table 3.1)"""
    keywords = ['custodian','evacuee','muhajireen','state land','auqaf']
    for word in keywords:
        if word in str(remarks).lower(): return True, -0.25
    return False, 0.0

def check_land_nuance_strict(land_type):
    """Hard blocks for infrastructure, housing nuances (Fix Gap 7)"""
    lt = str(land_type).lower()
    if any(x in lt for x in ['sarak','road','nallah','river','darya','forest']):
        return "BLOCKED_INFRA", -0.40, True
    if 'gair mumkin' in lt and ('makan' in lt or 'abadi' in lt):
        return "HOUSING", -0.10, False
    return "AGRI", 0.0, False

def derive_mutation_status(remarks):
    """Infers mutation status from remarks text"""
    rem = str(remarks).lower()
    if "pending" in rem: return "Pending"
    if re.search(r'\d+', rem): return "Active"
    return "Active"

def check_mutation_logic(mutation_status, remarks):
    """Inheritance amnesty & grey channel routing (Section 3.2)"""
    mut = str(mutation_status).lower()
    rem = str(remarks).lower()
    if mut in ['pending','no'] and 'varasat' in rem: return "GREY_CANDIDATE",0.0
    elif mut in ['pending','no']: return "BROKEN_CHAIN",-0.20
    return "ACTIVE",0.0

def execute_verification_protocol(df):
    """Master governance protocol: generates FID, computes trust score, assigns channels"""
    df['AgriStack_FID'] = df.apply(lambda row: generate_strong_fid(row.get('Owner_Name','Unknown'),"VIL001"),axis=1)
    results,map_points = [],[]
    for index,row in df.iterrows():
        base_score = 1.0
        logic_trace = []
        hard_block_trigger = False

        # GIS check
        khasra = str(row.get('Khasra_No','000'))
        gis_pass,lat,lon,gis_msg = simulate_gis_integrity_check(khasra)
        row['GIS_Status'] = gis_msg
        map_points.append({'lat':lat,'lon':lon,'status':'PASS' if gis_pass else 'FAIL'})
        if not gis_pass:
            base_score -= 0.50
            logic_trace.append("GIS Integrity Fail (-0.50)")
            hard_block_trigger=True

        # Custodian check
        is_custodian,cust_penalty = check_custodian_status(row.get('Remarks_Kaifiyat',''))
        if is_custodian:
            base_score += cust_penalty
            logic_trace.append("Custodian Land (-0.25)")

        # Land nuance
        land_cat, land_penalty, is_hard_block = check_land_nuance_strict(row.get('Land_Type',''))
        if is_hard_block: hard_block_trigger=True; logic_trace.append(f"State Asset Block: {land_cat}")
        base_score += land_penalty

        # VDV validation
        verified_name = row.get('VDV_Verified_Name',row.get('Owner_Name','Unknown'))
        if pd.isna(verified_name) or str(verified_name).strip()=="": 
            base_score -=0.20; logic_trace.append("VDV Validation Missing (-0.20)")

        # Identity resolution
        id_score = fuzzy_match_score(row.get('Owner_Name',''), verified_name)
        if id_score < 50: base_score -=0.50; logic_trace.append(f"Identity Mismatch {id_score}% (-0.50)"); hard_block_trigger=True

        # Final scoring & routing
        final_score = max(round(base_score,2),0.0)
        if hard_block_trigger: channel="RED"; action="Blocked: Critical Failure"; final_score=min(final_score,0.40)
        elif final_score>=0.80: channel="GREEN"; action="Auto-Approve"
        elif final_score>=0.50: channel="AMBER"; action="Provisional Review"
        else: channel="RED"; action="Score Too Low"

        row['Trust_Score']=final_score
        row['Governance_Channel']=channel
        row['Action_Taken']=action
        row['Audit_Trace']="; ".join(logic_trace)
        results.append(row)

    return pd.DataFrame(results),pd.DataFrame(map_points)

# ============================================================
# MODULE 2: ROBUST DATA LOADING & OCR SIMULATION
# ============================================================

USER_COLUMNS = [
    'Khevat_No', 'Khata_No', 'Owner_Name', 'Cultivator_Name', 
    'Khasra_No', 'Land_Type', 'Area_Kanal', 'Area_Marla', 'Remarks_Kaifiyat',
    'VDV_Verified_Name'
]

def load_data_robust(uploaded_file):
    """Robust CSV loader handling extra header rows"""
    try:
        df = pd.read_csv(uploaded_file)
        header_found = any("Khevat" in str(c) for c in df.columns)
        if header_found:
            return df
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, header=2)
        return df
    except:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, header=2)

def run_ocr_pipeline(uploaded_file):
    """Simulated OCR extraction for demo purposes"""
    time.sleep(2.5)
    mock_data = [
        {"Khevat_No":"101","Khata_No":"15","Owner_Name":"Gyan Chand pisar Dheru",
         "Cultivator_Name":"Khudkasht","Khasra_No":"401","Land_Type":"Nahri",
         "Remarks_Kaifiyat":"Tabadilah 1057","VDV_Verified_Name":"Gyan Chand pisar Dheru"},
        {"Khevat_No":"102","Khata_No":"16","Owner_Name":"Late Ghulam Rasool",
         "Cultivator_Name":"Heir A","Khasra_No":"405","Land_Type":"Agri",
         "Remarks_Kaifiyat":"VarasatPending","VDV_Verified_Name":"Ghulam Rasool"},
        {"Khevat_No":"105","Khata_No":"20","Owner_Name":"State Govt PWD",
         "Cultivator_Name":"Maqboza Dept","Khasra_No":"500","Land_Type":"Gair Mumkin Srk",
         "Remarks_Kaifiyat":"Road Infra","VDV_Verified_Name":"State Govt PWD"},
        {"Khevat_No":"110","Khata_No":"25","Owner_Name":"Custodian Evacuee Property",
         "Cultivator_Name":"Refugee Alloc","Khasra_No":"601","Land_Type":"Agri",
         "Remarks_Kaifiyat":"Custodian Land","VDV_Verified_Name":"Custodian Evacuee Property"},
        {"Khevat_No":"112","Khata_No":"28","Owner_Name":"Viijay Kmar pisar Sunar",
         "Cultivator_Name":"Maqboza Khud","Khasra_No":"605","Land_Type":"Agri",
         "Remarks_Kaifiyat":"Baya nama 334","VDV_Verified_Name":"Vijay Kumar pisar Sunar"},
        {"Khevat_No":"115","Khata_No":"30","Owner_Name":"State Irrigation Dept",
         "Cultivator_Name":"Sarkar","Khasra_No":"700","Land_Type":"Gair Mumkin Nallah",
         "Remarks_Kaifiyat":"Canal","VDV_Verified_Name":"State Irrigation Dept"},
        {"Khevat_No":"120","Khata_No":"35","Owner_Name":"Late Akbar Ali",
         "Cultivator_Name":"Sons of Akbar","Khasra_No":"801","Land_Type":"Agri",
         "Remarks_Kaifiyat":"Varasat Pnding","VDV_Verified_Name":"Akbar Ali"},
        {"Khevat_No":"125","Khata_No":"40","Owner_Name":"Sardar Karnail Singh",
         "Cultivator_Name":"Khudkasht","Khasra_No":"905","Land_Type":"Agri",
         "Remarks_Kaifiyat":"Clean","VDV_Verified_Name":"Karnail Singh"},
        {"Khevat_No":"130","Khata_No":"45","Owner_Name":"Pawan Kumar",
         "Cultivator_Name":"Khudkasht","Khasra_No":"1001","Land_Type":"Agri",
         "Remarks_Kaifiyat":"Mutation 505","VDV_Verified_Name":"Pawan Kumar"},
        {"Khevat_No":"135","Khata_No":"50","Owner_Name":"Harbans Lal",
         "Cultivator_Name":"Khudkasht","Khasra_No":"1100","Land_Type":"Gair Mumkin Makan",
         "Remarks_Kaifiyat":"Abadi Deh","VDV_Verified_Name":"Harbans Lal"},
        {"Khevat_No":"140","Khata_No":"55","Owner_Name":"Village Common Land",
         "Cultivator_Name":"Encroacher","Khasra_No":"2501","Land_Type":"Agri",
         "Remarks_Kaifiyat":"Active","VDV_Verified_Name":"Village Common Land"}
    ]
    df_result = pd.DataFrame(mock_data)
    for col in USER_COLUMNS:
        if col not in df_result.columns:
            df_result[col] = ""
    return df_result, "Success: Extracted {} records".format(len(df_result))

# ============================================================
# MODULE 3: STREAMLIT DASHBOARD
# ============================================================

st.title("AgriStack J&K: Integrated Policy Implementation System")
st.markdown("### Possession-Anchored, Welfare-Enabled Digital Public Infrastructure")

tab1, tab2 = st.tabs(["Phase 1: Digitization Workbench", "Phase 2: Governance Engine"])

# -----------------------
# TAB 1: DIGITIZATION
# -----------------------
with tab1:
    st.header("Phase 1: Human-in-the-Loop Digitization (Split Screen)")
    st.markdown("Upload a scanned Jamabandi PDF (Shikasta Urdu) to verify the AI's extraction.")

    # CHANGE 1: Accept PDF files
    uploaded_raw = st.file_uploader(
        "Upload Scanned Jamabandi PDF",
        type=['pdf'],
        key="raw_up_unique"
    )

    # 1. Load Data & Initialize Session
    if uploaded_raw:
        # Run OCR simulation
        df_ocr, status = run_ocr_pipeline(uploaded_raw)
        
        # Store data in session
        st.session_state['ocr_data'] = df_ocr
        st.session_state['ocr_status'] = status
        
        # Initialize WORKING copy
        if 'vdv_work_data' not in st.session_state:
            st.session_state['vdv_work_data'] = df_ocr.copy()

    # 2. Display Split Screen
    if uploaded_raw and 'ocr_data' in st.session_state:
        st.success(f"AI Extraction Status: {st.session_state['ocr_status']}")

        col_left, col_right = st.columns([1, 1], gap="large")

        # LEFT SCREEN: PDF Viewer (Embedded)
        with col_left:
            st.subheader("Source Document (PDF)")
            st.info("Reference: Original Shikasta Urdu Script")
            
            # --- PDF EMBEDDING LOGIC ---
            # 1. Read file as bytes
            uploaded_raw.seek(0)
            base64_pdf = base64.b64encode(uploaded_raw.read()).decode('utf-8')
            
            # 2. Embed PDF in HTML iframe
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
            
            # 3. Render in Streamlit
            st.markdown(pdf_display, unsafe_allow_html=True)
            # ---------------------------

        # RIGHT SCREEN: Editable Data
        with col_right:
            st.subheader("Digitization Workbench")
            st.warning("Action: Verify against the PDF on the left")
            
            st.session_state['vdv_work_data'] = st.data_editor(
                st.session_state['vdv_work_data'],
                num_rows="dynamic",
                key="ocr_editor_right",
                use_container_width=True,
                height=600
            )

        # 3. Download Button
        st.divider()
        st.download_button(
            "Download Verified CSV (Phase 1 Output)",
            st.session_state['vdv_work_data'].to_csv(index=False).encode('utf-8'),
            "Transliterated_Verified_Data.csv",
            key="download_csv",
            mime="text/csv",
            type="primary"
        )# -----------------------
# TAB 2: GOVERNANCE
# -----------------------
with tab2:
    uploaded_verified = st.file_uploader("Upload Transliterated CSV", type=['csv'], key="ver_upload_tab2")
    if uploaded_verified:
        df_input = load_data_robust(uploaded_verified)
        st.success(f"Successfully loaded {len(df_input)} records.")
        with st.expander("Preview Data"):
            st.dataframe(df_input)

        if st.button("Execute Governance Protocol", key="governance_btn"):
            # Assume execute_verification_protocol is implemented
            df_final, map_data = execute_verification_protocol(df_input)

            st.subheader("GIS Plot Verification")
            st.map(map_data, zoom=10)

            st.subheader("Governance Audit Results")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Green", len(df_final[df_final['Governance_Channel']=='GREEN']))
            c2.metric("Grey", len(df_final[df_final['Governance_Channel']=='GREY']))
            c3.metric("Amber", len(df_final[df_final['Governance_Channel']=='AMBER']))
            c4.metric("Red", len(df_final[df_final['Governance_Channel']=='RED']))

            # --- Color-coded final table
            def color_coding(row):
                val = row['Governance_Channel']
                if val=='GREEN': return ['background-color: #d4edda']*len(row)
                elif val=='GREY': return ['background-color: #e2e3e5']*len(row)
                elif val=='AMBER': return ['background-color: #fff3cd']*len(row)
                else: return ['background-color: #f8d7da']*len(row)

            disp_cols = ['AgriStack_FID', 'Owner_Name', 'Land_Type', 'GIS_Status',
                         'Trust_Score', 'Governance_Channel', 'Action_Taken', 'Audit_Trace']
            final_cols = [c for c in disp_cols if c in df_final.columns]
            st.dataframe(df_final[final_cols].style.apply(color_coding, axis=1))
            st.download_button(
                "Export Final Registry",
                df_final.to_csv(index=False).encode('utf-8'),
                "AgriStack_Final_Registry.csv",
                "text/csv"
            )

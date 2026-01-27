"""
AgriStack J&K: Integrated Policy Implementation System
Module: Governance & Verification Engine (v2.1 - Fixed)
"""

import streamlit as st
import hashlib
import pandas as pd
import numpy as np
import random
import time
from difflib import SequenceMatcher

# --- SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="AgriStack J&K: Governance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UTILS ---
def generate_fid(name, khasra):
    raw = f"{str(name).strip().upper()}|{str(khasra).strip()}"
    return f"JK-{hashlib.sha256(raw.encode()).hexdigest()[:8].upper()}"

def fuzzy_match_score(name1, name2):
    if pd.isna(name1) or pd.isna(name2): return 0
    n1 = str(name1).lower().replace("sardar", "").replace("shri", "").strip()
    n2 = str(name2).lower().replace("sardar", "").replace("shri", "").strip()
    return round(SequenceMatcher(None, n1, n2).ratio() * 100, 1)

# --- BUSINESS LOGIC ENGINE ---

def execute_verification_protocol(df):
    
    # 1. ID GENERATION
    df['AgriStack_FID'] = df.apply(lambda row: generate_fid(row['Owner_Name'], row['Khasra_No']), axis=1)
    
    processed_rows = []
    crops_list = ['Paddy (Basmati)', 'Maize', 'Wheat', 'Mustard', 'Fallow']
    
    # --- PHASE 2: SIMULATION LOOP ---
    for index, row in df.iterrows():
        
        # A. DATA INJECTION (Simulating Dirty Legacy Data)
        # This creates the AMBER cases by injecting risk keywords
        risk_dice = random.randint(0, 100)
        current_remarks = str(row.get('Remarks_Kaifiyat', ''))
        
        if risk_dice < 20: 
            # 20% Chance: Inject "Stay Order"
            row['Remarks_Kaifiyat'] = current_remarks + " [Court Stay Pending]"
        elif risk_dice < 25:
            # 5% Chance: Inject "Dispute"
            row['Remarks_Kaifiyat'] = current_remarks + " [Dispute on Title]"
        else:
            # 75% Chance: Clean Record (FIXED INDENTATION BELOW)
            row['Remarks_Kaifiyat'] = current_remarks

        # B. FIELD DATA SIMULATION (VDV)
        target_name = row['Owner_Name'] if "Khudkasht" in str(row['Cultivator_Name']) else row['Cultivator_Name']
        vdv_dice = random.randint(0, 100)
        
        if vdv_dice < 90:
            # 90% Success Rate (Verified)
            # Create a slight variation (Fuzzy Match) or exact match
            field_name = target_name.replace("Singh", "Sing").replace("Mohammed", "Mohd")
            row['VDV_Verified_Name'] = field_name
            row['VDV_Status'] = "VERIFIED"
            row['VDV_Mobile'] = f"9906{random.randint(100000, 999999)}"
        else:
            # 10% Failure (Refusal/Absent) -> Causes RED
            row['VDV_Verified_Name'] = "Beneficiary Absent"
            row['VDV_Status'] = "FAILED"
            row['VDV_Mobile'] = ""

        row['Crop_Status'] = random.choice(crops_list)
        processed_rows.append(row)
        
    df_processed = pd.DataFrame(processed_rows)

    # --- PHASE 3: ALGORITHMIC GOVERNANCE AUDIT ---
    results = []
    
    for i, row in df_processed.iterrows():
        base_score = 1.0
        
        # 1. Statutory Risk Analysis (Legacy Data)
        remarks = str(row.get('Remarks_Kaifiyat', '')).lower()
        land = str(row.get('Land_Type', '')).lower()
        
        # RISK LOGIC: Captures the injected keywords
        if 'dispute' in remarks or 'stay' in remarks or 'court' in remarks:
            base_score -= 0.30 # Penalty -> AMBER
            
        if 'gair mumkin' in land: 
            base_score -= 0.40 # Penalty -> AMBER/RED
            
        # 2. Identity Resolution
        legacy = str(row['Owner_Name'] if "Khudkasht" in str(row['Cultivator_Name']) else row['Cultivator_Name'])
        field = str(row['VDV_Verified_Name'])
        
        id_score = fuzzy_match_score(legacy, field)
        
        # 3. Penalties
        if row['VDV_Status'] == "FAILED":
            base_score -= 0.60 # Drop to Red
        elif id_score < 50:
            base_score -= 0.30
            
        # 4. Channel Assignment
        final_score = max(round(base_score, 2), 0.0)
        
        # Hard Blocks (Policy Appendix C)
        if "gair mumkin" in land:
            channel = "RED"
        elif row['VDV_Status'] == "FAILED":
            channel = "RED"
        
        # Score Thresholds (Policy Section 4.2)
        elif final_score >= 0.80:
            channel = "GREEN" # Clean Record
        elif final_score >= 0.50:
            channel = "AMBER" # Disputed Record
        else:
            channel = "RED"
            
        row['Identity_Confidence'] = id_score
        row['Trust_Score'] = final_score
        row['Governance_Channel'] = channel
        
        results.append(row)
        
    return pd.DataFrame(results)

# --- UI LAYER ---
st.sidebar.header("Data Ingestion Protocol")
uploaded_file = st.sidebar.file_uploader("Upload Legacy Record (CSV)", type=['csv'])

st.title("AgriStack J&K: Integrated Policy Implementation System")

if uploaded_file:
    # Load Data (Skipping 2 empty rows as per your file format)
    df_raw = pd.read_csv(uploaded_file, header=2)
    st.markdown("### 1. Legacy Data Analysis")
    st.info(f"Ingested {len(df_raw)} records from Revenue Repository.")
    
    if st.button("Execute Verification Protocol", type="primary"):
        with st.spinner("Injecting Stress Scenarios... Running Policy Rules..."):
            time.sleep(1)
            df_final = execute_verification_protocol(df_raw)
            
            # KPI Dashboard
            st.markdown("### 2. Governance Audit Results")
            k1, k2, k3 = st.columns(3)
            
            green = len(df_final[df_final['Governance_Channel']=='GREEN'])
            amber = len(df_final[df_final['Governance_Channel']=='AMBER'])
            red = len(df_final[df_final['Governance_Channel']=='RED'])
            
            k1.metric("Green Channel (Verified)", green, delta="Automated Approval")
            k2.metric("Amber Channel (Provisional)", amber, delta="Legacy Risk Detected", delta_color="off")
            k3.metric("Red Channel (Blocked)", red, delta="Policy Violation", delta_color="inverse")
            
            # Interactive Table
            st.subheader("Possession-Anchored Registry")
            
            cols = ['AgriStack_FID', 'Owner_Name', 'VDV_Verified_Name', 'Remarks_Kaifiyat', 'Trust_Score', 'Governance_Channel']
            
            def color_coding(row):
                if row['Governance_Channel'] == 'GREEN': 
                    return ['background-color: #d4edda; color: #155724'] * len(row)
                elif row['Governance_Channel'] == 'AMBER': 
                    return ['background-color: #fff3cd; color: #856404'] * len(row)
                else: 
                    return ['background-color: #f8d7da; color: #721c24'] * len(row)

            st.dataframe(df_final[cols].style.apply(color_coding, axis=1))
            
            # Download
            st.download_button(
                "Export Final Registry (CSV)", 
                df_final.to_csv(index=False).encode('utf-8'),
                "AgriStack_JK_Verified.csv", 
                "text/csv"
            )
else:
    st.info("System Ready. Awaiting Legacy Data Upload.")
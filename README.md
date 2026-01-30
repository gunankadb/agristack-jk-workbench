# AgriStack J&K: Integrated Policy Implementation System
### *Possession-Anchored, Welfare-Enabled Digital Public Infrastructure (DPI)*

![Status](https://img.shields.io/badge/Status-Prototype_v18.0-blue) ![Context](https://img.shields.io/badge/Event-Harvard_Policy_Hackathon-maroon) ![Tech](https://img.shields.io/badge/Built_With-Streamlit_|_Python-green)

## **1. Executive Summary**
This software serves as the **Digital Public Infrastructure (DPI)** for the *AgriStack J&K Policy Framework v2.0*. It automates the verification of legacy land records (*Jamabandis*), transitioning them from static paper documents to a dynamic, credit-ready digital registry.

By decoupling "Service Eligibility" from "Legal Title Finality," this system allows immediate welfare delivery to active cultivators while long-term legal disputes are resolved in the background.

### **⚠️ Project Scope & Limitations**
> **"This prototype focuses on the 'Land Governance & Registration' layer of AgriStack (cleaning the RoR, generating FIDs, and validating statutory compliance). It simulates the GIS Integrity Check but leaves the detailed Farmer Registration Process (e-KYC) and Seasonal Crop Survey module for a future 'Field App' integration."**

---

## **2. Key Functional Modules**

The application is divided into two distinct operational phases:

### **Phase 1: Human-in-the-Loop Digitization Workbench**
* **Problem:** Legacy records are in *Shikasta* (cursive) Urdu and often illegible.
* **Solution:** A split-screen interface where **AI-Simulated OCR** extracts raw data, and a Village Data Volunteer (VDV) verifies/edits the entries against the original PDF scan.
* **Tech:** Uses `Tesseract` (or Mock Engine for demo stability) to digitize columns like *Khevat*, *Owner Name*, and *Land Type*.

### **Phase 2: Governance & GIS Engine**
This is the algorithmic core that processes the digitized data:
1.  **Forensic Audit Logic:** Implements the **Risk Verification Matrix** to assign Trust Scores (0.0–1.0).
2.  **GIS Plot Integrity (New):** Simulates a real-time geofence check. It validates if the VDV's physical location matches the plot's official coordinates (blocking 'Ghost Surveys').
3.  **Governance Channels:**
    * 🟢 **Green:** Verified, eligible for full KCC (Kisan Credit Card).
    * ⚪ **Grey:** Inheritance (*Varasat*) cases deemed verified with a 24-month amnesty.
    * 🟡 **Amber:** Provisional; welfare allowed (CRC) but subject to review (e.g., Custodian Land).
    * 🔴 **Red:** Blocked due to identity failure, encroachment (*Sarak/Nallah*), or GIS mismatch.

---

## **3. Policy Alignment Matrix**

| Code Feature | Policy Principle Implemented |
| :--- | :--- |
| **Generates 'JK-HASH'** | **Sec 2.1.1:** Offline-Resilient Identity (No dependency on live Aadhaar API). |
| **Fuzzy Matching** | **Sec 3.1.A:** Handles spelling variations between Urdu and English IDs. |
| **GIS Module** | **Sec 4.2:** Plot Integrity; Ensures VDV physically visited the field. |
| **Grey Channel** | **Sec 3.2:** Amnesty for *Varasat* (Inheritance) pending mutations. |
| **Amber Channel** | **Table 3.1:** Financial inclusion for *Custodian/Evacuee* land occupants. |

---

## **4. Installation & Setup**

### **Prerequisites**
* Python 3.9+
* (Optional but recommended) Poppler installed for PDF processing.

### **Step 1: Install Dependencies**
    pip install streamlit pandas numpy fpdf pdf2image pytesseract

### **Step 2: Generate Demo Artifacts**
Run the generator script to create the "Transliterated Jamabandi" PDF for the Phase 1 demo:

    python create_demo_pdf.py

*This creates `Jamabandi_Demo_English.pdf` in your folder.*

### **Step 3: Launch the Application**
    streamlit run agristack_app_v9.py

The application will open in your browser at `http://localhost:8501`.

---

## **5. How to Run the Demo (Walkthrough)**

1.  **Phase 1 (Digitization):**
    * Go to the **"Phase 1"** tab.
    * Upload `Jamabandi_Demo_English.pdf`.
    * Click **"Initiate OCR"**.
    * *Narrative:* "The system digitizes the record. As a VDV, I verify the data." (Download the CSV).

2.  **Phase 2 (Governance):**
    * Go to the **"Phase 2"** tab.
    * Upload the CSV you just downloaded (or use the provided `Simulated_Jamabandi_Output.csv`).
    * Click **"Execute Governance Protocol"**.

3.  **The Result:**
    * Show the **Governance Channels** (Green/Grey/Amber/Red).
    * Show the **GIS Map Widget** (Point out the "Blue Dots" vs the "Red Flag" on Khasra 2501).
    * Explain the **Audit Trace** for a blocked farmer.

---

## **6. Disclaimer**
This is a policy demonstration prototype created for the **Harvard Kennedy School Policy Hackathon**. It simulates governance logic and system architecture for welfare-linked agricultural digitization. It does **not** create or modify official land ownership records and must not be used for legal title determination.

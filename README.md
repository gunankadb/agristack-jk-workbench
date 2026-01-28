# AgriStack J&K – Governance & Verification Workbench

## Overview

This repository contains the **Human-in-the-Loop Governance Workbench** developed for the **AgriStack Jammu & Kashmir: Possession-Anchored, Welfare-Enabled DPI Framework**.

The application is a **Streamlit-based prototype** that demonstrates the end-to-end workflow for transforming legacy land records into a **confidence-graded digital registry** for welfare and agricultural service delivery.

It operationalizes the policy principle that:

**Service Delivery Eligibility can be determined using verified possession and confidence scoring — without waiting for legal title finality.**

---

## What This Prototype Demonstrates

This workbench simulates how scanned legacy records move through a **digitization → verification → governance scoring → registry output** pipeline.

### Key Functional Components

**1. Human-in-the-Loop Digitisation Interface**
A split-screen workflow simulates how operators validate AI-suggested transliterations of legacy Urdu/Shikasta land records before structured data entry.

**2. Governance Engine (Confidence Scoring System)**
Implements the **Risk Verification Matrix** described in the policy.
Each record is assigned a **Trust Score (0.0–1.0)** and routed into one of four governance channels:

* **Green** – Verified, eligible for full welfare & credit linkage
* **Grey** – Inheritance (Varasat) cases deemed verified with time-bound grace
* **Amber** – Provisional, welfare allowed but subject to review
* **Red** – Blocked due to identity failure or ineligible land category

**3. Possession-Anchored Identity Logic**
Implements rules such as:

* Custodian / Evacuee land handling (CRC pathway)
* Varasat (inheritance) exemption logic
* Distinction between **Gair Mumkin Makan (allowed)** and **Gair Mumkin Sarak (blocked)**

**4. Offline-Resilient Provisional Farmer ID Generation**
Farmer IDs are generated using **SHA-256 hashing** that includes device and village context to prevent duplication in low-connectivity environments.

**5. Audit Trace Transparency**
Every scoring decision includes a human-readable audit trail explaining why penalties or routing decisions occurred.

---

## Input Data Files

The prototype works with two types of datasets:

### 1. Original Legacy Dataset

Raw digitised Jamabandi-style land record data (pre-transliteration).

### 2. Transliterated Dataset

**File name:** `Transliterated Data Updated.csv`
This dataset contains structured, transliterated fields derived from legacy Urdu records and is used to demonstrate the governance scoring and verification workflow.

---

## System Requirements

You need **Python 3.9+** and the following libraries:

* streamlit
* pandas
* numpy
* easyocr
* opencv-python-headless (or opencv-python)
* Pillow

---

## Installation

1. Clone or download this repository
2. Install dependencies:

pip install streamlit pandas easyocr numpy opencv-python-headless Pillow

---

## Running the Application

Launch the Streamlit app:

streamlit run agristack_app_v9.py

The app will open automatically in your browser at:

[http://localhost:8501](http://localhost:8501)

---

## How to Use the Prototype

1. Start the application
2. Upload the **transliterated dataset** (`Transliterated Data Updated.csv`) when prompted
3. Click **“Execute v2.0 Protocol”**
4. View:

   * Governance channel distribution (Green/Grey/Amber/Red)
   * Trust Scores for each record
   * Automated audit trace explaining each decision
5. Download the processed **Provisional Registry Output CSV**

---

## Policy Alignment

This prototype implements the core features of the **AgriStack J&K Policy Framework**, including:

* Possession-Anchored Registry Model
* Confidence-Graded Governance Channels
* Custodian / Evacuee Land Inclusion Pathway
* Varasat (Inheritance) Grey Channel Logic
* Human-in-the-Loop AI Transliteration Validation
* Legal Safe Harbor: Registry is **not a title document**

---

## Prototype vs Production System

This repository demonstrates **policy-to-algorithm translation** and governance logic.

In a production deployment:

* OCR/transliteration would be powered by **Bhashini AI models specialized for Shikasta Urdu**
* Records would be stored in a **secure government database with immutable audit logs**
* APIs would expose verified records to **banks, insurers, and welfare platforms**
* Role-based access control (VDV, Block Officer, Revenue Officer) would be enforced

---

## Disclaimer

This is a **policy demonstration prototype** created for the Harvard Kennedy School Policy Hackathon.

It simulates governance logic and system architecture for welfare-linked agricultural digitization.
It does **not** create or modify official land ownership records and must not be used for legal title determination.

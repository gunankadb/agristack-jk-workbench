AgriStack J&K: Governance & Verification Workbench
Overview
This repository contains the Human-in-the-Loop Governance Workbench developed for the AgriStack J&K policy framework. It is a Streamlit-based web application designed to demonstrate the end-to-end workflow of digitizing legacy land records in Jammu & Kashmir.
Key Features
	•	Split-Screen Interface: Simulates the side-by-side view of legacy Urdu records and the digitization entry form.
	•	Governance Engine: Implements the confidence scoring logic (Risk Verification Matrix) to assign Green, Amber, or Red channels automatically.
	•	Basic OCR Integration: Uses easyocr to demonstrate the technical pipeline for ingesting Urdu text, enabling human operators to validate AI suggestions.
	•	Offline-Ready ID Generation: Generates SHA-256 hashes for Provisional Farmer IDs.
Requirements
To run this prototype locally, you need Python installed along with the following libraries:
	•	streamlit
	•	pandas
	•	easyocr
	•	numpy
	•	opencv-python-headless (or opencv-python)
	•	Pillow
Installation
	1	Clone this repository.
	2	Install dependencies:bash pip install streamlit pandas easyocr numpy opencv-python-headless Pillow 
Usage
Run the application using Streamlit:
Bash

streamlit run agristack_app_v9.py
The application will open in your default web browser at http://localhost:8501.
Disclaimer
This prototype uses easyocr to demonstrate pipeline connectivity. In a production environment, this would be replaced/augmented by the Bhashini API for specialized Shikasta Urdu models.xx	

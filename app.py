import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AMR Data Entry System",
    page_icon="🔬",
    layout="wide"
)

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def connect_to_google_sheets():
    """Connect to Google Sheets using service account credentials"""
    try:
        # Load credentials from Streamlit secrets
        creds_dict = st.secrets["gcp_service_account"]
        
        # Define the scope
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Create credentials object
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        return client
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {str(e)}")
        return None

def append_to_sheet(data_dict, sheet_name="AMR_Data"):
    """Append data to Google Sheet"""
    try:
        client = connect_to_google_sheets()
        if client is None:
            return False
        
        # Open the spreadsheet (replace with your spreadsheet name or URL)
        sheet = client.open(sheet_name).sheet1
        
        # Add timestamp
        data_dict['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get existing headers
        existing_headers = sheet.row_values(1)
        
        # If sheet is empty, add headers
        if not existing_headers:
            headers = list(data_dict.keys())
            sheet.append_row(headers)
        
        # Append the data
        values = list(data_dict.values())
        sheet.append_row(values)
        
        return True
    except Exception as e:
        st.error(f"Error writing to Google Sheets: {str(e)}")
        return False

# App Title
st.title("🔬 Antimicrobial Resistance Data Entry System")
st.markdown("---")

# Create form
with st.form("patient_data_form"):
    st.subheader("Patient Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=120, value=65)
        gender = st.selectbox("Gender", ["Male", "Female"])
        setting = st.selectbox("Setting", ["ICU", "Internal Medicine"])
    
    with col2:
        acquisition = st.selectbox("Acquisition", ["Community", "Hospital"])
        bsi_source = st.selectbox("BSI Source", ["Primary", "Lung", "Abdomen", "UTI"])
        species = st.selectbox(
            "Species",
            ["E. coli", "Klebsiella spp.", "Proteus spp.", "Pseudomonas spp.", "Acinetobacter spp."]
        )
    
    st.subheader("Clinical Characteristics")
    
    col3, col4 = st.columns(2)
    
    with col3:
        rectal_cpe = st.selectbox("Rectal CPE Positive", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        chf = st.selectbox("CHF", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        ckd = st.selectbox("CKD", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    
    with col4:
        tumor = st.selectbox("Tumor", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        diabetes = st.selectbox("Diabetes", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        immunosuppressed = st.selectbox("Immunosuppressed", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    
    st.subheader("Resistance Profile")
    
    col5, col6 = st.columns(2)
    
    with col5:
        cr = st.selectbox("Carbapenem Resistance (CR)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        blbli_r = st.selectbox("BL/BLI Resistance", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    
    with col6:
        fqr = st.selectbox("Fluoroquinolone Resistance (FQR)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        three_gc_r = st.selectbox("3rd Gen Cephalosporin Resistance", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    
    st.markdown("---")
    
    # Submit button
    col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
    with col_submit2:
        submit_button = st.form_submit_button("📊 Submit Data", use_container_width=True)

# Handle form submission
if submit_button:
    # Create data dictionary
    data_dict = {
        'Age': age,
        'Gender': gender,
        'Species': species,
        'Rectal_CPE_Pos': rectal_cpe,
        'Setting': setting,
        'Acquisition': acquisition,
        'BSI_Source': bsi_source,
        'CHF': chf,
        'CKD': ckd,
        'Tumor': tumor,
        'Diabetes': diabetes,
        'Immunosuppressed': immunosuppressed,
        'CR': cr,
        'BLBLI_R': blbli_r,
        'FQR': fqr,
        '3GC_R': three_gc_r
    }
    
    # Show loading spinner
    with st.spinner('Submitting data to Google Sheets...'):
        success = append_to_sheet(data_dict)
    
    if success:
        st.success("✅ Data successfully submitted to Google Sheets!")
        st.balloons()
    else:
        st.error("❌ Failed to submit data. Please check your Google Sheets configuration.")

# Sidebar with instructions
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    ### Setup Steps:
    
    1. **Create a Google Sheet**
       - Go to Google Sheets
       - Create a new spreadsheet
       - Name it (e.g., "AMR_Data")
    
    2. **Set up Google Service Account**
       - Go to Google Cloud Console
       - Create a new project
       - Enable Google Sheets API
       - Create Service Account
       - Download JSON key file
    
    3. **Configure Streamlit Secrets**
       - Create `.streamlit/secrets.toml`
       - Add your service account credentials:
       
       ```toml
       [gcp_service_account]
       type = "service_account"
       project_id = "your-project-id"
       private_key_id = "your-key-id"
       private_key = "your-private-key"
       client_email = "your-email@project.iam.gserviceaccount.com"
       client_id = "your-client-id"
       auth_uri = "https://accounts.google.com/o/oauth2/auth"
       token_uri = "https://oauth2.googleapis.com/token"
       auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
       client_x509_cert_url = "your-cert-url"
       ```
    
    4. **Share Google Sheet**
       - Share your Google Sheet with the service account email
       - Give it "Editor" permissions
    
    5. **Update Sheet Name**
       - In the code, update `sheet_name` in the `append_to_sheet()` function
    
    ### Data Fields:
    - Patient demographics
    - Clinical characteristics
    - Microbiological data
    - Resistance profiles
    """)
    
    st.markdown("---")
    st.info("💡 **Tip**: All data is automatically timestamped upon submission.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "AMR Data Entry System v1.0 | Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True
  )

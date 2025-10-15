# 🔬 Antimicrobial Resistance (AMR) Data Entry System

A Streamlit-based demo web application for capturing and managing antimicrobial resistance data with seamless Google Sheets integration.

## 📋 Overview

This application provides a user-friendly interface for healthcare professionals to record patient data related to antimicrobial resistance, including demographics, clinical characteristics, microbiological findings, and resistance profiles. All data is automatically saved to Google Sheets with timestamps for easy tracking and analysis.

## ✨ Features

- **Intuitive Form Interface**: Organized sections for easy data entry
- **Real-time Google Sheets Integration**: Automatic data synchronization
- **Timestamp Tracking**: Every entry is automatically timestamped
- **Validation**: Input validation to ensure data quality
- **Visual Feedback**: Success/error notifications and loading indicators
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud account
- Google Sheets API enabled

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd amr-data-entry
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Google Cloud credentials** (see detailed setup below)

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🔧 Detailed Setup

### Step 1: Create Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Library**
4. Search for and enable **Google Sheets API** and **Google Drive API**
5. Go to **APIs & Services** → **Credentials**
6. Click **Create Credentials** → **Service Account**
7. Fill in the service account details and click **Create**
8. Grant the service account role (e.g., Editor) and click **Done**
9. Click on the created service account
10. Go to the **Keys** tab
11. Click **Add Key** → **Create New Key**
12. Select **JSON** format and click **Create**
13. Save the downloaded JSON file securely

### Step 2: Configure Streamlit Secrets

1. Create a `.streamlit` directory in your project root:
```bash
mkdir .streamlit
```

2. Create a `secrets.toml` file inside `.streamlit` directory:
```bash
touch .streamlit/secrets.toml
```

3. Open the JSON key file you downloaded and copy its contents to `secrets.toml` in this format:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

**Important**: Make sure to keep `\n` characters in the private_key field!

### Step 3: Set Up Google Sheet

1. Create a new Google Sheet
2. Name it (e.g., "AMR_Data")
3. Share the sheet with your service account email (found in `client_email` in the JSON file)
4. Give it **Editor** permissions

### Step 4: Update Application Configuration

In `app.py`, update the sheet name in the `append_to_sheet()` function:

```python
sheet = client.open("AMR_Data").sheet1  # Replace "AMR_Data" with your sheet name
```

## 📊 Data Fields

### Patient Demographics
- **Age**: Patient age (18-120 years)
- **Gender**: Male/Female
- **Setting**: ICU or Internal Medicine
- **Acquisition**: Community or Hospital-acquired
- **BSI Source**: Primary, Lung, Abdomen, or UTI

### Microbiological Data
- **Species**: E. coli, Klebsiella spp., Proteus spp., Pseudomonas spp., Acinetobacter spp.
- **Rectal CPE Positive**: Yes/No

### Clinical Characteristics (Comorbidities)
- Congestive Heart Failure (CHF)
- Chronic Kidney Disease (CKD)
- Tumor
- Diabetes
- Immunosuppressed status

### Resistance Profile
- **CR**: Carbapenem Resistance
- **BL/BLI**: Beta-lactam/Beta-lactamase Inhibitor Resistance
- **FQR**: Fluoroquinolone Resistance
- **3GC_R**: 3rd Generation Cephalosporin Resistance

## 📁 Project Structure

```
amr-data-entry/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .streamlit/
│   └── secrets.toml       # Google credentials (DO NOT COMMIT)
└── .gitignore             # Git ignore file
```

## 🔒 Security Best Practices

1. **Never commit `secrets.toml`** or service account JSON files to version control
2. Add to `.gitignore`:
```
.streamlit/secrets.toml
*.json
__pycache__/
*.pyc
```

3. Use environment variables for production deployments
4. Regularly rotate service account keys
5. Grant minimum necessary permissions to service accounts

## 🌐 Deployment

### Streamlit Cloud

1. Push your code to GitHub (exclude secrets)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in the Streamlit Cloud dashboard:
   - Go to App settings → Secrets
   - Paste your `secrets.toml` content

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t amr-app .
docker run -p 8501:8501 amr-app
```

## 🐛 Troubleshooting

### Common Issues

**1. Authentication Error**
- Verify service account credentials in `secrets.toml`
- Ensure Google Sheets API is enabled
- Check if the sheet is shared with the service account email

**2. Permission Denied**
- Verify the service account has Editor access to the Google Sheet
- Check if the sheet name in the code matches your actual sheet name

**3. Module Not Found**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try creating a virtual environment

**4. Private Key Format Error**
- Ensure private_key in secrets.toml maintains `\n` characters
- Check for proper escaping of special characters

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- Google Sheets API for data storage
- Healthcare professionals who provided requirements

## 📞 Support

For questions or issues, please open an issue on GitHub or contact [your-email@example.com]

## 🔄 Version History

- **v1.0.0** (2025-01-15)
  - Initial release
  - Basic data entry form
  - Google Sheets integration
  - Timestamp tracking

## 📈 Future Enhancements

- [ ] Data visualization dashboard
- [ ] Export functionality (CSV, Excel)
- [ ] Advanced search and filtering
- [ ] User authentication
- [ ] Batch data import
- [ ] Machine learning predictions
- [ ] Multi-language support
- [ ] Offline mode with sync capability

---

Made with ❤️ for better healthcare data management

import os

# Source API
CRM_API_URL    = os.getenv("CRM_API_URL")
CRM_API_TOKEN  = os.getenv("CRM_API_TOKEN")

# Google Sheets
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RAW_TAB_NAME   = "RawData"

# Local staging
STAGING_CSV    = "staging/raw_data.csv"

PRESCRIPTIVE_BUDGET = float(os.getenv("PRESCRIPTIVE_BUDGET", 0))
MAX_MONTHLY_SPEND  = float(os.getenv("MAX_MONTHLY_SPEND", PRESCRIPTIVE_BUDGET))
# Import dependencies
import streamlit as st
from datetime import date

from Utilities.read_files import read_files
from Utilities.mapping import mapping

# Set a title for the page
st.markdown("<h1 style = 'text-align: center; color: green;'>Green EconoME</h1>", unsafe_allow_html = True)
st.markdown("<h2 style = 'text-align: center; color: black;'>Transaction Pro Formatter</h2>", unsafe_allow_html = True)

# Create the upload files for the Quickbooks and Zoho reports
# Upload the quickbooks download containing the existing customers
qb_upload = st.file_uploader('Upload the Quickbooks download.')
st.caption('Upload the Quickbooks report containing existing customers')

# Upload the Zoho reports
# Upload the Opps contracted by account report
opps_acct_upload = st.file_uploader('Upload the Opps Contracted by Account')
st.caption('Upload the Zoho report titled "Opps Contracted Last Week (By Account - i.e. Company Name)"')
# Upload the Opps contracted by building
opps_building_upload = st.file_uploader('Upload the Opps Contracted by Building')
st.caption('Upload the Zoho report titled "Opps Contracted Last Week (By Bldg - i.e. Customer Name)"')

# Check if all files have been uploaded
if (qb_upload and opps_acct_upload and opps_building_upload) is not None:
    # Create a button to start the formatting
    if st.button('Format Transaction Pro Upload'):
        # Read in the dataframes and format the zoho_df
        zoho_df, qb_df = read_files(qb_upload, opps_acct_upload, opps_building_upload)

        # Map the zoho data to the transaction pro df
        tp_df = mapping(zoho_df, qb_df)

        # Create the csv file to be exported
        tp_export = tp_df.to_csv(index = False).encode('utf-8')

        # Get today's date to put in the title of the workbook export
        today = date.today()
        today = today.strftime("%m-%d-%y")

        # Create a download button for the transporter pro data
        st.download_button(label = 'Download Transaction Pro Worksheet', 
                            data = tp_export, 
                            file_name = f'TP Upload {today}.csv')


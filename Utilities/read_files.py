# Import dependencies
import pandas as pd

def read_files(qb_upload, opps_acct_upload, opps_building_upload):
    # Read in the files
    # Read in the quickbooks download
    qb_df = pd.read_excel(qb_upload, 
                            sheet_name = 'Sheet1', 
                            usecols = ['Customer'])
    # Read in the opps contracted by Acct
    opps_acct = pd.read_excel(opps_acct_upload, 
                            skiprows = 1, 
                            usecols = ['Opportunity Name', 
                                        'Contract Number', 
                                        'Account Name', 
                                        'Full Name', 
                                        'Phone',
                                        'Mobile', 
                                        'Email', 
                                        'Billing Name',
                                        'Billing Street',
                                        'Billing City',
                                        'Billing State',
                                        'Billing Zip Code'], 
                            skipfooter = 3)
    # Read in the opps contracted by Building
    opps_bldg = pd.read_excel(opps_building_upload, 
                            skiprows = 1, 
                            usecols = ['Contract Number',
                                        'Building Name'], 
                            skipfooter = 3)

    # Create the Zoho df by merging the Zoho reports and formatting
    zoho_df = pd.merge(opps_bldg, opps_acct, on = 'Contract Number', how = 'inner')
    # Drop the duplicates to avoid submitting multiples of the Year A of Year B
    zoho_df.drop_duplicates(inplace = True)
    # Create First and Last Name columns by splitting the Full Name column
    zoho_df['First Name'] = [x.split(' ', 1)[0] for x in zoho_df['Full Name']]
    zoho_df['Last Name'] = [x.split(' ', 1)[1] for x in zoho_df['Full Name']]
    # Remove the commas from the billing city - not all have commas can add after
    zoho_df['Billing City'] = zoho_df['Billing City'].str.replace(',', '')
    # Remove the .0 from the zip code and format as a string
    zoho_df['Billing Zip Code'] = zoho_df['Billing Zip Code'].astype(str).str.replace('.0', '', regex = False)
    # Create a column for the billing address by combining columns for city state and zipcode
    zoho_df['City State Zip'] = zoho_df['Billing City'] + ', ' + zoho_df['Billing State'] + ' ' + zoho_df['Billing Zip Code']

    # Create a helper function to parse the address into street, city, state and zip code
    def parse_address(x, part):
        try:
            if part == 'street':
                return(x.split(',')[0])
            elif part == 'city':
                return(x.split(',')[1].strip())
            elif part == 'state':
                return(x.split(',')[2].strip().split()[0])
            elif part == 'zip':
                return(x.split(',')[2].strip().split()[1])
            else:
                raise Exception('Enter part of address as one of street, city, state or zip')
        except:
            pass

    # Parse the Address to create the columns for street, city, state and zip
    zoho_df['ShipTo Line 2'] = [parse_address(x, 'street') for x in zoho_df['Building Name']]
    zoho_df['ShipTo City'] = [parse_address(x, 'city') for x in zoho_df['Building Name']]
    zoho_df['Ship To State'] = [parse_address(x, 'state') for x in zoho_df['Building Name']]
    zoho_df['Ship To Postal Code'] = [parse_address(x, 'zip') for x in zoho_df['Building Name']]

    # Return the Zoho and QuickBooks dfs
    return zoho_df, qb_df
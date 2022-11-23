# Import dependencies
import copy
import pandas as pd

# Define the function to map the zoho information to the Transaction Pro upload
def mapping(zoho_df, qb_df):
    # Create a variable to hold the names of customers that are created
    new_customers = []
    tp_data = []
    for row in zoho_df.index:
        # Create a dictionary to hold the data for the current job
        job_dict = {}
        
        # Create a boolean that will check to see if a customer needs to get created
        create_customer = False
        
        
        # Creating the customer name, this is the Opportunity name without the beginning of the contract number
        new_name = zoho_df.loc[row, 'Opportunity Name'].replace('-'.join(zoho_df.loc[row, 'Contract Number'].split('-', 2)[:2]), '').strip()
        if new_name[0] == '-':
            new_name = new_name.split('-', 1)[1].strip()
        
        # Check if the customer name already exists in QB, or if we have already created a customer during current upload
        if new_name not in qb_df['Customer'].values:
            if new_name not in new_customers:
                create_customer = True
                new_customers.append(new_name)
            
        # Create the customer:job name within the job dict
        job_dict['Customer Name'] = ':'.join([new_name, zoho_df.loc[row, 'Contract Number'].strip()])
                
        # Create a dictionary to map the columns from the zoho_df to the transaction pro labels
        mapping = {
                'Company Name' : 'Account Name', 
                'First Name' : 'First Name', 
                'Last Name' : 'Last Name', 
                'Phone' : 'Phone', 
                'Alt. Phone' : 'Mobile', 
                'Email' : 'Email',
                'Bill To Line 1' : 'Billing Name',
                'Bill 2 Line 2' : 'Full Name', 
                'Bill To Line 3' : 'Billing Street',
                'Bill To Line 4' : 'City State Zip', 
                'ShipTo Line 1' : 'Billing Name', 
                'ShipTo Line 2' : 'ShipTo Line 2', 
                'ShipTo City' : 'ShipTo City', 
                'Ship To State' : 'Ship To State',
                'Ship To Postal Code' : 'Ship To Postal Code'
        }
        
        # Add the columns that are included in both the job and customer uploads
        for key, value in mapping.items():
            job_dict[key] = zoho_df.loc[row, value]
        
        # If we need to create the customer, create a copy of the job_dict and make the name the customer name (new_name)
        if create_customer:
            # Copy the job dictionary to create a customer dictionary
            new_customer_dict = copy.deepcopy(job_dict)
            # Rename the customer name to just be the new_name (the customer's name)
            new_customer_dict['Customer Name'] = new_name
            # Remove the key,value pairs that are only used for the job upload from the customer dictionary
            for key in ['ShipTo Line 1', 'ShipTo Line 2', 'ShipTo City', 'Ship To State', 'Ship To Postal Code']:
                del new_customer_dict[key]
            # Append the new customer dictionary to the transaction pro list
            tp_data.append(new_customer_dict)
        # Append the job dictionary to the transaction pro list
        tp_data.append(job_dict)
    # Create a dataframe from the transaction pro job and customer data
    tp_df = pd.DataFrame(tp_data)

    # Return the transaction pro df
    return tp_df
import pandas as pd

def translate_columns(df, translation_dict):
    return df.rename(columns=translation_dict)

def categorize_description(description, keywords):
    for keyword in keywords:
        if keyword.lower() in description.lower():
            return keyword
    return None

def combine_xls_files(file1, file2, output_file):
    # Translation dictionary from Dutch to English
    translation_dict = {
        'Rekeningnummer': 'accountNumber',
        'Muntsoort': 'mutationcode',
        'Transactiedatum': 'transactiondate',
        'Rentedatum': 'valuedate',
        'Beginsaldo': 'startsaldo',
        'Eindsaldo': 'endsaldo',
        'Transactiebedrag': 'amount',
        'Omschrijving': 'description'
    }
    
    # Keywords to search for in the description
    keywords = ['picnic', 'dropbox', 'NS REIZIGERS', 'Gamma', 'Jumbo', 'Etos', 'Albert Heijn', 'Shell', 'Bol.com', 'Coolblue', 'IKEA', 'MediaMarkt', 'H&M', 'HEMA', 'Primark', 'Zalando', 'Wehkamp', 'BCC', 'KARWEI', 'Hornbach', 'Praxis', 'Action', 'Kwantum','AH to Go']
    
    # Read the two XLS files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # Remove leading empty columns if any
    df1 = df1.loc[:, ~df1.columns.str.match('Unnamed')]
    df2 = df2.loc[:, ~df2.columns.str.match('Unnamed')]
    
    # Translate Dutch columns to English
    df1 = translate_columns(df1, translation_dict)
    df2 = translate_columns(df2, translation_dict)
    
    # Combine the dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    # Add 'For' column based on keywords in 'description'
    combined_df['For'] = combined_df['description'].apply(lambda x: categorize_description(x, keywords))
    
    # Write the combined dataframe to a new XLSX file
    combined_df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == "__main__":
    file1 = 'data/XLS241025082845.xls'
    file2 = 'data/XLS241025203014.xls'
    output_file = 'data/combined_output.xlsx'  # Change the output file extension to .xlsx
    
    combine_xls_files(file1, file2, output_file)
    print(f"Combined file saved as {output_file}")
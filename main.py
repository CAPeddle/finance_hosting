import pandas as pd
import toml
from datetime import datetime

def translate_columns(df, translation_dict):
    return df.rename(columns=translation_dict)

def categorize_description(description, keywords):
    for keyword in keywords:
        if keyword.lower() in description.lower():
            return keyword
    return None

def categorize_for(for_value, category_dict):
    for category, keywords in category_dict.items():
        if isinstance(keywords, dict):
            for canonical_keyword, variations in keywords.items():
                if for_value in variations:
                    return category
        elif for_value in keywords:
            return category
    return 'Other'

def load_toml(file_path):
    with open(file_path, 'r') as file:
        data = toml.load(file)
    return data

def combine_xls_files(file1, file2, output_file, translation_file, category_mapping_file):
    # Load column translations from file
    translation_dict = load_toml(translation_file)['translations']
    
    # Load category mapping from file
    category_dict = load_toml(category_mapping_file)['categories']
    
    # Keywords to search for in the description
    keywords = []
    for kw in category_dict.values():
        if isinstance(kw, dict):
            for variations in kw.values():
                keywords.extend(variations)
        else:
            keywords.extend(kw)
    
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
    
    # Add 'Category' column based on 'For' column
    combined_df['Category'] = combined_df['For'].apply(lambda x: categorize_for(x, category_dict))
    
    # Convert 'transactiondate' to datetime
    combined_df['transactiondate'] = pd.to_datetime(combined_df['transactiondate'], format='%Y%m%d')
    
    # Group by month
    combined_df['Month'] = combined_df['transactiondate'].dt.to_period('M')
    
    # Move 'description' column to the end
    cols = [col for col in combined_df.columns if col != 'description'] + ['description']
    combined_df = combined_df[cols]
    
    # Write the combined dataframe to a new XLSX file with different sheets for each month
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for month, group in combined_df.groupby('Month'):
            group.drop(columns=['Month'], inplace=True)
            group.to_excel(writer, sheet_name=str(month), index=False)
    
    print(f"Combined file saved as {output_file}")

if __name__ == "__main__":
    file1 = 'data/XLS241025082845.xls'
    file2 = 'data/XLS241025203014.xls'
    output_file = 'data/combined_output.xlsx'  # Change the output file extension to .xlsx
    translation_file = 'data/column_translations.toml'  # Path to the column translations file
    category_mapping_file = 'data/category_mapping.toml'  # Path to the category mapping file
    
    combine_xls_files(file1, file2, output_file, translation_file, category_mapping_file)
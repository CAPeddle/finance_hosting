import pandas as pd
import yaml

def translate_columns(df, translation_dict):
    return df.rename(columns=translation_dict)

def categorize_description(description, keywords):
    for keyword in keywords:
        if keyword.lower() in description.lower():
            return keyword
    return None

def categorize_for(for_value, category_dict):
    for category, keywords in category_dict.items():
        if for_value in keywords:
            return category
    return 'Other'

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    # Check if 'categories' exists in the data
    if 'categories' in data:
        # Check for duplicate keywords
        all_keywords = [keyword for sublist in data['categories'].values() for keyword in sublist]
        duplicates = set([keyword for keyword in all_keywords if all_keywords.count(keyword) > 1])
        if duplicates:
            raise ValueError(f"Duplicate keywords found in category mapping file: {', '.join(duplicates)}")
            
    
    return data

def combine_xls_files(file1, file2, output_file, translation_file, category_mapping_file):
    # Load column translations from file
    translation_dict = load_yaml(translation_file)['translations']
    
    # Load category mapping from file
    category_dict = load_yaml(category_mapping_file)['categories']
    
    # Keywords to search for in the description
    keywords = [keyword for sublist in category_dict.values() for keyword in sublist]
    
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
    
    # Reorder columns to place 'For' and 'Category' before 'description'
    cols = list(combined_df.columns)
    cols.insert(cols.index('description'), cols.pop(cols.index('Category')))
    cols.insert(cols.index('description'), cols.pop(cols.index('For')))
    combined_df = combined_df[cols]
    
    # Write the combined dataframe to a new XLSX file
    combined_df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == "__main__":
    file1 = 'data/XLS241025082845.xls'
    file2 = 'data/XLS241025203014.xls'
    output_file = 'data/combined_output.xlsx'  # Change the output file extension to .xlsx
    translation_file = 'data/column_translations.yaml'  # Path to the column translations file
    category_mapping_file = 'data/category_mapping.yaml'  # Path to the category mapping file
    
    combine_xls_files(file1, file2, output_file, translation_file, category_mapping_file)
    print(f"Combined file saved as {output_file}")
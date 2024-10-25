import pandas as pd

def combine_xls_files(file1, file2, output_file):
    # Read the two XLS files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # Combine the dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    # Write the combined dataframe to a new XLSX file
    combined_df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == "__main__":
    file1 = 'data/XLS241025082845.xls'
    file2 = 'data/XLS241025203014.xls'
    output_file = 'data/combined_output.xlsx'  # Change the output file extension to .xlsx
    
    combine_xls_files(file1, file2, output_file)
    print(f"Combined file saved as {output_file}")
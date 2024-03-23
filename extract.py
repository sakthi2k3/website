import pandas as pd

# Function to extract all columns from an Excel file
def get_all_columns_from_excel(excel_path):
    try:
        df = pd.read_excel(excel_path)
        transposed_df = df.T
        list_of_lists = transposed_df.values.tolist()
        return list_of_lists
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to extract specific columns for specified names and return as a dictionary
def extract_columns_for_names(excel_path, names_list):
    try:
        original_df = pd.read_excel(excel_path)
        data_dict = {}
        for name in names_list:
            filtered_data = original_df[original_df['name'] == name]
            if not filtered_data.empty:
                data_dict[name] = filtered_data.to_dict(orient='records')
        return data_dict
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to find strings in a text file
def find_strings_in_file(file_path, search_strings):
    try:
        with open(file_path, 'r') as file:
            text_content = file.read()
        found_strings = [string for string in search_strings if string in text_content]
        return found_strings
    except Exception as e:
        print(f"Error: {e}")
        return None

# Helper function to check if list1 is a subset of list2
def is_subset(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return set1.issubset(set2)

# Define column extraction logic directly in the main function
def get_column_from_excel(excel_path, column_name):
    try:
        # Read Excel sheet into a DataFrame
        df = pd.read_excel(excel_path)

        # Check if the specified column exists in the DataFrame
        if column_name in df.columns:
            # Extract the specified column as a list
            column_values = df[column_name].tolist()
            return column_values
        else:
            print(f"Error: Column '{column_name}' not found in the Excel sheet.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main function
def extract(excel_file_path):
    # Extract all columns from Excel file
    result = get_all_columns_from_excel(excel_file_path)

    if result is not None:
        # Extracted column names
        column_names = result[0]

        # Extract the 'name' column from the Excel file
        column_name_to_extract = 'name'
        result_column = get_column_from_excel(excel_file_path, column_name_to_extract)
        
        if result_column is not None:
            d=extract_columns_for_names("meds.xlsx", result_column)
            print(d)
            return d
        else:
            print("Error extracting column from Excel file.")
            return None
    else:
        print("Error extracting columns from Excel file.")
        return None

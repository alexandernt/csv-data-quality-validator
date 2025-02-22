import pandas as pd
import re
import json

pd.options.display.max_rows = None  # Removes limit and show all rows

# File path and primary key settings

primary_key_column = "Rk"
path = "input/csv/"
file_name = "snic-provicias"
file_type = ".csv"
file_path = f"{path}{file_name}{file_type}"


# Define a regex pattern for special characters
special_chars_pattern = re.compile(r'[<>?/{}\[\]!@#$%^&*()]')

# Function to extract values with special characters in a single column
def extract_special_character_values(column):
    return column[column.astype(str).apply(lambda x: bool(special_chars_pattern.search(str(x))))]

# Function to extract all special character values across all columns
def extract_all_special_character_values(df):
    special_values_dict = {}
    for column in df.columns:
        special_values = extract_special_character_values(df[column])
        if not special_values.empty:
            special_values_dict[column] = special_values.tolist()  # Convert to list for JSON compatibility

    return special_values_dict  # Return as dictionary for JSON export

def main(path, primary_key):
    # Read CSV file
    df = pd.read_csv(path)

    # Function to count rows in each column that contain special characters
    def count_special_characters(column):
        return column.astype(str).apply(lambda x: bool(special_chars_pattern.search(str(x)))).sum()

    # Count columns and rows
    total_columns = len(df.columns)
    total_rows = df.shape[0]
    print(f'\n🛈 This dataset contains {total_columns} columns.')
    print(f'\n🛈 This dataset contains {total_rows} rows.')

    # Check for primary key duplicates
    if primary_key in df.columns:
        duplicate_pk_count = df[primary_key].duplicated().sum()
        if duplicate_pk_count > 0:
            print(f"\n❌ WARNING: The primary key '{primary_key}' has {duplicate_pk_count} duplicate values!")
        else:
            print(f"\n✅ The primary key '{primary_key}' is unique.")
    else:
        print(f"\n⚠️ WARNING: The primary key column '{primary_key}' was not found in the dataset.")
    
    # Calculate missing values
    missing_values = df.isnull().sum()

    # Count special character occurrences in each column
    special_character_counts = df.apply(count_special_characters)

    # Get data types of each column
    data_types = df.dtypes

    # Check if column names are duplicated
    is_duplicated_column = pd.Series(df.columns.duplicated(), index=df.columns)

    # Create a DataFrame with missing values and special character counts
    column_quality_df = pd.DataFrame({
        "column_name": missing_values.index,
        "data_type": data_types.values.astype(str),
        "total_nulls": missing_values.values,
        "percent_of_nulls": (missing_values.values / len(df)),
        "total_special_characters": special_character_counts.values,
        "is_duplicated_column": is_duplicated_column.values  # New column for column name duplication
    })

    # Print missing values DataFrame
    print("\n Data Quality Checks for Columns:")
    print(column_quality_df)

    # Identify duplicated rows
    duplicate_mask = df.duplicated(keep=False)  # Marks all duplicates (including first occurrence)
    duplicated_rows = df[duplicate_mask]  # Extract only duplicate rows

    # Print only if there are duplicate rows
    if not duplicated_rows.empty:
        print("\n❌ Duplicate Rows Found:")
        print(duplicated_rows)
    else:
        print("\n✅ No duplicate rows found.")

    return df, column_quality_df  # Keep the original return of main()

# Execute main() and store the resulting DataFrame and column quality report
df_original, column_quality_df = main(file_path, primary_key_column)

# Extract values with special characters
special_characters_json = extract_all_special_character_values(df_original)

# **Save special character values to a JSON file**
json_filename = "output/json/special_characters.json"
with open(json_filename, "w") as f:
    json.dump(special_characters_json, f, indent=4)

print(f"\n📁 Special character values saved to {json_filename}")

# **Save column quality DataFrame to CSV**
column_quality_filename = "output/csv/column_quality.csv"
column_quality_df.to_csv(column_quality_filename, index=False)

print(f"\n📁 Column quality report saved to {column_quality_filename}")
# Purpose
To analyze a .csv file for data quality errors/discrepencies.

# How to use
1) Inside input/csv add the .csv file that you would like to validate.
2) Replace following variables with the correct attributes:
```
primary_key_column = "Rk"
path = "input/csv/"
file_name = "snic-provicias"
file_type = ".csv"
special_chars_pattern = re.compile(r'[<>?/{}\[\]!@#$%^&*()]')
```
Special_chars_pattern runs a validation for each column and value, and identifies if any value contains a special character listed within this variable. Feel free to modify it accordingly. 

# What does this script anaylize:
- Returns total rows
- Returns total columns
- Checks if the primary key (assigned manually on the primary_key_column variable) has duplicates.
- Returns count and percentage of null values inside a column.
- Returns counts of special characters.
- Creates a flag that identifies if the column is duplicated on the spreadsheet. For instance, if column 'region' exists two times in all the spreadsheet, flag will be True.
- Checks for rows duplicates and returns duplicates as a dataframe.
- Creates a .json file inside output folder named 'special_characters'. You will be able to identfiy all the special characters.
- Returns .csv inside output folder with the data_quality checks results. 

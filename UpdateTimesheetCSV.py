import pandas as pd
import numpy as np
import os

# Get the input file path from the user
file_path = input("Enter the input file path: ")
# Load the CSV file
df = pd.read_csv(file_path)

# Ensure the date column is in datetime format (replace 'Date' with your actual column name if different)
df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by date in ascending order
df = df.sort_values(by='Date').reset_index(drop=True)

# Create a 'Day' column with the day of the week
df['Day'] = df['Date'].dt.day_name()

# Create a 'Week' column with the week of the month
def week_of_month(date):
    first_day = date.replace(day=1)
    dom = date.day
    adjusted_dom = dom + first_day.weekday()
    return int(np.ceil(adjusted_dom / 7.0))

df['Week'] = df['Date'].apply(week_of_month)

# Change the date format to DD/MM/YYYY
df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

# Generate a complete range of dates from the minimum to maximum date in the DataFrame
all_dates = pd.date_range(start=pd.to_datetime(df['Date'], format='%d/%m/%Y').min(),
                          end=pd.to_datetime(df['Date'], format='%d/%m/%Y').max())

# Create a new DataFrame with the complete date range
new_df = pd.DataFrame(all_dates, columns=['Date'])
new_df['Week'] = pd.to_datetime(new_df['Date'], format='%d/%m/%Y').apply(week_of_month)
new_df['Date'] = new_df['Date'].dt.strftime('%d/%m/%Y')
new_df['Day'] = pd.to_datetime(new_df['Date'], format='%d/%m/%Y').dt.day_name()

# Initialize columns for Project and Description with NaN values
new_df['Project'] = np.nan
new_df['Description'] = np.nan
new_df['Hours'] = np.nan

# Iterate through the new DataFrame and add rows for the week headers
output_rows = []
current_week = None

for index, row in new_df.iterrows():
    week_number = row['Week']
    
    # If the week changes, add a "Week X" row
    if current_week != week_number:
        output_rows.append({'Week': f'Week {week_number}', 'Date': '', 'Day': '', 'Project': '', 'Description': ''})
        current_week = week_number
    
    # Copy the Project and Description from the original df
    match = df[df['Date'] == row['Date']]
    if not match.empty:
        row['Project'] = match['Project'].values[0]
        row['Description'] = match['Description'].values[0]
        row['Hours'] = match['Time (h)'].values[0]
    
    # Add the actual data row
    output_rows.append(row)

# Convert the list of dictionaries to a DataFrame
final_df = pd.DataFrame(output_rows)

# Save the modified DataFrame to a new CSV file
# Generate the output file path with _updated postfix
output_file_path = os.path.splitext(file_path)[0] + '_updated.csv'
final_df.to_csv(output_file_path, index=False)

print(f"Modified csv saved to {output_file_path}")
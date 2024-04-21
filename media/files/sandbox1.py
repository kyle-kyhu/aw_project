import csv
import os
import glob

# Get the current directory
current_directory = os.getcwd()

# Find any CSV file in the current directory
csv_files = glob.glob(os.path.join(current_directory, '*.csv'))

# If there are any CSV files, open the first one
if csv_files:
    with open(csv_files[0], 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    # Add 'test complete' to cell A1
    data[0][0] = 'test complete'

    # Write the data back to the CSV file
    with open(csv_files[0], 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
else:
    print("No CSV files found in the current directory.")

    



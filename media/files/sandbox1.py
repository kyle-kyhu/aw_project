import csv
import os
import glob

# Get the path to the media/files directory
files_directory = os.path.join(os.getcwd(), 'media', 'files')

# Find any CSV file in the media/files directory
csv_files = glob.glob(os.path.join(files_directory, '*.csv'))

# If there are any CSV files, open the most recent one
if csv_files:
    most_recent_file = max(csv_files, key=os.path.getctime)  # Get the most recent file based on creation time
    with open(most_recent_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    # Add 'test complete' to cell A1
    data[0][0] = 'test complete'

    # Write the data back to the CSV file
    with open(most_recent_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

    print("CSV file updated successfully:", most_recent_file)
else:
    print("No CSV files found in the media/files directory.")

    



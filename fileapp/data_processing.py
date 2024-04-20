# import pandas as pd


# class BankReconciliation():
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def process_data_type(self):
#         # read csv file
#         df = pd.read_csv(self.file_path)

#         df = df.dropna(subset=['Data Type'])

#         # Remove rows with "Summary" in the "Data Type" column
#         data = df[df['Data Type'] != 'Summary']

#         return data
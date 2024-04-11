import pandas as pd

class BankCleanData:
    def __init__(self, file):
        self.file = file

    def remove_summary(self):
        df = pd.read_csv(self.file)

        # Remove rows where 'Data Type' is 'Summary'
        df = df[df['Data Type'] != 'Summary']

        return df
    
    def lockbox(self):
        df = pd.read_csv(self.file)

        # If 'Description' contains 'Lockbox Deposit Credit', set 'text' to 'Lockbox Deposit Credit'
        df['text'] = df['Description'].apply(lambda x: 'Lockbox Deposit Credit' if 'Lockbox Deposit Credit' in x else x)

        return df
    
    def remove_columns(self):
        df = pd.read_csv(self.file)

        # Remove columns 'Data Type' and 'Description'
        df = df.drop(columns=[
            'Currency', 
            'BankID Type', 
            'BankID', 
            'BAI Code', 
            'Immediate Availability', 
            '1 Day Float', 
            '2+ Day Float',
            '# of Items',
              ])

        return df
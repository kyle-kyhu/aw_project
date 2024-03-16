
from django.views import View
from django.shortcuts import render
import pandas as pd
from openpyxl import load_workbook

class UploadView(View):
    template_name = 'upload.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        csv_file = request.FILES['csv_file']
        excel_file = request.FILES['excel_file']

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Load the Excel workbook
        workbook = load_workbook(excel_file)

        # Add the DataFrame as a new sheet
        writer = pd.ExcelWriter(excel_file, engine='openpyxl') 
        writer.book = workbook
        df.to_excel(writer, sheet_name='Sheet1')

        # Save the updated Excel file
        writer.save()

        return render(request, self.template_name, {'message': 'Files uploaded and Excel updated successfully'})

from django.views.generic import TemplateView, FormView
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os


from .models import amwell_BOA_bank_rec
from .forms import BankForm
from .data_processing import BankCleanData

class UploadView(FormView):
    model = amwell_BOA_bank_rec
    template_name = 'upload.html'
    form_class = BankForm

    def form_valid(self, form):
        # get csv file from form
        file = form.cleaned_data['csv_upload']

        # clean data in cvs file
        bank_clean_data = BankCleanData(file)
        clean_data = bank_clean_data.clean()

         # save cleaned data to be downloaded
        file_path = os.path.join(settings.MEDIA_ROOT, 'cleaned_data.csv')
        clean_data.to_csv(file_path)

        # add the URL to the cleaned CSV file to the session
        self.request.session['file_url'] = os.path.join(settings.MEDIA_URL, 'cleaned_data.csv')

        # Add a success message
        messages.success(self.request, 'CSV file has been uploaded and processed.')

        # redirect to the same page
        return HttpResponseRedirect(self.request.path)

    
# class ReviewUpload(TemplateView):
#     model = amwell_BOA_bank_rec
#     template_name = 'review_upload.html'
#     form_class = BankForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['file_url'] = self.kwargs['file_url']
#         return context

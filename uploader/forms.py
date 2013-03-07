from django.forms import ModelForm

from uploader.models import *


class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        exclude = ('original_filename', 'sha1')

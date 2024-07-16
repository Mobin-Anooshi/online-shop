from django import forms


class UploadFileForm:
    file_name = forms.FileField()
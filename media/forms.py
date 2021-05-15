from django import forms

from media.util import get_files, get_directories


class GetUserForm(forms.Form):
	login = forms.CharField(label='Your login', max_length=200)
	password = forms.CharField(label='Your password', max_length=200, widget=forms.PasswordInput)


class AddDirectoryForm(forms.Form):
	name = forms.CharField(label='Directory name', max_length=200)
	description = forms.CharField(label='Description', max_length=1000, required=False)

class AddFileForm(forms.Form):
	name = forms.CharField(label='File name', max_length=200)
	description = forms.CharField(label='Description', max_length=1000, required=False)
	parent_directory = forms.ModelChoiceField(get_directories())
	source = forms.FileField()

class RemoveDirectoryForm(forms.Form):
	directory = forms.ModelChoiceField(get_directories())

class RemoveFileForm(forms.Form):
	file = forms.ModelChoiceField(get_files())

from django import forms

from media.util import get_directories


class GetUserForm(forms.Form):
	login = forms.CharField(label='Your login', max_length=200)
	password = forms.CharField(label='Your password', max_length=200, widget=forms.PasswordInput)

class AddDirectoryForm(forms.Form):
	name = forms.CharField(label='Directory name', max_length=200)
	description = forms.CharField(label='Description', max_length=1000, required=False)

class AddFileForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.login = kwargs.pop('login')
		super(AddFileForm, self).__init__(*args, **kwargs)
		self.fields['parent_directory'] = forms.ModelChoiceField(get_directories(self.login))

	name = forms.CharField(label='File name', max_length=200)
	description = forms.CharField(label='Description', max_length=1000, required=False)
	source = forms.FileField()

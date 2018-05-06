from django.forms import ModelForm, ValidationError
import library.models as models

class BookForm(ModelForm):
	class Meta:
		model = models.Book
		exclude = []

class EditorForm(ModelForm):
	class Meta:
		model = models.Editor
		exclude = []

class GenreForm(ModelForm):
	class Meta:
		model = models.Genre
		exclude = []

class EditionForm(ModelForm):
	class Meta:
		model = models.Edition
		exclude = ['item']

	def save(self):
		edition = super(EditionForm, self).save(commit=False)
		it = models.Item()
		it.save()
		edition.item_id = it.id
		edition.save()
		return edition

class AuthorForm(ModelForm):
	class Meta:
		model = models.Author
		exclude = []

	def clean(self):
		"""
		Check if not all the fields are empty
		"""
		cleaned_data = super(AuthorForm, self).clean()
		form_empty = True
		for field_value in cleaned_data.values():
		# Check for None or '', so IntegerFields with 0 or similar things don't seem empty.
			if field_value is not None and field_value != '':
				form_empty = False
				break
		if form_empty:
			raise ValidationError("You must fill at least one field!")
		return cleaned_data   # Important that clean should return cleaned_data!
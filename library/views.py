from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
import library.forms as forms


# Create your views here.
def home(request):
	return render(request, 'index.html')

def search(request):
	return render(request, 'search.html')

def add(request, type, success=None):
	if request.method == 'POST':
		if type == 'book':
			form = forms.BookForm(request.POST)
		elif type == 'author':
			form = forms.AuthorForm(request.POST)
		elif type == 'editor':
			form = forms.EditorForm(request.POST)
		elif type == 'genre':
			form = forms.GenreForm(request.POST)
		elif type == 'edition':
			form = forms.EditionForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('{}success/'.format(reverse('library:add', kwargs={'type': type})))
		else:
			return render(request, 'edit_form.html', {'form': form, 'type':type, 'add_success': False})
	else:
		if type == 'book':
			form = forms.BookForm()
		elif type == 'author':
			form = forms.AuthorForm()
		elif type == 'editor':
			form = forms.EditorForm()
		elif type == 'genre':
			form = forms.GenreForm()
		elif type == 'edition':
			form = forms.EditionForm()
		else:
			raise Http404("This type of item does not exists")
		return render(request, 'edit_form.html', {'form': form, 'type':type, 'add_success': success})

def edit(request, type, id):
	#return render(request, 'edit_form.html')
	return HttpResponse("Edit {}:{}".format(type, id))

def show(request, type, id):
	#return render(request, 'show_item.html')
	return HttpResponse("Show {}:{}".format(type, id))

def show_all(request, type):
	#return render(request, 'show_all.html')
	return HttpResponse("Show {}".format(type))

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
import library.forms as forms
import library.models as models

# Create your views here.
def home(request):
	return render(request, 'index.html')

def search(request):
	if request.method == 'GET':
		search_query = request.GET.get('search_box', None)

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
	if type == 'book':
		b = models.Book.objects.get(id=id)
		return render(request, 'show_item/book.html', {'b':b})
	elif type == 'author':
		a = models.Author.objects.get(id=id)
		return render(request, 'show_item/author.html', {'a':a})
		
	else:
		#return render(request, 'show_item.html')
		return HttpResponse("Show {}:{}".format(type, id))

def show_all(request, type):
	if type == 'book':
		books = models.Book.objects.all()
		return render(request, 'show_item/all.html', {'books':books})
	if type == 'author':
		authors = models.Author.objects.all()
		return render(request, 'show_item/all.html', {'authors':authors})
	#return render(request, 'show_all.html')
	return HttpResponse("Show {}".format(type))

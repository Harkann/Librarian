from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Q
import library.forms as forms
import library.models as models

# Create your views here.
def home(request):
	return render(request, 'index.html')

def search(request):
	if request.method == 'POST':
		form = forms.SearchForm(request.POST)
		books, editions, genres, editors, authors = None, None, None, None, None
		form.is_valid()
		s = form.cleaned_data['search_bar']
		if form.cleaned_data['books']:
			books = models.Book.objects.filter(
				Q(id__iexact=s) | Q(original_title=s) | (
					Q(authors__name=s) | Q(authors__surname=s) | Q(authors__pseudo=s)))
		if form.cleaned_data['authors']:
			authors = models.Author.objects.filter(
				Q(id__iexact=s) | Q(name=s) | Q(surname=s) | Q(pseudo=s))
		if form.cleaned_data['editors']:
			pass
		if form.cleaned_data['editions']:
			pass
		if form.cleaned_data['genres']:
			pass
		return render(request, 'show_item/all.html', {'books':books, 'authors':authors, 'genres':genres, 'editors':editors, 'editions':editions})
	
	form = forms.SearchForm()
	return render(request, 'search.html', {'form':form})
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

def edit(request, type, id, success=None):
	if request.method == 'POST':
		if type == 'book':
			obj = get_object_or_404(models.Book, id=id)
			form = forms.BookForm(request.POST, instance=obj)
		elif type == 'author':
			obj = get_object_or_404(models.Author, id=id)
			form = forms.AuthorForm(request.POST, instance=obj)
		elif type == 'editor':
			obj = get_object_or_404(models.Editor, id=id)
			form = forms.EditorForm(request.POST, instance=obj)
		elif type == 'genre':
			obj = get_object_or_404(models.Genre, id=id)
			form = forms.GenreForm(request.POST, instance=obj)
		elif type == 'edition':
			obj = get_object_or_404(models.Edition, id=id)
			form = forms.EditionForm(request.POST, instance=obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('{}success/'.format(reverse('library:add', kwargs={'type': type})))
		else:
			return render(request, 'edit_form.html', {'form': form, 'type':type, 'add_success': False})
	else:
		if type == 'book':
			obj = get_object_or_404(models.Book, id=id)
			form = forms.BookForm(instance=obj)
		elif type == 'author':
			bj = get_object_or_404(models.Author, id=id)
			form = forms.AuthorForm(instance=obj)
		elif type == 'editor':
			obj = get_object_or_404(models.Editor, id=id)
			form = forms.EditorForm(instance=obj)
		elif type == 'genre':
			obj = get_object_or_404(models.Genre, id=id)
			form = forms.GenreForm(instance=obj)
		elif type == 'edition':
			obj = get_object_or_404(models.Edition, id=id)
			form = forms.EditionForm(instance=obj)
		else:
			raise Http404("This type of item does not exists")
		return render(request, 'edit_form.html', {'form': form, 'type':type, 'add_success': success})


def show(request, type, id):
	if type == 'book':
		b = get_object_or_404(models.Book, id=id)
		return render(request, 'show_item/book.html', {'b':b})
	elif type == 'author':
		a = get_object_or_404(models.Author, id=id)
		return render(request, 'show_item/author.html', {'a':a})
	elif type == 'editor':
		e = get_object_or_404(models.Editor, id=id)
		return render(request, 'show_item/editor.html', {'e':e})
	elif type == 'genre':
		g = get_object_or_404(models.Genre, id=id)
		return render(request, 'show_item/genre.html', {'g':g})
	elif type == 'edition':

		if request.method == 'POST':
			form = forms.CommentForm(request.POST)
			if form.is_valid():
				form.save(id)

		e = get_object_or_404(models.Edition, id=id)
		form = forms.CommentForm()
		comments = models.Comment.objects.filter(about=id)
		return render(request, 'show_item/edition.html', {'e':e, 'form':form, 'comments':comments})
	else:
		raise Http404("This type of item does not exists")

def show_all(request, type):
	if type == 'book':
		books = models.Book.objects.all()
		return render(request, 'show_item/all.html', {'books':books})
	elif type == 'author':
		authors = models.Author.objects.all()
		return render(request, 'show_item/all.html', {'authors':authors})
	elif type == 'editor':
		editors = models.Editor.objects.all()
		return render(request, 'show_item/all.html', {'editors':editors})
	elif type == 'genre':
		genres = models.Genre.objects.all()
		return render(request, 'show_item/all.html', {'genres':genres})
	elif type == 'edition':
		editions = models.Edition.objects.all()
		return render(request, 'show_item/all.html', {'editions':editions})
	return HttpResponse("Show {}".format(type))

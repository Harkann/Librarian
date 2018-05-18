from django.db import models
from django.contrib.auth.models import User
from django.core import validators
import library.config as config

class LibUser(models.Model):
	"""
	An user of Librarian
	"""
	user = models.OneToOneField(User,
		on_delete=models.CASCADE)
	#name
	#surname
	#birthdate = models.DateField()
	#email
	#password
	#is_admin
	def __str__(self):
		return "{}'s profile".format(self.user)

class Item(models.Model):
	"""
	Regroup all items on which a comment can be added
	"""
	creator = models.ForeignKey(LibUser,
		null=True,
		on_delete=models.SET_NULL)

class Editor(models.Model):
	"""
	An editor
	"""
	name = models.CharField(max_length=256, unique=True)
	wiki_page = models.URLField(blank=True)

	def __str__(self):
		return '{}'.format(self.name)

class Genre(models.Model):
	"""
	A genre
	"""
	name = models.CharField(max_length=256)
	description = models.TextField(blank=True)

	def __str__(self):
		return '{}'.format(self.name)

class Author(models.Model):
	"""
	An author
	"""
	name = models.CharField(max_length=256,
		blank=True)
	surname = models.CharField(max_length=256,
		blank=True)
	pseudo = models.CharField(max_length=256,
		blank=True)
	birthdate = models.DateField(null=True)
	death = models.DateField(null=True)
	wiki_page = models.URLField(blank=True)

	def __str__(self):
		return ('{} {} {}'.format(self.surname, self.pseudo, self.name).strip())

	def required(self):
		return ['name', 'surname', 'pseudo']

class Book(models.Model):
	"""
	A book
	"""
	original_title = models.CharField(max_length=256)
	wiki_page = models.URLField(blank=True)
	authors = models.ManyToManyField(Author)
	genres = models.ManyToManyField(Genre)

	def __str__(self):
		authors_string = ''
		for aut in self.authors.all():
			authors_string += ', {}'.format(aut)
		return '{}{}'.format(self.original_title, authors_string)

class Edition(models.Model):
	"""
	An edition can regroup multiple books
	"""
	item = models.OneToOneField(Item,
		on_delete=models.CASCADE)
	ISBN = models.CharField(max_length=10,
		unique=True)
	ISBN13 = models.CharField(max_length=13,
		unique=True)
	title = models.CharField(max_length=256)
	lang = models.CharField(max_length=256)
	nb_pages = models.PositiveIntegerField(null=True)
	format = models.CharField(max_length=256,
		choices=config.BOOK_FORMAT,
		blank=True)
	#front_cover = ImageField(upload_to=upload_front)
	#back_cover = ImageField(upload_to=upload_back)
	#side = ImageField(upload_to=upload_side)
	editor = models.ForeignKey(Editor,
		on_delete=models.PROTECT)
	books = models.ManyToManyField(Book)

	def __str__(self):
		return '{}'.format(self.title)


class List(models.Model):
	"""
	A list of books created by an user
	"""
	item = models.OneToOneField(Item,
		on_delete=models.CASCADE)
	name = models.CharField(max_length=256)
	description = models.TextField(blank=True)
	editions = models.ManyToManyField(Edition)

	def __str__(self):
		return '{}'.format(self.name)


class Comment(models.Model):
	"""
	A comment about an item
	"""
	item = models.OneToOneField(Item,
		on_delete=models.CASCADE)
	title = models.CharField(max_length=256)
	content = models.TextField()
	about = models.ForeignKey(Item,
		on_delete=models.CASCADE,
		related_name='+')

	def __str__(self):
		return '{}'.format(self.title)


class Summary(models.Model):
	"""
	A summary about an edition
	"""
	item = models.OneToOneField(Item,
		on_delete=models.CASCADE)
	title = models.CharField(max_length=256)
	content = models.TextField()
	edition = models.ManyToManyField(Edition)

	def __str__(self):
		return '{}'.format(self.title)

class Rate(models.Model):
	"""
	A rate about an edition
	"""
	creator = models.ForeignKey(LibUser,
		on_delete=models.CASCADE)
	value = models.PositiveIntegerField(
		validators=[validators.MaxValueValidator(config.max_rate)]
		)
	edition = models.ManyToManyField(Edition)

	def __str__(self):
		return '{}/{}'.format(self.value, config.max_rate)


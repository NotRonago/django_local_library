from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import PermissionsMixin
import uuid

# Create your models here.

# class User(AbstractUser):
#     pass 

class Genre(models.Model):
    name = models.CharField(max_length= 200, unique= True, help_text="Enter a Book Genre")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(models.functions.Lower('name'), name= 'genre_name_case_insensitive_unique', violation_error_message= 'Genre already exists (case insensitive match)'),
        ]

class Language(models.Model):
    name = models.CharField(max_length= 200, unique= True, help_text= 'Enter the book\'s natural language (e.g. English, French, Japanese etc.)')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(models.functions.Lower('name'), name= 'language_name_case_insensitive_unique', violation_error_message= 'Language already exists (case insensitive match)'),
        ]

class Book(models.Model):
    title = models.CharField(max_length= 200)
    author = models.ForeignKey('Author', on_delete= models.RESTRICT, null= True)
    summary = models.TextField(max_length= 1000, help_text= 'Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length= 13, help_text= '13 Character <a href="https://www.isbn-international.org/content/what-isbn''">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'genre'
    
class BookInstace(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, help_text= 'Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete= models.RESTRICT, null= True)
    imprint = models.CharField(max_length= 200)
    due_back = models.DateField(null= True, blank= True)
    borrower = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, blank= True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length= 1, choices= LOAN_STATUS, blank= True, default= 'm', help_text= 'Book availability')

    def __str__(self):
        return '{} ({})'.format(self.id, self.book.title)

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

class Author(models.Model):
    first_name = models.CharField(max_length= 100)
    last_name = models.CharField(max_length= 100)
    date_of_birth = models.DateField(null= True, blank= True)
    date_of_death = models.DateField('Died', null= True, blank= True)

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.last_name)
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['last_name', 'first_name']

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Book, BookInstace, Author, Genre

# Create your views here.
def index(request):

    num_books = Book.objects.all().count()
    num_instance = BookInstace.objects.all().count()

    num_status = BookInstace.objects.filter(status__exact= 'a').count()

    num_author = Author.objects.all().count()
    num_genre = Genre.objects.all().count()

    filtered_book = Book.objects.filter(title__contains= 'teke').count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instance': num_instance,
        'num_status': num_status,
        'num_authors': num_author,
        'num_genres': num_genre,
        'num_filtered_books': filtered_book,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    # context_object_name = 'book_list'
    # template_name = 'books/my_arbitrary_template_list_name.html'

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains= 'teke')[:5]
class BookDetailList(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author
from django.shortcuts import render
from .models import Book, BookInstace, Author

# Create your views here.
def index(request):

    num_books = Book.objects.all().count()
    num_instance = BookInstace.objects.all().count()

    num_status = BookInstace.objects.filter(status__exact= 'a').count()

    num_author = Author.objects.all().count()

    context = {
        'num_books': num_books,
        'num_instance': num_instance,
        'num_status': num_status,
        'num_authors': num_author
    }

    return render(request, 'catalog/index.html', context)
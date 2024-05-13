import datetime
from typing import Any
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, BookInstace, Author, Genre
from catalog.forms import RenewBookForm



@login_required
@permission_required('catalog.can_mark_renewal', raise_exception= True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstace, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks= 3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstace
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstace.objects.filter(borrower = self.request.user)
            .filter(status__exact = 'o')
            .order_by('due_back')
        )

class BorrowedByUserListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstace
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 3
    permission_required = ('catalog/can_mark_returned')

    def get_queryset(self):
        return BookInstace.objects.filter(status__exact = 'o').order_by('due_back')
    
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_auther'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e: 
            return HttpResponseRedirect(reverse('author-delete', kwargs={'pk': self.object.pk}))
        
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book 
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except:
            return HttpResponseRedirect(reverse('book-delete', kwargs= {'pk': self.object.pk}))
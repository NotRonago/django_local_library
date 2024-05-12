from django.contrib import admin
from .models import Genre, Book, BookInstace, Author, Language


class BookInlineAdmin(admin.StackedInline):
    model = Book
    extra = 0
    list_display = ['title', 'author', 'display_genre']

class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInlineAdmin]

    list_display = ['last_name', 'first_name', 'date_of_birth', 'date_of_death']

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


# @admin.register(BookInstace)
class BookInstaceAdmin(admin.TabularInline):
    model = BookInstace
    list_display = ['book', 'status', 'due_back', 'borrowe', 'id',]
    list_filter = ['status', 'due_back']
    extra = 0

    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')})
    )

@admin.register(BookInstace)
class BookIAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back', 'borrower', 'id']
    list_filter = ['status', 'due_back']

    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')})    
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookInstaceAdmin]

    list_display = ['title', 'author', 'display_genre']


# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author, AuthorAdmin)



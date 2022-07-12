from django.contrib import admin


from .models import Books, Author, Genre, Customers, ImageAuthor, ImageBook, BookInstance

class BooksImageInline(admin.StackedInline):
    model = ImageBook
    max_num = 5
    extra = 0

class AuthorImageInlane(admin.StackedInline):
    model = ImageAuthor
    max_num = 5
    extra = 0

class BookInstanceInlane(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title_russian', 'display_author', 'display_genre']
    list_display_links = ['title_russian']
    search_fields = ['title_russian']
    ordering = ['title_russian']
    inlines = [BooksImageInline, BookInstanceInlane]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']
    ordering = ['name', 'surname']
    inlines = [AuthorImageInlane]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back', 'id', 'borrower', 'day_borrower']
    list_filter = ['due_back', 'status']
    fieldsets = [
        ('', {
            'fields': ['book', 'id']
        }),
        ('Наличие', {
            'fields': ('status', 'due_back', 'borrower', 'day_borrower')
        })
    ]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birthday', 'sex', 'place']






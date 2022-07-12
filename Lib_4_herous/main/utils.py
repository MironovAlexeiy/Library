from .models import *

def check_error(title_russian:str) ->str:
    b = [title[0] for title in Books.objects.values_list('title_russian')]
    if title_russian.title() in b:
         return 'Такая книга уже есть'

# b = Books.objects.create(title_russian='New_book', price=2, description='asfasf', cost_daily=2, amount_ex=2 ).pk
def create_book(request):
    d = {
        'title_russian': request.POST.get('title_russian'),
        'title_foreign': request.POST.get('title_foreign'),
        'description': request.POST.get('description'),
        'price': request.POST.get('price'),
        'cost_daily': request.POST.get('cost_daily'),
        'amount_ex': request.POST.get('amount_ex'),
        'number_of_pages': request.POST.get('number_of_pages'),
        'year_of_publication': request.POST.get('year_of_publication'),
    }
    return d

def add_genre(request, id_book):
    genres = request.POST.getlist('genre')
    book = Books.objects.get(id=id_book)
    for id_g in genres:
        book.genre.add(Genre.objects.get(id=id_g))

def add_author(request, id_book):
    authors = request.POST.getlist('authors')
    book = Books.objects.get(id=id_book)
    for id_a in authors:
        book.author.add(Author.objects.get(id=id_a))

def get_total_sum():
    clients = BookInstance.objects.all().filter(status='o')
    sum = 0
    for cl in clients:
        sum += cl.get_price
    return sum
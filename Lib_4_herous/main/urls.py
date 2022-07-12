from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
   path('search/', main_page, name='main_page'),
   path('', BookList.as_view(), name='list_book'),
   path('book/<int:pk>/', BookDetail.as_view(), name='book_detail'),
   path('author/<int:pk>/', AuthorDetail.as_view(), name='author_detail'),
   path('register/', register, name='register'),
   path('edit/', edit, name='edit_customer'),
   path('userbooks/', LoanedBooksByUserListView.as_view(), name='user_borrower'),
   path('allcustomers/', all_customers, name='all_customers'),
   path('allclients/', all_clients, name='all_clients'),
   path('registration_book/', register_book, name='reg_book'),
   path('book/<int:pk>/renew/', RenewBookForm, name='renew-book-librarian'),
   path('author/create', AuthorCreate.as_view(), name='author_create'),
   path('author/<int:pk>/update', AuthorUpdate.as_view(), name='author_update'),
   path('author/<int:pk>/delete', AuthorDelete.as_view(), name='author_delete'),

]
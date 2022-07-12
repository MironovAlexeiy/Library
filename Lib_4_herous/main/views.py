from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from .utils import *

def main_page(request):
    results = []
    if request.method == "GET":
        query = request.GET.get('search_book')
        if query == '':
            query = 'None'
        results = Books.objects.filter(Q(title_russian__icontains=query))

        return render(request, 'search.html', {'query': query, 'results': results})
    return render(request, 'main.html')


class BookList(generic.ListView):
    model = Books
    paginate_by = 20
    template_name = 'list_book.html'


class BookDetail(generic.DetailView):
    model = Books
    template_name = 'book_detail.html'


class AuthorDetail(generic.DetailView, MultipleObjectMixin):
    model = Author
    paginate_by = 5
    template_name = 'author_detail.html'

    def get_context_data(self, **kwargs):
        object_list = Books.objects.filter(author=self.get_object())
        context = super(AuthorDetail, self).get_context_data(object_list=object_list, **kwargs)
        return context


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            customers = Customers.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        customers_form = CustomersEditForm(instance=request.user.customers, data=request.POST)
        if customers_form.is_valid() and user_form.is_valid():
            user_form.save()
            customers_form.save()
            return redirect('main:list_book')
    else:
        user_form = UserEditForm(instance=request.user)
        customers_form = CustomersEditForm(instance=request.user.customers)
    return render(request, 'registration/edit.html', {'customers_form': customers_form, 'user_form': user_form})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 20

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


def all_customers(requests):
    customers = Customers.objects.all()
    return render(requests, 'all_customers.html', {'customers': customers})


def all_clients(requests):
    clients = BookInstance.objects.all().filter(status='o')
    total_sum = get_total_sum()
    return render(requests, 'all_clients.html', {'clients': clients, 'total_sum': total_sum})

@permission_required('main.can_mark_returned')
def renew_book_librian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-customers'))
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=5)
            form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        return render(request, 'book_renew_librian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    template_name = 'author_form.html'
    success_url = reverse_lazy('main:author_detail')


class AuthorUpdate(UpdateView):
    model = Author
    template_name = 'author_form.html'
    fields = '__all__'


class AuthorDelete(DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = reverse_lazy('authors')


def register_book(request):
    genre = Genre.objects.all()
    authors = Author.objects.all()
    context = {
        'genre': genre,
        'authors': authors
    }
    if request.method == "POST":
        error = check_error(request.POST.get('title_russian'))
        images = request.FILES.getlist('image')

        if error:
            context['error'] = error
            return render(request, 'registration_book.html', context)

        book = create_book(request)
        id_book = Books.objects.create(**book).pk
        if images:
            book = Books.objects.get(pk=id_book)
            for im in images:
                image = ImageBook(book=book, image=im)
                image.save()
        add_genre(request,id_book)
        add_author(request,id_book)

    return render(request, 'registration_book.html', context)





# def register_book(request):
#     reg_book = RegistrationBook()
#     if request.method == 'POST':
#         reg_book = RegistrationBook(data=request.POST, files=request.FILES)
#         if reg_book.is_valid():
#             reg_book.save()
#         return redirect('book-detail')
#     return render(request, 'registration_book.html', {'reg_book': reg_book})
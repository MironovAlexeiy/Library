import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from datetime import datetime, date

class Books(models.Model):
    title_russian = models.CharField(max_length=150, help_text='Введите название на русском языке', verbose_name='Название книги')
    title_foreign = models.CharField(max_length=150, help_text='Введите название на иностранном языке',
                                     null=True, blank=True, verbose_name='Название на иностранном языке')

    description = models.TextField(max_length=1000, help_text='Введите описание книги', verbose_name='Краткое описание книги')
    genre = models.ManyToManyField('Genre', verbose_name='Жанр')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    cost_daily = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена за день использования')
    amount_ex = models.IntegerField()
    author = models.ManyToManyField('Author', verbose_name='Авторы')
    date_registration = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    number_of_pages = models.IntegerField(blank=True, null=True, verbose_name='Количество страниц')
    year_of_publication = models.DateField(null=True, blank=True, verbose_name='Дата публикации')
    pubdate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title_russian

    def get_absolute_url(self):
        return reverse('main:book_detail', args=[str(self.id)])

    def display_genre(self):
        return [genre.name for genre in self.genre.all()]
    display_genre.short_description = 'Жанр'

    def display_author(self):
        return [' '.join((author.name, author.surname)) for author in self.author.all()]
    display_author.short_description = 'Авторы'

    class Meta:
        ordering = ["title_russian", "-pubdate"]
        verbose_name_plural = 'Книги'
        verbose_name = 'Книга'

class Author(models.Model):
    surname = models.CharField(max_length=150, verbose_name='Фамилия')
    name = models.CharField(max_length=150, verbose_name='Имя')
    second_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отчество')

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse('main:author_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'
        ordering = ['name', "surname"]

class Customers(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    second_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    date_of_birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    ages = models.IntegerField(verbose_name='Возраст', default=16)

    option = (
        ('Male', 'Мужчина'),
        ('Female', 'Женщина'),
    )
    sex = models.CharField(max_length=7, choices=option, default='Male', verbose_name='Пол')
    number_of_passport = models.CharField(max_length=9, unique=True, verbose_name='Номер паспорта', null=True)
    place = models.CharField(max_length=30,verbose_name='Город проживания', null=True)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        ordering = ['user']

    def __str__(self):
        return self.user.username

class Genre(models.Model):
    name = models.CharField(max_length=50, help_text='Введите', unique=True, verbose_name='Название жанра')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class ImageAuthor(models.Model):
    image = models.ImageField(upload_to='images/author', verbose_name='Фотография автора')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='Автор')

    def __str__(self):
        return self.author.name


    class Meta:
        verbose_name = 'Изображение автора'
        verbose_name_plural = 'Изображения авторов'


class ImageBook(models.Model):
    image = models.ImageField(upload_to='images/book', verbose_name='Изображение книги')
    book = models.ForeignKey('Books', on_delete=models.SET_NULL, null=True)



    def __str__(self):
        return f'{self.book.title_russian} {self.book.author.all()}'


    class Meta:
        verbose_name = 'Изображения книги'
        verbose_name_plural = 'Изображения книг'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True, verbose_name='Книга')
    imprint = models.CharField(max_length=200, default='yes')
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата возврата')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    day_borrower = models.DateField(verbose_name='Дата выдачи в пользование', null=True, blank=True)
    LOAN_STATUS = [
        ('m', 'На обслуживании'),
        ('o', 'В аренде'),
        ('a', 'В наличии'),
        ('r', 'Зарезервирована'),
    ]
    status = models.CharField(max_length=10, choices=LOAN_STATUS, blank=True, default='m', verbose_name='Статус')

    class Meta:
        verbose_name = 'Копия'
        verbose_name_plural = 'Копии книг'
        ordering = ['book', "due_back"]
        permissions = [
            ('can_mark_returned', 'Set book as returned'),
        ]

    def __str__(self):
        return self.book.title_russian

    @property
    def get_price(self):
        date_today = self.day_borrower
        day_back = self.due_back
        day_on_loan = (day_back - date_today).days
        price = day_on_loan * self.book.cost_daily
        return price

    @property
    def bad_book(self):
        return True


    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

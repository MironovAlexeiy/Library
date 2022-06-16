import uuid

from django.db import models
from django.urls import reverse


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
        return reverse('books-detail', args=[str(self.id)])

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
        return reverse('author-detail', args=[str(self.id)])

    class Meta:
        ordering = ['name',"surname"]
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'


class Customers(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    second_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    email = models.EmailField(unique=True)
    date_of_birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    ages = models.IntegerField(verbose_name='Возраст')

    option = (
        ('Male', 'Man'),
        ('Female', 'Woman'),
    )
    sex = models.CharField(max_length=7, choices=option, default='Male', verbose_name='Пол')
    number_of_passport = models.CharField(max_length=9, unique=True, verbose_name='Номер паспорта')
    place = models.CharField(max_length=30,verbose_name='Город проживания')

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['name', 'surname']





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
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата возврата')

    LOAN_STATUS = [
        ('m', 'На обслуживании'),
        ('o', 'Нет в наличии'),
        ('a', 'В наличии'),
        ('r', 'Зарезервирована'),
    ]
    status = models.CharField(max_length=10, choices=LOAN_STATUS, blank=True, default='m', verbose_name='Статус')

    class Meta:
        verbose_name = 'Копия'
        verbose_name_plural = 'Экземпляры книг'
        ordering = ['book', "due_back"]

    def __str__(self):
        return self.book.title_russian

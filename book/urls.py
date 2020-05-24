from django.urls import path
from .views import home,book_detail,add_book,my_books,delete_book


urlpatterns = [
    path('',home,name='home'),
    path('book/<str:book_id>',book_detail, name="book_detail"),
    path('book/add/<str:book_id>',add_book,name="add_book"),
    path('my_books',my_books,name="my_books"),
    path('book/<str:book_id>/delete',delete_book,name="delete_book")
]

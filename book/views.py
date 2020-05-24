from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Books


import requests
import math


def home(request):
    #PAGINATION

    #if page_number did not assigned return homepage 
    page_number = 1
    try:
        page_number = int(request.GET.get('page'))
    except:
        pass

    ##increment and decrement next and previous page
    next_page_number = page_number +1
    previous_page_number = page_number -1

    #if page_number less than 1 raise 404 Error
    if page_number < 1:
        raise Http404

    books = []
    if request.method=="POST":
        q = request.POST.get('q')
        maxResult = 12
        startIndex = (page_number-1)*maxResult
        search_url = f'https://www.googleapis.com/books/v1/volumes?q={q}'
        params = {
            'key':settings.GOOGLE_BOOKS_API_KEY,
            'printType':'books',
            'orderBy':'relevance',
            'maxResults':maxResult,
            'startIndex':startIndex
        }
        
        r = requests.get(search_url,params=params).json()
        try:
            for i in range(len(r['items'])):
                info = r['items'][i]['volumeInfo']
                book_info = {
                    'id':r['items'][i]['id'],
                    'title':info['title'],
                    'author':info['authors'][0] if 'authors' in info else '' ,
                    'publisher':info['publisher'] if 'publisher' in info else '',
                    'pageCount':info.get('publisher'),
                    'thumbnail':info['imageLinks']['smallThumbnail'] if 'imageLinks' in info else 'http://placehold.jp/128x192.png',
                    'totalItems':r['totalItems']
                    
                }
                books.append(book_info)
        except KeyError:
            if q != "":
                messages.error(request,"There is no more page for this book")
            else:
                messages.info(request,"Search field can't be empty")

    q_value =request.POST.get('q')
    context = {
        'books':books,
        'q_value':q_value,
        'page_number':page_number,
        'next_page_number':next_page_number,
        'previous_page_number':previous_page_number,
    }
    return render(request,'book/home.html',context)




def book_detail(request,book_id):
    book = None
    try:
        book = Books.objects.get(book_id=book_id,user=request.user)
    except:
        pass
    detail_url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
    r = requests.get(detail_url).json()
    context = {
        'id' : r['id'],
        'title':r['volumeInfo']['title'],
        'image':r['volumeInfo']['imageLinks']['thumbnail'],
        'author':r['volumeInfo']['authors'][0],
        'publisher':r['volumeInfo']['publisher'],
        'description':r['volumeInfo']['description'] if 'description' in r['volumeInfo'] else 'No Description',
        'average_rating':r['volumeInfo']['averageRating'] if 'averageRating' in r['volumeInfo'] else '',
        'ratings_count':r['volumeInfo']['ratingsCount'] if 'ratingsCount' in r['volumeInfo'] else '',
        'isbn':r['volumeInfo']['industryIdentifiers'][1]['identifier'] if 'industryIdentifiers' in r['volumeInfo'] else 'No Isbn',
        'language':r['volumeInfo']['language'],
        'pageCount':r['volumeInfo'].get('pageCount'),
        'publisher':r['volumeInfo'].get('publisher'),
        'publishedDate':r['volumeInfo'].get('publishedDate'),
        'book':book
    }

    return render(request,'book/book_detail.html',context)




def add_book(request,book_id):
    read_status = request.GET.get('read_status')
    book = Books.objects.filter(user=request.user,book_id=book_id)
    if book.exists():
        _book = Books.objects.get(book_id=book_id)
        _book.read_status = read_status
        _book.save()
    else:
        url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
        r = requests.get(url).json()
        user = request.user
        title = r['volumeInfo']['title']
        author = r['volumeInfo']['authors'][0]
        description = r['volumeInfo']['description']  if 'description' in r['volumeInfo'] else 'No Description'
        page_count = r['volumeInfo'].get('pageCount')
        image_url = r['volumeInfo']['imageLinks']['smallThumbnail']
        average_rating = r['volumeInfo']['averageRating'] if 'averageRating' in r['volumeInfo'] else '';

        Books.objects.create(
            user=user,
            book_id=book_id,
            title=title,
            author=author,
            description = description,
            read_status = read_status,
            page_count = page_count,
            image_url = image_url,
            average_rating = average_rating
        )
    return JsonResponse({'read_status':read_status})

    
@login_required   
def my_books(request):
    books = Books.objects.filter(user=request.user)
    return render(request,'book/my_books.html',{'books':books})


def delete_book(request,book_id):
    book_id = request.GET.get('id')
    book = get_object_or_404(Books,book_id=book_id,user=request.user)
    book.delete()
    _book = model_to_dict(book)
    return JsonResponse({'book_id':book.id,'book':_book})

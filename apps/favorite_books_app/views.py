from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book
import bcrypt

def index(request):
    return render(request,'favorite_books_app/index.html')

def registration(request):
    errors = User.objects.register_user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="r"+key)

            # messages.error(request, value)
        return redirect ('/')

    if request.method == 'POST':
        # encode the password
        pw_hash = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['reg_email'], password = pw_hash)

    return redirect('/')

def auth_user(request):
    login_errors = User.objects.login_user_validator(request.POST) 
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags="l"+key)
            # messages.error(request, value)
        return redirect ('/')
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['user_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
            else: 
                print('Incorrect password, try again')
                return redirect('/')
    return redirect('/')

def user_logged(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        books = Book.objects.all()
        # Create an object for my current user
        # Once I have the object, user the shared field 'liked_books'
        # to get a list of all the books the user has liked
        my_books = user.liked_books.all()

        context = {
            'logged_user_info' : user,
            'all_books' : books,
            'my_books' : my_books
        }
    return render(request, 'favorite_books_app/books.html', context)

def add_book(request):
    adding_book_errors = Book.objects.add_book_validator(request.POST) 
    
    if len(adding_book_errors) > 0:
        for key, value in adding_book_errors.items():
            messages.error(request, value, extra_tags="b"+key)
            # messages.error(request, value)
        return redirect ('/books')

    # Creates a relationship between user/books, 'users_who_like' is an attribute
    # of the books table to add an instance of the user
    if request.method == 'POST': 
        added_by_user = User.objects.get(id = request.POST['book_added_by'])
        book_created = Book.objects.create(title = request.POST['book_title'], description = request.POST['book_description'], uploaded_by = added_by_user)
        book_created.users_who_like.add(added_by_user)
    return redirect('/books')

def display_info(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        book_info = Book.objects.get(id = book_id)
        # my_fav_books = User.objects.filter(liked_books = )

        # Create an instance of the book, once the instance is created
        # Through the user, we need to filter or a way to get all the 
        # books that the user has liked. Get all the users and in the 
        # template, we will be able to access it.
        users_who_like = User.objects.filter(liked_books = book_info)

        context = {
            'logged_user_info' : user,
            'book_info' : book_info,
            'users_who_like' : users_who_like
        }
    return render(request,'favorite_books_app/book_info.html', context)

def edit_description(request, book_id):
    if request.method == 'POST':
        if 'delete_book' in request.POST:
            return redirect(f'/delete/{book_id}')
        else:
            update_book_errors = Book.objects.update_description_validator(request.POST) 
    
            if len(update_book_errors) > 0:
                for key, value in update_book_errors.items():
                    messages.error(request, value, extra_tags="u"+key)
                return redirect (f'/books/{book_id}')

            book = Book.objects.get(id = book_id)
            book.description = request.POST['edit_description']
            book.save()
    return redirect('/books')

def add_to_favorites(request, book_id):
    user = User.objects.get(id = request.session['user_id'])
    add_book = Book.objects.get(id = book_id)
    add_book.users_who_like.add(user)
    return redirect('/books')

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def clear_session(request):
    del request.session['user_id']
    return redirect('/')

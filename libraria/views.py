from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import ProfileForm, ReviewWebForm, SignupForm, addbookForm, CategoryForm, ReviewBookForm, ReviewAccountForm
from .models import Profile, ReviewWeb, review_user, category, listbook, review_book, borrowing, review_user

# Create your views here.
def firstpage(request):
    return render(request, 'libraria/firstpage.html')

def review_web(request):
    if request.method == 'POST':
        form = ReviewWebForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('firstpage')
    else:
        form = ReviewWebForm()
    return render(request, 'libraria/review.html', {'form': form})

def insert_review(request):
    reviews = ReviewWeb.objects.all()
    context = {
        'Review':reviews,
    }
    return render(request, 'libraria/firstpage.html', context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='admin').exists():
                return redirect('admin_home')  
            else:
                return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'libraria/login.html')

@unauthenticated_user
def signup(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='user')
            user.groups.add(group)

            login(request, user)
                
            return redirect('addProfile')

    context = {'form':form}
    return render(request, 'libraria/signup.html', {'form': form})

@login_required(login_url='login_view')
def logoutPage(request):
    logout(request)
    return redirect('firstpage')

def review(request):
    return render(request, 'libraria/review.html')

@allowed_users(allowed_roles=['user'])
def addProfile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  
            profile.signup = request.user      
            profile.save()                     
            return redirect('login_view')
    else:
        form = ProfileForm()

    return render(request, 'libraria/completeProfile.html', {'form': form})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def profile(request):
    user_profile = Profile.objects.get(signup=request.user)
    reuser = review_user.objects.filter(reviewee=request.user)
    total_reviews = reuser.count()

    if total_reviews > 0:
        total_rating = sum(review.rating for review in reuser)
        average_rating = total_rating / total_reviews
    else:
        average_rating = 0 

    full_stars = list(range(int(average_rating)))  
    empty_stars = list(range(5 - len(full_stars)))

    context = {
        'user_profile': user_profile,
        'join_date': request.user.date_joined,
        'reuser': reuser,
        'full_stars': full_stars,
        'empty_stars': empty_stars,
    }
    return render(request, 'libraria/profile.html', context)



@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def editProfile(request):
    user_profile = Profile.objects.get(signup=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = ProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'libraria/editProfile.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def addbook(request):
    user_profile = Profile.objects.get(signup=request.user)

    if request.method == 'POST':
        form = addbookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)  
            book.librender = request.user
            form.save()
            return redirect('librender')
    else:
        form = addbookForm()

    categories = category.objects.all()
    return render(request, 'libraria/addbook.html', {'form': form, 'categories': categories, 'user_profile': user_profile,})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def librender(request):
    user_profile = Profile.objects.get(signup=request.user)
    Category = category.objects.all()
    Book = listbook.objects.filter(librender=request.user)
    

    context = {
        'user_profile':user_profile,
        'Category':Category,
        'Book':Book,
    }

    return render(request, 'libraria/librender.html', context)

#admin home
@login_required(login_url='login_view')
@admin_only
def admin_home(request):
    user_count = User.objects.count()
    book_count = listbook.objects.count()
    category_count = category.objects.count()
    
    context = {
        'user_count' : user_count,
        'book_count' : book_count,
        'category_count' : category_count,
    }
    return render(request, 'libraria/admin_home.html', context)

#admin user-list
@login_required(login_url='login_view')
@admin_only
def user_list(request):
    users = User.objects.all()

    context = {
        'users' : users,
        'join_date': request.user.date_joined,
    }
    return render(request, 'libraria/user_list.html', context)

@login_required(login_url='login_view')
@admin_only
def delete_selected_users(request):
    if request.method == "POST":
        selected_users = request.POST.getlist('selected_users') #ngambil list dari yang di select
        if selected_users:
            User.objects.filter(username__in=selected_users).delete() #mencari data yg sama dengan yg di list pake lookup __in
            messages.success(request, "Selected users have been deleted.")
        else:
            messages.error(request, "No users selected.")
    return redirect('user_list')

@login_required(login_url='login_view')
@admin_only
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, f'User {username} has been deleted')
    except user.DoesNotExist:
        messages.error(request, 'User not found')
    return redirect ('user_list')

#admin book-list
@login_required(login_url='login_view')
@admin_only
def book_list(request):
    books = listbook.objects.all()
    return render(request, 'libraria/book_list.html', {'books':books})

@login_required(login_url='login_view')
@admin_only
def delete_book(request, title): 
    try:
        Books = listbook.objects.get(title=title)
        Books.delete()
        messages.success(request, f'{title} has been deleted')
    except Books.DoesNotExist:
        messages.error(request, 'Category not found')
    return redirect ('book_list')

@login_required(login_url='login_view')
@admin_only
def delete_selected_book(request):
    if request.method == "POST":
        selected_book = request.POST.getlist('selected_book') 
        if selected_book:
            listbook.objects.filter(title__in=selected_book).delete() #mencari data yg sama dengan yg di list pake lookup __in
            messages.success(request, "Selected books have been deleted.")
        else:
            messages.error(request, "No books selected.")
    return redirect('book_list')

#admin category
@login_required(login_url='login_view')
@admin_only
def category_add(request):
    cat_form = CategoryForm()
    if request.method == 'POST':
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, "Category has been saved")
            return redirect('category_add')
    else:
            print(cat_form.errors)
    return render(request, 'libraria/category_add.html', {'form': cat_form})

@login_required(login_url='login_view')
@admin_only
def books_by_category(request, category_id):
    categories = category.objects.all()
    selected_category = get_object_or_404(category, category_id=category_id)

    books_in_category = listbook.objects.filter(categoryid=selected_category).annotate(avg_rating=Avg('review_book__rating'))

    for book_item in books_in_category:
        avg_rating = book_item.avg_rating or 0 
        book_item.full_stars = list(range(int(avg_rating)))  
        book_item.empty_stars = list(range(5 - int(avg_rating))) 

    context = {
        'selected_category': selected_category,
        'books_in_category': books_in_category,
        'categories':categories,
    }

    return render(request, 'libraria/books_by_category.html', context)

@login_required(login_url='login_view')
@admin_only
def category_list(request):
    categories = category.objects.all()
    return render(request, 'libraria/category_list.html', {'categories':categories})

@login_required(login_url='login_view')
@admin_only
def delete_category(request, category_name):
    try:
        Category = category.objects.get(category_name=category_name)
        Category.delete()
        messages.success(request, f'Category {category_name} has been deleted')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found')
    return redirect ('category_list')

@login_required(login_url='login_view')
@admin_only
def delete_selected_category(request):
    if request.method == "POST":
        selected_category = request.POST.getlist('selected_category') #ngambil list dari yang di select
        if selected_category:
            category.objects.filter(category_name__in=selected_category).delete() #mencari data yg sama dengan yg di list pake lookup __in
            messages.success(request, "Selected users have been deleted.")
        else:
            messages.error(request, "No users selected.")
    return redirect('category_list')

@login_required(login_url='login_view')
@admin_only
def edit_category(request, category_name):
    category_obj = get_object_or_404(category, category_name=category_name)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category_name}' has been updated successfully")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category_obj)
    
    return render(request, 'libraria/category_edit.html', {
        'form': form,
        'category_name': category_name,
    })

#admin review-user
@login_required(login_url='login_view')
@admin_only
def review_base(request):
    return render(request, 'libraria/base_review.html')

@login_required(login_url='login_view')
@admin_only
def reuser_list(request):
    reuser = review_user.objects.all()
    for review in reuser:
        if 1 <= review.rating <= 5:
            review.full_stars = list(range(review.rating))  # Bintang penuh
            review.empty_stars = list(range(5 - review.rating))  # Bintang kosong
        else:
            review.full_stars = []
            review.empty_stars = [1, 2, 3, 4, 5]
    return render(request, 'libraria/reuser_list.html', {'reuser':reuser})

@login_required(login_url='login_view')
@admin_only
def delete_reuser(request, comment): 
    try:
        reuser = review_user.objects.get(comment=comment)
        reuser.delete()
        messages.success(request, f'Review has been deleted')
    except review_user.DoesNotExist:
        messages.error(request, 'Review not found')
    return redirect ('reuser_list')

@login_required(login_url='login_view')
@admin_only
def delete_selected_reuser(request):
    if request.method == "POST":
        selected_reuser = request.POST.getlist('selected_reuser') #ngambil list dari yang di select
        if selected_reuser:
            review_user.objects.filter(comment__in=selected_reuser).delete() #mencari data yg sama dengan yg di list pake lookup __in
            messages.success(request, "Selected review has been deleted.")
        else:
            messages.error(request, "No review selected.")
    return redirect('reuser_list')

#admin review-book
@login_required(login_url='login_view')
@admin_only
def rebook_list(request):
    rebook = review_book.objects.all()
    for review in rebook:
        if 1 <= review.rating <= 5:
            review.full_stars = list(range(review.rating))  # Bintang penuh
            review.empty_stars = list(range(5 - review.rating))  # Bintang kosong
        else:
            review.full_stars = []
            review.empty_stars = [1, 2, 3, 4, 5]
    return render(request, 'libraria/rebook_list.html', {'rebook':rebook})

@login_required(login_url='login_view')
@admin_only
def delete_rebook(request, comment): 
    try:
        rebook = review_book.objects.get(comment=comment)
        rebook.delete()
        messages.success(request, f'Review has been deleted')
    except review_book.DoesNotExist:
        messages.error(request, 'Review not found')
    return redirect ('rebook_list')

@login_required(login_url='login_view')
@admin_only
def delete_selected_rebook(request):
    if request.method == "POST":
        selected_rebook = request.POST.getlist('selected_rebook') #ngambil list dari yang di select
        if selected_rebook:
            review_book.objects.filter(comment__in=selected_rebook).delete() #mencari data yg sama dengan yg di list pake lookup __in
            messages.success(request, "Selected review has been deleted.")
        else:
            messages.error(request, "No review selected.")
    return redirect('rebook_list')

#admin review-web
@login_required(login_url='login_view')
@admin_only
def reweb_list(request):
    reweb = ReviewWeb.objects.all()
    return render(request, 'libraria/reweb_list.html', {'reweb':reweb})

@login_required(login_url='login_view')
@admin_only
def delete_reweb(request, review_field): 
    try:
        reweb = ReviewWeb.objects.get(review_field=review_field)
        reweb.delete()
        messages.success(request, f'Review has been deleted')
    except ReviewWeb.DoesNotExist:
        messages.error(request, 'Review not found')
    return redirect ('reweb_list')

@login_required(login_url='login_view')
@admin_only
def delete_selected_reweb(request):
    if request.method == "POST":
        selected_reweb = request.POST.getlist('selected_reweb') #ngambil list dari yang di select
        if selected_reweb:
            ReviewWeb.objects.filter(review_field__in=selected_reweb).delete() #mencari data yg sama dengan yg di list pake lookup __in
            messages.success(request, "Selected review has been deleted.")
        else:
            messages.error(request, "No review selected.")
    return redirect('reweb_list')

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def base_user(request):
    return render(request, 'libraria/base_user.html')

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def search_books(request):
    user_profile = Profile.objects.get(signup=request.user)

    categories = category.objects.all()
    query = request.GET.get('q')
    results = []
    
    if query:
        results = listbook.objects.filter(
            Q(title__icontains=query) | Q(category_id__category_name__icontains=query)
        )
        
    context = {
        'query' : query,
        'results' : results,
        'categories' : categories,
        'user_profile' : user_profile,
    }
    
    return render(request, 'libraria/search_results.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def dashboard(request):
    user_profile = Profile.objects.get(signup=request.user)

    categories = category.objects.all()
    book_of_the_month = listbook.objects.annotate(avg_rating=Avg('review_book__rating')).order_by('-avg_rating')[:3]
    
    for book_item in book_of_the_month:
        avg_rating = book_item.avg_rating or 0  
        book_item.full_stars = list(range(int(avg_rating)))  
        book_item.empty_stars = list(range(5 - int(avg_rating)))  

    recommendation = listbook.objects.annotate(avg_rating=Avg('review_book__rating')).filter(avg_rating__gte=3, avg_rating__lte=5).order_by('?')[:6]
    
    for book_item in recommendation:
        avg_rating = book_item.avg_rating or 0  
        book_item.full_stars = list(range(int(avg_rating))) 
        book_item.empty_stars = list(range(5 - int(avg_rating))) 
    
    library_stars = Profile.objects.annotate(total_rating=Avg('signup__reviews_received__rating')).order_by('-total_rating')[:4]

    for user_obj in library_stars:
        total_rating = user_obj.total_rating or 0  
        user_obj.full_stars = list(range(int(total_rating))) 
        user_obj.empty_stars = list(range(5 - int(total_rating)))
        
    context = {
        'book_of_the_month': book_of_the_month,
        'recommendation': recommendation,
        'library_stars': library_stars,
        'categories':categories,
        'user_profile':user_profile,
    }

    
    return render(request, 'libraria/dashboard.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def books_by_category(request, category_id):
    user_profile = Profile.objects.get(signup=request.user)

    categories = category.objects.all()
    selected_category = get_object_or_404(category, category_id=category_id)

    books_in_category = listbook.objects.filter(category_id=selected_category).annotate(avg_rating=Avg('review_book__rating'))

    for book_item in books_in_category:
        avg_rating = book_item.avg_rating or 0 
        book_item.full_stars = list(range(int(avg_rating)))  
        book_item.empty_stars = list(range(5 - int(avg_rating))) 

    context = {
        'selected_category': selected_category,
        'books_in_category': books_in_category,
        'categories':categories,
        'user_profile' : user_profile
    }

    return render(request, 'libraria/books_by_category.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def halamanpinjam(request, book_id):
    user_profile = Profile.objects.get(signup=request.user)
    selected_book = get_object_or_404(listbook, book_id=book_id)
    librarian_profile = Profile.objects.get(signup=selected_book.librender)
    review = review_book.objects.filter(booktitle=selected_book)

    context = {
        'user_profile': user_profile,
        'selected_book': selected_book,
        'librarian_profile': librarian_profile,
        'review' : review,
    }

    return render(request, 'libraria/halamanpinjam.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def shelf(request):
    user_profile = Profile.objects.get(signup=request.user)
    borrowings = borrowing.objects.filter(borrower=request.user).select_related('book')

    for item in borrowings.filter(status="Borrowed"):  
        if item.return_date and timezone.now().date() > item.return_date:
            item.status = "Returned"
        else:
            item.status = "Borrowed"

        overdue_days = (timezone.now().date() - item.return_date).days if item.return_date and timezone.now().date() > item.return_date else 0
        item.denda = overdue_days * 1000 if overdue_days > 0 else 0
        item.save()

    context = {
        'user_profile': user_profile,
        'borrowings': borrowings,
    }

    return render(request, 'libraria/shelf.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def borrow_book(request, book_id):
    user_profile = Profile.objects.get(signup=request.user)
    selected_book = get_object_or_404(listbook, book_id=book_id)

    if selected_book.stok > 0:
        try:
            with transaction.atomic():
                selected_book.stok -= 1
                selected_book.save()

                borrowing.objects.create(
                    borrower=request.user,
                    book=selected_book,
                    return_date=timezone.now().date() + timedelta(days=7)
                )
                messages.success(request, f'You have successfully borrowed {selected_book.title}!')
        except Exception as e:
            messages.error(request, 'An error occurred while borrowing the book.')
    else:
        messages.error(request, 'This book is out of stock.')

    return redirect('shelf')

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def return_book(request, borrowing_id):
    borrowing_item = get_object_or_404(borrowing, borrowing_id=borrowing_id)

    try:
        with transaction.atomic():
            borrowing_item.book.stok += 1 
            borrowing_item.book.save()

            borrowing_item.status = "Returned" 
            borrowing_item.return_date = timezone.now().date()  
            borrowing_item.save()

            messages.success(request, f'You have successfully returned {borrowing_item.book.title}!')
    except Exception as e:
        messages.error(request, f'An error occurred while returning the book: {e}')

    return redirect('shelf')

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def reviewbook(request, borrowing_id):
    borrowing_item = get_object_or_404(borrowing, borrowing_id=borrowing_id, borrower=request.user)

    existing_review = review_book.objects.filter(username=request.user, booktitle=borrowing_item.book).exists()
    if existing_review:
        return redirect('shelf') 

    if request.method == 'POST':
        form = ReviewBookForm(request.POST)
        if form.is_valid():
            
            new_review = form.save(commit=False)
            new_review.username = request.user 
            new_review.booktitle = borrowing_item.book 
            new_review.save()
            
            return redirect('review_user', borrowing_id=borrowing_item.borrowing_id) 
    else:
        form = ReviewBookForm()
    print("Received borrowing_id:", borrowing_id)
    context = {
        'form': form,
        'book': borrowing_item.book,
        'borrowing_item': borrowing_item,
    }
    
    return render(request, 'libraria/reviewbooks.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def reviewaccount(request, borrowing_id):
    borrowing_item = get_object_or_404(borrowing, borrowing_id=borrowing_id, borrower=request.user)
    librarian_profile = Profile.objects.get(signup=borrowing_item.book.librender)

    existing_review = review_user.objects.filter(reviewer=request.user, reviewee=borrowing_item.book.librender).exists()
    if existing_review:
        return redirect('shelf') 

    if request.method == 'POST':
        form = ReviewAccountForm(request.POST)
        if form.is_valid():
            
            new_review = form.save(commit=False)
            new_review.reviewer = request.user 
            new_review.reviewee = borrowing_item.book.librender
            new_review.save()

            return redirect('shelf')  
    else:
        form = ReviewAccountForm()

    context = {
        'form': form,
        'librarian_profile': librarian_profile, 
        'borrowing_item': borrowing_item,
    }
    
    return render(request, 'libraria/reviewaccounts.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def edit_book(request, book_id):
    book = get_object_or_404(listbook, book_id=book_id)
    
    if request.method == 'POST':
        form = addbookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save() 
            return redirect('librender') 
    else:
        form = addbookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'libraria/edit_book.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['user'])
def deletebook(request, book_id):
    book = get_object_or_404(listbook, book_id=book_id)
    book.delete()

    return redirect ('librender')
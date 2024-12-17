from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.insert_review, name='firstpage'),
    path('login_view/', views.login_view, name='login_view'),
    path('logoutPage/', views.logoutPage, name='logoutPage'),
    path('signup/', views.signup, name='signup'),
    path('review/', views.review, name='review'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('addbook/', views.addbook, name='addbook'),
    path('librender/', views.librender, name='librender'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_books, name='search_books'),
    path('categories/<str:category_id>/', views.books_by_category, name='books_by_category'),
    path('halamanpinjam/<str:book_id>/', views.halamanpinjam, name='halamanpinjam'),
    path('shelf/', views.shelf, name='shelf'),

    path('borrow/<str:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<str:borrowing_id>/', views.return_book, name='return_book'),

    path('edit_book/<str:book_id>/', views.edit_book, name='edit_book'),
    path('deletebook/<str:book_id>/', views.deletebook, name='deletebook'),

    path('addProfile/', views.addProfile, name='addProfile'),
    path('review_web/', views.review_web, name='review_web'),

    path('review_book/<str:borrowing_id>/', views.reviewbook, name='review_book'),
    path('review_user/<str:borrowing_id>/', views.reviewaccount, name='review_user'),

    #admin
    path('admin/', views.admin_home, name='admin_home'),

    path('users/', views.user_list, name="user_list"),
    path('delete-selected/', views.delete_selected_users, name='delete_selected_users'),
    path('delete-user/<str:username>/', views.delete_user, name='delete_user'),

    path('book-list/', views.book_list, name="book_list"),
    path('delete-book/<str:title>/', views.delete_book, name='delete_book'),
    path('delete-selected-book/', views.delete_selected_book, name='delete_selected_book'),

    path('category-add/', views.category_add, name='category_add'),
    path('category-list/', views.category_list, name="category_list"),
    path('delete-category/<str:category_name>/', views.delete_category, name='delete_category'),
    path('delete-selected-category/', views.delete_selected_category, name='delete_selected_category'),
    path('category/edit/<str:category_name>/', views.edit_category, name='edit_category'),

    path('review-list/', views.review_base, name="review_base"),
    
    path('delete-rebook/<str:comment>/', views.delete_rebook, name='delete_rebook'),
    path('delete-selected-rebook/', views.delete_selected_rebook, name='delete_selected_rebook'),
    path('rebook-list/', views.rebook_list, name="rebook_list"),
    
    path('delete-reuser/<str:comment>/', views.delete_reuser, name='delete_reuser'),
    path('delete-selected-reuser/', views.delete_selected_reuser, name='delete_selected_reuser'),
    path('reuser-list/', views.reuser_list, name="reuser_list"),
    
    path('delete-reweb/<str:review_field>/', views.delete_reweb, name='delete_reweb'),
    path('delete-selected-reweb/', views.delete_selected_reweb, name='delete_selected_reweb'),
    path('reweb-list/', views.reweb_list, name="reweb_list"),
]   
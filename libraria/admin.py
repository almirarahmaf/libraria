from django.contrib import admin

# Register your models here.
from .models import Profile, review_user, ReviewWeb, category, listbook, borrowing, review_book

admin.site.register(Profile)
admin.site.register(review_user)
admin.site.register(ReviewWeb)
admin.site.register(category)
admin.site.register(listbook)
admin.site.register(borrowing)
admin.site.register(review_book)
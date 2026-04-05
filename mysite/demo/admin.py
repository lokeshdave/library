from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Classroom, Student, StudentLog, Author, Genre, Book, BorrowRequest

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Classroom)
admin.site.register(StudentLog)
admin.site.register(Student)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BorrowRequest)

# Register your models here.

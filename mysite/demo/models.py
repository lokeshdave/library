from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'student'),
        ('librarian', 'librarian'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='user')
    

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    marks = models.IntegerField()
    age = models.IntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class StudentLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    
    def __str__(self):
        return self.student
    
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(default=None, null=True)
    
    def __str__(self):
        return self.name
    

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    isbn = models.IntegerField()
    available_copies = models.IntegerField()
    total_copies = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    
class BorrowRequest(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    request_at = models.DateTimeField(default=datetime.now)
    approved_at = models.DateField(null=True)
    return_at = models.DateField(null=True)
    
    def __str__(self):
        return self.book.title
    
    
class BookReview(models.Model):
    
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.book.title
    
    

@receiver(post_save, sender=BorrowRequest)
def copy_changes(sender, instance, created, **kwargs):
    book = instance.book
    if not created:
        if sender.status == "approved":
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()

        elif instance.status == "returned":
            book.available_copies += 1
            book.save()
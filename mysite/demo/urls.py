from django.urls import path
from .views import (first_api, reg_page, login_page,
                    refresh_token, books, author, genre, borrow,
                    reviews)


urlpatterns = [
  path("first-app", first_api, name="first-app"),
  path("api/register/", reg_page, name="register"),
  path("api/token/", login_page, name="token"),
  path("api/token/refresh/", refresh_token, name="token"),
  path("api/books/", books, name="books"),
  path("api/books/<str:pk>/", books, name="books"),
  path("api/authors/", author, name="authors"),
  path("api/authors/<str:pk>/", author, name="authors"),
  path("api/genres/", genre, name="genres"),
  path("api/genres/<str:pk>/", genre, name="genres"),
  path("api/borrow/", borrow, name="borrow"),
  path("api/borrow/<str:pk>/<str:action>/", borrow, name="borrow"),
  path("api/books/<str:pk>/reviews/", reviews, name="reviews"),
  path("api/books/<str:pk>/reviews/", reviews, name="reviews"),
  path("api/books/<str:pk>/reviews/<str:review_id>/", reviews, name="reviews"),
  
]

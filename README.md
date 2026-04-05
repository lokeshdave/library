# Library Management API

A Django REST Framework project for managing books, authors, genres, borrowing system, and reviews with JWT authentication.

---

## Features

- JWT Authentication (Login, Refresh)
- Custom User (Student, Librarian)
- Book CRUD (Librarian only)
- Author & Genre Management
- Borrow System (Approve, Reject, Return)
- Reviews (Only owner can edit/delete)
- Filtering, Pagination, Ordering
- Custom Permissions
- Signals (auto update book copies)

---

## Tech Stack

- Django
- Django REST Framework
- Simple JWT
- SQLite

---

## Setup

```bash
git clone https://github.com/lokeshdave/library-api.git
cd library-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
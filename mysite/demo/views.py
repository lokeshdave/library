from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (Student, StudentLog,
                     Classroom, CustomUser,
                     Book, Author, Genre,
                     BorrowRequest, BookReview)
from rest_framework_simplejwt.tokens import RefreshToken
import random
from rest_framework import status
from django.contrib.auth import authenticate
from .helper import get_tokens_for_user
from .serializers import (UserSerializer, BookSerializer,
                          BookSerializerSave, AuthorSerializer,
                          GenreSerializer, BorrowRequestSerializer,
                          UserSerializerGet, BookReviewSerializer,
                          BookReviewSerializerAdd)
from datetime import datetime

# Create your views here.
@api_view(["GET", "POST"])
def first_api(request, pk=None):
    if request.method == "GET":
        names = ["abc", "xyz","abcd", "des", "abcde", "sae","dees", "see"]
        for i in range(0, 20):
            num = random.randint(1, 100)
            age = random.randint(18, 22)
            class_name = f"class_{random.choice(names)}"
            student_name = random.choice(names)
            class_ = Classroom(name=class_name)
            class_.save()
            student = Student(
                name=student_name,
                marks=num,
                age=age,
                classroom=class_
            )
            student.save()
            StudentLog(
                student=student,
                action="done"
            ).save()
        # top 5 
        # marks should be in descending order
    if request.method == "POST":
        students = Student.objects.all()
        total = students.count()
        print("total>>", total)
        students = students.order_by("-marks")[:20]
        student_list = []
        
        for student in students:
            student_list.append(
                {"name": student.name, "marks": student.marks}
            )
        return Response({"data": student_list, "total_students": total})
    
    # if request.method == "PUT":
    #     student_get = Student.objects.get(id=pk)
    #     current_time = datetime.datetime.now()
    #     if student_get.date:
    #         current_time = student_get.date()
        
    return Response({"msg":"ok"})


@api_view(["POST"])
def reg_page(request):
    if request.method == "POST":
        user = request.user 
        if user.role != "admin":
            return Response({"error": "only admin can create user account"})
        
        data = request.data
        if not data.get("role"):
            return Response({"error": "Role is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def books(request, pk=None):
    
    if request.method == "GET":  
        if pk:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book).data
            return Response({"data": serializer})
        
        
        book = Book.objects.all().select_related("author").prefetch_related("genre")
        filter_book = {}
        request_get = request.GET
        if request_get.get("author"):
            filter_book["author__name__icontains"] = request_get.get("author")
        
        if request_get.get("genre"):
            filter_book["genre__name__icontains"] = request_get.get("genre")
            
        if request_get.get("title"):
            filter_book["title__icontains"] = request_get.get("title")
        
        if filter_book:
            book = book.filter(**filter_book).distinct()
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 5))
        
        start = (page - 1) * limit
        end = page * limit
        
        book = book[start:end]
        serializer = BookSerializer(book, many=True).data
        return Response({"data": serializer})

    if request.method == "POST":
        if request.user.role == "librarian":
            serializer = BookSerializerSave(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Book added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only librarian have access to do this action"}, status=status.HTTP_400_BAD_REQUEST)
            
    if request.method == "PUT":
        if pk:
            if request.user.role == "librarian":
                book = Book.objects.get(id=pk)
                serializer = BookSerializer(book, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"msg": "Book data edited successfully"},
                                    status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Only librarian have access to do this action"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Book id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        if pk:
            if request.user.role == "librarian":
                book = Book.objects.get(id=pk)
                book.delete()
                return Response({"msg": "Book delete successfully"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error": "Only librarian have access to do this action"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Book id is required"}, status=status.HTTP_400_BAD_REQUEST)
                
                
@api_view(['GET', 'POST'])
def author(request, pk=None):
    if request.method == "GET":  
        if pk:
            author = Author.objects.get(id=pk)
            serializer = AuthorSerializer(author).data
            return Response({"data": serializer})
        
        author = Author.objects.all()            
        serializer = AuthorSerializer(author, many=True).data
        return Response({"data": serializer})

    if request.method == "POST":
        if request.user.role == "librarian":
            serializer = AuthorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Author added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only librarian have access to do this action"}, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET', 'POST'])
def genre(request, pk=None):
    if request.method == "GET":  
        if pk:
            genre = Genre.objects.get(id=pk)
            serializer = GenreSerializer(genre).data
            return Response({"data": serializer})
        
        genre = Genre.objects.all()            
        serializer = GenreSerializer(genre, many=True).data
        return Response({"data": serializer})

    if request.method == "POST":
        if request.user.role == "librarian":
            serializer = GenreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Genre added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only librarian have access to do this action"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PATCH'])
def borrow(request, pk=None, action=None):
    if request.method == "GET":     
        customUser = CustomUser.objects.all()            
        serializer = UserSerializerGet(customUser, many=True).data
        return Response({"data": serializer})

    if request.method == "POST":
        if request.user.role == "student":
            data = request.data
            data["user"] = request.user.id
            serializer = BorrowRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Borrowed successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only student have access to do this action"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        if pk and action:
            try:
                borrow_request = BorrowRequest.objects.get(id=pk)
            except BorrowRequest.DoesNotExist:
                return Response({"error": "Borrow request doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
            if action.lower() == "approve":
                borrow_request.status = action.lower() 
                borrow_request.approved_at = datetime.now()
                borrow_request.save()
            
            elif action.lower() == "reject":
                borrow_request.status = action.lower()
                borrow_request.save()
            
            elif action.lower() == "return":
                borrow_request.status = action.lower()
                borrow_request.return_at = datetime.now()
                borrow_request.save()
                
            else:
                return Response({"error": "Status is not valid"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            
            return Response({"msg": f"Borrow request {action} successfully"},
                            status=status.HTTP_202_ACCEPTED)
            
        else:
           return Response({"error": "Id and Status is required"},
                           status=status.HTTP_400_BAD_REQUEST) 
           
           
@api_view(['GET', 'POST'])
def reviews(request, pk=None):
    
    if request.method == "GET":  
        review = BookReview.objects.filter(book__id=pk)
        serializer = BookReviewSerializer(review, many=True).data
        return Response({"data": serializer})

    if request.method == "POST":
        data = request.data
        data["user"] = request.user.id
        data["book"] = pk
        data["created_at"] = datetime.now().date()
        serializer = BookReviewSerializerAdd(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Reviews added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    
@api_view(["POST"])
def login_page(request):
    if request.method == "POST":
        data = request.data
        # property = data["property"]
        password = data.get("password")
        username = data.get("username")
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user, data.get("remember_me"))
            id = CustomUser.objects.get(username=username)
            id = id.id  
            context = {
                "token": token,
                "msg": "Login Succsess",
                "userid": id,
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": {"none_field_errors": ["username or password not vaild"]}},
                status=status.HTTP_404_NOT_FOUND,
            )
            
@api_view(['POST'])
def refresh_token(request):
    refresh = request.data.get("refresh")
    
    try:
        token = RefreshToken(refresh)
        
        return Response({
            "access": str(token.access_token)
        })
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=400)

# @api_view(["POST"])
# def register(request):
    
    

# @authentication_classes([])
# @permission_classes([])
# class UserLoginview(APIView):
#     def post(self, request):  # pragma: no cover
#         data = json.loads(request.body)
#         # property = data["property"]
#         password = data.get("password")
#         username = data.get("username")
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             token = get_tokens_for_user(user, data.get("remember_me"))
#             id = User.objects.get(username=username)
            
#             id = id.id  
#             token["access"] = f"{token['access']}---{db}"

#             context = {
#                 "token": token,
#                 "msg": "Login Succsess",
#                 "userid": id,
#             }
#             return Response(context, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {"errors": {"none_field_errors": ["username or password not vaild"]}},
#                 status=status.HTTP_404_NOT_FOUND,
#             )


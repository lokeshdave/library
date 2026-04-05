from rest_framework import serializers
from .models import CustomUser, Author, Genre, Book, BorrowRequest, BookReview


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    
    class Meta:
        model = Book
        fields = "__all__"
        
class BookSerializerSave(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = "__all__"
        
class BorrowRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BorrowRequest
        fields = "__all__"
        
class UserSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class BookReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializerGet(read_only=True)
    
    class Meta:
        model = BookReview
        fields = "__all__"

class BookReviewSerializerAdd(serializers.ModelSerializer):
    class Meta: 
        model = BookReview
        fields = "__all__"
        
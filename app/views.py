from . import serializer
from . import models
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from userauths.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db import IntegrityError


class ProductListPagination(PageNumberPagination):
    page_size = 10  # Adjust this based on the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializer.CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access for user creation
# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializer.CustomUserSerializer
#     permission_classes = [AllowAny]  # Allow unauthenticated access for user creation

#     def perform_create(self, serializer):
#         user = serializer.save()
#         Token.objects.create(user=user)

# class UserLoginView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializer.UserLoginSerializer
#     permission_classes = [AllowAny]  # Allow unauthenticated access for user login

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']

#         # Log in the user
#         login(request, user)

#         # Retrieve or create a token for the user
#         token, created = Token.objects.get_or_create(user=user)

#         return Response({'token': token.key})
    
@csrf_exempt  
def customer_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email,password=password)
    if user:
        msg ={
            'bool':True,
            'user': user.email
        }
    else:
        msg ={
            'bool': False,
            'msg': 'Invalid username or password'
        }
    return JsonResponse(msg)


# @csrf_exempt
# @api_view(['POST'])
# def customer_register(request):
#     username = request.POST.get('username', '')
#     email = request.POST.get('email', '')
#     password = request.POST.get('password', '')
#     user = User.objects.create_user(
#         username=username,
#         email=email,
#         password=password,
#     )
#     if user:
#         # customer = models.User.objects.create_user(
#         #     user=user
#         # )
#         msg ={
#             'bool':True,
#             'user': user.id,
#             'msg': 'Thank you for registering, You can now login'
#         }
#     else:
#         msg ={
#             'bool': False,
#             'msg': 'Oops...Something went wrong'
#         }
#     return JsonResponse(msg)
@permission_classes([AllowAny])
class CustomerRegisterView(generics.ListAPIView):
    queryset = []  # Add this line to define an empty queryset
    serializer_class = serializer.CustomUserSerializer 
    def get_queryset(self):
        return self.queryset
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'bool': True,
                    'user': user.id,
                    'msg': 'Thank you for registering, You can now login'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'bool': False,
                    'msg': 'Oops...Something went wrong',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({
                'bool': False,
                'msg': 'Email/Username already exists',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializer.CategorySerializer

class ProductImageList(generics.ListAPIView):
    queryset = models.ProductImages.objects.all()
    serializer_class = serializer.ProductImageSerializer

class ProductList(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializer.ProductSerializer
    # pagination_class = ProductListPagination


class NicheList(generics.ListAPIView):
    queryset = models.Niche.objects.all()
    serializer_class = serializer.NicheSerializer

class NicheDetail(generics.RetrieveAPIView):
    queryset = models.Niche.objects.all()
    serializer_class = serializer.NicheDetailSerializer



class CartOrderList(generics.ListAPIView):
    queryset = models.CartOrder.objects.all()
    serializer_class = serializer.CartOrderSerializer


# class CartOrderItemsList(generics.ListAPIView):
#     queryset = models.CartOrderItems.objects.all()
#     serializer_class = serializer.CartOrderItemsSerializer

class CartOrderItemsList(generics.ListCreateAPIView):
    queryset = models.CartOrderItems.objects.all()
    serializer_class = serializer.CartOrderItemsSerializer
    def create(self, request, *args, **kwargs):
        product_name = request.data.get('item')
        existing_item = models.CartOrderItems.objects.filter(item=product_name).first()

        if existing_item:
            # If a product with the same name already exists, increment its quantity
            existing_item.qty += 1
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the product doesn't exist, create a new one
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

def CartOrderItemsTotal(request):
    queryset = models.CartOrderItems.objects.all()
    total_price = sum(item.total for item in queryset)
    return JsonResponse({'total_price': total_price})

class CartOrderItemsIncrease(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CartOrderItems.objects.all()
    serializer_class = serializer.CartOrderItemsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Custom logic for decreasing quantity and price
        if instance.qty >= 0:
            instance.qty += 1
            instance.total += serializer.validated_data['price']  # Adjust this line based on your specific logic
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Item doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


    
class CartOrderItemsDecrease(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CartOrderItems.objects.all()
    serializer_class = serializer.CartOrderItemsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Custom logic for decreasing quantity and price
        if instance.qty >= 1:
            instance.qty -= 1
            instance.total -= serializer.validated_data['price']  # Adjust this line based on your specific logic
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Quantity cannot be less than 0"}, status=status.HTTP_400_BAD_REQUEST)
        
class CartOrderItemDeleteView(generics.DestroyAPIView):
    queryset = models.CartOrderItems.objects.all()
    serializer_class = serializer.CartOrderItemsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






class ProductReviews(generics.ListAPIView):
    queryset = models.ProductReview.objects.all()
    serializer_class = serializer.ProductReviewSerializer


class WishlistDetail(generics.ListAPIView):
    queryset = models.wishlist.objects.all()
    serializer_class = serializer.WishlistSerializer

class AddressDetail(generics.ListAPIView):
    queryset = models.Address.objects.all()
    serializer_class = serializer.AddressSerializer
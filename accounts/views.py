from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.tokenauthentication import JWTAuthentication
from .serializers import UserSerializer, LoginSerialzer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



@api_view(['POST'])
@swagger_auto_schema(
    responses={201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'bio': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )}
)
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@swagger_auto_schema(
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )}
)
def login(request):
    serializer = LoginSerialzer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.validated_data
        is_admin = user_data['is_admin']  
        token = JWTAuthentication.generate_token(payload=serializer.validated_data)
        return Response({
            "message": "Login Successful",
            'token': token,
            'user': serializer.data,
            'is_admin': is_admin 
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
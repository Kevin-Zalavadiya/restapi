
import logging
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Tea
from .permissions import IsUser, IsAdmin, IsSuperUser
from .serializers import TeaSerializer, RegisterSerializer, UserSerializer


logger = logging.getLogger(__name__)


@api_view(['GET'])
def home_view(request):
    
    return JsonResponse({"message": "Welcome to the Chai REST API!"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    try:
        logger.info("Registration request received", extra={"data": request.data})
        
       
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            logger.warning("Missing required fields", extra={"missing_fields": missing_fields})
            return Response(
                {"error": "Missing required fields", "missing": missing_fields},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        data = request.data.copy()
        if 'password2' not in data:
            data['password2'] = data['password']
            
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User {user.username} registered successfully")
            
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )
            
        
        logger.warning("Validation failed", extra={"errors": serializer.errors})
        return Response(
            {"error": "Validation failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    except Exception as e:
        logger.exception("Error during user registration")
        return Response(
            {"error": "An error occurred during registration", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TeaViewSet(viewsets.ViewSet):

    
    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [IsUser]
        elif self.action == 'create':
            permission_classes = [IsAdmin]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]

    def list(self, request):
        teas = Tea.objects.all()
        serializer = TeaSerializer(teas, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            tea = Tea.objects.get(pk=pk)
        except Tea.DoesNotExist:
            return Response(
                {"detail": "Tea not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = TeaSerializer(tea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        try:
            tea = Tea.objects.get(pk=pk)
            tea.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Tea.DoesNotExist:
            return Response(
                {"detail": "Tea not found"},
                status=status.HTTP_404_NOT_FOUND
            )

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Tea, CustomUser
from .serializers import TeaSerializer, RegisterSerializer, UserSerializer
from .permissions import IsUser, IsAdmin, IsSuperUser

def home_view(request):
    return HttpResponse("<h1>Welcome to the Tea API</h1><p>Use the API endpoints to interact with the application.</p>")

from django.http import JsonResponse


def home_view(request):
    return JsonResponse({"message": "Welcome to the Chai REST API!"})

@api_view(['POST'])
def register(request):
    try:
        print("\n=== Registration Request ===")
        print("Request data:", request.data)
        
        # Ensure required fields are present
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in request.data:
                return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # If password2 is not provided, set it to match password
        data = request.data.copy()
        if 'password2' not in data:
            data['password2'] = data['password']
            
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"User {user.username} registered successfully")
            return Response({
                "message": "User registered successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
            
        print("Validation errors:", serializer.errors)
        return Response({
            "error": "Validation failed",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        import traceback
        print("Error in register view:")
        traceback.print_exc()
        return Response({
            "error": "An error occurred during registration",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class TeaViewSet(viewsets.ViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsUser]
        elif self.action == 'create':
            permission_classes = [IsAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):

        teas = Tea.objects.all()
        return Response(TeaSerializer(teas, many=True).data)

    def create(self, request):
        """
        Create a new tea.
        Permissions: admin, superuser
        """
        serializer = TeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        try:
            tea = Tea.objects.get(pk=pk)
        except Tea.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
            
        serializer = TeaSerializer(tea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            tea = Tea.objects.get(pk=pk)
            tea.delete()
            return Response(status=204)
        except Tea.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

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
        print("Received registration request with data:", request.data)  # Debug log
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"User {user.username} registered successfully")  # Debug log
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)  # Debug log
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error in register view: {str(e)}")  # Debug log
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class TeaViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if not IsUser().has_permission(request, self):
            return Response({"detail": "Access denied"}, status=403)
        teas = Tea.objects.all()
        return Response(TeaSerializer(teas, many=True).data)

    def create(self, request):
        if not IsAdmin().has_permission(request, self):
            return Response({"detail": "Access denied"}, status=403)
        serializer = TeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        if not IsSuperUser().has_permission(request, self):
            return Response({"detail": "Access denied"}, status=403)
        try:
            tea = Tea.objects.get(pk=pk)
        except Tea.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        serializer = TeaSerializer(tea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        if not IsSuperUser().has_permission(request, self):
            return Response({"detail": "Access denied"}, status=403)
        try:
            tea = Tea.objects.get(pk=pk)
            tea.delete()
            return Response(status=204)
        except Tea.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

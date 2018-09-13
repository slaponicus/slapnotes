from .models import Note
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import (NoteSerializer, CreateUserSerializer, 
        UserSerializer, LoginUserSerializer)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


#@method_decorator(csrf_exempt, name='dispatch')
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return self.request.user.notes.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#@method_decorator(csrf_exempt, name='post')
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

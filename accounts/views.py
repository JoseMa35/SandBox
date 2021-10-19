from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from accounts.models import User, Profile
from accounts.serializars import ProfileSerializer
from rest_framework import generics


class ProfileListView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user__pk=pk)
        serializador = ProfileSerializer(profile)
        return Response(serializador.data)

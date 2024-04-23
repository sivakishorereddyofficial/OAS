from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    objs = User.objects.all()
    serializer = UserSerializer(objs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count(request):
    objs = User.objects.all().count()
    return Response({"users":objs})



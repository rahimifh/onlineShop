from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Albom, BlogPost, Like
from ..serializers import AlbumeSerializers, LikeSerializer, PostSerializer


@api_view(["get"])
@permission_classes((AllowAny,))
def banner(request):
    """
    return three first item for banners
    """
    obj = Albom.objects.all()[:3]

    res = AlbumeSerializers(obj, many=True)

    return Response(res.data, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        like = serializer.validated_data["is_liked"]
        user = serializer.validated_data["user"]
        post = serializer.validated_data["post"]
        print("user", user)
        print("is_liked : ", like)
        new_liked = Like.objects.filter(is_liked=True, post=post, user=user)
        if new_liked.exists():
            raise serializers.ValidationError(f"You have liked is post already.")
        else:
            serializer.save()
            serializer = LikeSerializer()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostViewSet(viewsets.ViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

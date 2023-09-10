from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import TodoItem
from ..serializers import TodoItemSerializer


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def todo_item_list(request: Request):
    user = request.user
    if not user:
        return

    if request.method == "GET":
        todo_items = TodoItem.objects.filter(owner=user.id)
        serializer = TodoItemSerializer(todo_items, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            todo_item = TodoItem(
                owner=user, done=serializer.data["done"], content=serializer.data["content"])
            todo_item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def todo_item(request: Request, id: int):
    user = request.user
    if not user:
        return

    try:
        todo_item = TodoItem.objects.get(pk=id, owner=user.id)
    except TodoItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TodoItemSerializer(todo_item)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = TodoItemSerializer(todo_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


todos_view = (
    [
        path("", todo_item_list),
        path("<int:id>", todo_item),
    ],
    "todos",
    "todos",
)

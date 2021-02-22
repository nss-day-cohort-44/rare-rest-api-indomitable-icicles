"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Category, RareUser


class Categories(ViewSet):

    def create(self, request):
       
        # Create a new Python instance of the class
        # and set its properties from what was sent in the
        # body of the request from the client.
        
        category = Category()
        category.label = request.data['label']
        

        # Try to save the new cat to the database, then
        # serialize the instance as JSON, and send the
        # JSON as a response to the client request
        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        categories = Category.objects.all()

        # Support filtering by type
        
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
       
        category = Category.objects.get(pk=pk)
        category.label = request.data['label']
        category.save()
        # 204 status send back
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        #Handle DELETE requests/ single comment, returns 200, 404, or 500 status code
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer 
    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1



"""View module for handling requsts about tags"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Tag

class Tags(ViewSet):
    """Rare Tags"""

    def create(self, request):
        """Handle POST operations
    
        Returns: 
            Response: JSON serialized tag instance
        """

        #Create a new Python instance of the Tags class
        #Set its properties from what was sent in the body
        #Of the request from the client
        tag = Tag()
        tag.label = request.data["label"]

        #Try and save the new tag to the database
        #Then serialize the tag instance as JSON
        #And send the JSON as a response to the client request
        try: 
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a tag

        Returns:
            Response: Empty body with a 204 status code
        """
        #Similar to POST
        #Instead of creating a new instance of Tag
        #Get the tag record from the database whose primary key is 'pk'
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

        #204 status code means everything worked but the
        #server isn't sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response --JSON serialized tag instance
        """
        try:
            # `pk` is a parameter to this function
            # Django parses it from the URL route parameter
            #   http://localhost:8000/tags/2
            # The `2` at the end of the route becomes `pk`
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()

        # `many=True` argument to the serializer.
        # needed when serializing a list of objects instead of a single object
        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Tag

        Returns:
            Response: 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments: serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')
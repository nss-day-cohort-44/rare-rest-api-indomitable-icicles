
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, Category, RareUser, rareuser


class Posts(ViewSet):

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all post records from the database
        posts = Post.objects.all()
        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            posts = posts.filter(rare_user=user_id)
        
        # Support filtering posts by categories
        #    http://localhost:8000posts?category=1
        #
        # That URL will retrieve all categories
        category = self.request.query_params.get('label', None)
        if category is not None:
            posts = posts.filter(category__id=category)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

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
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """

        # Uses the token passed in the `Authorization` header
        rare_user = RareUser.objects.get(user=request.auth.user)

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        post = Post()
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.image = request.data["image"]
        post.rare_user = rare_user

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.
        category = Category.objects.get(pk=request.data["categoryId"])
        post.category = category

        # Try to save the new post to the database, then
        # serialize the post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('title', 'publication_date',
                  'content', 'image','category')
        depth = 1

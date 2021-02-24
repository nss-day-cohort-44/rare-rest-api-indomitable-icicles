
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rareapi.models import Post, Category, RareUser, rareuser, PostTag, Tag, tag
from django.contrib.auth.models import User




class Posts(ViewSet):

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all post records from the database
        posts = Post.objects.all()

        sort_parameter = self.request.query_params.get('sortby', None)

        if sort_parameter is not None and sort_parameter == 'user':
            current_rare_user = RareUser.objects.get(user=request.auth.user)
            user_posts = Post.objects.filter(rare_user=current_rare_user)

            for post in user_posts: 
                posttags = PostTag.objects.filter(post=post)
                post.posttags = posttags

            serializer = PostSerializer(
                user_posts, many=True, context={'request': request})
            return Response(serializer.data)
        # Support filtering posts by categories
        #    http://localhost:8000posts?category=1
        #
        # That URL will retrieve all categories
        category = self.request.query_params.get('label', None)
        if category is not None:
            posts = posts.filter(category__id=category)

        else:
            for post in posts: 

                posttags = PostTag.objects.filter(post=post)
                post.posttags = posttags 
        
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
            posttags = PostTag.objects.filter(post=post)
            post.posttags = posttags
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
        category = Category.objects.get(pk=request.data["category_id"])
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


    def update(self, request, pk=None):
        """Handle PUT requests for a post
        Returns:
            Response -- Empty body with 204 status code
        """
        rare_user = RareUser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Post, get the post record
        # from the database whose primary key is `pk`
        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.image = request.data["image"]
        post.rare_user = rare_user

        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category
        post.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def changetag(self, request, pk=None):
        if request.method == "POST":
            post = Post.objects.get(pk=pk)

            try: 
                tagger = PostTag.objects.get(
                    tag=tag, post=post)
                return Response(
                    {'message': 'Post already features this tag.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except PostTag.DoesNotExist:
                tagger = PostTag()
                tagger.post = post
                tagger.tag = tag
                tagger.save()

                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                return Response(
                   {'message': 'This does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST 
                )

            try:
                # Try to delete the signup
                tagger = PostTag.objects.get(
                    post=post, tag=tag)
                tagger.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except PostTag.DoesNotExist:
                return Response(
                    {'message': 'Not currently a tag on this post.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ['tag'] 
        depth = 1


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class PostRareUserSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(many=False)

    class Meta:
        model =RareUser
        fields = ['user']


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    Arguments:
        serializer type
    """
    rare_user = PostRareUserSerializer(many=False)
    posttags = PostTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date',
                  'content', 'image', 'category', 'posttags', 'rare_user')
        depth = 1


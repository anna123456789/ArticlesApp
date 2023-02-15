#from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Article
from .serializers import ArticleSerializer

#@api_view(['GET', 'POST', 'PUT'])
@api_view(['GET'])
def getRoute(request):
    routes = [
        'GET /api',
        'GET /api/articles/',
        'GET /api/articles/:id'
    ]
    #return JsonResponse(routes, safe=False)
    return Response(routes)

@api_view(['GET'])
def getArticles(request):
    # generates an error, Python objects can not passed to Response, it has to be serialized before
    # books = Book.objects.all()
    # return Response(books)
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getArticle(request, pk):
    article = Article.objects.get(id = pk)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)

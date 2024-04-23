

from . import models
from . import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from rest_framework.decorators import permission_classes, action

class Product(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        print(request.headers)

        products = models.Product.objects.filter(count__gte=1)
        serializer = serializers.GenericProductSerializer(products, many=True)
        res = {
            'products' : serializer.data,
            'count' : products.count()
        }
        return Response(res)

    def post(self, request):

        product_data = request.data
        # img = product_data.pop('image')
        serializer = serializers.GenericProductSerializer(data=product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        # new_product_id = serializer.data.id
        # models.ProdutGallery.objects.create()
        return Response(serializer.data)
    
class ProductGallery(APIView):
    # permission_classes

    def get(self, request, id=None):
        if id is None:
            obj = models.ProdutGallery.objects.all()
            return Response(obj.values())
        obj = models.ProdutGallery.objects.filter(id=id)
        return Response(obj.values())
    
class Cart(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart_items = models.Cart.objects.filter(user__id = request.user.id)
        return Response(cart_items.values())

    def put(self, request, prod_id):
        
        #check if product is in cart
        print(request.COOKIES)
        cart_items = models.Cart.objects.filter(user__id=request.user.id, product__id=prod_id)

        if cart_items.exists():

            count=cart_items.first().count
            cart_items.update(count=count+1)
        else:
            cart_items = models.Cart.objects.create(user_id=request.user.id, product_id=prod_id)
            cart_items.save()
        return Response({"status":True})
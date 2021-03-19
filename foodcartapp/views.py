from django.http import JsonResponse
from django.templatetags.static import static
import json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .models import OrderItem
from .models import Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_details = request.data
    if 'products' not in order_details.keys() \
        or not isinstance(order_details['products'], list) \
        or not order_details['products']:
            return Response({'error': 'products key not presented or not list'},
                            status=status.HTTP_404_NOT_FOUND)
    order = Order.objects.create(
    firstname = order_details['firstname'],
    lastname = order_details['lastname'],
    address = order_details['address'],
    phonenumber = order_details['phonenumber'],
    )
    for commodity in order_details['products']:
        product = get_object_or_404(Product, id=commodity['product'])
        order.items.create(product=product, quantity=commodity['quantity'])
    return Response({})

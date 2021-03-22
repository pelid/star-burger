from django.http import JsonResponse
from django.templatetags.static import static
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order
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
    products = Product.objects.all()
    products_id = []
    for product in products:
        products_id.append(product.id)

    if 'products' not in order_details.keys():
        return Response(['products key not presented'], status=400)

    if order_details['products'] is None:
        return Response(['products key is None'], status=400)

    if not isinstance(order_details['products'], list):
        return Response(['products key not list'], status=400)

    if not order_details['products']:
        return Response(['products key does not matter'], status=400)

    if 'firstname' and 'lastname' and 'phonenumber' and 'address' not in order_details.keys():
        return Response(['no order keys'], status=400)

    if order_details['firstname'] is None \
        and order_details['lastname'] is None \
        and order_details['phonenumber'] is None \
        and order_details['address'] is None:
        return Response(['all order keys are None'])

    if order_details['firstname'] is None:
        return Response(['firstname key is None'], status=400)

    if not order_details['phonenumber']:
        return Response(['phonenumber key does not matter'], status=400)

    if order_details['products'][0]['product'] not in products_id:
        return Response(['product number does not exist'], status=400)

    if not isinstance(order_details['firstname'], str):
        return Response(['products key not str(string)'], status=400)

    order = Order.objects.create(
        firstname=order_details['firstname'],
        lastname=order_details['lastname'],
        address=order_details['address'],
        phonenumber=order_details['phonenumber'],
    )
    for commodity in order_details['products']:
        product = get_object_or_404(Product, id=commodity['product'])
        order.items.create(product=product, quantity=commodity['quantity'])
    return Response({})

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='категория', related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    description = models.TextField('описание', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items',
                                   verbose_name="ресторан")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='menu_items',
                                verbose_name='продукт')
    availability = models.BooleanField('в продаже', default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):
    firstname = models.CharField('имя', max_length=20)
    lastname = models.CharField('фамилия', max_length=20)
    address = models.CharField('адрес', max_length=40)
    phonenumber = PhoneNumberField('телефон', max_length=15)
    comment = models.TextField('Комментарий', max_length=300, blank=True)
    ORDER_STATUS = ('no', 'Не обработан'), ('yes', 'Обработан')
    order_status = models.CharField('Статус', max_length=15, choices=ORDER_STATUS, default='no')
    registated_at = models.DateTimeField('Заказ получен', default=timezone.now)
    called_at = models.DateTimeField('Звонок произведен', null=True, blank=True)
    delivered_at = models.DateTimeField('Доставка', null=True, blank=True)
    PAYMENT_METHOD = ('cash', 'Наличные'), ('card', 'Банковская карта')
    payment_method = models.CharField('Способ оплаты', max_length=15, choices=PAYMENT_METHOD, default='')

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items', verbose_name='заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.IntegerField('количество', validators=[MinValueValidator(0), MaxValueValidator(20)])
    price = models.DecimalField('цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], null=True)

    def __str__(self):
        return f'{self.product} {self.order}'

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    description = models.TextField(verbose_name="Описание категории", blank=True)
    image = models.ImageField(upload_to='category/', verbose_name='Изображение категории')
    slug = models.SlugField(max_length=150, unique=True, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-created_at']


class Furniture(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    # Технические поля
    sku = models.CharField(max_length=50,unique=True,verbose_name='Артикул',blank=True,null=True)
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL')

    # Статус и видимость
    is_active = models.BooleanField(default=True, verbose_name='Активный товар')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')

    # Цены
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Цена',validators=[MinValueValidator(0)])
    old_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Старая цена',blank=True,null=True,validators=[MinValueValidator(0)])

    # Характеристики
    material = models.CharField(max_length=200,verbose_name='Материал',blank=True)
    color = models.CharField(max_length=100,verbose_name='Цвет',blank=True)
    dimensions = models.CharField(max_length=100,verbose_name='Габариты (В×Ш×Г)',blank=True)
    weight = models.CharField(max_length=50,verbose_name='Вес',blank=True)
    assembly_required = models.BooleanField(default=True,verbose_name='Требуется сборка')
    warranty = models.CharField(max_length=50,verbose_name='Гарантия',default='5 лет')

    # Изображения
    image = models.ImageField(upload_to='furniture/', verbose_name='Основное изображение')

    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def save(self, *args, **kwargs):
        # Автоматически генерируем slug если не указан
        if not self.slug:
            self.slug = slugify(self.name)

        # Автоматически генерируем SKU если не указан
        if not self.sku:
            self.sku = f"FUR{self.id:06d}" if self.id else "FUR000000"

        super().save(*args, **kwargs)

    # Метод для проверки наличия скидки
    def has_discount(self):
        return self.old_price and self.old_price > self.price

    # Метод для расчета скидки в процентах
    def discount_percentage(self):
        if self.has_discount():
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    # Метод для проверки наличия товара
    def is_in_stock(self):
        return self.stock > 0

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


# В конец main/models.py добавьте:

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price() for item in self.items.all())

    def item_count(self):
        """Количество товаров в корзине"""
        return self.items.count()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """Товар в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Furniture,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def total_price(self):
        """Стоимость позиции (цена * количество)"""
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ['cart', 'product']  # чтобы один товар не повторялся
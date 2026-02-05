from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from main.models import Category, Furniture
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Furniture, Cart, CartItem

class Template(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:4]
        return context


class CategoryList(ListView):
    model = Category
    context_object_name = "cat"
    template_name = 'main/category_list.html'


class FurnitureList(ListView):
    model = Furniture
    context_object_name = 'fur'
    template_name = 'main/furniture_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')

        # ИСПРАВЛЕНО: используем 'category' вместо 'cat'
        return Furniture.objects.filter(
            category__slug=category_slug,  # было cat__slug, стало category__slug
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)

        context['category'] = category
        return context


class FurnitureDetail(DetailView):
    model = Furniture
    context_object_name = 'product'
    template_name = 'main/furniture_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['related_products'] = Furniture.objects.filter(
            category=product.category,  # было cat, стало category
            is_active=True
        ).exclude(id=product.id)[:4]
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно добавить дополнительные данные, например:
        context['team_members'] = [
            {'name': 'Александр Иванов', 'position': 'Основатель и CEO', 'experience': '15 лет в мебельном бизнесе'},
            {'name': 'Мария Петрова', 'position': 'Главный дизайнер', 'experience': 'Опыт работы в Италии и Германии'},
            {'name': 'Дмитрий Сидоров', 'position': 'Технолог производства',
             'experience': 'Специалист по редким породам дерева'},
            {'name': 'Елена Кузнецова', 'position': 'Менеджер по работе с клиентами',
             'experience': 'Персональный подход к каждому клиенту'},
        ]
        context['statistics'] = {
            'years': 12,
            'projects': 1500,
            'clients': 3200,
            'countries': 8,
        }
        return context






@login_required
def cart_view(request):
    """Просмотр корзины (только для авторизованных)"""
    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        'cart': cart,
        'items': cart.items.all(),
        'total': cart.total_price(),
    }
    return render(request, 'main/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину (только для авторизованных)"""
    if request.method == 'POST':
        product = get_object_or_404(Furniture, id=product_id, is_active=True)

        # Получаем корзину пользователя
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Проверяем есть ли уже такой товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            # Если товар уже есть, увеличиваем количество
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f'Товар "{product.name}" добавлен в корзину!')

        # Возвращаемся на предыдущую страницу
        return redirect(request.META.get('HTTP_REFERER', 'main:index'))

    return redirect('main:index')


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.info(request, f'Товар "{product_name}" удален из корзины')
    return redirect('main:cart')


@login_required
def update_cart_quantity(request, item_id):
    """Изменение количества товара в корзине"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Количество обновлено')
            else:
                cart_item.delete()
                messages.info(request, 'Товар удален из корзины')
        except ValueError:
            messages.error(request, 'Неверное количество')

    return redirect('main:cart')


class DesignProjectsView(TemplateView):
    """Страница дизайн-проектов"""
    template_name = 'main/design_projects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = {
            'phone': '+7 (999) 123-45-67',
            'email': 'info@blackwood.ru',
            'address': 'Москва, ул. Премиальная, 15',
            'work_hours': 'Пн-Пт: 10:00-20:00, Сб-Вс: 11:00-18:00',
            'showroom_hours': 'Ежедневно с 11:00 до 19:00',
        }
        context['social_links'] = [
            {'name': 'Telegram', 'icon': 'bi-telegram', 'url': 'https://t.me/blackwood_furniture'},
            {'name': 'Instagram', 'icon': 'bi-instagram', 'url': 'https://instagram.com/blackwood'},
            {'name': 'WhatsApp', 'icon': 'bi-whatsapp', 'url': 'https://wa.me/79991234567'},
            {'name': 'VK', 'icon': 'bi-vimeo', 'url': 'https://vk.com/blackwood'},
        ]
        return context
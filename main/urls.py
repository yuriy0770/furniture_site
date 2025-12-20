from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Template.as_view(), name='index'),
    path('categories/', views.CategoryList.as_view(), name='category'),
    path('category/<slug:slug>/', views.FurnitureList.as_view(), name='furniture'),
    path('product/<slug:product_slug>/', views.FurnitureDetail.as_view(), name='furniture_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('design-projects/', views.DesignProjectsView.as_view(), name='design_projects'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart'),
]
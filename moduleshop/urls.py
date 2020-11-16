"""moduleshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from myshop.API.resources import PurchaseViewSet
from myshop.API.serializers import OrderSerializer
from myshop.views import Main, Login, Register, Success, ItemListView, Logout, \
    ProfileView, SuperUserView, ItemCreateView, ItemUpdateView, CreateRefund, RefundView, RefundManage, ItemDetailView, \
    CreateOrder

router = routers.DefaultRouter()
router.register(r'orders', PurchaseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('success/', Success.as_view(), name='success'),
    path('logout/', Logout.as_view(), name='logout'),
    path('products/', ItemListView.as_view(), name='products'),
    path('products/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('buy/', CreateOrder.as_view(), name='buy'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('super/', SuperUserView.as_view(), name='super'),
    path('create_item/', ItemCreateView.as_view(), name='create_item'),
    path('products/<int:pk>/update/', ItemUpdateView.as_view(), name='product_update'),
    path('refund/', CreateRefund.as_view(), name='refund'),
    path('refunds/', RefundView.as_view(), name='manage_refunds'),
    path('manage/<int:pk>/', RefundManage.as_view(), name='manage'),
    url(r'^', include(router.urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

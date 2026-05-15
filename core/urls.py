from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from products.views import home, collection, product_detail
from cart.views import add_to_cart, decrease_qty, remove_from_cart, cart_page

urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Home & Search
    path("", home, name="home"),

    # Nawabi Collection (category filter)
    path("collection/", collection, name="collection"),

    # Product Detail
    path("product/<int:product_id>/", product_detail, name="product_detail"),

    # Cart
    path("cart/", cart_page, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/decrease/<int:product_id>/", decrease_qty, name="decrease_qty"),
    path("cart/remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

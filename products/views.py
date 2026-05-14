from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

NAWABI_CATEGORIES = [
    "One Gram Gold",
    "Imitation Jewelry",
    "AD Stone",
    "Oxidized",
    "Anti Tarnish",
]

WHATSAPP_NUMBER = "918081501338"  # ← Apna number yahan


def base_context(request):
    cart = request.session.get("cart", {})
    cart_count = sum(item["qty"] for item in cart.values())
    return {
        "nav_categories": NAWABI_CATEGORIES,
        "cart_count": cart_count,
        "whatsapp_number": WHATSAPP_NUMBER,
    }


def home(request):
    products = Product.objects.select_related('category').order_by('-created_at')
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    ctx = base_context(request)
    ctx["products"] = products
    return render(request, "home.html", ctx)


def collection(request):
    active_category = request.GET.get("category", "").strip()
    if active_category:
        products = Product.objects.filter(
            category__name=active_category
        ).select_related('category').order_by('-created_at')
    else:
        products = Product.objects.select_related('category').order_by('-created_at')
    ctx = base_context(request)
    ctx["products"] = products
    ctx["active_category"] = active_category
    return render(request, "collection.html", ctx)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).select_related('category')[:4]
    ctx = base_context(request)
    ctx["product"] = product
    ctx["related_products"] = related
    return render(request, "product_detail.html", ctx)

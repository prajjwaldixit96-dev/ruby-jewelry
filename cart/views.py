from django.shortcuts import redirect, render, get_object_or_404
from urllib.parse import quote
from products.views import base_context, WHATSAPP_NUMBER
from products.models import Product


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    key = str(product_id)
    if key in cart:
        cart[key]["qty"] += 1
    else:
        cart[key] = {
            "product_id": product.id,
            "name": product.title,
            "price": product.price,
            "image": product.image.url if product.image else "",
            "qty": 1,
        }
    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER", "/"))


def decrease_qty(request, product_id):
    cart = request.session.get("cart", {})
    key = str(product_id)
    if key in cart:
        cart[key]["qty"] -= 1
        if cart[key]["qty"] <= 0:
            del cart[key]
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def cart_page(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0
    for key, item in cart.items():
        subtotal = item["price"] * item["qty"]
        total += subtotal
        cart_items.append({**item, "subtotal": subtotal})
    if cart_items:
        lines = ["Hi Ruby Jewelry, I want to place an order:%0A%0A"]
        for item in cart_items:
            lines.append(
                f"%F0%9F%92%8D {quote(item['name'])} x {item['qty']} = "
                f"%E2%82%B9{item['subtotal']}%0A"
            )
        lines.append(f"%0A*Total: %E2%82%B9{total}*")
        lines.append("%0A%0APlease confirm availability and delivery details.")
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={''.join(lines)}"
    else:
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}"
    ctx = base_context(request)
    ctx.update({"cart_items": cart_items, "total": total, "whatsapp_url": whatsapp_url})
    return render(request, "cart.html", ctx)
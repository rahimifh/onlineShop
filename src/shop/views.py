from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Category, Product
# from .recommender import Recommender

def home(request):
    All = Product.objects.all()
    length = len(All)
    products = All.filter(available=True)[:4]
    chipest = All.order_by("price")[:4]
    mid = All.order_by("price")[length/2-3:length/2+1]

    expensive = All.order_by("-price")[:4]
    return render(
        request,
        'shop/product/home.html',
        {
            'products': products,
            'chipest': chipest,
            'mid': mid,
            'expensive': expensive,
        },)
def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()

    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
           
        },
    )


def product_detail(request, id, slug):

 
    product = get_object_or_404(
        Product, id=id, slug=slug
    )
    cart_product_form = CartAddProductForm()
    # r = Recommender()
    # recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            
            # 'recommended_products': recommended_products,
        },
    )

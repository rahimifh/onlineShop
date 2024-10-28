
from django.shortcuts import get_object_or_404, redirect, render

from cart.forms import CartAddProductForm
from shop.forms import addOrderForm
from .models import Category, Product,SpecialSale
from django.views.generic import  ListView
from django.db.models import Q 
# from .recommender import Recommender
class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/product/search_results.html'
    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
  
        return object_list
def add_order(request):

    if request.method == 'POST':
        form = addOrderForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
        return redirect("shop:home")
    return redirect("shop:home")


def home(request):
    All = Product.objects.all()
    length = len(All)
    products = All.filter(available=True)[:4]
    chipest = All.order_by("price")[:4]
    special =SpecialSale.objects.all()[:1]
    mid = All.order_by("price")[length/2-3:length/2+1]
    categories = Category.objects.all()
    expensive = All.order_by("-price")[:4]
    return render(
        request,
        'shop/product/home.html',
        {
            'products': products,
            'chipest': chipest,
            'categories': categories,
            'mid': mid,
            'special':special,
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

def about(request):
    return render(request, "shop/aboutus.html")
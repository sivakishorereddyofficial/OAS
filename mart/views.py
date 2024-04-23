from django.shortcuts import render, redirect
from . import models
from . import apis


def admin_home(request):
    # if request.user.is_superuser:
    #     return render(request, 'adminHome.html')
    # return redirect('login')
    
    return render(request, 'adminHome.html')




def homePage(request):
    if request.user.is_superuser:
        return redirect('admin-home')
    return render(request, 'home.html')

def homePageRedirect(request):
    print("hello world!")
    return redirect(to='logged-in-user-home')


def createProductView(request):
    return render(request, 'Products.html')

def productDetailedView(request, id):
    prod = models.Product.objects.filter(id=id)
    img_data = models.ProdutGallery.objects.filter(product__id=id).first()
    if prod.exists():
        prod = prod.first()
    print(prod,"---")
    cost = prod.original_cost + prod.making_charges - (prod.original_cost / 100) * (prod.discount_percentage)
    return render(request, 'ProductDetails.html', {"product" : prod, "image":img_data, "cost":cost})

def cart(request):
    cart_objs = models.Cart.objects.filter(user__id=request.user.id)
    print(cart_objs, "==================")
    return render(request, 'Cart.html',{"items": cart_objs})
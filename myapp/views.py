from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import ProductsForm
from .models import Products

# Create your views here.
@never_cache
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request,"login.html",{"form":form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required 
@never_cache
def home(request):
    return render(request,"home.html")

@login_required
@never_cache
def register_products(request):
    if request.method == "POST":
        form = ProductsForm(request.POST)
        if form.is_valid():
            # check if product exist
            productName = form.cleaned_data['name']
            if Products.objects.filter(name=productName).exists():
                messages.error(request,"this product already exists")
                return redirect("registerProducts")
            form.save()
            messages.success(request,"product registered successfully")
            return redirect("viewProducts")
    else:
        form = ProductsForm()

    return render(request,"registerProducts.html",{"form":form})

@login_required
@never_cache
def view_products(request):
    # read all products
    products = Products.objects.all()
    count = products.count()
    return render(request,"viewProducts.html",{"products":products, "count":count})

@login_required
@never_cache
def update_products(request,id):
    product = get_object_or_404(Products,id=id)    
    if request.method == "POST":
        form = ProductsForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect("viewProducts")
    else:
        form = ProductsForm(instance=product)
    return render(request,"updateProduct.html",{"product":form})

@login_required
@never_cache
def delete_products(request,id):
    product = get_object_or_404(Products,id=id)
    product.delete()
    return redirect("viewProducts")
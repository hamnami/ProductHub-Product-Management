from django.contrib import messages
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm, CategoryForm, SaleForm
from .models import Product, Category, Sale

def dashboard(request):
    products = Product.objects.select_related('category')
    total_value = products.aggregate(v=Sum(ExpressionWrapper(F('price')*F('stock'), output_field=DecimalField(max_digits=14, decimal_places=2))))['v'] or 0
    context = {'product_count': products.count(), 'category_count': Category.objects.count(), 'low_stock': products.filter(stock__lte=5).count(), 'inventory_value': total_value, 'recent_sales': Sale.objects.select_related('product').order_by('-sold_at')[:5], 'top_products': products.order_by('-updated_at')[:6]}
    return render(request,'products/dashboard.html',context)

def product_list(request):
    products = Product.objects.select_related('category').order_by('-updated_at')
    q = request.GET.get('q','').strip(); category = request.GET.get('category',''); stock = request.GET.get('stock','')
    if q: products = products.filter(Q(name__icontains=q)|Q(sku__icontains=q)|Q(description__icontains=q))
    if category: products = products.filter(category_id=category)
    if stock == 'low': products = products.filter(stock__lte=5, stock__gt=0)
    elif stock == 'out': products = products.filter(stock=0)
    elif stock == 'available': products = products.filter(stock__gt=0)
    return render(request,'products/product_list.html',{'products':products,'categories':Category.objects.all(),'q':q,'selected_category':category,'selected_stock':stock})

def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid(): form.save(); messages.success(request,'Product added successfully.'); return redirect('product_list')
    return render(request,'products/product_form.html',{'form':form,'title':'Add Product'})

def product_detail(request,pk):
    product = get_object_or_404(Product.objects.select_related('category'),pk=pk)
    return render(request,'products/product_detail.html',{'product':product,'sales':product.sales.order_by('-sold_at')})

def product_edit(request,pk):
    product=get_object_or_404(Product,pk=pk); form=ProductForm(request.POST or None,request.FILES or None,instance=product)
    if form.is_valid(): form.save(); messages.success(request,'Product updated successfully.'); return redirect('product_detail',pk=pk)
    return render(request,'products/product_form.html',{'form':form,'title':'Edit Product'})

def product_delete(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='POST': product.delete(); messages.success(request,'Product deleted.'); return redirect('product_list')
    return render(request,'products/confirm_delete.html',{'object':product,'kind':'product'})

def product_sell(request,pk):
    product=get_object_or_404(Product,pk=pk); form=SaleForm(request.POST or None,product=product)
    if request.method=='POST' and form.is_valid():
        sale=form.save(commit=False); sale.product=product; sale.unit_price=product.price; sale.save(); product.stock -= sale.quantity; product.save(update_fields=['stock','updated_at']); messages.success(request,'Sale recorded and stock updated.'); return redirect('product_detail',pk=pk)
    return render(request,'products/sale_form.html',{'product':product,'form':form})

def category_list(request): return render(request,'products/category_list.html',{'categories':Category.objects.all().order_by('name')})
def category_create(request):
    form=CategoryForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,'Category added.'); return redirect('category_list')
    return render(request,'products/category_form.html',{'form':form,'title':'Add Category'})
def category_edit(request,pk):
    category=get_object_or_404(Category,pk=pk); form=CategoryForm(request.POST or None,instance=category)
    if form.is_valid(): form.save(); messages.success(request,'Category updated.'); return redirect('category_list')
    return render(request,'products/category_form.html',{'form':form,'title':'Edit Category'})
def category_delete(request,pk):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST': category.delete(); messages.success(request,'Category deleted.'); return redirect('category_list')
    return render(request,'products/confirm_delete.html',{'object':category,'kind':'category'})

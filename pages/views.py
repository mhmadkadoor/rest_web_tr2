from django.shortcuts import render
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from .models import Profile, Category
from products.models import Product, Hotdeals
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Q 





restaurant = Profile.objects.get(id=1)


# Create your views here.
def custom_page_not_found_view(request, exception):
    return render(request, '404.html')

def custom_error_view(request):
    return render(request, '500.html')


def home(request):
    user = request.user
    products = Product.objects.all()
    hotdeals = Hotdeals.objects.all()
    categories = Category.objects.filter(restaurant=restaurant)


    return render(request, 'pages/home.html', {"thisPage": 'home', 'restaurant': restaurant, 'products': products, 'hotdeals': hotdeals, 'user': user, 'categories': categories})


def login(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'pages/login.html', {"thisPage": 'login', 'logged': True, 'user': user, 'restaurant': restaurant})
        else:
            return render(request, 'pages/login.html', {"thisPage": 'login', 'error': "Geçersiz bilgiler, lütfen tekrar deneyin.", 'user': user, 'restaurant': restaurant})
    else:
        return render(request, 'pages/login.html', {"thisPage": 'login',"user":user, 'restaurant': restaurant})

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def admin(request):
    user = request.user
    return render(request, 'pages/admin.html', {"thisPage": 'admin', 'user': user, 'restaurant': restaurant})

@login_required(login_url='login')
def proSettings(request):
    user = request.user
    categories = Category.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        if 'btnUpdateInfo' in request.POST:
            restaurant.name = request.POST['name'].strip()
            if 'image' in request.FILES:
                if restaurant.image != 'rest_def.jpg':
                    os.remove(os.path.join(settings.MEDIA_ROOT, restaurant.image.name))
                restaurant.image = request.FILES['image']
            if 'cover' in request.FILES:
                if restaurant.cover != 'cover_def.jpg':
                    os.remove(os.path.join(settings.MEDIA_ROOT, restaurant.cover.name))
                restaurant.cover = request.FILES['cover']
            restaurant.openTime = str(request.POST['openTime'])
            restaurant.closeTime = str(request.POST['closeTime'])
            restaurant.currency = request.POST['currency'].upper()
            restaurant.tiktok = request.POST['tiktok'].strip()
            restaurant.whatsapp = request.POST['whatsapp'].strip()
            restaurant.facebook = request.POST['facebook'].strip()
            restaurant.instagram = request.POST['instagram'].strip()
            restaurant.googleMaps = request.POST['googleMaps'].strip()
            restaurant.save()
            return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'user': user, 'categories': categories, 'restaurant': restaurant, 'success1': "Restoran bilgileri başarıyla güncellendi."})
        if 'btnUpdatePassword' in request.POST:
            recent = str(request.POST['oldPassword'])
            new = str(request.POST['newPassword'])
            confirm = str(request.POST['confirmPassword'])
            if user.check_password(recent) and new == confirm:
                user.set_password(new)
                user.save()
                return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'categories': categories,'user': user, 'restaurant': restaurant, 'success2': "Parola başarıyla değiştirildi."})
            else:
                return render(request, 'pages/proSettings.html', 
                              {
                                "thisPage": 'proSettings', 
                                'user': user, 
                                'categories': categories,
                                'restaurant': restaurant, 
                                'error': "Eski parola yanlış veya yeni parolalar eşleşmiyor."
                                })
        if 'btnAddCategory' in request.POST:
            category_name = request.POST['newCategoryName'].strip()

            if category_name and not Category.objects.filter(name=category_name).exists():
                Category.objects.create(name=category_name, restaurant=restaurant).save()
                return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'user': user, 'restaurant': restaurant, 'categories': categories, 'success3': "Kategori başarıyla eklendi."})
            else:
                return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'user': user, 'restaurant': restaurant, 'categories': categories, 'error': "Kategori adı zaten mevcut veya boş."})
        if 'btnDeleteCategory' in request.POST:
            category_id = request.POST['category']
            if Category.objects.filter(id=category_id).exists() and not category_id == '0':
                category = Category.objects.get(id=category_id)
                category.delete()
                return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'user': user, 'restaurant': restaurant, 'categories': categories, 'success3': "Kategori başarıyla silindi."})
            else:
                return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'user': user, 'restaurant': restaurant, 'categories': categories, 'error': "Kategori bulunamadı."})
    else:
        return render(request, 'pages/proSettings.html', {"thisPage": 'proSettings', 'user': user, 'restaurant': restaurant, 'categories': categories})

def viewProduct(request, product_id):
    user = request.user
    currentProduct = Product.objects.get(id=product_id)
    return render(request, 'products/view/viewProduct.html', {"thisPage": 'viewProduct', 'restaurant': restaurant, 'product': currentProduct, 'user': user})

def viewProductAdmin(request, product_id):
    user = request.user
    currentProduct = Product.objects.get(id=product_id)
    return render(request, 'products/view/viewProductAdmin.html', {"thisPage": 'viewProductAdmin', 'restaurant': restaurant, 'product': currentProduct, 'user': user})

def editProduct(request, product_id):
    user = request.user
    currentProduct = Product.objects.get(id=product_id)
    categories = Category.objects.filter(restaurant=restaurant)
    if request.method == 'POST':
        currentProduct.title = request.POST['title'].strip()
        currentProduct.description = request.POST['description'].strip()
        currentProduct.price = request.POST['price'].strip()
        currentProduct.category = Category.objects.get(id=request.POST['category'].strip())
        if 'image' in request.FILES:
            if currentProduct.image != 'meal_def.jpg':
                os.remove(os.path.join(settings.MEDIA_ROOT, currentProduct.image.name))
            currentProduct.image = request.FILES['image']
        currentProduct.save()
        return render(request, 'products/edit/editProduct.html', {"thisPage": 'editProduct', 'restaurant': restaurant, 'product': currentProduct, 'user': user, 'success': "Ürün başarıyla güncellendi.", 'categories': categories})
    else:
        return render(request, 'products/edit/editProduct.html', {"thisPage": 'editProduct', 'restaurant': restaurant, 'categories': categories, 'product': currentProduct, 'user': user })

def viewProductsAdmin(request):
    user = request.user
    products = Product.objects.all()
    if request.method == 'POST':
        if 'btnAddProduct' in request.POST:
            title = request.POST['title'].strip()
            description = request.POST['description'].strip()
            price = request.POST['price'].strip()
            buyingMassage = request.POST['buyingMassage'].strip()
            image = request.FILES['image']
            category_id = request.POST['category'].strip()                
            category = Category.objects.get(id=category_id)
            if not Product.objects.filter(title=title, description = description).exists():
                newProduct = Product.objects.create(title=title, description=description, price=price, category=category, sender_id=user.id, image=image, buyingMassage=buyingMassage)
                newProduct.save()
                return render(request, 'products/admin/viewProducts.html', {"thisPage": 'viewProductsAdmin', 'restaurant': restaurant, 'products': products, 'user': user, 'success': "Ürün başarıyla eklendi."})
            else:
                return render(request, 'products/admin/viewProducts.html', {"thisPage": 'viewProductsAdmin', 'restaurant': restaurant, 'products': products, 'user': user, 'error':  "Ürün zaten mevcut."})

    return render(request, 'products/admin/viewProducts.html', {"thisPage": 'viewProductsAdmin', 'restaurant': restaurant, 'products': products, 'user': user})


def deleteProduct(request, product_id):
    user = request.user
    products = Product.objects.all()
    if user.is_authenticated:
        currentProduct = Product.objects.get(id=product_id)
        if currentProduct.image != 'meal_def.jpg':
            os.remove(os.path.join(settings.MEDIA_ROOT, currentProduct.image.name))
        currentProduct.delete()
        return render(request, 'products/admin/viewProducts.html', 
                      {
                        "thisPage": 'viewProductsAdmin', 
                       'restaurant': restaurant, 
                       'products': products,
                       'user': user, 
                       'success': "Ürün başarıyla silindi."})
    else:
        return redirect('home')
    
def editHotdeal(request, hotdeal_id):
    user = request.user
    currentHotdeal = Hotdeals.objects.get(id=hotdeal_id)
    categories = Category.objects.filter(restaurant=restaurant)
    if request.method == 'POST':
        if 'btnUpdateHotdeal' in request.POST:
            currentHotdeal.title = request.POST['title'].strip()
            currentHotdeal.description = request.POST['description'].strip()
            currentHotdeal.oldPrice = request.POST['oldPrice'].strip()
            currentHotdeal.newPrice = request.POST['newPrice'].strip()
            currentHotdeal.category = Category.objects.get(id=request.POST['category'].strip())     
            currentHotdeal.end_time = request.POST['end_time'].strip()
            
            if 'image' in request.FILES:
                if currentHotdeal.image != 'hotDeal_def.jpg':
                    os.remove(os.path.join(settings.MEDIA_ROOT, currentHotdeal.image.name))
                currentHotdeal.image = request.FILES['image']
            currentHotdeal.save()
            return render(request, 'products/edit/editHotProduct.html', 
                          {
                           "thisPage": 'editHotdeal',
                           'categories': categories,
                           'restaurant': restaurant, 
                           'hotdeal': currentHotdeal, 
                           'user': user, 
                           'success': "Teklif başarıyla güncellendi."})
        if 'btnDeleteHotdeal' in request.POST:
            hotdeals = Hotdeals.objects.all()
            if currentHotdeal.image != 'hotDeal_def.jpg':
                os.remove(os.path.join(settings.MEDIA_ROOT, currentHotdeal.image.name))
            currentHotdeal.delete()
            return render(request, 'products/admin/viewHotdeals.html', 
                          {
                           "thisPage": 'viewHotdealsAdmin',
                           'categories': categories,
                           'restaurant': restaurant, 
                           'hotdeals': hotdeals, 
                           'user': user, 
                           'success': "Teklif başarıyla silindi."
                           })
    else:
        return render(request, 'products/edit/editHotProduct.html', 
                    {
                    "thisPage": 'editHotdeal',
                    'categories': categories, 
                    'restaurant': restaurant, 
                    'hotdeal': currentHotdeal, 
                    'user': user})
    
def viewHotdeal(request, hotdeal_id):
    user = request.user
    categories = Category.objects.filter(restaurant=restaurant)
    currentHotdeal = Hotdeals.objects.get(id=hotdeal_id)
    return render(request, 'products/view/viewHotdeal.html', 
                  {
                    "thisPage": 'viewHotdeal', 
                    'restaurant': restaurant,
                    'categories': categories, 
                    'hotdeal': currentHotdeal, 
                    'user': user})

def viewHotdealsAdmin(request):
    user = request.user
    hotdeals = Hotdeals.objects.all()
    categories = Category.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        if 'btnAddHotdeal' in request.POST:
            title = request.POST['title'].strip()
            description = request.POST['description'].strip()
            oldPrice = request.POST['oldPrice'].strip()
            newPrice = request.POST['newPrice'].strip()
            buyingMassage = request.POST['buyingMassage'].strip()
            category_id = request.POST['category'].strip()
            category = Category.objects.get(id=category_id)

            end_time_str = request.POST['end_time'].strip()
            end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
            image = request.FILES['image']
            
            
            if not Hotdeals.objects.filter(title=title, description = description).exists():
                newHotdeal = Hotdeals.objects.create(title=title, description=description, oldPrice=oldPrice, newPrice=newPrice, category=category, sender_id=user.id, end_time=end_time, image=image, buyingMassage=buyingMassage)
                newHotdeal.save()
                return render(request, 'products/admin/viewHotdeals.html', 
                          {
                            "thisPage": 'viewHotdealsAdmin', 
                            'restaurant': restaurant, 
                            'hotdeals': hotdeals, 
                            'user': user,
                            'categories': categories, 
                            'success': "Teklif başarıyla eklendi."})
            else:
                return render(request, 'products/admin/viewHotdeals.html', 
                          {
                            "thisPage": 'viewHotdealsAdmin', 
                            'restaurant': restaurant, 
                            'hotdeals': hotdeals, 
                            'user': user,
                            'categories': categories, 
                            'error': "Teklif zaten mevcut."})

    return render(request, 'products/admin/viewHotdeals.html', 
                  {
                   "thisPage": 'viewHotdealsAdmin', 
                   'restaurant': restaurant, 
                   'hotdeals': hotdeals, 
                   'user': user,
                   'categories': categories
                   }
    )

def deleteHotdeal(request, hotdeal_id):
    user = request.user
    categories = Category.objects.filter(restaurant=restaurant)

    hotdeals = Hotdeals.objects.all()
    if user.is_authenticated:
        try:
            currentHotdeal = Hotdeals.objects.get(id=hotdeal_id)
            if currentHotdeal.image != 'hotDeal_def.jpg':
                os.remove(os.path.join(settings.MEDIA_ROOT, currentHotdeal.image.name))
            currentHotdeal.delete()
            return render(request,'products/admin/viewHotdeals.html',
                {
                    "thisPage": 'viewHotdealsAdmin',
                    'restaurant': restaurant,
                    'categories': categories,
                    'hotdeals': hotdeals,
                    'user': user,
                    'success': "Teklif başarıyla silindi."
                }
            )
        except Hotdeals.DoesNotExist:return render(request,'products/admin/viewHotdeals.html',
            {
                    "thisPage": 'viewHotdealsAdmin',
                    'restaurant': restaurant,
                    'categories': categories,
                    'hotdeals': hotdeals,
                    'user': user,
                    'error': "Teklif bulunamadı."}
            )
    else:
        return redirect('home')


def viewHotdealAdmin(request, hotdeal_id):
    user = request.user
    categories = Category.objects.filter(restaurant=restaurant)
    currentHotdeal = Hotdeals.objects.get(id=hotdeal_id)
    return render(request, 'products/view/viewHotdealAdmin.html', 
                  {
                    "thisPage": 'viewHotdealAdmin', 
                    'restaurant': restaurant,
                    'categories': categories, 
                    'hotdeal': currentHotdeal, 
                    'user': user})





def search(request):
    query = request.GET.get('q')
    selected_category_id = request.GET.get('category', '')
    selected_category_name = ""

    product_results = Product.objects.none()
    hotdeal_results = Hotdeals.objects.none()

    if selected_category_id == '-1':  # Check if selected_category_id equals -1
        product_results = Product.objects.all()
        hotdeal_results = Hotdeals.objects.all()
    elif selected_category_id:  # Check for category selection only
        try:
            selected_category = Category.objects.get(id=selected_category_id)
            selected_category_name = selected_category.name
            product_results = Product.objects.filter(category=selected_category)
            hotdeal_results = Hotdeals.objects.filter(category=selected_category)
        except Category.DoesNotExist:
            pass

    # If there is a query and category, filter by both. Otherwise, filter by category or query alone.
    if query and selected_category_id:
        product_results = product_results.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        hotdeal_results = hotdeal_results.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    elif query:
        product_results = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        hotdeal_results = Hotdeals.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'pages/search.html', {
        'query': query,
        'product_results': product_results,
        'hotdeal_results': hotdeal_results,
        'restaurant': restaurant,
        'selected_category': selected_category_id, 
        'selected_category_name': selected_category_name,
        'lastSearch': query,
        
    })



def all(request):
    user = request.user
    products = Product.objects.all()
    hotdeals = Hotdeals.objects.all()
    categories = Category.objects.filter(restaurant=restaurant)
    return render(request, 'pages/all.html', {"thisPage": 'all', 'restaurant': restaurant, 'products': products, 'hotdeals': hotdeals, 'user': user, 'categories': categories})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import City, Category, Service, Master, GalleryPicture, Review
from core.forms import MasterRegistrationForm, ReviewForm
from django.db.models import Count


def index(request):
    return render(request, 'index.html')

def cities(request):
    cities = City.objects.all()
    return render(request, 'cities.html', {'cities': cities})

def category(request, city_id):
    city = City.objects.get(pk=city_id)
    categories = Category.objects.filter(city=city).annotate(num_masters=Count('service__master')).filter(num_masters__gt=0)
    return render(request, 'category.html', {'city': city, 'categories': categories})

def service(request, city_id, category_id):
    city = City.objects.get(pk=city_id)
    category = Category.objects.get(pk=category_id)
    filtered_services = Service.objects.filter(city=city, category=category).annotate(num_masters=Count('master')).filter(num_masters__gt=0)
    return render(request, 'service.html', {'city': city, 'category': category, 'services': filtered_services})

def register_master(request):
    gallery = request.FILES.getlist('gallery')
    if request.method == 'POST':
        form = MasterRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            master = form.save(commit=False)  # Создаем экземпляр мастера, но не сохраняем его в базу данных
            master.is_moderated = False  # Устанавливаем флаг модерации в значение False
            master.save()  # Сохраняем экземпляр мастера в базе данных
            if gallery:  # Проверяем файлы
                for i in gallery:
                    GalleryPicture.objects.create(master=master, image=i)
            return redirect('registered') # return redirect('profile_url', master_id=master.id) если редирект на профиль сразу
    else:
        form = MasterRegistrationForm()

    # Логика для получения списка городов, категорий и услуг
    cities = City.objects.all()
    categories = Category.objects.all()
    services = Service.objects.all()
    data ={
        'form': form,
        'cities': cities,
        'categories': categories,
        'services': services,
        }

    return render(request, 'registration.html', data)

def registered(request):
    return render(request, 'registered.html')

def get_categories_and_services(request):
    city_id = request.GET.get('city_id')
    category_id = request.GET.get('category_id')

    categories = Category.objects.filter(city_id=city_id)
    services = Service.objects.filter(city_id=city_id, category_id=category_id)  # фильтруем услуги по городу и категории
    
    categories_data = [{'id': category.id, 'name': category.name} for category in categories]
    services_data = [{'id': service.id, 'name': service.name} for service in services]

    data = {
        'categories': categories_data,
        'services': services_data,
    }

    return JsonResponse(data)

def profile_view(request, master_id):
    master = Master.objects.get(pk=master_id)
    if master.is_moderated:  # Проверяем, модерирован ли профиль
        return render(request, 'profile.html', {'master': master})  # Передаем профиль для отображения
    else:
        return HttpResponse('Профиль находится на модерации')  # Иначе выводим сообщение об отсутствии доступа

def master_profile(request, master_id):
    if Master.objects.filter(pk=master_id).exists():
        master = Master.objects.get(pk=master_id)
        if master:
            images = GalleryPicture.objects.filter(master_id=master.id)
        else:
            images = None

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                author = form.cleaned_data['author']
                email = form.cleaned_data['email']
                content = form.cleaned_data['content']
                rating = form.cleaned_data['rating']

                review = Review(author=author, email=email, content=content, rating=rating, master=master)
                review.save()

                return redirect('profile_url', master_id=master.id)
        else:
            form = ReviewForm()

        data = {
            'master': master,
            'images': images,
            'form': form
        }
        return render(request, 'profile.html', data)
    else:
        data = {
            'msg': 'Такого мастера нет'
        }
        return render(request, 'error.html', data)
    

def masters_for_service(request, city_id, category_id, service_id):
    city = City.objects.get(pk=city_id)
    category = Category.objects.get(pk=category_id)
    service = Service.objects.get(pk=service_id)
    masters = Master.objects.filter(city=city, category=category, service=service)
    return render(request, 'masters_for_service.html', {'city': city, 'category': category, 'service': service, 'masters': masters})

def all(request):
    masters_list = Master.objects.all()  
    return render(request, 'all.html', {'masters': masters_list})

def online(request):
    return render(request, 'online.html') 

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def editprofile(request):
    return render(request, 'editprofile.html')

def error(request):
    return render(request, 'error.html')

def help(request):
    return render(request, 'help.html')

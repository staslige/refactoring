from django.db import models
from django.views import View
from django.http import JsonResponse
from django.core.validators import MaxValueValidator, MinValueValidator

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def is_invisible(self):
        invisible_cities = [44]  # id города, который нужно скрыть из списка
        return self.id in invisible_cities

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Города"
        ordering = ['name']
        

class Category(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Категории услуг"
        ordering = ['name']
        

class Service(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Услуги"
        ordering = ['name']


class Master(models.Model):
    email = models.EmailField(unique=True, verbose_name='Почта', null=True, blank=False)
    password = models.CharField(max_length=100, verbose_name='Пароль', blank=False)
    name = models.CharField(max_length=100, verbose_name='Имя', blank=False)
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, verbose_name='Услуга')
    service_name = models.CharField(max_length=255, verbose_name='Название услуги', null=False, blank=False) 
    pricemin = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Цена от', null=True, blank=False)
    pricemax = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Цена до', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True) 
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=False) 
    whatsapp = models.CharField(max_length=20, verbose_name='WhatsApp', null=True, blank=True) 
    instagram = models.CharField(max_length=100, verbose_name='Instagram', null=True, blank=True)
    languages = models.CharField(max_length=100, verbose_name='Языки помимо русского', null=True, blank=True)
    about = models.TextField(blank=False)
    photo = models.ImageField(upload_to='media/masters', verbose_name='Фото', blank=False) 
    gallery = models.ImageField(upload_to='media/gallery', verbose_name='Фото ваших работ', null=True, blank=True) # Поле изменить на multi pics
    is_moderated = models.BooleanField(default=False, verbose_name='Модерация')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Мастера"
    
    @property
    def average_rating(self):
        total_rating = sum(review.rating for review in self.reviews.all())
        review_count = self.reviews.count()
        if review_count > 0:
            return total_rating / review_count
        else:
            return 0

    
class GetServicesView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category')
        city_id = request.GET.get('city')
        services = Service.objects.filter(category__id=category_id, city__id=city_id)
        services_data = [{'id': service.id, 'name': service.name} for service in services]
        return JsonResponse(services_data, safe=False)
    
    
class GalleryPicture(models.Model):
    image = models.ImageField(upload_to='profisrael/media/gallery/')
    master = models.ForeignKey("Master", verbose_name="Master", on_delete=models.CASCADE, default=None, null=True)
    
    def __str__(self):
         return self.image.url
        
    
class Review(models.Model):
    master = models.ForeignKey('Master', on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=30)
    email = models.EmailField(unique=True, verbose_name='Почта', null=True, blank=False)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Review for {self.master.name} by {self.author}"      
      
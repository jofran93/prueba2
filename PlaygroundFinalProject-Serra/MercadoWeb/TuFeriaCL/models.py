from django.db import models
from django.contrib.auth.models import User
import bcrypt

#Clase del Usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.jpg', blank=True, null=True)
    
    # Campo adicional para almacenar la contraseña de manera segura
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username

    def set_password(self, raw_password):
        # Función para establecer la contraseña utilizando bcrypt
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, raw_password):
        # Función para verificar la contraseña utilizando bcrypt
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
#Clase del Producto
class Item(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='item_photos/')
    quantity_available = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
#Clase de la publicacion
class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='available')
    
    def post_image(self):
        return self.item.photo  # Accede a la imagen del Item
    
    def __str__(self):
        return f"{self.user.full_name} - {self.item.name}"
    
    
#Clase de la compra
class Purchase(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.item.name} - {self.purchase_date}"

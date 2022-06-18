from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.

COUNTIES = [
    ('', ('Choose')), 
    ('Baringo', ('Baringo')),
    ('Bomet', ('Bomet')),
    ('Bungoma ', ('Bungoma ')),
    ('Busia', ('Busia')),
    ('Elgeyo Marakwet', ('Elgeyo Marakwet')),
    ('Embu', ('Embu')),
    ('Garissa', ('Garissa')),
    ('Homa Bay', ('Homa Bay')),
    ('Isiolo', ('Isiolo')),
    ('Kajiado', ('Kajiado')),
    ('Kakamega', ('Kakamega')),
    ('Kericho', ('Kericho')),
    ('Kiambu', ('Kiambu')),
    ('Kilifi', ('Kilifi')),
    ('Kirinyaga', ('Kirinyaga')),
    ('Kisii', ('Kisii')),
    ('Kisumu', ('Kisumu')),
    ('Kitui', ('Kitui')),
    ('Kwale', ('Kwale')),
    ('Laikipia', ('Laikipia')),
    ('Lamu', ('Lamu')),
    ('Machakos', ('Machakos')),
    ('Makueni', ('Makueni')),
    ('Mandera', ('Mandera')),
    ('Meru', ('Meru')),
    ('Migori', ('Migori')),
    ('Marsabit', ('Marsabit')),
    ('Mombasa', ('Mombasa')),
    ('Muranga', ('Muranga')),
    ('Nairobi', ('Nairobi')),
    ('Nakuru', ('Nakuru')),
    ('Nandi', ('Nandi')),
    ('Narok', ('Narok')),
    ('Nyamira', ('Nyamira')),
    ('Nyandarua', ('Nyandarua')),
    ('Nyeri', ('Nyeri')),
    ('Samburu', ('Samburu')),
    ('Siaya', ('Siaya')),
    ('Taita Taveta', ('Taita Taveta')),
    ('Tana River', ('Tana River')),
    ('Tharaka Nithi', ('Tharaka Nithi')),
    ('Trans Nzoia', ('Trans Nzoia')),
    ('Turkana', ('Turkana')),
    ('Uasin Gishu', ('Uasin Gishu')),
    ('Vihiga', ('Vihiga')),
    ('Wajir', ('Wajir')),
    ('West Pokot', ('West Pokot')),
]



class Hood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    county = models.CharField(choices=COUNTIES, max_length=50)
    description = models.TextField(max_length=500)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', default='https://res.cloudinary.com/dz275mqsc/image/upload/v1654858776/default_nbsolf.png')
    police_department = models.CharField(max_length=25, null=True)
    health_department = models.CharField(max_length=25, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_hoods(self):
        hoods = Hood.objects.all()
        return hoods
    
    def create_hood(self):
        self.save()

    def delete_hood(self):
        self.delete()

    def find_hood(self,hood_id):
        hood = Hood.objects.filter(self = hood_id)
        return hood

    def update_hood(self, id, name, location, county, image):
        update = Hood.objects.filter(id = id).update(name = name , location = location, county = county, image = image)
        return update

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Hoods'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True)
    national_id = models.CharField(max_length=10, null=True)
    profile_pic = CloudinaryField('profile_pic', default='https://res.cloudinary.com/dz275mqsc/image/upload/v1654858776/default_nbsolf.png')
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = 'Profiles'

class Business(models.Model):
    name = models.CharField(max_length=80, null=True, verbose_name='Business Name')
    description = models.TextField(max_length=500, null=True)
    email = models.CharField(max_length=150, null=True, verbose_name='Business Email Address')
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, verbose_name='Business Phone Number')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Business Owner')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_businesses(self):
        businesses = Business.objects.all()
        return businesses

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    def find_business(self,business_id):
        business = Business.objects.filter(self = business_id)
        return business

    def update_business(self, id, name, description, email, hood):
        update = Hood.objects.filter(id = id).update(name = name , description = description, email = email, hood = hood)
        return update
    

    class Meta:
        verbose_name_plural = 'Businesses'




    

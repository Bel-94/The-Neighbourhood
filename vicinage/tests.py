from django.test import TestCase
from .models import Hood, Profile, Business, Post
from django.contrib.auth.models import User


user = User.objects.get(id=1)
profile = Profile.objects.get(id=1)

# Create your tests here.
class HoodTestClass(TestCase):
    def setUp(self):
        self.newhood=Hood(name='ClayCity', location='Kasarani', county='Nairobi', image='default.png', admin='user')
        self.newhood.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.newhood,Hood))

    def test_save_image(self):
        new_hood=self.new_hood
        new_hood.create_hood()
        posts=Hood.get_hoods()
        self.assertTrue(len(posts)>0)

    def update_image(self):
        new_hood=self.new_hood
        new_hood.update_hood()
        posts=Hood.get_hoods()
        self.assertTrue(len(posts)==0)

    def test_delete_image(self):
        new_hood=self.new_hood
        new_hood.delete_hood()
        posts=Hood.get_hoods()
        self.assertTrue(len(posts)==0)


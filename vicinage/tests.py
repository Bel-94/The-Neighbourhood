from django.test import TestCase
from .models import Hood, Profile, Business
from django.contrib.auth.models import User


user = User.objects.get(id=1)
profile = Profile.objects.get(id=1)

# Create your tests here.
class HoodTestClass(TestCase):
    def setUp(self):
        self.new_hood=Hood(name='ClayCity', location='Kasarani', county='Nairobi', image='default.png', admin='user')
        self.new_hood.save()

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


class TestBusiness(TestCase):
    def setUp(self):
        self.new_business=Business(bs_name = "", description="", bs_email='', owner=profile)
        self.new_business.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_business,Business))

    def test_save_image(self):
        new_biz=self.new_business
        new_biz.create_business()
        posts=Business.get_businesses()
        self.assertTrue(len(posts)>0)

    def update_image(self):
        new_biz=self.new_business
        new_biz.update_business()
        posts=Business.get_businesses()
        self.assertTrue(len(posts)==0)

    def test_delete_image(self):
        new_biz=self.new_business
        new_biz.delete_business()
        posts=Business.get_businesses()
        self.assertTrue(len(posts)==0)






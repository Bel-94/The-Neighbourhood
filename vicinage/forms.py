from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Business, Hood, Membership, Post

COUNTIES = [
    ('Choose County', ('Choose County')), 
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

CATEGORIES = [
    ('1', 'Crimes and Safety'),
    ('2', 'Health Emergency'),
    ('3', 'Recommendations'),
    ('4', 'Fire Breakouts'),
    ('5', 'Lost and Found'),
    ('6', 'Death'),
    ('7', 'Event'),
]

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-4'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'readonly':'readonly'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']



class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify', 'data-height':420, 'data-max-file-size':"1M"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 5, 'placeholder':'Keep it short, preferably in one concise sentence'}))
    national_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder':'National ID'}))
    hood = forms.ChoiceField(label=u'Select Your Hood', required=True, widget=forms.Select(attrs={'class': 'form-control mb-4'}))

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['hood'].choices = [(e.id, e.name) for e in Hood.objects.all()]
    
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'national_id', 'hood']


class AddBussinessForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Business Name','class': 'form-control mb-4'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Business Description','class': 'form-control mb-4','rows': 5,}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Business Email','class': 'form-control mb-4'}))
    hood = forms.ChoiceField(required=True, widget=forms.Select(attrs={'placeholder': 'Neighbourhood','class': 'form-control mb-4'}))

    def __init__(self, *args, **kwargs):
        super(AddBussinessForm, self).__init__(*args, **kwargs)
        self.fields['hood'].choices = [(e.id, e.name) for e in Hood.objects.all()]

class AddHoodForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Title','class': 'form-control mb-4'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control mb-4','rows': 3,}))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Location','class': 'form-control mb-4'}))
    county = forms.ChoiceField(required=True, widget=forms.Select( attrs={'class': 'form-control mb-4'}), choices=COUNTIES)
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'dropify', 'data-height':300, 'data-max-file-size':"1M"}))
    health_department = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Health Department','class': 'form-control mb-4'}))
    police_department = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Police Department','class': 'form-control mb-4'}))

    class Meta:
        model = Hood
        fields = ('name','description','location','county','image','health_department','police_department')

class AddPostForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder':'Post Title'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 5, 'placeholder':'Description'}))
    category = forms.ChoiceField(choices=CATEGORIES, required=True, widget=forms.Select(attrs={'class': 'form-control mb-4', 'placeholder':'Select Category'}))
    neighbourhood = forms.ChoiceField(label=u'Select Your Neighbourhood', required=True, widget=forms.Select(attrs={'class': 'form-control mb-4'}))

    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['hood'].choices = [(e.id, e.name) for e in Hood.objects.all()]


# class RegistrationForm(UserCreationForm):
#     email=forms.EmailField()
#     class Meta:
#         model = User
#         fields = ['username', 'email','password1', 'password2']

#     def save(self, commit=True):
#         user=super().save(commit=False)
#         user.email=self.cleaned_data['email']
#         if commit:

#             user.save()
#         return user


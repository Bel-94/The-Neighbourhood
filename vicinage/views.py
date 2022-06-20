from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Business, Hood, Membership, Post
from django.contrib.auth.models import User
from .forms import AddBussinessForm, AddHoodForm, AddPostForm,  UpdateProfileForm, UpdateUserForm
from Hood import settings
from django.contrib import messages

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import threading

# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Vicinage Account'
    email_body = render_to_string('Account Activation Email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
    from_email=settings.EMAIL_FROM_USER, to=[user.email])

    if not settings.TESTING:
        EmailThread(email).start()

def Register(request):
    if request.method == 'POST':
        context = {'has_error': False}
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, '⚠️ Passwords Do Not Match! Try Again')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username Already Exists! Choose Another One')
            return redirect('Register')

        if User.objects.filter(email=email).exists():
            messages.error(request, '⚠️ Email Address Already Exists! Choose Another One')
            return redirect('Register')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.is_active = False
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)
            messages.success(request, '✅ Regristration Successful! An Activation Link Has Been Sent To Your Email')
            return redirect('Register')

    return render(request, 'registration/register.html')

def ActivateAccount(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        messages.success(request, ('✅ Email Verified! You can now Log in'))
        return redirect('Login')
    else:
        messages.error(request, ('⚠️ The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('Login')
    
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if not User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username Does Not Exist! Choose Another One')
            return redirect('Login')

        if user is None:
            messages.error(request, '⚠️ Username/Password Is Incorrect or Account Is Not Activated!! Please Try Again')
            return redirect('Login')

        if user is not None:
            login(request, user)
            return redirect('Index')
        
    return render(request, 'registration/login.html')

@login_required(login_url='Login')
def Logout(request):
    logout(request)
    return redirect('Index')

# function for creating the landing page
def Index(request):
    hoods = Hood.objects.all()
    return render(request, 'main/index.html', {'hoods': hoods})

# function for creating user profile
def MyProfile(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    return render(request, 'main/profile.html', {'profile':profile, 'profile_details':profile_details})

# function for edditing user profile
def EditProfile(request, username):
    user = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = user.id)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_picture = profile_form.cleaned_data['profile_pic']
            neighbourhood = profile_form.cleaned_data['hood']
            bio = profile_form.cleaned_data['bio']
            national_id = profile_form.cleaned_data['national_id']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            username = user_form.cleaned_data['username']
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            profile_details.national_id = national_id
            profile_details.bio = bio
            profile_details.profile_pic = profile_picture
            profile_details.hood = Hood.objects.get(pk=int(neighbourhood))

            neighbourhood_obj = Hood.objects.get(pk=int(neighbourhood))
            member = Membership.objects.filter(user = profile_details.id, neighbourhood_membership = neighbourhood_obj.id)

            if not member:
                messages.error(request, "⚠️ You Need To Be A Member of The Selected Hood First!")
                return redirect('EditProfile', username=username)
            else:   
                user.save()
                profile_details.save()
                messages.success(request, '✅ Your Profile Has Been Updated Successfully!')
                return redirect('EditProfile', username=username)
        else:
            messages.error(request, "⚠️ Your Profile Wasn't Updated!")
            return redirect('EditProfile', username=username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'main/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form, 'profile_details':profile_details})

# function for adding a business
def AddBusiness(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    form = AddBussinessForm()
    if request.method == "POST":
        form = AddBussinessForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            neighbourhood = form.cleaned_data['hood']
            description = form.cleaned_data['description']

            neighbourhood_obj = Hood.objects.get(pk=int(neighbourhood))
            member = Membership.objects.filter(user = profile.id, neighbourhood_membership = neighbourhood_obj.id)

            if not member:
                messages.error(request, "⚠️ You Need To Be A Member of The Selected Neighbourhood First!")
                return redirect('AddBusiness', username=username)

            else:
                neighbourhood_obj = Hood.objects.get(pk=int(neighbourhood))
                new_business = Business(name = name, email = email, neighbourhood = neighbourhood_obj, description = description, owner = request.user.profile)
                new_business.save()

                messages.success(request, '✅ A Business Was Created Successfully!')
                return redirect('MyBusinesses', username=username)
        else:
            messages.error(request, "⚠️ A Business Wasn't Created!")
            return redirect('AddBusiness')
    else:
        form = AddBussinessForm()
    return render(request, 'main/add_business.html', {'form':form})


# function for creating a user business
def MyBusinesses(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    businesses = Business.objects.filter(owner = profile.id).all()
    return render(request, 'main/my_business.html', {'businesses':businesses, 'profile_details':profile_details})

# function for adding a hood
def AddHood(request):
    # profile = User.objects.get(username=username)
    # profile_details = Profile.objects.get(user = profile.id)

    current_user = request.user
    hoods = Hood.objects.all()
    
    if request.method == 'POST':
        form = AddHoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.admin = current_user
            neighbourhood.save()
            messages.success(request, '✅ A Hood Was Created Successfully!')
            return redirect('/')
        else:
            messages.error(request, "⚠️ A Hood Wasn't Created!")
            return redirect('AddHood')
    else:
        form = AddHoodForm()
    return render(request, 'main/add_hood.html', {'form':form, 'hoods':hoods})


# function for adding user to a hood
def Myhoods(request):
    # profile = User.objects.get(username=username)
    # profile_details = Profile.objects.get(user = profile.id)
    # neighbourhoods = Hood.objects.filter(admin = profile.id).all()
    # for neighbourhood in neighbourhoods:
    #     print(neighbourhood.name)
    #     print(neighbourhood.description)
    hoods = Hood.objects.all().order_by('-id')

    return render(request, 'main/my_hoods.html', {'hoods':hoods})

# function for creating a post
def MyPosts(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    posts = Post.objects.filter(author = profile.id).all()
    return render(request, 'main/my_posts.html', {'posts':posts, 'profile_details':profile_details})

# function for adding a post
def AddPost(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user.id)

    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            neighbourhood = form.cleaned_data['neighbourhood']
            category = form.cleaned_data['category']

            neighbourhood_obj = Hood.objects.get(pk=int(neighbourhood))
            member = Membership.objects.filter(user = profile.id, neighbourhood_membership = neighbourhood_obj.id)

            if not member:
                messages.error(request, "⚠️ You Need To Be A Member of The Selected Neighbourhood First!")
                return redirect('AddPost', username=username)

            else:
                neighbourhood_obj = Hood.objects.get(pk=int(neighbourhood))
                new_post = Post(title = title, category = category, neighbourhood = neighbourhood_obj, description = description, author = request.user.profile)
                new_post.save()

                messages.success(request, '✅ Your Post Was Created Successfully!')
                return redirect('MyPosts', username=username)
        else:
            messages.error(request, "⚠️ Your Post Wasn't Created!")
            return redirect('AddPost', username=username)
    else:
        form = AddPostForm()
    return render(request, 'main/add_post.html', {'form':form})


# function for searching a business
def Search(request):
    if request.method == 'POST':
        search = request.POST['BusinessSearch']
        print(search)
        businesses = Business.objects.filter(name__icontains = search).all()
        return render(request, 'main/search.html', {'search':search, 'businesses':businesses})
    else:
        return render(request, 'main/search.html')


# function for a singlehood
def SingleHood(request, name):
    # current_profile = request.user.profile
    current_user = request.user
    neighbourhood = get_object_or_404(Hood, name=name)
    businesses = Business.objects.filter(hood = neighbourhood.id).all()
    posts = Post.objects.filter(hood = neighbourhood.id).all()
    members = Membership.objects.filter(hood_membership=neighbourhood.id).all()
    member = Membership.objects.filter(user = current_user.id, hood_membership = neighbourhood.id)
    is_member = False
    if member:
        is_member = True
    else:
        is_member = False
    return render(request, 'main/hood.html', {'neighbourhood': neighbourhood, 'businesses':businesses, 'posts':posts, 'is_member':is_member, 'members':members})


# function for joining a hood
def JoinHood(request, name):
    neighbourhoodTobejoined = Hood.objects.get(name=name)
    currentUserProfile = request.user.profile

    if not neighbourhoodTobejoined:
        messages.error(request, "⚠️ Hood Does Not Exist!")
        return redirect('Index')
    else:
        member_elsewhere = Membership.objects.filter(user = currentUserProfile)
        joined = Membership.objects.filter(user = currentUserProfile, neighbourhood_membership = neighbourhoodTobejoined)
        if joined:
            messages.error(request, '⚠️ You Can Only Join A Hood Once!')
            return redirect('SingleHood', name=name)
        elif member_elsewhere:
            messages.error(request, '⚠️ You Are Already A Member In Another Hood! Leave To Join This One')
            return redirect('SingleHood', name=name)
        else:
            neighbourhoodToadd = Membership(user = currentUserProfile, neighbourhood_membership = neighbourhoodTobejoined)
            neighbourhoodToadd.save()
            messages.success(request, "✅ You Are Now A Member Of This NeighbourHood!")
            return redirect('SingleHood', name=name)


# function for leaving a hood
def LeaveHood(request, name):
    neighbourhoodToLeave = Hood.objects.get(name=name)
    currentUserProfile = request.user.profile

    if not neighbourhoodToLeave:
        messages.error(request, "⚠️ Hood Does Not Exist!")
        return redirect('Index')
    else:
        membership = Membership.objects.filter(user = currentUserProfile, neighbourhood_membership = neighbourhoodToLeave)
        if membership:
            membership.delete()
            messages.success(request, "✅ You Have Left This Hood!")
            return redirect('SingleHood', name=name)



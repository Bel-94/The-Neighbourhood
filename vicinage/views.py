from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Business, Hood, Membership, Post
from django.contrib.auth.models import User
from .forms import AddBussinessForm, AddHoodForm, AddPostForm,  UpdateProfileForm, UpdateUserForm
from Hood import settings
from django.contrib import messages

# Create your views here.


# function for the registration form
# def register(request):
#     if request.method=="POST":
#         form=RegistrationForm(request.POST)
#         procForm=profileForm(request.POST, request.FILES)
#         if form.is_valid() and procForm.is_valid():
#             username=form.cleaned_data.get('username')
#             user=form.save()
#             profile=procForm.save(commit=False)
#             profile.user=user
#             profile.save()

#             # messages.success(request, f'Successfully created Account!.You can now login as {username}!')
#         return redirect('login')
#     else:
#         form= RegistrationForm()
#         prof=profileForm()
#     params={
#         'form':form,
#         'profForm': prof
#     }
#     return render(request, 'registration/register.html', params)

# function for creating the landing page
def Index(request):
    hoods = Hood.objects.all()
    return render(request, 'main/index.html', {'hoods': hoods})

# function for creating user profile
def Profile(request, username):
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
            profile_details.profile_picture = profile_picture
            profile_details.neighbourHood = Hood.objects.get(pk=int(neighbourhood))

            neighbourhood_obj = Hood.objects.get(pk=int(neighbourhood))
            member = Membership.objects.filter(user = profile_details.id, neighbourhood_membership = neighbourhood_obj.id)

            if not member:
                messages.error(request, "⚠️ You Need To Be A Member of The Selected Neighbourhood First!")
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
            neighbourhood = form.cleaned_data['neighbourhood']
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
def AddHood(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    if request.method == 'POST':
        form = AddHoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.neighbourhood_admin = request.user
            neighbourhood.save()
            messages.success(request, '✅ A Hood Was Created Successfully!')
            return redirect('Myhoods', username=username)
        else:
            messages.error(request, "⚠️ A Hood Wasn't Created!")
            return redirect('AddHood')
    else:
        form = AddHoodForm()
    return render(request, 'main/add_hood.html', {'form':form, 'profile_details':profile_details})


# function for adding user to a hood
def Myhoods(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    neighbourhoods = Hood.objects.filter(neighbourhood_admin = profile.id).all()
    for neighbourhood in neighbourhoods:
        print(neighbourhood.name)
        print(neighbourhood.description)
    return render(request, 'main/my_hoods.html', {'neighbourhoods':neighbourhoods, 'profile_details':profile_details})

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


# function for searching a post
def Search(request):
    if request.method == 'POST':
        search = request.POST['BusinessSearch']
        print(search)
        businesses = Business.objects.filter(name__icontains = search).all()
        return render(request, 'main/search.html', {'search':search, 'businesses':businesses})
    else:
        return render(request, 'main/search.html')


# function for a singlehood
def SingleNeighbourhood(request, name):
    current_profile = request.user.profile
    neighbourhood = get_object_or_404(Hood, name=name)
    businesses = Business.objects.filter(neighbourhood = neighbourhood.id).all()
    posts = Post.objects.filter(neighbourhood = neighbourhood.id).all()
    members = Membership.objects.filter(neighbourhood_membership=neighbourhood.id).all()
    member = Membership.objects.filter(user = current_profile.id, neighbourhood_membership = neighbourhood.id)
    is_member = False
    if member:
        is_member = True
    else:
        is_member = False
    return render(request, 'main/hood.html', {'neighbourhood': neighbourhood, 'businesses':businesses, 'posts':posts, 'is_member':is_member, 'members':members})


# function for joining a hood
def JoinNeighbourhood(request, name):
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
            return redirect('SingleNeighbourhood', name=name)
        elif member_elsewhere:
            messages.error(request, '⚠️ You Are Already A Member In Another Hood! Leave To Join This One')
            return redirect('SingleNeighbourhood', name=name)
        else:
            neighbourhoodToadd = Membership(user = currentUserProfile, neighbourhood_membership = neighbourhoodTobejoined)
            neighbourhoodToadd.save()
            messages.success(request, "✅ You Are Now A Member Of This NeighbourHood!")
            return redirect('SingleNeighbourhood', name=name)


# function for leaving a hood
def LeaveNeighbourhood(request, name):
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
            return redirect('SingleNeighbourhood', name=name)



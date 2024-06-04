from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.http import *

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = signup(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return redirect('personalized_home')
    else:
        form = signup()
    return render(request, 'signup.html', {'form': form})



#edit profile

@login_required(login_url='login')
def edit_profile(request): 
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})



# LOGIN 



def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('personalized_home')
    return render(request, 'login.html')



#LOGOUT 


def logout_(request):
    logout(request)
    return redirect('login')



# Update the home view to include posts and reload to show post updates



@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts,'form':form})


#personalized homepage
@login_required
def personalized_home(request):
    user = request.user
    profile = user.profile  # Access the user's profile

    # Filter posts based on profile attributes
    group_posts = Post.objects.filter(user__profile__groups__in=profile.groups.all())
    friend_posts = Post.objects.filter(user__profile__friends__in=profile.friends.all())
    community_posts = Post.objects.filter(user__profile__communities__in=profile.communities.all())
    college_posts = Post.objects.filter(user__profile__college=profile.college)
    university_posts = Post.objects.filter(user__profile__university=profile.university)
    course_posts = Post.objects.filter(user__profile__course=profile.course)
    following_posts = Post.objects.filter(user__profile__following__in=profile.following.all())

    # Combine the querysets (assuming no duplicates)
    posts = (group_posts | friend_posts | community_posts | college_posts |
             university_posts | course_posts | following_posts).distinct()

    context = {
        'posts': posts,
    }

    return render(request, 'phome.html', context)



#when user comments

def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        comment_text = request.POST.get('comment')
        Comment.objects.create(post=post, user=request.user, text=comment_text)
    return redirect('home')




#when user likes
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.no_of_likes -= 1
        user_has_liked = False
    else:
        post.likes.add(request.user)
        post.no_of_likes += 1
        user_has_liked = True
    post.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'post': {
                'no_of_likes': post.no_of_likes,
                'user_has_liked': user_has_liked,
            }
        })
    return redirect('home')




def explore(request):
    return render(request, 'explore.html')
def groups(request):
    return render(request, 'groups.html')




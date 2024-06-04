from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *
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
            return redirect('phome')
    else:
        form = signup()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('phome')
    return render(request, 'login.html')

def logout_(request):
    logout(request)
    return redirect('login')


@login_required
def phome(request):
    # Handle post creation
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('phome')
    else:
        form = PostForm()
    
    # Fetch personalized posts
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
        'form': form,
    }

    return render(request, 'phome.html', context)


def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        comment_text = request.POST.get('comment')
        Comment.objects.create(post=post, user=request.user, text=comment_text)
    return redirect('phome')

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
    return redirect('phome')
@user_passes_test(lambda u: u.is_superuser)
def delete_all_posts(request):
    if request.method == 'POST':
        Post.objects.all().delete()
        return redirect('phome')
    return redirect('phome')

def explore(request):
    return render(request, 'explore.html')

def groups(request):
    return render(request, 'groups.html')

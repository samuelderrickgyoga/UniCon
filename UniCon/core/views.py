from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import *
from .forms import *
from .models import *
from django.http import *
from django.views.decorators.csrf import *



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

def logout(request):
    auth_logout(request)
    return redirect('login')
# story views


def add_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('phome')
    else:
        form = StoryForm()
        context = {
            'stories': stories,
            'form': form
        }
    stories = Story.objects.all()
    return render (request, 'phome.html', context)
    

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
    user_profile_picture = user.profile.profile_picture.url #fetch user's profile picture 

    # Filter posts based on profile attributes and order by creation date descending
    group_posts = Post.objects.filter(user__profile__groups__in=profile.groups.all()).order_by('-created_at')
    friend_posts = Post.objects.filter(user__profile__friends__in=profile.friends.all()).order_by('-created_at')
    community_posts = Post.objects.filter(user__profile__communities__in=profile.communities.all()).order_by('-created_at')
    college_posts = Post.objects.filter(user__profile__college=profile.college).order_by('-created_at')
    university_posts = Post.objects.filter(user__profile__university=profile.university).order_by('-created_at')
    course_posts = Post.objects.filter(user__profile__course=profile.course).order_by('-created_at')
    following_posts = Post.objects.filter(user__profile__following__in=profile.following.all()).order_by('-created_at')

    # Combine the querysets (assuming no duplicates) and order by creation date descending
    posts = (group_posts | friend_posts | community_posts | college_posts |
             university_posts | course_posts | following_posts).distinct().order_by('-created_at')

    context = {
        'posts': posts,
        'form': form,
        'user_profile_picture': user_profile_picture,
    }

    return render(request, 'phome.html', context)





# comments views


def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        comment_text = request.POST.get('comment')
        comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
        return JsonResponse({
            'comment': {
                'user': comment.user.username,
                'text': comment.text,
            }
        })
    return HttpResponseRedirect('phome')

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


# super user deletse posts


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

# messages view
@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    messages_sent = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {'messages_received': messages_received, 'messages_sent': messages_sent})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})
@login_required
def get_messages(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    messages_sent = Message.objects.filter(sender=request.user).order_by('-timestamp')
    messages = list(messages_received.union(messages_sent))
    data = {
        'messages': [
            {'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp}
            for msg in messages
        ]
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        receiver = User.objects.get(id=request.POST['receiver'])
        content = request.POST['content']
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return JsonResponse({'status': 'success'})
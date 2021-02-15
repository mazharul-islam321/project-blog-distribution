from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post
from marketing.models import Signup
from .form import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_categorie_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest
    } 
    return render(request, 'index.html', context)
    

def blog(request):
    categorie_count = get_categorie_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 1)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
     
    context = {
        'queryset' : paginated_queryset,
        'most_recent' : most_recent,
        'page_request_var' : page_request_var,
        'categorie_count' : categorie_count
    }
    return render(request, 'blog.html', context) 

def post(request, id):
    categorie_count = get_categorie_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))

    context = {
        'form': form,
        'post': post,
        'most_recent' : most_recent,
        'categorie_count' : categorie_count
    }
    return render(request, 'post.html', context)

   
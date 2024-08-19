from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm


def post_list(request, tag_slug=None):
    posts = Post.objects.all().order_by('-published')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page,
                                                   'tag': tag})


# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post/detail.html', {'post': post})

def post_detail(request, year, month, day, slug_post):
    post = get_object_or_404(Post, slug=slug_post, status='published',
                             published__year=year,
                             published__month=month,
                             published__day=day)

    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'post': post,
               'comments': comments,
               'comment_form': comment_form}

    return render(request, 'blog/post/detail.html', context=context)

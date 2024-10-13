from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from blog.models import Post

from django.views.decorators.http import require_POST

from django.core.mail import send_mail

from django.views.generic import ListView

from blog.forms import CommentForm, EmailPostForm

def post_list(request):
    post_list = Post.published.all()
    
    paginator = Paginator(post_list, 3) 
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
            request,
            'blog/post/list.html',
            { 'posts': posts }
            )


class PostListView(ListView):
    
    queryset = Post.published.all()
    # default is 'object_list', so for iterating throught posts,
    # it would be {% for post in object_list %}
    context_object_name = 'posts'
    paginate_by = 3 
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    
    # Shortcut:
    post = get_object_or_404(
            Post,
            status=Post.Status.PULBISHED,
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=post,
            )
    # Explicit alternative: 
     #try:
     #    post = Post.published.get(id=id)
     #except Post.DoesNotExist:
     #    raise Http404("No Post Found")

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(
            request,
            'blog/post/detail.html',
            { 
             'post': post,
             'comments': comments,
             'form': form
             }
            )



def post_share(request, post_id):
    post = get_object_or_404(
            Post,
            id=post_id,
            status=Post.Status.PULBISHED
            )
    
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            post_url = request.build_absolute_uri(
                    post.get_absolute_url()
                    )
            subject = (
                    f"{cd['name']} ({cd['email']})"
                    f"recommends you read {post.title}"
                    )
            message = (
                    f"Read  {post.title} at {post_url}\n\n"
                    f"{cd['name']}\'s comments: {cd['comments']}"
                    )

            send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[cd['to']]
                    )
            sent = True

    else:
        form = EmailPostForm()
    
    return render(
            request,
            'blog/post/share.html',
            {
                'post': post,
                'form': form,
                'sent': sent
            }
        )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
            Post,
            id=post_id,
            status=Post.Status.PULBISHED
            )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        print(f"Form is valid!")
        comment = form.save(commit=False)
        comment.post = post
        print("Saving comment...")
        comment.save()
        print("Comment saved!")

        return render(
            request,
            'blog/post/comment.html',
            {
                'post': post,
                'form': form,
                'comment': comment
            }
        )
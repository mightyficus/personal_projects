from django.shortcuts import render, get_object_or_404
from .models import Post

# Takes the request object (parameter required by all views)
# Retrieve all the posts with the published status using our custom manager
def post_list(request):
    posts = Post.published.all()
    # Shortcut to render the list of posts with the given template
    # Takes the request object, the template path, and the context
    # variables to render the provided template
    # Returns a HttpResponse object with rendered text
    # render() shortcut takes the request context into account, so any 
    # variable set by the template context processors is accessible by the given template
    return render(request, 
                  'blog/post/list.html', 
                  {'posts': posts})

# Post detail view. Uses year, month, day, and post parameters to
# retrieve a published post with the given slug and date. Note that the slug field for the 
# Post model was given the unique_for_date parameter. This way, we ensure that there will 
# be only one post with a slug for the given date, and thus we can retrieve single posts 
# using the date and slug.
def post_detail(request, year, month, day, post):
    # We use the get_object_or_404 shortcut to retrieve the desired post. If the query doesn't 
    # return a post, it'll return a 404 error
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    return render(request,
                    'blog/post/detail.html',
                    {'post': post})
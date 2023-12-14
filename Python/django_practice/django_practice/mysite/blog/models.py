from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Custom model manager
class PublishedManager(models.Manager):
    # Only returns posts that have been published
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    # Title of the post. CharField translates to a VARCHAR column in SQL
    title = models.CharField(max_length=250)

    # Intended to be used in URLs. It's a short label that only contains letters, numbers,
    # underscores, and hyphens. The slug field can create SEO-friendly URLS for blog posts.
    # The unique_for_date parameter uses the publish date and `slug`
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # Acts as a foreign key defining a one-to-many relationship. 
    # Tells Django that each user can have many posts
    # Django will create a foreign key for that user using the User database
    # on_delete tells Django how to act when the user is deleted - CASCADE means that if a 
    #   user is deleted, the associated blogs will be too. This is an SQL standard, not Django
    #   more options at https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
    # Finally we specify the name of the reverse relationship, from User to Post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # Bosy of post, translates to a TEXT column in SQL
    body = models.TextField()

    # Indicate when post was published, timezone aware
    # Note that we're passing the timezone.now function itself, not the value
    publish = models.DateTimeField(default=timezone.now) 

    # Datetime when post was created
    created = models.DateTimeField(auto_now_add=True)

    # Indicates when post was last updated. With the "auto_now" parameter, the date will 
    # update automatically when the object is saved
    updated = models.DateTimeField(auto_now=True)

    # Shows the status of a post. Because of the "choices" parameter, the value 
    # can only be set to one of the given choices.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Django has different types of fields that can be used to define models.
    # All available fields can be found here: https://docs.djangoproject.com/en/5.0/ref/models/fields/

    objects = models.Manager() # Default Manager
    published = PublishedManager() # Custom Manager

    # Contains metadata. This tells Django to sort results in the publish field in descending 
    # order by default when we query the database. Descending order is specified with the negative prefix. 
    # With this, post published recently will appear first.
    class Meta:
        ordering = ('-publish',)

    # Human readable name. used in many places, such as the admin site.
    def __str__(self):
        return self.title
    
    # Convention is to add a get_absolute_url() method to the model that returns the canonical 
    # URL of the object. For this, we'll use the reverse() method that allows you to build URLs 
    # by their name and passing optional parameters.
    def get_absolute_url(self): # Use this in templates to link to specific posts
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

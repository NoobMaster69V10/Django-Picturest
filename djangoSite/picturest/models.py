from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """ Categories """
    name = models.CharField("Name", max_length=100)
    image = models.ImageField("Image", upload_to='categories/', null=True)
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat': self.url})


class Post(models.Model):
    """ Posts """
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", blank=True, null=True, upload_to="post/")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True, null=True, auto_created=True)
    owner = models.IntegerField('Owner', null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, unique=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.url})

    def save(self, **kwargs):
        self.url = slugify(self.title)
        super(Post, self).save(**kwargs)


class Profile(models.Model):
    """ Profile """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=100, null=True)
    image = models.ImageField("Image", upload_to='avatars/', null=True, default='placeholder/placeholder.svg')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Comments(models.Model):
    """ Comments """
    user = models.IntegerField('User')
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, unique=False)
    text = models.CharField('Comment', max_length=100)
    post = models.SlugField('Post slug', max_length=100, unique=False)

    def __str__(self):
        return self.post

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

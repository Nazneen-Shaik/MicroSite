import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class Category(models.Model):
    name = models.CharField(max_length=20, unique = True)
    slug = models.CharField(max_length=20, unique = True)
    description = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @property
    def get_url(self):
        return settings.SITE_BLOG_URL + "category/" + self.slug


class Tags(models.Model):
    name = models.CharField(max_length=20, unique = True)
    slug = models.CharField(max_length=20, unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICE = (
                    ('D','Draft'),
                    ('P','Published'),
                    ('T','Rejected'),
                    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tags,related_name='rel_posts', blank=True,null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE,blank=True)


    def __unicode__(self):
        return self.title


    @property
    def author(self):
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        tempslug = slugify(self.title)
        if self.id:
            blogpost = Post.objects.get(pk=self.id)
            if blogpost.title != self.title:
                self.slug = create_slug(tempslug)
        else:
            self.slug = create_slug(tempslug)

        super(Post, self).save(*args, **kwargs)

    @property
    def get_url(self):
        return settings.SITE_BLOG_URL + self.slug

    def is_editable_by(self, user):
        if self.user==user or user.is_admin:
            return True
        return False

    def is_deletable_by(self, user):
        if self.user==user or user.is_admin:
            return True
        return False


class Image_File(models.Model):
    upload = models.FileField(upload_to="static/uploads/%Y/%m/%d/")
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to="static/uploads/%Y/%m/%d/",blank=True,null=True)

    def __unicode__(self):
        return self.date_created


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug = tempslug)
            slugcount = slugcount + 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug

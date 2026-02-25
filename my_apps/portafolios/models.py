from django.forms import ValidationError
from django.utils.text import slugify
from django.db import models
import uuid
# Create your models here.


class ProjectQuerySet(models.QuerySet):

    def published(self):
        return self.filter(is_published=True)
    
    def with_tag(self, tag_name):
        return self.filter(tags__name=tag_name).distinct()

    def with_relations(self):
        return self.prefetch_related("tags", "details")

    def ordered(self):
        return self.order_by("-created_at")
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    url = models.URLField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="projects")
    is_published = models.BooleanField(default=False)
    
    objects = ProjectQuerySet.as_manager()
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def publish(self):
        if not self.is_published:
            self.is_published = True
            self.save(update_fields=["is_published"])

    def __str__(self):
        return self.title
    
    def clean(self):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_id}"
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    
    class Meta:
        indexes = [
            models.Index(fields=["is_published"]),
            models.Index(fields=["slug"]),
        ]
        
        
class ProjectContent(models.Model):
    
    class ContentTypeChoices(models.TextChoices):
        TEXT = 'TEXT', 'Text'
        IMAGE = 'IMAGE', 'Image'
        LINK = 'LINK', 'Link'
        CODE = 'CODE', 'Code'
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='details')
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=ContentTypeChoices.choices)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='project_details/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "order"],
                name="unique_order_per_project"
            )
        ]
        
    def clean(self):
        if self.content_type == self.ContentTypeChoices.TEXT and not self.content:
            raise ValidationError("Text content requires `content` field.")
        

    def __str__(self):
        return f"{self.project.title} - Detail"
    
    

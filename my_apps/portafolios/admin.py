from django.contrib import admin
from my_apps.portafolios.models import Project, Tag, ProjectContent

# Register your models here.



class ProjectContentInline(admin.TabularInline):
    model = ProjectContent
    extra = 1
    ordering = ("order",)
    fields = ("order", "title", "content_type", "content", "image", "url", "code")
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    list_display_links = ("title", "slug")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("tags",)

    inlines = (ProjectContentInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("tags")
    
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    
    
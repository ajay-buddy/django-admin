from django.contrib import admin
from django.utils import timezone
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

# Register your models here.

# admin.StackedInline or admin.TabularInline
class InlineComments(admin.StackedInline):
    model = Comment
    fields = ('text', 'is_active')
    extra = 1

class BlogAdmin(SummernoteModelAdmin):
    list_display = ('name', 'day_since_created', 'day_since_last_updated', 'created_date', 'last_modified', 'is_draft')
    list_filter = ('is_draft', 'created_date', 'last_modified')
    ordering = ('name', 'created_date', 'last_modified')
    search_fields = ('name', 'slug')
    prepopulated_fields = { 'slug' : ('name', )}
    list_per_page = 10
    actions = ('publish_blog',)
    date_hierarchy = 'created_date'
    # fields = (('name','slug'), 'text', 'is_draft')
    fieldsets = (
        ('Basic Details', {
            'fields': (('name','slug'), 'text', ),
            'description': '* Blog details'
        }),
        ('Advanced Options', {
            'fields': ('is_draft',)
        }),
    )

    summernote_fields = ('text',)
    inlines = (InlineComments,)

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('name', 'created_date')
        return ('last_modified',)

    def publish_blog(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(request, "{} Blogs Published Successfully".format(count))
    
    publish_blog.short_description = 'Publish Blog'

    def day_since_last_updated(self, blog):
        diff = timezone.now() - blog.last_modified
        return diff.days
    day_since_last_updated.short_description = 'Days Modified'

class BlogComment(SummernoteModelAdmin):
    list_display = ('blog', 'text', 'created_date', 'is_active')
    summernote_fields = ('text',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, BlogComment)

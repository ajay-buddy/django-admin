from django.contrib import admin
from django.utils import timezone
from django.db.models import Count
from django_summernote.admin import SummernoteModelAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from blog.models import Blog, Comment, Catagory

# Register your models here.

# admin.StackedInline or admin.TabularInline
class InlineComments(admin.StackedInline):
    model = Comment
    fields = ('text', 'is_active')
    extra = 1
    classes = ('collapse', )

class BlogAdmin(SummernoteModelAdmin):
    list_display = ('name', 'day_since_created', 'day_since_last_updated', 'number_comments', 'created_date', 'last_modified', 'is_draft')
    list_filter = ('is_draft', 'created_date', ('created_date', DateRangeFilter), ('last_modified', DateTimeRangeFilter))
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
            'description': '* Blog details',
            # 'classes': ('collapse', )
        }),
        ('Advanced Options', {
            'fields': ('is_draft', 'catagories'),
            'classes': ('collapse', )
        }),
    )

    summernote_fields = ('text',)
    inlines = (InlineComments,)
    filter_horizontal = ('catagories', )
    # filter_vertical = ('catagories', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(comments_count=Count('comments'))
        return qs
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions
    
    def number_comments(self, blog):
        return blog.comments_count

    number_comments.short_description = 'Comments'
    number_comments.admin_order_field = 'comments_count'

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
    list_editable = ('is_active',)
    list_per_page = 20
    summernote_fields = ('text',)
    # list_filter = ('blog',)
    list_filter = (
        # for ordinary fields
        ('created_date', DropdownFilter),
        # for choice fields
        # ('is_active', ChoiceDropdownFilter),
        # for related fields
        ('blog', RelatedDropdownFilter),
    )
    list_select_related =True
    readonly_fields = ('blog', )
    # raw_id_fields = ('blog', )

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, BlogComment)
admin.site.register(Catagory)

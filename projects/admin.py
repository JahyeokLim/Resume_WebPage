from django.contrib import admin

from .models import Project, ProjectMedia


class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_ko', 'visibility', 'is_published', 'start_date', 'end_date', 'order')
    list_filter = ('visibility', 'is_published')
    prepopulated_fields = {'slug': ('title_en',)}
    ordering = ('order', '-start_date')
    inlines = [ProjectMediaInline]
    fieldsets = (
        ('기본 정보', {
            'fields': ('title_ko', 'title_en', 'slug', 'summary_ko', 'summary_en', 'cover_image'),
        }),
        ('상세 내용', {
            'fields': ('overview_ko', 'overview_en', 'role_ko', 'role_en', 'architecture_ko', 'architecture_en', 'architecture_diagram'),
        }),
        ('기간 / 기술', {
            'fields': ('start_date', 'end_date', 'tech_stack'),
        }),
        ('공개 설정', {
            'fields': ('visibility', 'is_published', 'order'),
            'description': '"추상화하여 공개"를 선택한 경우, 위 항목들에서 회사명·제품명 등 민감 정보를 직접 가려서 작성하세요.',
        }),
    )

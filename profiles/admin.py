from django.contrib import admin

from .models import Profile, Skill, SkillCategory, TimelineEntry


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name_ko', 'role_ko', 'email', 'phone')
    list_display_links = ('name_ko',)

    def has_add_permission(self, request):
        # 싱글턴: 이미 하나 있으면 추가로 만들지 못하게 막는다.
        return not Profile.objects.exists()


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ko', 'name_en', 'order')
    inlines = [SkillInline]


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ('title_ko', 'category', 'start_date', 'end_date', 'order')
    list_filter = ('category',)
    ordering = ('order', '-start_date')

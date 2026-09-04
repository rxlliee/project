from django.contrib import admin
from .models import (
    PortfolioProfile, SkillCategory, Skill, Project, ProjectImage,
    Education, Experience, Achievement, Certificate, SocialLink, ContactMessage
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'published', 'featured', 'display_order')
    list_filter = ('published', 'featured')
    search_fields = ('title', 'short_description')
    inlines = [ProjectImageInline]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'slug', 'is_active', 'menu_order')
    search_fields = ('full_name', 'slug', 'user__username')
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'display_order')
    list_filter = ('profile',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'category', 'display_order')
    list_filter = ('profile', 'category')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Achievement)
admin.site.register(Certificate)
admin.site.register(SocialLink)
admin.site.register(ContactMessage)

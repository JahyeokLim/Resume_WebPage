from django.shortcuts import render

from projects.models import Project

from .models import Profile, SkillCategory, TimelineEntry


def home(request):
    profile = Profile.objects.first()
    timeline = TimelineEntry.objects.all()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    featured_projects = Project.objects.filter(is_published=True)[:3]

    context = {
        'profile': profile,
        'timeline': timeline,
        'skill_categories': skill_categories,
        'featured_projects': featured_projects,
    }
    return render(request, 'profiles/home.html', context)

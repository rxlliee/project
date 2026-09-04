import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST

from .models import PortfolioProfile, Project


def image_url(image):
    return image.url if image else None


def profile_summary(profile):
    return {
        'slug': profile.slug,
        'name': profile.full_name,
        'short_name': profile.short_name,
        'headline': profile.headline,
        'description': profile.short_description,
        'image': image_url(profile.profile_image),
        'accent_colour': profile.accent_colour,
    }


def profile_payload(profile):
    return {
        **profile_summary(profile),
        'bio': profile.bio,
        'location': profile.location,
        'email': profile.email,
        'phone': profile.phone,
        'current_status': profile.current_status,
        'primary_interest': profile.primary_interest,
        'secondary_interests': profile.secondary_interests,
        'cover_image': image_url(profile.cover_image),
        'resume': profile.resume_file.url if profile.resume_file else None,
        'skills': [
            {
                'name': skill.name,
                'category': skill.category.name if skill.category else None,
                'proficiency': skill.proficiency,
                'icon_text': skill.icon_text,
            }
            for skill in profile.skills.all()
        ],
        'projects': [
            {
                'slug': project.slug,
                'title': project.title,
                'description': project.short_description,
                'image': image_url(project.project_image),
                'technologies': project.technologies,
                'status': project.status,
                'featured': project.featured,
                'github_link': project.github_link,
                'live_demo': project.live_demo,
            }
            for project in profile.projects.filter(published=True)
        ],
        'education': [
            {
                'institution': item.institution,
                'programme': item.programme,
                'start_date': item.start_date,
                'end_date': item.end_date,
                'current': item.current,
                'description': item.description,
            }
            for item in profile.education.all()
        ],
        'experience': [
            {
                'organisation': item.organisation,
                'position': item.position,
                'type': item.type,
                'start_date': item.start_date,
                'end_date': item.end_date,
                'current': item.current,
                'description': item.description,
            }
            for item in profile.experience.all()
        ],
        'achievements': [
            {
                'title': item.title,
                'issuer': item.issuer,
                'date': item.date,
                'description': item.description,
                'link': item.link,
                'image': image_url(item.image),
            }
            for item in profile.achievements.all()
        ],
        'social_links': [
            {'platform': item.platform, 'label': item.label, 'url': item.url}
            for item in profile.social_links.filter(is_visible=True)
        ],
    }


def profile_detail(request, slug):
    get_object_or_404(PortfolioProfile, slug=slug, is_active=True)
    return redirect('core:landing')


def project_detail(request, profile_slug, project_slug):
    profile = get_object_or_404(PortfolioProfile, slug=profile_slug, is_active=True)
    get_object_or_404(Project, profile=profile, slug=project_slug, published=True)
    return redirect('core:landing')


@require_GET
def profile_list(request):
    profiles = PortfolioProfile.objects.filter(is_active=True).only(
        'slug', 'full_name', 'short_name', 'headline', 'short_description',
        'profile_image', 'accent_colour'
    )
    return JsonResponse({'profiles': [profile_summary(profile) for profile in profiles]})


@require_GET
def profile_api_detail(request, slug):
    profile = get_object_or_404(
        PortfolioProfile.objects.prefetch_related(
            'skills__category', 'projects', 'education', 'experience',
            'achievements', 'social_links'
        ),
        slug=slug,
        is_active=True,
    )
    return JsonResponse({'profile': profile_payload(profile)}, json_dumps_params={'default': str})


@require_POST
def contact_api(request, slug):
    profile = get_object_or_404(PortfolioProfile, slug=slug, is_active=True)
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    required = ('sender_name', 'sender_email', 'message')
    missing = [field for field in required if not str(payload.get(field, '')).strip()]
    if missing:
        return JsonResponse({'error': 'Missing required fields.', 'fields': missing}, status=400)

    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(payload['sender_email'])
    except ValidationError:
        return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

    message = profile.messages.create(
        sender_name=str(payload['sender_name']).strip()[:200],
        sender_email=str(payload['sender_email']).strip(),
        subject=str(payload.get('subject', '')).strip()[:250],
        message=str(payload['message']).strip(),
    )
    return JsonResponse({'message': 'Contact message received.', 'id': message.pk}, status=201)

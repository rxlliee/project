import uuid
import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


def unique_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    name = uuid.uuid4().hex
    return os.path.join('uploads', f"{name}.{ext}")


class PortfolioProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(max_length=120, unique=True)
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=80, blank=True)
    headline = models.CharField(max_length=200, blank=True)
    short_description = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=unique_upload_path, blank=True, null=True)
    cover_image = models.ImageField(upload_to=unique_upload_path, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    current_status = models.CharField(max_length=120, blank=True)
    primary_interest = models.CharField(max_length=200, blank=True)
    secondary_interests = models.CharField(max_length=400, blank=True)
    accent_colour = models.CharField(max_length=20, default='#4a90e2')
    accent_colour_secondary = models.CharField(max_length=20, blank=True)
    resume_file = models.FileField(upload_to=unique_upload_path, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    menu_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['menu_order', 'full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.full_name) or self.user.username
            slug = base
            n = 1
            while PortfolioProfile.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SkillCategory(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='skill_categories')
    name = models.CharField(max_length=120)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='skills')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills', null=True, blank=True)
    name = models.CharField(max_length=120)
    proficiency = models.CharField(max_length=50, blank=True)
    icon_text = models.CharField(max_length=10, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    project_image = models.ImageField(upload_to=unique_upload_path, blank=True, null=True)
    technologies = models.CharField(max_length=400, blank=True)
    team_members = models.CharField(max_length=400, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=120, blank=True)
    github_link = models.URLField(blank=True)
    live_demo = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Project.objects.filter(profile=self.profile, slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=unique_upload_path)
    caption = models.CharField(max_length=250, blank=True)
    alt_text = models.CharField(max_length=250, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Image for {self.project.title}"


class Education(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=250)
    programme = models.CharField(max_length=250, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.institution} — {self.programme}"


class Experience(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='experience')
    organisation = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    type = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.position} @ {self.organisation}"


class Achievement(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=250)
    issuer = models.CharField(max_length=250, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to=unique_upload_path, blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class Certificate(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=250)
    issuer = models.CharField(max_length=250, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_link = models.URLField(blank=True)
    image = models.FileField(upload_to=unique_upload_path, blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


PLATFORM_CHOICES = [
    ('linkedin', 'LinkedIn'),
    ('github', 'GitHub'),
    ('twitter', 'Twitter'),
    ('website', 'Website'),
    ('other', 'Other'),
]


class SocialLink(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=60, choices=PLATFORM_CHOICES, default='website')
    label = models.CharField(max_length=120, blank=True)
    url = models.URLField()
    display_order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.platform} - {self.url}"


class ContactMessage(models.Model):
    target = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message to {self.target} from {self.sender_name}"

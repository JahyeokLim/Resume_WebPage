from django.db import models
from django.utils.translation import get_language


class Profile(models.Model):
    """싱글턴 성격의 프로필 정보. 사이트에 한 명분만 존재한다."""

    name_ko = models.CharField(max_length=100, default='임재혁')
    name_en = models.CharField(max_length=100, default='jaehyeok Lim')
    role_ko = models.CharField(max_length=150, default='임베디드 소프트웨어 엔지니어')
    role_en = models.CharField(max_length=150, default='Embedded Software Engineer')
    tagline_ko = models.CharField(max_length=200, blank=True)
    tagline_en = models.CharField(max_length=200, blank=True)
    bio_ko = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_pdf = models.FileField(upload_to='resume/', blank=True, null=True)

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필'

    def __str__(self):
        return self.name_ko

    @property
    def name(self):
        return self.name_en if get_language() == 'en' else self.name_ko

    @property
    def role(self):
        return self.role_en if get_language() == 'en' else self.role_ko

    @property
    def tagline(self):
        return self.tagline_en if get_language() == 'en' else self.tagline_ko

    @property
    def bio(self):
        return self.bio_en if get_language() == 'en' else self.bio_ko


class TimelineEntry(models.Model):
    """경력/학력 타임라인 한 항목."""

    CATEGORY_CHOICES = [
        ('work', '경력'),
        ('education', '학력'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='work')
    title_ko = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    description_ko = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text='비워두면 "현재"로 표시됩니다.')
    order = models.PositiveIntegerField(default=0, help_text='숫자가 작을수록 먼저 표시됩니다.')

    class Meta:
        verbose_name = '타임라인 항목'
        verbose_name_plural = '타임라인 항목'
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.title_ko

    @property
    def title(self):
        return self.title_en if get_language() == 'en' else self.title_ko

    @property
    def description(self):
        return self.description_en if get_language() == 'en' else self.description_ko


class SkillCategory(models.Model):
    """기술 스택을 묶는 카테고리 (언어, RTOS, MCU, 통신 등)."""

    name_ko = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '기술 카테고리'
        verbose_name_plural = '기술 카테고리'
        ordering = ['order']

    def __str__(self):
        return self.name_ko

    @property
    def name(self):
        return self.name_en if get_language() == 'en' else self.name_ko


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '기술'
        verbose_name_plural = '기술'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

from django.db import models
from django.urls import reverse
from django.utils.translation import get_language


class Project(models.Model):
    VISIBILITY_CHOICES = [
        ('full', '전체 공개'),
        ('abstracted', '추상화하여 공개'),
    ]

    title_ko = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    summary_ko = models.CharField(max_length=300, help_text='목록 카드에 보일 한 줄 요약')
    summary_en = models.CharField(max_length=300)

    overview_ko = models.TextField(help_text='개요')
    overview_en = models.TextField()
    role_ko = models.TextField(help_text='본인 역할 / 담당 범위')
    role_en = models.TextField()
    architecture_ko = models.TextField(blank=True, help_text='시스템 구조/아키텍처 설명')
    architecture_en = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text='비워두면 "진행중"으로 표시됩니다.')

    tech_stack = models.CharField(max_length=400, help_text='쉼표로 구분 (예: C, FreeRTOS, STM32, CAN)')

    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    architecture_diagram = models.ImageField(upload_to='projects/diagrams/', blank=True, null=True)

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='full',
        help_text='추상화 공개 선택 시, 회사명·제품명 등 민감 정보는 제목/본문에서 직접 가려서 작성하세요.',
    )

    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='숫자가 작을수록 먼저 표시됩니다.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '프로젝트'
        verbose_name_plural = '프로젝트'
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.title_ko

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.title_en if get_language() == 'en' else self.title_ko

    @property
    def summary(self):
        return self.summary_en if get_language() == 'en' else self.summary_ko

    @property
    def overview(self):
        return self.overview_en if get_language() == 'en' else self.overview_ko

    @property
    def role(self):
        return self.role_en if get_language() == 'en' else self.role_ko

    @property
    def architecture(self):
        return self.architecture_en if get_language() == 'en' else self.architecture_ko

    @property
    def tech_tags(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    @property
    def is_abstracted(self):
        return self.visibility == 'abstracted'


class ProjectMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', '이미지'),
        ('video', '동영상'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media_items')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='projects/media/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='YouTube 등 외부 동영상 링크')
    caption_ko = models.CharField(max_length=200, blank=True)
    caption_en = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '프로젝트 첨부'
        verbose_name_plural = '프로젝트 첨부'
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title_ko} - {self.get_media_type_display()} #{self.order}'

    @property
    def caption(self):
        return self.caption_en if get_language() == 'en' else self.caption_ko

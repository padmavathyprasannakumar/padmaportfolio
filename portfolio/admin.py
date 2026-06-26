from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Profile,
    AboutSection,
    SkillCard,
    PersonalInfo,
    Skill,
    Language,
    Education,
    Experience,
    Certification,
    Project,
    HomeProjectSection,
    ProjectsPageContent,
    ContactPageContent,
    ContactDetail,
    ContactMessage,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'email', 'phone')
    search_fields = ('full_name', 'job_title', 'email')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'logo_text',
                'full_name',
                'job_title',
                'short_intro',
                'about_me',
            )
        }),
        ('Profile Image and CV', {
            'fields': (
                'profile_image',
                'cv_file',
            )
        }),
        ('Contact Information', {
            'fields': (
                'address',
                'phone',
                'email',
                'portfolio_website',
            )
        }),
        ('Social Links', {
            'description': 'Add your GitHub and LinkedIn URLs here. Icons will automatically appear on the website.',
            'fields': (
                'github',
                'linkedin',
            )
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

    fieldsets = (
        ('About Page Content', {
            'fields': (
                'title',
                'description',
                'order',
            )
        }),
    )


@admin.register(SkillCard)
class SkillCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_highlighted', 'order')
    list_editable = ('is_highlighted', 'order')
    search_fields = ('title', 'description')

    fieldsets = (
        ('Skill Card Information', {
            'fields': (
                'title',
                'description',
                'is_highlighted',
                'order',
            )
        }),
    )


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('nationality', 'marital_status', 'gender')

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'father_name',
                'mother_name',
                'husband_name',
                'date_of_birth',
                'gender',
                'nationality',
                'marital_status',
            )
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('course', 'institution', 'year', 'order')
    list_editable = ('order',)
    search_fields = ('course', 'institution', 'year')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'duration', 'order')
    list_editable = ('order',)
    search_fields = ('job_title', 'company', 'location', 'duration')

    fieldsets = (
        ('Work Experience', {
            'fields': (
                'job_title',
                'company',
                'location',
                'duration',
                'description',
                'order',
            )
        }),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'screenshot_preview',
        'title',
        'technology',
        'project_links',
        'is_latest',
        'order',
        'created_at',
    )
    list_editable = ('is_latest', 'order')
    search_fields = ('title', 'technology', 'short_description')
    list_filter = ('is_latest', 'created_at')
    readonly_fields = ('screenshot_preview',)

    fieldsets = (
        ('Project Basic Details', {
            'fields': (
                'title',
                'short_description',
                'full_description',
                'screenshot',
                'screenshot_preview',
            )
        }),
        ('Technology and Links', {
            'description': 'Add screenshot, live project link, and GitHub link here. They will automatically show as buttons on the website.',
            'fields': (
                'technology',
                'live_link',
                'github_link',
            )
        }),
        ('Display Settings', {
            'fields': (
                'is_latest',
                'order',
            )
        }),
    )

    @admin.display(description='Screenshot')
    def screenshot_preview(self, obj):
        if obj and obj.screenshot:
            return format_html(
                '<img src="{}" alt="{}" style="width: 88px; height: 58px; object-fit: cover; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.18);" />',
                obj.screenshot.url,
                obj.title,
            )
        return 'No screenshot'

    @admin.display(description='Links')
    def project_links(self, obj):
        links = []
        if obj.live_link:
            links.append(format_html('<a href="{}" target="_blank">Live</a>', obj.live_link))
        if obj.github_link:
            links.append(format_html('<a href="{}" target="_blank">GitHub</a>', obj.github_link))
        if not links:
            return 'No links'
        return mark_safe(' &nbsp;|&nbsp; '.join(str(link) for link in links))


@admin.register(HomeProjectSection)
class HomeProjectSectionAdmin(admin.ModelAdmin):
    list_display = ('small_title', 'heading', 'button_text', 'is_visible')
    list_editable = ('is_visible',)
    search_fields = ('small_title', 'heading', 'description', 'button_text')

    fieldsets = (
        ('Home Page Project Heading', {
            'description': 'Change the heading shown above the project cards on the home page. No code changes needed.',
            'fields': (
                'small_title',
                'heading',
                'description',
                'button_text',
                'is_visible',
            )
        }),
    )


@admin.register(ProjectsPageContent)
class ProjectsPageContentAdmin(admin.ModelAdmin):
    list_display = ('small_title', 'heading', 'is_visible')
    list_editable = ('is_visible',)
    search_fields = ('small_title', 'heading', 'description')

    fieldsets = (
        ('Projects Page Heading', {
            'description': 'Change the heading shown above the all projects page. No code changes needed.',
            'fields': (
                'small_title',
                'heading',
                'description',
                'is_visible',
            )
        }),
    )


@admin.register(ContactPageContent)
class ContactPageContentAdmin(admin.ModelAdmin):
    list_display = ('small_title', 'heading')
    search_fields = ('small_title', 'heading', 'description')

    fieldsets = (
        ('Dynamic Contact Page Text', {
            'description': 'Change the contact page title and description from here. No code changes needed.',
            'fields': (
                'small_title',
                'heading',
                'description',
            )
        }),
    )


@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'value', 'link', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'value', 'link')
    list_filter = ('is_active',)

    fieldsets = (
        ('Contact Detail', {
            'description': 'Add contact details one by one. Active details automatically show on the left side of the contact page.',
            'fields': (
                'icon',
                'title',
                'value',
                'link',
                'is_active',
                'order',
            )
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'subject', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'subject',
        'message',
        'created_at',
    )

    fieldsets = (
        ('Sender Details', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
            )
        }),
        ('Message Details', {
            'fields': (
                'subject',
                'message',
                'created_at',
            )
        }),
    )

from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    short_intro = models.TextField()
    about_me = models.TextField()

    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)

    logo_text = models.CharField(max_length=100, default='PadmaFolio')

    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    portfolio_website = models.URLField(blank=True)

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class AboutSection(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self):
        return self.title


class SkillCard(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Skill Card"
        verbose_name_plural = "Skill Cards"

    def __str__(self):
        return self.title


class PersonalInfo(models.Model):
    father_name = models.CharField(max_length=150, blank=True)
    mother_name = models.CharField(max_length=150, blank=True)
    husband_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "Personal Information"


class Skill(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Education(models.Model):
    course = models.CharField(max_length=150)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.course


class Experience(models.Model):
    job_title = models.CharField(max_length=150)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.job_title


class Certification(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=150)
    short_description = models.TextField()
    full_description = models.TextField(blank=True)

    screenshot = models.ImageField(upload_to='projects/')
    technology = models.CharField(
        max_length=255,
        help_text="Separate technologies with commas. Example: HTML, CSS, JavaScript, Django"
    )

    live_link = models.URLField(blank=True, help_text="Paste the live website/project URL here.")
    github_link = models.URLField(blank=True, help_text="Paste the GitHub repository URL here.")

    is_latest = models.BooleanField(
        default=False,
        help_text="Turn this on to show the project on the home page. If none are selected, the newest projects are shown."
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower number appears first.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def technology_list(self):
        """Return clean technology badges for templates."""
        normalized = self.technology.replace('|', ',').replace('•', ',')
        parts = [item.strip() for item in normalized.split(',') if item.strip()]
        if parts:
            return parts
        return [item.strip() for item in self.technology.split() if item.strip()]

    @property
    def has_external_links(self):
        return bool(self.live_link or self.github_link)


class HomeProjectSection(models.Model):
    small_title = models.CharField(
        max_length=80,
        default='Portfolio',
        help_text='Small label shown above the home page project heading.'
    )
    heading = models.CharField(
        max_length=160,
        default='Featured Projects',
        help_text='Main heading shown above the home page project cards.'
    )
    description = models.TextField(
        blank=True,
        default='Projects added from Django Admin are shown here with screenshots, details, live links, and GitHub links.',
        help_text='Optional short description shown under the project heading.'
    )
    button_text = models.CharField(
        max_length=80,
        default='View More Projects',
        help_text='Button text shown below home page project cards.'
    )
    is_visible = models.BooleanField(
        default=True,
        help_text='Turn off to hide the home page project heading.'
    )

    class Meta:
        verbose_name = 'Home Project Section Content'
        verbose_name_plural = 'Home Project Section Content'

    def __str__(self):
        return self.heading


class ProjectsPageContent(models.Model):
    small_title = models.CharField(
        max_length=80,
        default='Portfolio',
        help_text='Small label shown above the projects page heading.'
    )
    heading = models.CharField(
        max_length=160,
        default='My Projects',
        help_text='Main heading shown on the projects page.'
    )
    description = models.TextField(
        blank=True,
        default='A collection of projects added from Django Admin with screenshots, live links, and GitHub links.',
        help_text='Optional short description shown under the projects page heading.'
    )
    is_visible = models.BooleanField(
        default=True,
        help_text='Turn off to hide the projects page heading.'
    )

    class Meta:
        verbose_name = 'Projects Page Content'
        verbose_name_plural = 'Projects Page Content'

    def __str__(self):
        return self.heading


class ContactPageContent(models.Model):
    small_title = models.CharField(
        max_length=80,
        default='Contact Us',
        help_text='Small label shown above the contact heading.'
    )
    heading = models.CharField(
        max_length=160,
        default="Let's Connect & Collaborate",
        help_text='Main heading shown on the contact page.'
    )
    description = models.TextField(
        default='Feel free to contact me for projects, collaborations, or job opportunities.',
        help_text='Short description shown below the heading.'
    )

    class Meta:
        verbose_name = 'Contact Page Content'
        verbose_name_plural = 'Contact Page Content'

    def __str__(self):
        return self.heading


class ContactDetail(models.Model):
    icon = models.CharField(
        max_length=30,
        default='📧',
        help_text='Add any emoji/icon text. Example: 📞, 📧, 📍, 🌐'
    )
    title = models.CharField(
        max_length=100,
        help_text='Example: Phone, Email, Location, Website'
    )
    value = models.CharField(
        max_length=255,
        help_text='The contact detail text shown on the website.'
    )
    link = models.CharField(
        max_length=300,
        blank=True,
        help_text='Optional clickable link. Examples: tel:+60123456789, mailto:name@gmail.com, https://example.com'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Only active contact details are shown on the website.'
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text='Lower number appears first.'
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Contact Detail'
        verbose_name_plural = 'Contact Details'

    def __str__(self):
        return f"{self.title}: {self.value}"

    @property
    def open_in_new_tab(self):
        return self.link.startswith(('http://', 'https://'))


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} - {self.subject}"

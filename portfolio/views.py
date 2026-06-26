from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContactForm

from .models import (
    Profile,
    AboutSection,
    SkillCard,
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
)


def get_profile():
    """
    Get first profile added from Django admin.
    This keeps the website dynamic.
    """
    return Profile.objects.first()


def home(request):
    profile = get_profile()

    # Show selected home-page projects first.
    # If no project is selected as latest, show newest admin-added projects.
    latest_projects = Project.objects.filter(is_latest=True).order_by("-id")

    if not latest_projects.exists():
        latest_projects = Project.objects.all().order_by("-id")

    latest_projects = latest_projects[:6]

    # Dynamic home projects heading from admin dashboard
    home_project_section = HomeProjectSection.objects.first()

    return render(
        request,
        "portfolio/home.html",
        {
            "profile": profile,
            "latest_projects": latest_projects,
            "home_project_section": home_project_section,
        },
    )


def about(request):
    profile = get_profile()

    # Dynamic About Me contents from admin dashboard
    about_sections = AboutSection.objects.all().order_by("id")

    # Dynamic skill cards from admin dashboard
    skill_cards = SkillCard.objects.all().order_by("id")

    # Resume related details from admin dashboard
    skills = Skill.objects.all().order_by("id")
    languages = Language.objects.all().order_by("id")
    education = Education.objects.all().order_by("-id")
    experience = Experience.objects.all().order_by("-id")
    certifications = Certification.objects.all().order_by("-id")

    return render(
        request,
        "portfolio/about.html",
        {
            "profile": profile,
            "about_sections": about_sections,
            "skill_cards": skill_cards,
            "skills": skills,
            "languages": languages,
            "education": education,
            "experience": experience,
            "certifications": certifications,
        },
    )


def projects(request):
    profile = get_profile()

    # All projects added from Django admin dashboard
    all_projects = Project.objects.all().order_by("-id")

    # Dynamic projects page heading from admin dashboard
    projects_page = ProjectsPageContent.objects.first()

    return render(
        request,
        "portfolio/projects.html",
        {
            "profile": profile,
            "projects": all_projects,
            "projects_page": projects_page,
        },
    )


def project_detail(request, pk):
    profile = get_profile()

    # Single project detail page
    project = get_object_or_404(Project, pk=pk)

    return render(
        request,
        "portfolio/project_detail.html",
        {
            "profile": profile,
            "project": project,
        },
    )


def contact(request):
    profile = get_profile()

    contact_page = ContactPageContent.objects.first()
    contact_details = ContactDetail.objects.filter(is_active=True).order_by("order", "id")

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_message = form.save()

            full_name = f"{contact_message.first_name} {contact_message.last_name}".strip()

            email_subject = f"Portfolio Contact: {contact_message.subject}"

            email_body = f"""
New message from portfolio website.

Name: {full_name}
Email: {contact_message.email}
Phone: {contact_message.phone}

Subject:
{contact_message.subject}

Message:
{contact_message.message}
"""

            try:
                email = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECEIVER_EMAIL],
                    reply_to=[contact_message.email],
                )

                email.send(fail_silently=False)

                messages.success(
                    request,
                    "Your message has been sent successfully.",
                )

                return redirect("contact")

            except Exception as e:
                logger.exception("EMAIL SEND ERROR: %s", e)
                print("EMAIL SEND ERROR:", repr(e))

                messages.error(
                    request,
                    "Message saved, but email could not be sent. Please check SMTP settings.",
                )

                return redirect("contact")

        else:
            messages.error(
                request,
                "Please check the form and try again.",
            )

    else:
        form = ContactForm()

    return render(
        request,
        "portfolio/contact.html",
        {
            "profile": profile,
            "form": form,
            "contact_page": contact_page,
            "contact_details": contact_details,
        },
    )

from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import uuid

#spoorthi----------------------------

def upload_filename(instance, filename):
    ts = timezone.now().strftime("%Y%m%d%H%M%S")
    uid = getattr(instance, "pk", None) or uuid.uuid4().hex[:8]
    base = filename.replace(" ", "_")
    return f"profiles/{uid}/{ts}_{base}"


class UserProfile(models.Model):

    IDENTITY_CHOICES = [
        ("bride", "Bride"),
        ("groom", "Groom"),
        ("lgbtq", "LGBTQ+"),
    ]

    GENDER_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("transgender", "Transgender"),
        ("gay", "Gay"),
        ("lesbian", "Lesbian"),
        ("bisexual", "Bisexual"),
        ("queer", "Queer"),
    ]

    # BASIC REQUIRED FIELDS
    identity = models.CharField(max_length=20, choices=IDENTITY_CHOICES)
    derived_gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()  # required now

    is_available = models.BooleanField(default=True)

    # CONTACT REQUIRED
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    # LOCATION REQUIRED
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)  # updated to 10

    # PHYSICAL — REQUIRED except blood_group
    height_cm = models.PositiveIntegerField()
    weight_kg = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=10, null=True, blank=True)

    # RELIGION & COMMUNITY REQUIRED
    religion = models.CharField(max_length=100)
    community = models.CharField(max_length=100)
    sub_community = models.CharField(max_length=100)

    # EDUCATION — can stay optional
    education = models.CharField(max_length=100)
    college = models.CharField(max_length=200, null=True, blank=True)

    # WORKING STATUS REQUIRED
    working_status = models.CharField(max_length=100)

    # PROFESSION — required only if working (handled in views)
    profession = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    annual_income = models.CharField(max_length=50, null=True, blank=True)

    # LIFESTYLE — REQUIRED
    diet = models.CharField(max_length=50)
    drinking = models.CharField(max_length=50)
    smoking = models.CharField(max_length=50)

    # PERSONALITY — REQUIRED
    hobbies = models.CharField(max_length=300)
    about_me = models.TextField()

    # VERIFICATION
    face_verified = models.BooleanField(default=False)
    match_score = models.FloatField(null=True, blank=True)

    # PASSWORD
    password = models.CharField(max_length=255)

    # ID DOCUMENTS
    id_type = models.CharField(max_length=50)
    id_proof_front = models.FileField(upload_to="id_proofs/front/")
    id_proof_back = models.FileField(upload_to="id_proofs/back/", null=True, blank=True)

    selfie_image = models.FileField(upload_to="photos/selfie/", null=True, blank=True)
    uploaded_photo = models.FileField(upload_to="photos/uploaded/", null=True, blank=True)
    avatar_image = models.ImageField(upload_to="avatars/", null=True, blank=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.first_name} ({self.identity})"

#spoorthi_________________________________

  #ojjuu-------------------------------------------------------------
class BusinessEnquiry(models.Model):
    name = models.CharField(max_length=100)
    nature_of_business = models.CharField(max_length=255)
    email = models.EmailField()
    organisation_company = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    queries_partnership_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.organisation_company}"

    class Meta:
        verbose_name_plural = "Business Enquiries"


class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('app', 'App / website'),
        ('profiles', 'Profiles & matching'),
        ('payments', 'Payment & plans'),
        ('safety', 'Safety / report user'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='app')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    suggestions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback #{self.id} - {self.get_category_display()}"

    class Meta:
        verbose_name_plural = "Feedback & Suggestions"

    #ojju__________________________________________________________________________________________________
from django.contrib import admin
from .models import BusinessEnquiry, Feedback, UserProfile  

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    # Columns shown in list view
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "mobile",
        "identity",
        "derived_gender",
        "city",
        "state",
        "face_verified",
        "match_score",
        "created_at",
    )

    # Add filters on right side
    list_filter = (
        "identity",
        "derived_gender",
        "state",
        "city",
        "religion",
        "working_status",
        "face_verified",
        "created_at",
    )

    # Add search bar
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "mobile",
        "community",
        "sub_community",
    )

    # Read-only fields in admin
    readonly_fields = (
        "created_at",
        "updated_at",
        "match_score",
        "face_verified",
        "id_proof_front",
        "id_proof_back",
        "selfie_image",
        "uploaded_photo",
    )

    # Organize fields into collapsible sections
    fieldsets = (
        ("Basic Identity", {
            "fields": ("identity", "derived_gender", "first_name", "last_name", "dob", "is_available")
        }),

        ("Contact", {
            "fields": ("mobile", "email")
        }),

        ("Location", {
            "fields": ("state", "city", "pincode")
        }),

        ("Physical Details", {
            "fields": ("height_cm", "weight_kg", "blood_group")
        }),

        ("Religion & Community", {
            "fields": ("religion", "community", "sub_community")
        }),

        ("Education", {
            "fields": ("education", "college")
        }),

        ("Work & Profession", {
            "fields": ("working_status", "profession", "company_name", "annual_income")
        }),

        ("Lifestyle", {
            "fields": ("diet", "drinking", "smoking")
        }),

        ("Personality", {
            "fields": ("hobbies", "about_me")
        }),

        ("Verification Details", {
            "fields": ("face_verified", "match_score"),
        }),

        ("ID Documents", {
            "fields": ("id_type", "id_proof_front", "id_proof_back"),
        }),

        ("Photos", {
            "fields": ("selfie_image", "uploaded_photo"),
        }),

        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

@admin.register(BusinessEnquiry)
class BusinessEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation_company', 'email', 'contact_phone', 'created_at')
    list_filter = ('created_at', 'nature_of_business')
    search_fields = ('name', 'email', 'organisation_company')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact_phone')
        }),
        ('Business Information', {
            'fields': ('organisation_company', 'nature_of_business')
        }),
        ('Details', {
            'fields': ('queries_partnership_details',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'category', 'priority', 'created_at')
    list_filter = ('category', 'priority', 'created_at')
    search_fields = ('name', 'email', 'suggestions')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('name', 'email')
        }),
        ('Feedback', {
            'fields': ('category', 'priority', 'suggestions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
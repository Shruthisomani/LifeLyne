
import base64
from io import BytesIO
import datetime
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.db import transaction
from lyne.models import UserProfile
from PIL import Image

from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from .forms import BusinessEnquiryForm, FeedbackForm
from .models import BusinessEnquiry, Feedback



# Create your views here.
def home(request):
    return render(request, "home.html")

def services(request):
    return render(request, "services.html")

def help_view(request):
    return render(request, "help.html")
def register_page(request):
    return render(request, "register.html")
def login(request):
    return render(request, "login.html")

#  LOGIN / LOGOUT (function-based)
# ---------------------------------------------------------
def login_view(request):
    """
    Simple login view using Django auth. Expects 'username' and 'password' in POST.
    Make sure you have a template at templates/login.html.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html", {"username": username})
    return render(request, "login.html")


def logout_view(request):
    auth_logout(request)
    return redirect("home")


def dashboard(request):
    # demo profile — replace with real user data later
    profile = {
        "id": 1,
        "name": "Shruti (Demo)",
        "avatar": "img/avatar_demo.png",
        "completion": 80,
        "location": "Hyderabad"
    }

    demo_matches = [
        {"id": 1, "name": "Rahul Kumar", "age": 27, "profession": "Software Engineer", "location": "Bangalore", "match": 92, "preferred": "N/A", "img": "img/rahul.jpg"},
        {"id": 2, "name": "Arjun Reddy", "age": 29, "profession": "Doctor", "location": "Hyderabad", "match": 86, "preferred": "N/A", "img": "img/arjun.jpg"},
        {"id": 3, "name": "Imran", "age": 26, "profession": "Data Analyst", "location": "Pune", "match": 84, "preferred": "N/A", "img": "img/imran.jpg"},
    ]

    context = {"profile": profile, "matches": demo_matches, "stats": {"new_matches": 8, "shortlisted": 5, "views": 21}}
    return render(request, "dashboard.html", context)

def matches(request):
    return render(request, "matches.html")


# -------------------------
# Profile view (single definition)
# -------------------------
def profile_full(request, user_id):
    """
    Simple placeholder profile view.
    Replace with real logic later (fetch UserProfile from DB).
    """
    # Example: profile = get_object_or_404(UserProfile, id=user_id)
    profile = {
        "id": user_id,
        "name": f"Demo User {user_id}",
        "age": 25,
        "location": "Hyderabad",
        "bio": "This is a demo profile. Replace with real data."
    }
    return render(request, "profile_full.html", {"profile": profile})

def bride_registration(request):
    return render(request, "bride_register.html")

def groom_registration(request):
    return render(request, "groom_register.html")

def lgbtq_registration(request):
    return render(request, "lgbtq_register.html")

def registration_success(request):
    name = request.session.get("registered_name", "User")
    return render(request, "registration_success.html", {"user_name": name})

#spoorthi--------------------------------------
# ---------------------------
# Utility: convert base64 → ContentFile
# ---------------------------
def content_file_from_dataurl(data_url, default_name="image.jpg"):
    """
    Convert a data URL (data:image/jpeg;base64,...) to a Django ContentFile.
    Returns None if invalid input.
    """
    try:
        if not data_url:
            return None

        header, b64data = data_url.split(",", 1)
        decoded = base64.b64decode(b64data)

        # detect file format
        try:
            img = Image.open(BytesIO(decoded))
            fmt = (img.format or "JPEG").lower()
            ext = "jpg" if fmt == "jpeg" else fmt
            filename = f"{default_name}.{ext}"
        except Exception:
            filename = default_name

        return ContentFile(decoded, name=filename)

    except Exception:
        return None


# ---------------------------
# Helpers: field validators
# ---------------------------
def parse_date_iso(value):
    if not value:
        return None
    if isinstance(value, datetime.date):
        return value
    try:
        # expects 'YYYY-MM-DD'
        return datetime.date.fromisoformat(value)
    except Exception:
        return None


def to_int_safe(val):
    if val is None or val == "":
        return None
    try:
        return int(str(val).strip())
    except Exception:
        return None


def is_valid_pincode(value, max_len=10):
    if value is None:
        return False
    v = str(value).strip()
    if not v:
        return False
    if len(v) > max_len:
        return False
    # allow numeric pincodes; if you want alphanumeric (e.g., other countries), relax this
    return v.isdigit()


# ---------------------------
# Main Registration Submit Handler
# ---------------------------
def register_user_submit(request):
    """
    Full server-side validation and safe save.
    Enforces:
      - first_name, last_name, password required
      - both mobile AND email required
      - dob required and 18+
      - id_type required and id_proof_front required
      - profession/company/annual_income required when working_status == "working"
      - sub_community required
      - lifestyle fields required (diet/drinking/smoking)
      - hobbies and about_me required
      - numeric conversions for height_cm/weight_kg
      - pincode max length 10 numeric
    """
    if request.method != "POST":
        return HttpResponse("Invalid Access", status=405)

    try:
        data = request.POST
        files = request.FILES

        # Basic fields (trim strings)
        first_name = (data.get("first_name") or "").strip()
        last_name = (data.get("last_name") or "").strip()
        password_raw = data.get("password") or ""
        confirm_password = data.get("confirm_password") or ""

        # contact
        mobile = (data.get("mobile") or "").strip()
        email = (data.get("email") or "").strip()

        # identity
        identity = (data.get("identity") or "").strip().lower()
        id_type = (data.get("id_type") or "").strip()

        # dob - expects YYYY-MM-DD from your front-end
        dob_raw = data.get("dob")
        dob = parse_date_iso(dob_raw)

        # physical
        height_raw = data.get("height_cm")
        weight_raw = data.get("weight_kg")
        blood_group = (data.get("blood_group") or "").strip()

        # location
        state = (data.get("state") or "").strip()
        city = (data.get("city") or "").strip()
        pincode = (data.get("pincode") or "").strip()

        # religion/community
        religion = (data.get("religion") or "").strip()
        community = (data.get("community") or "").strip()
        sub_community = (data.get("sub_community") or "").strip()

        # education & work
        education = (data.get("education") or "").strip()
        college = (data.get("college") or "").strip()
        working_status = (data.get("working_status") or "").strip()
        profession = (data.get("profession") or "").strip()
        company_name = (data.get("company_name") or "").strip()
        annual_income = (data.get("annual_income") or "").strip()

        # lifestyle
        diet = (data.get("diet") or "").strip()
        drinking = (data.get("drinking") or "").strip()
        smoking = (data.get("smoking") or "").strip()

        # interests
        hobbies = (data.get("hobbies") or "").strip()
        about_me = (data.get("about_me") or "").strip()

        # verification-related
        face_verified_flag = data.get("face_verified") in ["1", "true", "yes"]
        match_score_raw = data.get("match_score")

        # files
        id_front_file = files.get("id_proof_front")
        id_back_file = files.get("id_proof_back")
        uploaded_photo = files.get("uploaded_photo")

        # selfie (base64) optional until you require it
        selfie_data = data.get("selfie_data")

        # --------------------------
        # Begin validation
        # --------------------------
        # Required base checks
        if not first_name or not last_name:
            return HttpResponse("First name and last name are required", status=400)

        if not password_raw:
            return HttpResponse("Password is required", status=400)

        # password confirmation check (frontend also covers this)
        if password_raw != confirm_password:
            return HttpResponse("Passwords do not match", status=400)

        # require both mobile and email
        if not mobile or not email:
            return HttpResponse("Mobile and email are required", status=400)

        # prevent duplicate email
        if email and UserProfile.objects.filter(email=email).exists():
            print("DUPLICATE EMAIL TRIGGERED:", email)
            context = {
                "error_email": "Email already registered. Please use another email.",
                "show_step": 5,
            }
            return render(request, "bride_register.html", context)


        # identity and id_type required
        if not identity:
            return HttpResponse("Identity (bride/groom/lgbtq) is required", status=400)
        if not id_type:
            return HttpResponse("ID type is required", status=400)

        # DOB: required and 18+
        if not dob:
            return HttpResponse("Valid date of birth is required", status=400)
        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            return HttpResponse("Must be 18 or older", status=400)

        # height/weight — require and convert to ints (safe ranges can be adjusted)
        height_cm = to_int_safe(height_raw)
        weight_kg = to_int_safe(weight_raw)
        if height_cm is None:
            return HttpResponse("Height (cm) is required and must be a number", status=400)
        if weight_kg is None:
            return HttpResponse("Weight (kg) is required and must be a number", status=400)
        # optional: range checks
        if not (90 <= height_cm <= 250):
            return HttpResponse("Height must be between 90 and 250 cm", status=400)
        if not (25 <= weight_kg <= 300):
            return HttpResponse("Weight must be a sensible number (25-300 kg)", status=400)

        # pincode: allow up to 10 digits (per your instruction)
        if not is_valid_pincode(pincode, max_len=10):
            return HttpResponse("Pincode is required and must be numeric (max 10 digits)", status=400)

        # religion/community/sub_community required
        if not religion:
            return HttpResponse("Religion is required", status=400)
        if not community:
            return HttpResponse("Community/Caste is required", status=400)
        if not sub_community:
            return HttpResponse("Sub-community is required", status=400)

        # education (you asked to require everything)
        if not education:
            return HttpResponse("Education is required", status=400)
        # working_status required
        if not working_status:
            return HttpResponse("Working status is required", status=400)

        # if working, require profession/company/annual_income
        if working_status == "working":
            if not profession or not company_name or not annual_income:
                return HttpResponse("Profession, company and income are required for working status", status=400)

        # lifestyle required
        if not diet:
            return HttpResponse("Dietary preference is required", status=400)
        if not drinking:
            return HttpResponse("Drinking preference is required", status=400)
        if not smoking:
            return HttpResponse("Smoking preference is required", status=400)

        # interests required
        if not hobbies:
            return HttpResponse("Hobbies are required", status=400)
        if not about_me:
            return HttpResponse("About me / bio is required", status=400)

        # id_proof_front required
        if not id_front_file:
            return HttpResponse("Front side of ID proof is required", status=400)

        # If using uploaded_photo route (availability false), ensure uploaded_photo present
        # (Your front-end branches already handle this — double-check on server)
        # optional: check uploaded_photo presence if provided route expects it

        # match_score parsing
        match_score = None
        if match_score_raw:
            try:
                match_score = float(match_score_raw)
            except Exception:
                match_score = None

        # --------------------------
        # All validations passed — build model instance safely
        # --------------------------
        # derive gender
        if identity == "bride":
            derived_gender = "female"
        elif identity == "groom":
            derived_gender = "male"
        else:
            derived_gender = None

        # Wrap save in a transaction
        with transaction.atomic():
            profile = UserProfile(
                identity=identity,
                derived_gender=derived_gender,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                is_available=(data.get("is_available") == "yes"),
                mobile=mobile,
                email=email,
                state=state,
                city=city,
                pincode=pincode,
                height_cm=height_cm,
                weight_kg=weight_kg,
                blood_group=blood_group or "",     # blood_group optional per your note
                religion=religion,
                community=community,
                sub_community=sub_community,
                education=education,
                college=college,
                working_status=working_status,
                profession=profession,
                company_name=company_name,
                annual_income=annual_income,
                diet=diet,
                drinking=drinking,
                smoking=smoking,
                hobbies=hobbies,
                about_me=about_me,
                id_type=id_type,
                face_verified=face_verified_flag,
                match_score=match_score,
            )

            # hash and set password
            profile.set_password(password_raw)

            # assign files (id front required)
            profile.id_proof_front = id_front_file
            if id_back_file:
                profile.id_proof_back = id_back_file
            if uploaded_photo:
                profile.uploaded_photo = uploaded_photo
                profile.avatar_image = files["uploaded_photo"]

            # selfie base64 -> save if present
            if selfie_data:
                selfie_file = content_file_from_dataurl(selfie_data, default_name=f"{first_name}_selfie")
                if selfie_file:
                    profile.selfie_image.save(selfie_file.name, selfie_file, save=False)

            # save profile
            profile.save()

        # set session and redirect
        request.session["registered_name"] = profile.first_name
        return redirect("registration_success")

    except Exception as e:
        # Do not leak internal errors in production — consider logging and returning generic message
        return HttpResponse(f"Server error: {str(e)}", status=500)


#spoorthi_______________________________________

# def password_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             # use Django built-in password reset flow or send mail here
#             messages.success(request, "If an account exists, reset instructions were sent.")
#             return redirect('password_reset_done')
#     else:
#         form = PasswordResetForm()
#     return render(request, "registration/password_reset_form.html", {"form": form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                html_email_template_name='registration/password_reset_email_html.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            messages.success(request, 'Password reset email sent — check your inbox.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def edit_demo(request):
    # Renders the demo edit page (no database, just a static preview)
    return render(request, 'edit_profile.html')


def edit_profile(request, user_id):
    # load profile
    profile = get_object_or_404(UserProfile, pk=user_id)

    # NOTE: add your permission check here if needed (only owner/admin should edit)
    # if request.user.is_authenticated and request.user.profile.id != profile.id: return HttpResponseForbidden()

    if request.method == "POST":
        # simple fields
        profile.first_name = request.POST.get("first_name", profile.first_name)
        profile.last_name  = request.POST.get("last_name", profile.last_name)
        profile.state      = request.POST.get("state", profile.state)
        profile.city       = request.POST.get("city", profile.city)
        profile.education  = request.POST.get("education", profile.education)
        profile.profession = request.POST.get("profession", profile.profession)
        profile.hobbies    = request.POST.get("hobbies", profile.hobbies)
        profile.about_me   = request.POST.get("about_me", profile.about_me)

        # privacy select (optional)
        visibility = request.POST.get("photo_visibility")
        if visibility:
            profile.photo_visibility = visibility  # create this field if you want; optional

        # file upload: uploaded_photo
        if "uploaded_photo" in request.FILES and request.FILES["uploaded_photo"]:
            profile.uploaded_photo = request.FILES["uploaded_photo"]
            # new photo uploaded -> require re-verification
            profile.face_verified = False

        # id proof uploads (optional)
        if "id_proof_front" in request.FILES and request.FILES["id_proof_front"]:
            profile.id_proof_front = request.FILES["id_proof_front"]
        if "id_proof_back" in request.FILES and request.FILES["id_proof_back"]:
            profile.id_proof_back = request.FILES["id_proof_back"]

        profile.save()
        messages.success(request, "Profile saved.")
        # after save, go back to dashboard (or to profile panel)
        return redirect("dashboard")

    # GET -> show form
    return render(request, "edit_profile.html", {"profile": profile})


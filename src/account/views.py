import datetime
import jdatetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from unidecode import unidecode



from account.sms import veri_cod

from .forms import AccountUpdateForm, PersonDetailForm
from .models import Account, Business, Category, ver_code
from .sms import smsSender
import random
def generate_otp():
    code = str(random.randrange(100000, 999999))
    return code

def login_user(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    View for user login.

    Authenticates the user with the provided username and password.
    If the authentication is successful, the user is logged in and redirected to the dashboard:account_overview or next url page.
    Otherwise, a PermissionDenied exception is raised.

    Returns:
        Redirect to clickDashboard if the login is successful.
        Rendered HTML template: login.html if the login is unsuccessful.
    """
    if request.user.is_authenticated:
        messages.warning(request, "شما هم اکنون در حساب کاربری خود هستید.")
        return redirect("dashboard:account_overview")

    next_url = request.GET.get("next") or ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        next_url = request.POST.get("next") or ""
        default_message = "نام کاربری یا رمز عبور اشتباه است."

        try:
            user = Account.objects.get(username=username)
            if not user.check_password(password):
                user = None
        except:
            user = None
            
            
        if user is not None:
            login(request, user)
            
            return redirect("dashboard:account_overview") if next_url == "" else HttpResponseRedirect(next_url)

        context = {
            "message": default_message,
            "next": next_url,
        }

        return render(request, "account/login.html", context)

    return render(
        request,
        "account/login.html",
        context={"next": next_url},
    )


def login_with_sms(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        messages.warning(request, "شما هم اکنون در حساب کاربری خود هستید.")
        return redirect("dashboard:account_overview")

    next_url = request.GET.get("next") or ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Account.objects.get(username=username)
        except:
            default_message =  "کاربری با این شماره ثبت نام نکرده است شماره را چک کنید یا ثبت نام کنید"
            user = None
        try:
            code_instance = ver_code.objects.get(phone=username, code=password)
            wait_time = datetime.timedelta(minutes=2)
            if (code_instance.date_created + wait_time) < datetime.datetime.now():
                default_message = "زمان انقضای کد گذشته است."
                user = None
            code_instance.delete()
        except:
            default_message = "کد وارد شده اشتباه است."
            user = None
            context = {
                "message": default_message,
                "next": next_url,
            }
            return render(request, "account/sms_login.html", context)
        if user is not None:
            login(request, user)
        
            return redirect("dashboard:account_overview") if next_url == "" else HttpResponseRedirect(next_url)
        else:
            context = {
                "message": default_message,
                "next": next_url,
            }

            return render(request, "account/sms_login.html", context)

    return render(
        request,
        "account/sms_login.html",
        context={"next": next_url},
    )
# ------------------------------------------------------------------


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    """
    View for user logout.

    Logs out the currently authenticated user.

    Returns:
        Redirect to login page.
    """
    logout(request)
    return redirect("core:home")


# ------------------------------------------------------------------


def verify(request: HttpRequest, dir: str) -> HttpRequest | HttpResponseRedirect:
    """
    View for handling user verification in the account system.

    This view allows users to go through a two-step verification process.
    In the first step, the user receives a verification code (OTP) via SMS.
    In the second step, the user enters the received code to complete the verification.

    Args:
        request (HttpRequest): The HTTP request object.
        dir (str): A string indicating the direction of verification (e.g., 'signup' or 'pass').

    Returns:
        HttpRequest or HttpResponseRedirect: Depending on the verification status,
        the view may return an HTTP response for rendering a verification form or redirect to a different view.

    Exceptions:
        - If the 'ver_code' object with the entered code does not exist (ver_code.DoesNotExist),
          it means the entered code is incorrect. In this case, the view will re-render the
          verification form with an error message indicating that the code is incorrect.

    Alternatives:
        - If the user enters an incorrect code, they can retry the verification process by entering
          a valid code.
        - If 'dir' is not 'signup' or 'pass', it will return a 404 error page, indicating an invalid
          'dir' value. This can be handled by extending the 'alternatives' section to specify how
          to handle other 'dir' values.

    """
    if request.method == "POST":
        status = request.POST.get("status")
        if status == "1":
            # First step: Request a verification code and display the code entry form
            number = request.POST.get("number")
            code = generate_otp()
            veri_cod(phone=number, code=code)
            ver_code.objects.create(phone=number, code=code)
            return render(request, "account/verify.html", {"status": "2", "dir": dir})
        elif status == "2":
            # Second step: Verify the entered code and redirect to the appropriate view
            code = request.POST.get("code")
            try:
                var = ver_code.objects.get(code=code)
            except ver_code.DoesNotExist:
                # Handle incorrect code input
                return render(
                    request,
                    "account/verify.html",
                    {"status": "2", "error": "کد اشتباه است.", "dir": dir},
                )
            if dir == "signup":
                # Redirect to the signup view with the code
                return redirect("account:signup", code=code)
            elif dir == "pass":
                # Redirect to the forgetPass view with the code
                return redirect("account:forgetPass", code=code)
            else:
                # Handle an invalid 'dir' value
                return render(request, "404.html")
    # Display the initial verification form in the 'status' 1
    return render(request, "account/verify.html", {"status": "1", "dir": dir})


# ------------------------------------------------------------------


def forgetPass(request: HttpRequest, code: str) -> HttpRequest | HttpResponseRedirect:
    """
    View for handling the 'forget password' process.

    This view allows users to reset their password after verifying their identity with a valid code.

    Args:
        request (HttpRequest): The HTTP request object.
        code (str): The verification code used to reset the password.

    Returns:
        HttpRequest or HttpResponseRedirect: Depending on the verification and password reset process,
        the view may return an HTTP response for rendering a password reset form, redirect to the 'verify' view,
        or redirect to the 'login' view with a success or error message.

    Exceptions:
        - If the 'ver_code' object with the entered code does not exist, it means the code is invalid.
          In this case, the view will redirect to the 'verify' view for re-verification.

    Alternatives:
        - If the code is invalid or not found, users are redirected to the 'verify' view to start the verification process again.
        - If the entered phone number (username) does not match the code's phone number, an error message is displayed.
        - If the user with the provided phone number does not exist, an error message is displayed.

    """
    try:
        var = ver_code.objects.get(code=code)
    except ver_code.DoesNotExist:
        # Handle an invalid code by redirecting to the 'verify' view
        return redirect("account:verify")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if var.phone == str(username):
            try:
                user = Account.objects.get(username=var.phone)
            except Account.DoesNotExist:
                # Handle the case where the user does not exist
                return render(request, "account/forgetPass.html", {"error": "user404"})

            # Reset the user's password and activate the account
            user.set_password(password)
            user.is_active = True
            user.save()
            return render(
                request,
                "account/login.html",
                {"message": "رمز عبور با موفقیت تغییر کرد وارد شوید!"},
            )
        else:
            # Handle phone number mismatch
            return render(request, "account/forgetPass.html", {"error": "notMatch"})

    # Display the password reset form with the phone number
    return render(request, "account/forgetPass.html", {"phone": var.phone})


# ------------------------------------------------------------------


def signup(request: HttpRequest, code: str) -> HttpRequest | HttpResponseRedirect:
    """
    View for user registration and signup.

    This view allows users to sign up and create an account. It handles both regular user registration and registration
    after receiving a verification code via SMS.

    Args:
        request (HttpRequest): The HTTP request object.
        code (str): The verification code used to complete the signup process.

    Returns:
        HttpRequest or HttpResponseRedirect: Depending on the signup process and its success or errors, the view may return an HTTP response for rendering a signup form, redirect to the 'verify' view, or redirect to the 'signupBusiness' view.

    Exceptions:
        - If the 'ver_code' object with the entered code does not exist, it means the code is invalid.
          In this case, the view will redirect to the 'verify' view for re-verification.

    Alternatives:
        - If the code is invalid or not found, users are redirected to the 'verify' view to start the verification process again.
        - After successful registration, users are redirected to the 'signupBusiness' view for additional setup.

    """
    if request.user.is_authenticated:
        messages.warning(request, "شما هم اکنون در حساب کاربری خود هستید.")
        return redirect("dashboard:account_overview")

    errorlist = []

    try:
        var = ver_code.objects.get(code=code)
    except ver_code.DoesNotExist:
        # Handle an invalid code by redirecting to the 'verify' view
        return redirect("account:verify")

    if request.method == "POST":
        try:
            user = Account.objects.get(username=var.phone)
            if not user.is_active:
                # Complete the registration process with user details
                name = request.POST.get("name")
                email = request.POST.get("email")
                password = request.POST.get("password")
                user.name = name
                user.email = email
                user.set_password(password)
                user.is_active = True
                user.save()
                var.delete()
                login(request, user)
                smsSender(
                    number=user.username,
                    message="ممنون که ثبت نام کردید به سورجی خوش آمدید www.soorchi.com",
                )
                return redirect("account:signupBusiness")
            else:
                var.delete()
                errorlist.append("این شماره تلفن قبلا ثبت نام کرده است. از فراموشی رمز عبور اقدام کنید.")
                form = PersonDetailForm()
                return render(request, "account/signup.html", {"form": form, "errors": errorlist})
        except Account.DoesNotExist:
            # Handle registration using the 'PersonDetailForm'
            form = PersonDetailForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = var.phone
                try:
                    user.save()
                except Exception as inst:
                    return render(request, "error.html", {"error": inst})
                var.delete()
                login(request, user)
                smsSender(
                    number=user.username,
                    message="ممنون که ثبت نام کردید به سورجی خوش آمدید www.soorchi.com",
                )
                return redirect("account:signupBusiness")
            else:
                for fields in form:
                    try:
                        errorlist.append(form.errors[fields.name][0])
                    except:
                        pass
                var.delete()
                form = PersonDetailForm()
                return render(request, "account/signup.html", {"form": form, "errors": errorlist})
    else:
        form = PersonDetailForm()

    return render(request, "account/signup.html", {"form": form})


# ------------------------------------------------------------------


@login_required
def signUpBusiness(request: HttpRequest):
    """
    View for business signup and profile creation.

    This view allows authenticated users to create a business profile and provide various details about their business.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: After successful business profile creation, users are redirected to the 'account_offer_templates' view.

    """
    account = request.user
    if request.method == "POST":
        B_name = request.POST.get("B_name")
        # category = Category.objects.filter(id=int(request.POST.get("category")))
        # Nationalcode = request.POST.get("Nationalcode")
        # web_address = request.POST.get("web_address")
        # social_network = request.POST.get("social_network")
        # shop_address = request.POST.get("shop_address")
        # description = request.POST.get("description")
        # B_phone = request.POST.get("B_phone")
        # online = True if request.POST.get("online") == "on" else False
        # ofline = True if request.POST.get("ofline") == "on" else False
        # profile_image = request.FILES.get("profile_image")

        if len(Business.objects.filter(account=account)) == 0:
            bu = Business(
                account=account,
                B_name=B_name,
                # Nationalcode=Nationalcode,
                # web_address=web_address,
                # social_network=social_network,
                # shop_address=shop_address,
                # description=description,
                # B_phone=B_phone,
                # online=online,
                # ofline=ofline,
                # profile_image=profile_image,
            )
            bu.save()
            # bu.category.set(category)
            bu.subscription = 1
            bu.save()
            account.is_Business = True
            account.save()
    


        return redirect("dashboard:account_offer_templates")

    categories = Category.objects.all()

    return render(request, "dashboard/business_signUp.html", {"categories": categories, "user": account})


# ------------------------------------------------------------------


@login_required
def UpdateAccount(request: HttpRequest) -> HttpResponseRedirect:
    """
    View for updating user account information.

    This view allows authenticated users to update their account information, including personal details,
    contact information, and profile picture.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: After successfully updating the account information, users are redirected to the 'account_info' view.

    Exceptions:
        - The view expects POST requests for updating the account information. If the request method is not POST,
          users are redirected to an 'error' page.

    """
    if request.method == "POST":
        user = request.user
        user.name = request.POST.get("name")
        user.username = request.POST.get("username")
        user.phone = request.POST.get("phone")
        user.country = request.POST.get("country")
        user.city = request.POST.get("city")
        user.email = request.POST.get("email")

        birthday = request.POST.get("birthday")

        # Convert and format the Persian date to a Gregorian date
        birthday = unidecode(f"{birthday}")
        birthday = birthday.split("/")
        birthday = jdatetime.date(int(birthday[0]), int(birthday[1]), int(birthday[2]), locale="fa_IR")
        birthday = jdatetime.date.togregorian(birthday)
        birthday = f"{birthday.strftime('%Y-%m-%d')}"
        user.birthday = birthday
        user.gender = request.POST.get("gender")
        user.education = request.POST.get("education")
        user.social_media = request.POST.get("social_media")
        user.address = request.POST.get("address")
        user.profile_image = request.FILES.get("profile_image")
        user.save()

        return redirect("dashboard:account_info")
    else:
        return render(request, "error.html")


# ------------------------------------------------------------------


@login_required
def UpdateBusiness(request: HttpRequest) -> HttpResponseRedirect:
    """
    View for updating business profile information.

    This view allows authenticated users with a business profile to update their business information, including
    business name, contact details, and profile picture.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: After successfully updating the business profile information, users are redirected to the 'account_info' view.

    Exceptions:
        - The view expects POST requests for updating the business information. If the request method is not POST,
          users are redirected to an 'error' page.

    """
    if request.method == "POST":
        user = request.user
        business = Business.objects.get(account=user)
        business.B_name = request.POST.get("B_name")
        business.Nationalcode = request.POST.get("Nationalcode")
        business.web_address = request.POST.get("web_address")
        business.social_network = request.POST.get("social_network")
        business.shop_address = request.POST.get("shop_address")
        business.B_phone = request.POST.get("B_phone")
        business.profile_image = request.FILES.get("profile_image")
        business.save()

        return redirect("dashboard:account_info")
    else:
        return render(request, "error.html")


# ------------------------------------------------------------------


@login_required
def updateBusiness(request: HttpRequest, business_id: int) -> HttpResponseRedirect:
    """
    View for updating business profile information.

    This view allows authenticated users to update their business profile information, including
    category, social network, shop address, description, phone number, and profile picture.

    Args:
        request (HttpRequest): The HTTP request object.
        business_id (int): The ID of the business profile to be updated.

    Returns:
        HttpResponseRedirect: After successfully updating the business profile information, users are redirected to the 'account_overview' view.

    """
    DEFAULT_CATEGORY_ID = 1
    business = Business.objects.get(id=business_id, account=request.user)
    if request.method == "POST":
        category_id = request.POST.get("category")
        if category_id is None:
            category_id = DEFAULT_CATEGORY_ID
        category = Category.objects.get(id=int(category_id))
        social_network = request.POST.get("social_network")
        if social_network is None:
            social_network = business.social_network
        shop_address = request.POST.get("shop_address")
        if shop_address is None:
            shop_address = business.shop_address
        description = request.POST.get("description")
        if description is None:
            description = business.description
        B_phone = request.POST.get("B_phone")
        if B_phone is None:
            B_phone = business.B_phone
        profile_image = request.FILES.get("profile_image")
        if profile_image is None:
            profile_image = business.profile_image

        business.B_name = business.B_name  # No change in business name
        business.Nationalcode = business.Nationalcode  # No change in national code
        business.web_address = business.web_address  # No change in web address
        business.social_network = social_network
        business.shop_address = shop_address
        business.description = description
        business.B_phone = B_phone
        business.online = business.online
        business.ofline = business.ofline
        business.category.set([category])
        business.profile_image = profile_image

        business.save()

        return redirect("dashboard:account_overview")


# ------------------------------------------------------------------

import os
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import Http404
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from Products.models import Product
from payment.models import  order
from account.models import Business, Account
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from text_unidecode import unidecode
from openpyxl import Workbook

from core import common_functions

ipList = []

@login_required(login_url='account:login')
def account_overview(request):
    """
    View for the home page of the dashboard.

    Displays the user's account information and handles account editing.

    Requires user authentication.

    Returns:
        Rendered HTML template: account_overview.html
    """

    user = request.user

    # Bar chart - Number of customers signed up for offers by date
    offers = Offer.objects.filter(owner=user)
    customers_by_date = (
        Customer.objects.filter(offer__in=offers)
        .annotate(date=TruncDate('date_participate'))
        .values('date')
        .annotate(total_customers=Count('id'))
        .order_by('date')
    )

    # Pie chart - Number of customers per offer
    pie_labels = []
    pie_data = []
    for offer in offers:
        customers_count = Customer.objects.filter(offer=offer).count()
        pie_labels.append(offer.title)
        pie_data.append(customers_count)

    # Line chart - Number of customers for the last offer by date
    last_offer = offers.last()
    last_offer_customers_by_date = (
        Customer.objects.filter(offer=last_offer)
        .annotate(date=TruncDate('date_participate'))
        .values('date')
        .annotate(total_customers=Count('id'))
        .order_by('date')
    )

    # Table - Last 10 customers for the last offer
    last_offer_customers = (
        Customer.objects.filter(offer=last_offer)
        .order_by('-date_participate')[:10]
    )

    context = {
        'bar_chart_labels': [entry['date'].strftime('%Y-%m-%d') for entry in customers_by_date],
        'bar_chart_data': [entry['total_customers'] for entry in customers_by_date],
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'line_chart_labels': [entry['date'].strftime('%Y-%m-%d') for entry in last_offer_customers_by_date],
        'line_chart_data': [entry['total_customers'] for entry in last_offer_customers_by_date],
        'last_offer_customers': last_offer_customers,
        'last_offer' : last_offer,
    }
    path = request.path
    context['path'] = path
    return render(request, 'dashboard/account_overview.html', context)

# ----------------------------------------------------------------------

@login_required(login_url="account:login")
def account_info(request):
    """
    View for displaying the user's account information.

    Retrieves the user's account information and profile details from the database.

    Requires user authentication.

    Returns:
        Rendered HTML template: account_info.html
    """

    # Get user's account information
    user_account = Account.objects.get(id=request.user.id)

    context = {
        'account': user_account,
        'path': request.path,
    }

    if user_account.is_Business:
        # Get business account information
        user_business = Business.objects.get(account=user_account)
        user_subscription = Subscription.objects.get(id=user_business.subscription)
        context.update({
            'business': user_business,
            'subscription': user_subscription,
        })
    else:
        context["message"] = "برای استفاده از امکانات  ارسی نیاز به اکانت کسب و کار دارید."

    return render(request, 'dashboard/account_info.html', context)

# ---------------------------------------------------------------------------

@login_required(login_url='account:login')
def account_orders(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    View for displaying the user's orders.

    Retrieves the user's business account and fetches the orders associated with it.

    Requires user authentication.

    Returns:
        Rendered HTML template: account_orders.html
    """
    user = request.user
    context = {}
    try:
        business = Business.objects.get(account=user)
    except:
        return redirect("account:signupBusiness")

    orders = business.orders.all()

    context = {
        'orders': orders,
        'path': request.path,
    }
    return render(request, 'dashboard/account_orders.html', context)

# ----------------------------------------------------------------------

@login_required(login_url='account:login')
def account_offers(request):
    """
    View for displaying the user's offers.

    Retrieves the offers created by the user.

    Requires user authentication.

    Returns:
        Rendered HTML template: account_offers.html
    """
    offers = request.user.offers.all().order_by("-id")

    paginator = Paginator(offers, 30)   # show up to 30 offers in one page
    page = request.GET.get('page')
    paged_list = paginator.get_page(page)
    
    context = {
        'offers': offers,
        'path': request.path,
        'offers_pages_list': paged_list,
    }

    return render(request, 'dashboard/account_offers.html',context)

# ----------------------------------------------------------------------

@login_required(login_url='account:login')
def account_offers_export(request: HttpRequest) -> HttpResponse:
    """
    View for exporting user's offer data to an Excel file.

    Parameters:
    - request (HttpRequest): The HTTP request from the user.

    Returns:
    - HttpResponse: An HTTP response containing the Excel file for download.

    This view exports the user's offer data to an Excel file. The exported data includes offer details such as
    ID, title, start date, end date, and landing page URL.

    The view performs the following steps:
    1. Create an HttpResponse with the content type set to 'application/ms-excel'.
    2. Set the filename for the downloaded Excel file, using the user's username and '-offers.xlsx'.
    3. Create an Excel workbook (openpyxl) and add a worksheet with the title 'کمپین ها' (campaigns).
    4. Add column headers to the worksheet, including: 'شناسه' (ID), 'عنوان' (Title), 'تاریخ شروع' (Start Date),
       'تاریخ پایان' (End Date), and 'آدرس کمپین' (Landing Page).
    5. Fetch the user's offers from the database (Offer objects) and add their details to the worksheet.
    6. Save the workbook to the HttpResponse as an Excel file.
    7. Return the HttpResponse for the user to download the Excel file.

    This view ensures that only logged-in users can access it. Users can export their offer data by
    navigating to the specified URL.

    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{request.user}-offers.xlsx"'
    
    # create Workbook and Worksheet and set sheet title
    wb = Workbook()
    ws = wb.active
    ws.title = "کمپین ها"
    
    # Add Columns titles
    headers = ("شناسه", "عنوان", "تاریخ شروع", "تاریخ پایان", "آدرس کمپین")
    ws.append(headers)

    # Add data from the model
    offers = Offer.objects.filter(owner=request.user)
    for offer in offers:
        ws.append((offer.id, offer.title, str(offer.JaliliStartDate()), str(offer.JaliliEndDate()), offer.landingPage))

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response

# ----------------------------------------------------------------------

@login_required(login_url='account:login')
def account_customers(request, offer_id):
    """
    View for displaying the offer's customers.

    Retrieves the customers associated with the user's offer.

    Requires user authentication.

    Returns:
        Rendered HTML template: account_customers.html
    """

    offer = Offer.objects.get(id=offer_id)
    customers = offer.customers.all().order_by('-score')
    
    search_input = request.GET.get('search-area') or ''
    if search_input:
        customers = Customer.objects.filter(account__username=search_input).order_by('-score')
    
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    customers_paged_list = paginator.get_page(page)
    
    if request.method == 'POST':
        score = request.POST.get('score')

        if score:
            try:
                score = int(score)
                results = Customer.objects.filter(score=score)
            except ValueError:
                # Handle the case where the provided score is not an integer
                results = []
        else:
            results = []
    else:
        results = []

        context = {
            'offer': offer, 
            'customers': customers_paged_list,
            'results':results,
            'search_input': search_input,
        }

    return render(request, 'dashboard/account_customers.html',context=context)


# ----------------------------------------------------------------------

@login_required(login_url='account:login')
def account_customers_export(request: HttpRequest , offer_id: int) -> HttpResponse:
    """
    View for exporting customer data of a specific offer to an Excel file.

    Parameters:
    - request (HttpRequest): The HTTP request from the user.
    - offer_id (int): The ID of the specific offer for which customer data should be exported.

    Returns:
    - HttpResponse: An HTTP response containing the Excel file for download.

    This view exports customer data of a specific offer to an Excel file. The exported data includes customer details
    such as row number, name, email, phone number, score, viral counter, participation date, and prize.

    The view performs the following steps:
    1. Retrieve the specific offer using the provided `offer_id`.
    2. Create an HttpResponse with the content type set to 'application/ms-excel'.
    3. Set the filename for the downloaded Excel file, including the user's username, offer title, and '-customers.xlsx'.
    4. Create an Excel workbook (openpyxl) and add a worksheet with the title 'کمپین ها' (campaigns).
    5. Add column headers to the worksheet, including: 'ردیف' (Row), 'نام' (Name), 'ایمیل' (Email),
       'شماره تلفن' (Phone Number), 'امتیاز' (Score), 'تعداد وایرال' (Viral Counter),
       'تاریخ مشارکت' (Participation Date), and 'جایزه' (Prize).
    6. Fetch customer data related to the specific offer from the database (Customer objects) and add their details to the worksheet.
    7. Save the workbook to the HttpResponse as an Excel file.
    8. Return the HttpResponse for the user to download the Excel file.

    This view ensures that only logged-in users can access it. Users can export customer data for a specific offer by
    navigating to the specified URL and providing the offer's ID.
    """
    offer = Offer.objects.get(id=offer_id)
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{request.user}-{offer.title}-customers.xlsx"'
    
    # create Workbook and Worksheet and set sheet title
    wb = Workbook()
    ws = wb.active
    ws.title = "کمپین ها"
    
    # Add Columns titles
    headers = ("ردیف", "نام", "ایمیل", "شماره تلفن", "امتیاز", "تعداد وایرال", "تاریخ مشارکت", "جایزه")
    ws.append(headers)

    # Add data from the model
    customers = Customer.objects.filter(offer=offer).order_by('-score')
    
    phone = request.GET.get('phone') or None
    if phone:
        customers = customers.filter(account__username=phone).order_by('-score')
    
    for index,customer in enumerate(customers,start=1):
        gift = customer.Gift.name if customer.Gift else "نگرفته"
        ws.append((
            index,
            customer.account.name,
            customer.account.email,
            customer.account.username,
            customer.score,
            customer.viral_counter,
            str(customer.JaliliDateParticipate()),
            gift
        ))

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response

# ----------------------------------------------------------------------

def customer_search(request,offer_id):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        print(type(phone))
        print('phone',phone)
        results = []

        if phone:
            try:

                account=Account.objects.get(username=phone)
                print('acoount',account)
                offer = Offer.objects.get(id=offer_id)
                results=Customer.objects.filter(offer=offer,account=account)

            except ValueError:
                # Handle the case where the provided score is not an integer
                pass

        data = results
        # data = [{'score': customer.score} for customer in results]
        print('res',data)
        alldata = render_to_string('dashboard/account_customers_search.html', {'data': data})
        return JsonResponse({'data': alldata})

# ----------------------------------------------------------------------

def fetch_customers(request,offer_id):

    selected_customers_date_ids = request.GET.getlist('customers')
    start_date = common_functions.jalali_to_gregorian(selected_customers_date_ids[0])

    offer = Offer.objects.get(id=offer_id)
    allCustomer = offer.customers.all()

    if len(selected_customers_date_ids) > 0:
        allCustomer = allCustomer.filter(offer=offer,date_participate__date__in=[start_date]).distinct()

    alldata = render_to_string('dashboard/account_customers_fiter.html', {'data': allCustomer})
    return JsonResponse({'data': alldata})

# ----------------------------------------------------------------------

def fetch_offers(request):

    selected_offers_date_ids = request.GET.getlist('offers')
    start_date = common_functions.jalali_to_gregorian(selected_offers_date_ids[0])

    all_offers = Offer.objects.all().order_by('start_date')
    if len(selected_offers_date_ids) > 0:
        all_offers = all_offers.filter(start_date__date__in=[start_date]).distinct()
    alldata = render_to_string('dashboard/account_offers_fiter.html', {'data': all_offers})
    return JsonResponse({'data': alldata})

# ----------------------------------------------------------------------

def calculate_age_range(birth_date):
    if birth_date is None:
        return None
    today = timezone.now().date()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

# ----------------------------------------------------------------------

@login_required(login_url="account:login")
def offer_analysis(request: HttpRequest):
    """
    View for displaying the offer's analysis.

    Retrieves the analysis associated with the user's offer.

    Requires user authentication.

    Returns:
        Rendered HTML template: offer_analysis.html
    """
    user = request.user
    offer_id = request.GET.get('offer', None)

    if offer_id is not None:
        # Get the offer based on the offer ID
        offer = Offer.objects.get(id=offer_id)

        # Get the customers associated with the offer
        customers = Customer.objects.filter(offer=offer)

        # Extract the account objects from the customers
        customer_accounts = [customer.account for customer in customers]

        # Age range chart - Number of customers based on age range
        age_ranges = ['<18', '18-24', '25-34', '35-44', '45-54', '55+']
        age_data = [0] * len(age_ranges)

        for customer in customers:
            age = calculate_age_range(customer.account.birthday)
            if age is not None:
                if age < 18:
                    age_data[0] += 1
                elif age < 25:
                    age_data[1] += 1
                elif age < 35:
                    age_data[2] += 1
                elif age < 45:
                    age_data[3] += 1
                elif age < 55:
                    age_data[4] += 1
                else:
                    age_data[5] += 1

        # Education chart - Number of customers based on education level
        education_levels = ['زیردیپلم', 'دیپلم', 'کاردانی', 'کارشناسی', 'کارشناسی ارشد', 'دکتری']
        education_data = [0] * len(education_levels)

        for account in customer_accounts:
            if account.education == 'زیردیپلم':
                education_data[0] += 1
            elif account.education == 'دیپلم':
                education_data[1] += 1
            elif account.education == 'کاردانی':
                education_data[2] += 1
            elif account.education == 'کارشناسی':
                education_data[3] += 1
            elif account.education == 'کارشناسی ارشد':
                education_data[3] += 1
            elif account.education == 'دکتری':
                education_data[3] += 1

        # Pie chart - Number of customers based on gender
        gender_counts = (
            Account.objects.filter(id__in=[account.id for account in customer_accounts])
            .values('gender')
            .annotate(count=Count('gender'))
        )

        gender_data = [count['count'] for count in gender_counts]
        pie_data = gender_data

        # Assign gender labels based on the actual values
        gender_labels = ['مرد' if count['gender'] == 'مرد' else 'زن' for count in gender_counts]
        pie_labels = gender_labels

        # Line chart - Number of customers for the last offer by date
        last_offer_customers_by_date = (
            customers
            .annotate(date=TruncDate('date_participate'))
            .values('date')
            .annotate(total_customers=Count('id'))
            .order_by('date')
        )

        # Prepare the context for rendering the template
        context = {
            'customers': customers,
            'offer': offer,
            'age_ranges': age_ranges,
            'age_data': age_data,
            'education_levels': education_levels,
            'education_data': education_data,
            'pie_labels': pie_labels,
            'pie_data': pie_data,
            'line_chart_labels': [entry['date'].strftime('%Y-%m-%d') for entry in last_offer_customers_by_date],
            'line_chart_data': [entry['total_customers'] for entry in last_offer_customers_by_date],
        }

        return render(request, 'dashboard/offer_analysis.html', context)
    else:
        raise Http404("Offer parameter is missing.")

# ----------------------------------------------------------------------

@login_required(login_url="account:login")
def account_viral(request):
    """
    View for displaying the user's viral count.

    Retrieves the viral counter for the user's customer account.

    Requires user authentication.

    Returns:
        Rendered HTML template: account_viral.html
    """
    user = request.user
    customer = Customer.objects.filter(id=user.id).first()
    viral_counter = customer.viral_counter if customer else None

    context = {
        'viral_counter': viral_counter,
        'path': request.path,
    }
    return render(request, 'dashboard/account_viral.html', context)

# ----------------------------------------------------------------------

@login_required(login_url="account:login")
def account_offer_templates(request):  
    try:
        business = Business.objects.get(account=request.user)
    except:
        return redirect("account:signupBusiness")
    
    free_subscription = Subscription.objects.get(id=1)
    free_templates = free_subscription.OfferTemplates.all()
    
    business_orders = order.objects.filter(buyerBussiness=business, Expiration_date__gt=timezone.now())    
    business_subscriptions = [order.plan for order in business_orders]
    
    business_templates = set(template for subscription in business_subscriptions for template in subscription.OfferTemplates.all().order_by('slug'))
    business_templates.update(free_templates)
    non_free_templates = OfferTemplate.objects.exclude(id__in=[template.id for template in business_templates]).order_by("slug")
    
    context = {
        'business_templates': business_templates,
        'business_subscriptions': business_subscriptions,
        'non_free_templates': non_free_templates,
        'path': request.path,
    }

    return render(request, "dashboard/account_offer_templates.html", context)

# ----------------------------------------------------------------------

def catalog(request):
    """
    View for displaying the catalog of games.

    Retrieves a list of games from the database and renders the catalog page.

    Returns:
        Rendered HTML template: catalog.html
    """
    games = []
    html5games = []
    html5games_id = []
   
    game_list = eval(os.environ.get('GAME_LIST'))
    
    for i in game_list:
        games.append(Offer.objects.get(id=i))
        if HTML5OfferDetail.objects.filter(offer_detail=Offer.objects.get(id=i)):
            html5games.append(HTML5OfferDetail.objects.get(offer_detail=Offer.objects.get(id=i)))
            html5games_id.append(HTML5OfferDetail.objects.get(offer_detail=Offer.objects.get(id=i)).offer_detail.id)
    context = {"games": games, "html5games":html5games, "html5games_id":html5games_id}
    return render(request, "dashboard/catalog.html", context)

# ----------------------------------------------------------------------

def preview(request, id):
    """
    View for displaying the catalog of games.

    Retrieves a list of games from the database and renders the catalog page.

    Returns:
        Rendered HTML template: catalog.html
    """


    gameList ={"Q01y01m02d18":"https://sorchi.com/landing/117",
               "MQ04y01m03d24":"https://sorchi.com/landing/232",
               "R03y01m03d04":"https://sorchi.com/landing/118",
               'MQ05y01m09d21':'https://sorchi.com/landing/232',
               "my11y01m10d02":"https://sorchi.com/landing/117",
               "PU07y01m12d11":"https://sorchi.com/landing/249",
               "BUIL02y01m16d":"https://sorchi.com/landing/267",
               "H5y02m04d27-2":"https://soorchi.com/static/demos/G2.html",
               "H5y02m04d27-4":"https://soorchi.com/static/demos/G4.html",
    }
    offer = OfferTemplate.objects.get(id = id)
    ChCode = eval(offer.ChallengeCode)
    try:    
        x = gameList[ChCode[0]]
        
    except:
        x = "dashboard:catalog"
    return redirect(x)

# ----------------------------------------------------------------------

def clickDashboard(request):
    """
    View for the click dashboard.

    Retrieves the authenticated user's account and fetches the associated offer clicks.

    Returns:
        Rendered HTML template: clickDashbord.html
    """
    try:
        Acc = request.user
    except:
        return render(request, "404.html")
    offer_clicks = ClickCounter.objects.filter(account=Acc)
    return render(request, "dashboard/clickDashbord.html", {'OFC': offer_clicks})

# ----------------------------------------------------------------------

def click_center(request, id):
    """
    View for handling offer clicks.

    Registers a click for the specified offer and redirects the user to the offer's landing page.
    The click is only registered if the user's IP address is not already recorded.

    Args:
        id (int): The ID of the offer being clicked.

    Returns:
        Redirect to the offer's landing page.
    """
    global ipList
    offer = Offer.objects.get(id=id)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ipList:
        ipList.append(ip)
        Distributor_code = request.GET.get('D', None)
        if Distributor_code is not None:
            try:
                obj = ClickCounter.objects.get(code=Distributor_code)
                print(obj.click)
                obj.click += 1
                obj.save()
            except:
                pass

    # with open('ips.txt', 'a') as f:
    #     f.write(str(ipList))
    if len(ipList) > 500:
        ipList = []
    return redirect(offer.landingPage)

# ----------------------------------------------------------------------

def getPhone(request, id):
    """
    View for retrieving phone numbers.

    Retrieves the phone numbers of customers associated with the specified offer.

    Args:
        id (int): The ID of the offer.

    Returns:
        Rendered HTML template: plist.html
    """
    offer = Offer.objects.get(id=id)
    obj = Customer.objects.filter(offer=offer)
    for i in obj:
        with open('phone.txt', 'a') as f:
            f.write(i.account.phone + "\n")
    return render(request, 'dashboard/plist.html', {'obj': obj})


# ----------------------------------------------------------------------

@login_required(login_url="account:login")
def subscription(request):
    SMS = Subscription.objects.filter(code = "SMS")
    TOT = Subscription.objects.filter(code = "TOT")
    sub_name = request.GET.get('search-area', '')
    if sub_name:
        TOT = TOT.filter(title__icontains=sub_name)
    
    try:
        user_business = Business.objects.get(account=request.user)
        business_orders = order.objects.filter(
            buyerBussiness=user_business, Expiration_date__gt=timezone.now()
        )
        business_subscriptions = [order.plan for order in business_orders]
    except:
        business_subscriptions = []
    
    
    context = {
        "SMS": SMS,
        "TOT": TOT,
        "business_subs": business_subscriptions,
        "search_input": sub_name,
    }
    return render(request, 'dashboard/Subscription.html', context)

# ----------------------------------------------------------------------

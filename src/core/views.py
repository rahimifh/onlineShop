from django.shortcuts import render
from django.utils import timezone

from Products import models as pruduct_models
from payment import models as payment_models
from account import models as account_models


def Core(request):
    context = {}
    lastOffers = pruduct_models.Product.objects.filter(available=True)[:5]
    lastTemplates = pruduct_models.Category.objects.order_by("slug")[:4]
    context["lastOffers"] =  lastOffers #lastOfferslastOffers.order_by("-start_date")
    context["lastTemplates"] = lastTemplates
    return render(request, "core/landing.html", context)


def last_games(request):
    context = {}
    lastOffers = pruduct_models.Offer.objects.filter(finall_check=True)
    context["lastOffers"] =  lastOffers.order_by("-start_date")
    return render(request, "core/last_games.html", context)


# ----------------------------------------------------------------


def aboutUs(request):
    return render(request, "core/aboutUs.html")


# ----------------------------------------------------------------
def vip_projects(request, switch):
    match switch:
        case "daity":
            path = "vip/daity/index.html"
        case "anten":
            path = "vip/anten/index.html"
        case "roja":
            path = "vip/roja/index.html"
        case "xvision":
            path = "vip/xvision/index.html"
    return render(request, "core/vip_landing.html", {"path":path})

#-----------------------
def priceTable(request):
    subscriptions = payment_models.Subscription.objects.all()

    try:
        user_business = account_models.Business.objects.get(account=request.user)
        business_orders = payment_models.order.objects.filter(
            buyerBussiness=user_business, Expiration_date__gt=timezone.now()
        )
        business_subscriptions = [order.plan for order in business_orders]
    except:
        business_subscriptions = []

    context = {
        "subscriptions": subscriptions,
        "business_subs": business_subscriptions,
    }
    return render(request, "core/priceTable.html", context=context)


# ----------------------------------------------------------------


def examble(request):
    context = {}
    offers = pruduct_models.OfferTemplate.objects.all().order_by("slug")

    context["offers"] = offers
    return render(request, "core/examble.html", context)


# ----------------------------------------------------------------
def process_data(code):
    path = f"game/{code}/index.html"
    
    match code:
        case "MQ05y01m09d21":
            data = {
        "type": "Data",
        "StartingTime": 60,
        "ScoreValue": 10,
        "Questions": [
            [
                " ارسی ابزار ساخت کدام روش تبلیغاتی است؟",
                "تبلیغات تعاملی",
                "تبلیغات کلیکی",
                "تبلیغات اینفلوانسری",
                "تبلیغات ویدئوی",
                "https://soorchi.com/media/blog/2024/1/29/hneg7fbeyv.png",
            ],
            [
              "ساخت یک بازی تبلیغاتی در  ارسی چقدر زمان خواهد برد؟ ",
                "کمتر از نیم ساعت",
                "5 ساعت",
                "1 روز",
                "1 هفته",
                "https://soorchi.com/media/blog/2024/1/29/njxwyl320t.png",
            ],
            [
                " چه مهارتی برای ساخت بازی تبلیغاتی در  ارسی نیاز است؟",
                "هیچکدام",
                "برنامه نویسی",
                "طراح کاربری",
                "گرافیک ",
                "https://soorchi.com/media/blog/2024/1/29/5hr8i6yv9e.png",
            ],
            [
               "کدام بازی باعث افزایش تعامل شما با مخاطب میشوند؟",
               "همه موارد",
                "گردونه شانس",
                "کوییزی",
                "پیلینکو",
                "https://soorchi.com/media/blog/2024/1/29/tiqlhrv4o3.png",
            ],
            [
               "کدام ویژگی در  ارسی به وایرال شدن بازی کمک کند؟ ",
                "دعوت از دوستان",
                "گرافیک بازی",
                "سورلینک",
                "تخفیف لایه ای",
                "https://soorchi.com/media/blog/2024/1/29/5vijqswm1e.png",
            ],


        ],
        "StartPopupText": "سلام \n خوش اومدی! \n\n شما [x] ثانیه وقت داری تا به [y] سوال جواب بدی.",
        "BgColor": "#330077",
        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
    }

        case "MQ04y01m03d24":
            path = f"game/MQ05y01m09d21/index.html"
            data = {
        "type": "Data",
        "StartingTime": 60,
        "ScoreValue": 10,
        "Questions": [
            [
                "نام این حیوان چیست؟",
                "سیاهگوش اوراسیا",
                "پانترا اونکا",
                "کاراکال",
                "وحشی بافقی",

            ],
            [
                "چه معبد تاریخی مشهور در شهر شیراز واقع شده است؟",
                "معبد زرتشت",
                "معبد فاروهر",
                "معبد انوشیروان",
                "معبد اردیبهشت",

            ],
            [
                "کدام پادشاه هخامنشی ایران، سیاست‌های توسعه‌ای و ساختار دولتی را تقویت کرد؟",
                "داریوش بزرگ",
                "کمبوجیه",
                "کامبیسه",
                "کوروش بزرگ",
          
            ],
            [
                "نام این ورزش چیست؟",
                "سپک تاکرا",
                "پینگ پونگ فضایی",
                "والیبال پایی",
                "واترپولو",
            ],
            [
                "تیم ملی فوتبال ایران در چندین دوره از جام جهانی شرکت کرده است؟",
                "5",
                "6",
                "7",
                "10",
            
            ],
            [
                "کدام شهر ایران به عنوان پایتخت باستانی ایران شناخته می‌شود؟",
                "پرسپولیس",
                "پرتوک",
                "هگمتانه",
                "شوش",
          
            ],
            [
                "مراسم سنتی معروف در ایران که به شکل موسیقی و رقص جشن گرفته می‌شود چه نام دارد؟",
                "چهارشنبه‌ سوری",
                "مهرجان",
                "نوروز",
                "سیزده‌ بدر",

            ],
        ],
        "StartPopupText": "سلام \n خوش اومدی! \n\n شما [x] ثانیه وقت داری تا به [y] سوال جواب بدی.",
        "BgColor": "#330077",
        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
    }

        case "my11y01m10d02":
            data = {
                        "type": "Data",

                        "StartingTime": 60,

                        "Images": [
                            "https://soorchi.com/media/blog/2024/1/29/clhlbyyoff.png",
                            "https://soorchi.com/media/blog/2024/1/29/5dlk2kbhvi.png",
                            "https://soorchi.com/media/blog/2024/1/29/n9hcgja8tz.png",
                            "https://soorchi.com/media/blog/2024/1/29/3epps7gwsj.png",
                        ],

                        "Word": "بیمه موبایل",

                        "LettersCount": 16,

                        "StartPopupText": "سلام \n خوش اومدی! \nبا توجه به تصاویر خدمت مارا حدس بزنید",
        

                        "BgColor": "#330077",

                        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",

                    }
        case "Pli02m08d24":
            data = {
                        "type" : "Data",
                        "BallSize": 80,
                        "PegSize": 25,
                        "StartingPegs": 2,
                        "ItemsSide": 0,
                        "Items": [
                            [
                                "پوچ",
                                10
                            ],
                            [
                                "کد تخفیف 30%",
                                40
                            ],
                            [
                                "کد تخفیف 40%",
                                5
                            ],
                            [
                                "کد تخفیف 50%",
                                20
                            ],
                            [
                                "کد تخفیف 60%",
                                45
                            ],
                            [
                               "کد تخفیف 70%",
                                5
                            ],
                            [
                                "کد تخفیف 80%",
                                10
                            ],
                            [
                                "پوچ",
                                20
                            ]
                        ],
                        "StartPopupText": "سلام \n خوش اومدی! \n\n توی این چالش شما x تا شانس داری \n اما با هر بار پرتاب توپ، شانس قبلی که بدست آوردی از بین میره. \n",

                        "BallColor": ["Yellow", "Green,Yellow,Red,Blue,Pink,Orange"],
                        "BallChances": 3,
                        "BgColor": "#3e1466",
                        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                    }      
        case "PU07y01m12d11":
            data = {
                        "type": "Data",

                        "StartingTime": 60,

                        "Cards": [
                            "https://soorchi.com/media/blog/2024/1/29/uyvswyyspy.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/dhlrc6bj4c.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/7xfgbw8mn8.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/2kbil8a5n4.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/z0coopxy6d.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/s30c802fvq.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/xxxkqj6o37.jfif",
                            "https://soorchi.com/media/blog/2024/1/29/ygai8rrc7z.png",
                        ],

                        "StartPopupText": "به بازی عکس برگردون خوش اومدی! \n بیشترین امتیاز رو بدست بیار تا برنده جایزه بشی.",

                        "TopPanelColor": "#2aa4c3",

                        "BgColor": "#2942b0",

                        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                    };   
        case "PUZZ02y09m12d":
            data =  {
                        "type": "Data",

                        "StartingTime": 60,

                        "ScoreValue": 10,

                        "Images": [
                            "https://soorchi.com/media/blog/2024/1/29/ieobusu5t6.png",
                            "https://soorchi.com/media/blog/2024/1/29/0dezol3mpn.jpg",
                            "https://soorchi.com/media/blog/2024/1/29/ba1l97csvz.jpg",
                            "https://soorchi.com/media/blog/2024/1/29/7ltfqgl71u.jpg",
                            "https://soorchi.com/media/blog/2024/1/29/u05wlo5fl2.png",
                        ],

                        "Grid": [
                            [[3, 3], ["x", 1, 2], ["y", 1, 3]],
                            [[4, 5], ["x", 1, 2], ["x", 3, 4], ["y", 1, 3], ["y", 4, 5]],
                            [[4, 4], ["x", 1, 2], ["x", 3, 4], ["y", 1, 3], ["y", 3, 4]]
                        ],


                        "StartPopupText": "سلام \n خوش اومدی! \n\n شما [x] ثانیه وقت داری تا [y] تا تصویر رو درست کنی. هر چی زودتر تموم کنی امتیاز بیشتری میگیری.",

                        "BgColor": "#330077",

                        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                    }
  
        case "R03y01m03d04":
            data = {
                        "Items": [
                            "کد تخفیف 20%",
                            "کد تخفیف 30%",
                            "کد تخفیف 40%",
                            "کد تخفیف 50%",
                            "کد تخفیف 60%",
                            "کد تخفیف 70%",
                            "کد تخفیف 80%",
                            "کد تخفیف 90%",

                        ],

                        "Selected": 2,

                        "Colors": ["#4294ba", "#fdb10d", "#e8414b", "#dfeedb"],

                        "BgColor": "#501698",

                        "LogoLink":  "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                    }

        case "DWC02y10m03d":
            data ={
                        "type": "Data",

                        "SecondMultiplier": 0.3,

                        "Score": {
                            "Goal": 1,
                            "Win": 3,
                            "FinalGameWin": 7
                        },

                        "InGameAds": [
                            "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                           "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                            "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png",
                            "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png"
                        ],

                        "StartPopupText": "سلام\nخوش اومدی!\nکشورت رو انتخاب کن و وارد بازی شو. \n با هر گل [x] امتیاز و با هر برد [y] امتیاز بدست میاری.",

                        "LogoLink": "https://soorchi.com/media/blog/2024/1/29/t2u5v2rui6.png"
                    }
        case "jorchin":
            data = {}
            path = "demos/G7.html"
        case "puzzel":
            data = {}
            path = "demos/G6.html"
        case "H5y02m04d27-4":
            data = {}
            path = "demos/G4.html"
        case "dart":
            data= {}
            path = "demos/G8.html"
        case "Knife":
            data = {}
            path = "demos/G10.html"
        case "BUIL02y01m16d":
            data={}
            path ="demos/G9.html"
        case "S02y01m02d018":
            data = {}
            path = "demos/G5.html"

        case _:
            path =None
            data =None

    return data, path


def TemplateDetail(request, id):
    template = pruduct_models.OfferTemplate.objects.get(id=id)
    try:
        code = template.ChallengeCodeList[0]

        data, path = process_data(code)
    except:
        path = None
        data =None

    offers = pruduct_models.OfferTemplate.objects.all().order_by("slug")

    context = {
        "template": template,
        "offers": offers,
        "gamePath": path,
        "data": data
    }
    return render(request, "core/TemplateDetail.html", context)


# ----------------------------------------------------------------

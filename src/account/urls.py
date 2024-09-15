from django.urls import path


from . import views

app_name = "account"

urlpatterns = [
    path("logout/", views.logout_user, name="logout"),
    path("signup/<str:code>/", views.signup, name="signup"),
    path("signupBusiness/", views.signUpBusiness, name="signupBusiness"),
    path("login/", views.login_user, name="login"),
    path("login_s/", views.login_with_sms, name="login_s"),
    path("verify/<str:dir>/", views.verify, name="verify"),
    path("forgetPass/<str:code>/", views.forgetPass, name="forgetPass"),
    path("UpdateAccount/", views.UpdateAccount, name="UpdateAccount"),
    path(
        "updateBusiness/<int:business_id>/", views.updateBusiness, name="updateBusiness"
    ),
    path("UpdateBusiness/", views.UpdateBusiness, name="UpdateBusiness"),
]

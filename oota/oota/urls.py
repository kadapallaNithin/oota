"""oota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users import views as user_views
from home import views as home_views
#from payments import views as payments_views
from payments.views import PostPaidCreateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_views.index,name='home'),
    path(r'error/<str:message>/<str:redirect>/',home_views.error,name='error'),
    path('about/',home_views.about,name='about'),
    path('',include('product.urls')),
    path('',include('payments.urls')),
    path('signup/',user_views.signup,name='signup'),
    path('profile/',user_views.profile,name='profile'),
    #path('postpaid/',payments_views.postpaid,name='post-paid'),
    path('postpaid_create/<int:product_id>',PostPaidCreateView.as_view(),name='postpaid_create'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('password-reset/',
            auth_views.PasswordResetView.as_view(
                template_name='users/password_reset.html'
            ),
            name='password_reset'),
    path('password-reset/done',
            auth_views.PasswordResetDoneView.as_view(
                template_name='users/password_reset_done.html'
            ),
            name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='users/password_reset_confirm.html'
            ),
            name='password_reset_confirm'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
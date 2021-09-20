
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from shop.forms import PasswordChange, Passwordreset,SetPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    path('login/', views.login_attemp),

    path('logout/', auth_views.LogoutView.as_view(next_page='/login'),name='logout'),
    path('changepass/',auth_views.PasswordChangeView.as_view(template_name='changepassword.html',form_class=PasswordChange,
                                                     success_url='/changepassdone/'), name='changepass'),

    path('changepassdone/',auth_views.PasswordChangeDoneView.as_view(template_name='passchangedone.html'),name='passchangedone'),

    path('register/', views.register_attempt,name='register'),
    path('token/', views.token_send),
    path('success/', views.success),
    path('verify/<auth_token>', views.verify, name="verify"),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='pass_reset.html',form_class=Passwordreset),name='password_reset'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='passreset_done.html'),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset_confirm.html',form_class=SetPassword),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetView.as_view(template_name='password_complete.html'),name='password_reset_complete'),

    path('base1/', views.base1),
    path('address/', views.address),
    path('productdtails/<int:pk>', views.ProductDetailVeiw.as_view(),name='product_detail'),
    path('mobile/', views.Mobile,name="mobile"),
    path('mobile/<slug:data>',views.Mobile,name="mobiledata"),

    path('add_to_cart/', views.add_to_cart),
    path('show_cart/',views.show_cart,name='show_cart'),
    path('pluscart/',views.plus_cart,),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.removecart),

    path('checkout/', views.check),
    path('paymentdone/', views.payment_done,name="payment_done"),
    path('profile/', views.ProfileView.as_view(),name='profile'),
    path('order/', views.order),
    path('search/',views.search),
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

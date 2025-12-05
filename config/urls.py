from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from lostandfound import views as lf_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Main application
    path('', include('lostandfound.urls')),

    # Login (custom template)
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    # LOGOUT — FIXED ✔
    path('logout/', lf_views.user_logout, name='user_logout'),

    # Django Auth (password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Media files (images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

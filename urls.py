from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from jiezi import views


urlpatterns = [
    # app urls
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('learning/', include('learning.urls')),
    path('jiezi_admin/', include('jiezi_admin.urls')),

    # front-page urls
    path('index/', views.index, name="index"),
    path('', RedirectView.as_view(url='index')),
    path('about_us/', views.about_us, name="about_us"),
    path('the_science_behind/', views.the_science_behind, name="the_science_behind"),
    path('help/', views.help, name="help"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

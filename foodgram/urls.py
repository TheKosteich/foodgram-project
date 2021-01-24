from django.conf import settings
from django.conf.urls import handler404, handler500  # noqa
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views as fp_views

from recipes.views import get_recipes

handler404 = 'recipes.views.page_not_found'  # noqa
handler500 = 'recipes.views.server_error'  # noqa

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', get_recipes, name='index'),
    path('recipes/', include('recipes.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
]

# flatpages urls
urlpatterns += [
    path('about/author/', fp_views.flatpage,
         {'url': '/about-author/'}, name='about_author'),
    path('about/technologies/', fp_views.flatpage,
         {'url': '/about-technologies/'}, name='about_technologies')
]

# Django urls setting for development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    import debug_toolbar  # noqa

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

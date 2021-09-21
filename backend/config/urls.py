from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/',
        include('recipes.urls')
    ),
#     path(
#         'api/users/',
#         include('users.urls')
#     ),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    #OK http://localhost/api/auth/token/login/ получение токена
    #OK http://localhost/api/auth/token/logout/ удаление токена
]

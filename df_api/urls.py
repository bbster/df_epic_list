from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger Study API",
        default_version="v1",
        description="Swagger Study를 위한 API 문서",

    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', include('df_epic_list.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)/v1$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/v1/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/v1/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]

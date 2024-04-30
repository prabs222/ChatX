from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="ChatX Api Documentation",
        default_version='v3.0',
        description="Description of your API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="prabhakarmishra222@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=(),
)

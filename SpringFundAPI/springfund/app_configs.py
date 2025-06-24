from django.contrib.admin.apps import AdminConfig
from django.contrib.auth.apps import AuthConfig
from django.contrib.contenttypes.apps import ContentTypesConfig


class MyAdminConfig(AdminConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'


class MyAuthConfig(AuthConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'


class MyContentTypesConfig(ContentTypesConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'

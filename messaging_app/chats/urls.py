"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include # 'path' and 'include' are imported here

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line includes your chats app's URLs under the 'api/' prefix.
    # 'path' is used to define the URL pattern.
    # 'api/' is the prefix for your API endpoints.
    # 'include' is used to pull in URLs from another URLconf (chats.urls).
    path('api/', include('chats.urls')),
]

from django.contrib import admin
from django.views import generic
from django.urls import path, include
messages_view = generic.TemplateView.as_view(template_name="_messages.html")
urlpatterns = [
    path('admin/', admin.site.urls),
    path("messages", messages_view, name="messages"),
    path('', include('core.urls')),
]

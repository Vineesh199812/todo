from django.urls import path
from todoapi.views import TodosView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("todos",TodosView,basename="todos")

urlpatterns=[

]+router.urls
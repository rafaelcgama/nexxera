from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from accountapp.views import AccountViewSet, TransactionViewSet, get_statement

router = DefaultRouter()  # Creates router for ViewSet urls
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^statement/$', get_statement, name='statement'),
]

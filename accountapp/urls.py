from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from accountapp.views import AccountViewSet, TransactionViewSet

router = DefaultRouter() # Creates router dor ViewSet urls
router.register(r'account', AccountViewSet)
router.register(r'transaction', TransactionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^calculations/$', CalculationsView.as_view()),
]
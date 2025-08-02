from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
    UserViewSet, PropertyViewSet, ImageViewSet,
    BookingViewSet, ReviewViewSet,
    CustomLoginView, UserRegisterView, LogoutView
)

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('properties', PropertyViewSet)
router.register('images', ImageViewSet)
router.register('bookings', BookingViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]

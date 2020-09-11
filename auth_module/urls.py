from rest_framework.routers import DefaultRouter
from auth_module.views import(
	SignUpView
	)
from django.urls import path
from rest_framework_simplejwt.views import(
	TokenObtainPairView,
	TokenRefreshView,
	)
from auth_module.views import(
    CityView,
    MovieView,
    CinemaView,
	ShowtimeView,
	SeatView,
	BookView,
)

app_name = 'auth_module'

router = DefaultRouter()
router.register('city',CityView,basename='city')
router.register('movie',MovieView,basename='movie')
router.register('cinema',CinemaView,basename='cinema')
router.register('showtime',ShowtimeView,basename='showtime')
router.register('book',BookView,basename='book')

urlpatterns = [
	path('login/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
	path('signup/',SignUpView.as_view(), name='signup'),
	path('seat/',SeatView.as_view(), name='seat'),
]

urlpatterns += router.urls
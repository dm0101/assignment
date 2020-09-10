from rest_framework.serializers import(
    ModelSerializer,
    )
from auth_module.models import(
	City,
    Movie,
    Cinema,
	Showtime,
	)

class CitySerializer(ModelSerializer):
	
	class Meta:
		model = City
		fields = '__all__'

class MovieSerializer(ModelSerializer):
	
	class Meta:
		model = Movie
		fields = '__all__'

class CinemaSerializer(ModelSerializer):
	
	class Meta:
		model = Cinema
		fields = '__all__'

class ShowtimeSerializer(ModelSerializer):
	movie = MovieSerializer()
	class Meta:
		model = Showtime
		fields = '__all__'
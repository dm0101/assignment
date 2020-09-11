from django.contrib import admin
from django.contrib.auth import get_user_model
from auth_module.models import(
    City,
    Movie,
    Showtime,
    Cinema,
    Booking,
)

User = get_user_model()

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name','last_name')
    list_display =('username', 'first_name','last_name')
admin.site.register(User, UserAdmin)

admin.site.register(City)

admin.site.register(Movie)

class CinemaAdmin(admin.ModelAdmin):
    search_fields = ('name','movie')
    list_display =('name','movie')
admin.site.register(Cinema, CinemaAdmin)

class ShowtimeAdmin(admin.ModelAdmin):
    search_fields = ('movie','time','seats')
    list_display =('movie','time','seats')
admin.site.register(Showtime, ShowtimeAdmin)

class BookingAdmin(admin.ModelAdmin):
    search_fields = ('showtime','user',)
    list_display =('showtime','user',)
admin.site.register(Booking, BookingAdmin)

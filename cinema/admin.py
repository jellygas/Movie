from django.contrib import admin
from .models import Member, Movie, Theater, Schedule, Reservation, Food, Order, OrderDetail

admin.site.register(Member)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Schedule)
admin.site.register(Reservation)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderDetail)
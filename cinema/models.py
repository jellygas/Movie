from django.db import models

class Member(models.Model):
    member_id = models.CharField(max_length=20, primary_key=True, db_column='회원ID')
    name = models.CharField(max_length=50, db_column='이름')
    age = models.IntegerField(db_column='나이')
    phone = models.CharField(max_length=20, db_column='전화번호')
    grade = models.CharField(max_length=10, default='일반', db_column='등급')

    class Meta:
        db_table = '회원'

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.CharField(max_length=10, primary_key=True, db_column='영화ID')
    title = models.CharField(max_length=100, db_column='제목')
    genre = models.CharField(max_length=30, null=True, blank=True, db_column='장르')
    running_time = models.IntegerField(null=True, blank=True, db_column='상영시간')
    rating = models.CharField(max_length=10, null=True, blank=True, db_column='관람등급')
    price = models.IntegerField(null=True, blank=True, db_column='가격')
    poster = models.CharField(max_length=300, null=True, blank=True, db_column='poster')

    class Meta:
        db_table = '영화'

    def __str__(self):
        return self.title


class Theater(models.Model):
    theater_id = models.CharField(max_length=10, primary_key=True, db_column='상영관ID')
    name = models.CharField(max_length=20, db_column='관이름')
    seats = models.IntegerField(db_column='좌석수')

    class Meta:
        db_table = '상영관'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    schedule_id = models.CharField(max_length=10, primary_key=True, db_column='상영ID')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='영화ID')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, db_column='상영관ID')
    date = models.DateField(db_column='상영날짜')
    time = models.TimeField(db_column='상영시간')

    class Meta:
        db_table = '상영정보'

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"


class Reservation(models.Model):
    reservation_id = models.CharField(max_length=20, primary_key=True, db_column='예매ID')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='회원ID')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='상영ID')
    seat_number = models.CharField(max_length=5, db_column='좌석번호')
    reserved_at = models.DateField(db_column='예매일자')

    class Meta:
        db_table = '예매'

    def __str__(self):
        return f"{self.member.name} - {self.schedule}"


class Food(models.Model):
    food_id = models.CharField(max_length=10, primary_key=True, db_column='음식ID')
    name = models.CharField(max_length=50, db_column='음식명')
    category = models.CharField(max_length=20, db_column='분류')
    price = models.IntegerField(db_column='가격')
    
    class Meta:
        db_table = '식음료'

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.CharField(max_length=20, primary_key=True, db_column='주문ID')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='회원ID')
    date = models.DateField(db_column='주문날짜')
    total_price = models.IntegerField(db_column='총금액')

    class Meta:
        db_table = '주문'

    def __str__(self):
        return self.order_id


class OrderDetail(models.Model):
    detail_id = models.CharField(max_length=20, primary_key=True, db_column='주문상세ID')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='주문ID')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='음식ID')
    quantity = models.IntegerField(db_column='수량')

    class Meta:
        db_table = '주문상세'

    def __str__(self):
        return f"{self.order.order_id} - {self.food.name}"
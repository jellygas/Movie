from django.shortcuts import render, get_object_or_404
from .models import Movie, Schedule, Reservation, Member, Food
from django.utils import timezone
from django.shortcuts import redirect

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'cinema/movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    schedules = Schedule.objects.filter(movie=movie)
    return render(request, 'cinema/movie_detail.html', {
        'movie': movie,
        'schedules': schedules
    })


def movie_schedule(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    schedules = Schedule.objects.filter(movie=movie).order_by('date', 'time')
    
    return render(request, 'cinema/movie_schedule.html', {
        'movie': movie,
        'schedules': schedules
    })


def reserve(request, schedule_id):
    schedule = get_object_or_404(Schedule, schedule_id=schedule_id)

    # 전 좌석
    seats = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]

    # 이미 예약된 좌석
    reserved = Reservation.objects.filter(schedule=schedule)
    reserved_seats = [r.seat_number for r in reserved]

    # 로그인 여부 체크
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('login')  # 로그인 안 한 사람은 로그인 강제

    member = get_object_or_404(Member, member_id=member_id)

    if request.method == "POST":
        seat = request.POST.get("seat")

        # 좌석 선택 안 했을때
        if not seat:
            return render(request, 'cinema/reserve.html', {
                'schedule': schedule,
                'seats': seats,
                'reserved_seats': reserved_seats,
                'error': '좌석을 선택해주세요.'
            })

        # 이미 누가 예약했는지 다시 검사(동시예약 방지)
        if seat in reserved_seats:
            return render(request, 'cinema/reserve.html', {
                'schedule': schedule,
                'seats': seats,
                'reserved_seats': reserved_seats,
                'error': '이미 예약된 좌석입니다. 다른 좌석을 선택해주세요.'
            })

        # 정상 예약 처리
        Reservation.objects.create(
            reservation_id="R" + timezone.now().strftime("%Y%m%d%H%M%S"),
            member=member,
            schedule=schedule,
            seat_number=seat,
            reserved_at=timezone.now().date()
        )

        return render(request, 'cinema/reserve_done.html', {
            'schedule': schedule,
            'seat': seat
        })

    # GET 요청일 경우 단순 페이지 렌더링
    return render(request, 'cinema/reserve.html', {
        'schedule': schedule,
        'seats': seats,
        'reserved_seats': reserved_seats
    })

def reservation_list(request, member_id):
    member = get_object_or_404(Member, member_id=member_id)
    reservations = Reservation.objects.filter(member=member).order_by('-reserved_at')

    return render(request, 'cinema/reservation_list.html', {
        'member': member,
        'reservations': reservations
    })

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, reservation_id=reservation_id)

    if request.method == "POST":
        member_id = reservation.member.member_id
        reservation.delete()
        return redirect('reservation_list', member_id=member_id)

    return redirect('reservation_list', member_id=reservation.member.member_id)

def food_list(request):
    foods = Food.objects.all()
    return render(request, 'cinema/food_list.html', {'foods': foods})

from .models import Food, Order, OrderDetail

def order_food(request, food_id):
    food = get_object_or_404(Food, food_id=food_id)

    if request.method == "POST":
        member_id = request.session.get('member_id')
        if not member_id:
            return redirect('login')
        quantity = int(request.POST.get("quantity"))

        member = get_object_or_404(Member, member_id=member_id)

        # 총가격 계산
        total_price = food.price * quantity

        # 주문 생성
        order = Order.objects.create(
            order_id="O" + timezone.now().strftime("%Y%m%d%H%M%S"),
            member=member,
            date=timezone.now().date(),
            total_price=total_price
        )

        # 주문 상세 생성
        OrderDetail.objects.create(
            detail_id="D" + timezone.now().strftime("%Y%m%d%H%M%S"),
            order=order,
            food=food,
            quantity=quantity
        )

        return render(request, "cinema/order_done.html", {
            "order": order,
            "food": food,
            "quantity": quantity,
            "total_price": total_price
        })

    return render(request, "cinema/order_food.html", {
        "food": food
    })

def order_list(request, member_id):
    member = get_object_or_404(Member, member_id=member_id)

    orders = Order.objects.filter(member=member).order_by('-date')

    # 주문에 연결된 상세 데이터 붙여주기
    order_details = {
        order.order_id: OrderDetail.objects.filter(order=order)
        for order in orders
    }

    return render(request, "cinema/order_list.html", {
        "member": member,
        "orders": orders,
        "order_details": order_details
    })

def signup(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        grade = request.POST.get('grade', '일반')

        # 중복 ID 체크
        if Member.objects.filter(member_id=member_id).exists():
            return render(request, 'cinema/signup.html', {
                'error': '이미 존재하는 회원 ID입니다.'
            })

        Member.objects.create(
            member_id=member_id,
            name=name,
            age=age,
            phone=phone,
            grade=grade
        )

        return render(request, 'cinema/signup_done.html', {
            'member_id': member_id,
            'name': name
        })

    return render(request, 'cinema/signup.html')

from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        phone = request.POST.get("phone")

        try:
            member = Member.objects.get(member_id=member_id, phone=phone)
            # 로그인 성공 → 세션 저장
            request.session['member_id'] = member.member_id
            request.session['member_name'] = member.name

            return redirect('movie_list')

        except Member.DoesNotExist:
            return render(request, 'cinema/login.html', {
                'error': '회원정보가 일치하지 않습니다.'
            })

    return render(request, 'cinema/login.html')


def logout_view(request):
    request.session.flush()  # 세션 전체 삭제
    return redirect('movie_list')
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.db.models import Count
from .models import Lecture, LectureView
from collections import Counter
# Create your views here.

def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/iconn/login/')
def index(request):
    lectures = Lecture.objects.all()
    context = {
        'lectures': lectures
    }
    return render(request, 'myapp/index.html', context)

@xframe_options_sameorigin
@login_required(login_url='/iconn/login/')
def lecture_view(request, pk):
    lecture = Lecture.objects.get(pk=pk)
    user = request.user
    if not request.session.get(f'page_viewed_{pk}', False):
        # If not viewed in this session, increment by 2 and mark as viewed
        today = timezone.now().date()
        lect_view = LectureView.objects.create(lecture=lecture, date=today)
        # lecture.views += 1
        # lecture.save()
        request.session[f'page_viewed_{pk}'] = True

    context = {
        'lecture': lecture,
        'user': user
    }

    return render(request, 'myapp/lecture_details.html', context)

@login_required(login_url='/iconn/login/')
@user_passes_test(is_superuser)
def dashboard(request):
    # Users count
    users_count = User.objects.count()

    # Count active users
    active_users = User.objects.filter(is_active=True)
    count = active_users.count()

    # COunt Lectures
    lectures = Lecture.objects.all()

    lecture_views = LectureView.objects.all()
    lec_view_counts = Counter(view.lecture.name for view in lecture_views)
    
    lec_names = list(lec_view_counts.keys())
    view_count_list = list(lec_view_counts.values())

    context = {
        'users_count': users_count,
        'active_users_count': count,
        'lectures': lectures,
        'lec_names': lec_names,
        'view_count_list': view_count_list
    }
    return render(request, 'myapp/dashboard.html', context)


@login_required(login_url='/iconn/login/')
@user_passes_test(is_superuser)
def lect_dashboard(request, pk):
    today = date.today()
    # next_month_first_day = today.replace(day=1, month=today.month + 1, year=today.year) if today.month < 12 else today.replace(day=1, month=1, year=today.year + 1)
    

    if request.method == "POST":
        end_date_str = request.POST.get('end_date')
        start_date_str = request.POST.get('start_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        print(end_date)
    else:
        end_date = today
        start_date = end_date.replace(day=1)
        print(end_date)


    lec_to_display = Lecture.objects.get(pk=pk)
    lecture_views_data = LectureView.objects.filter(lecture__name=lec_to_display.name, date__range=(start_date, end_date))\
        .values('date')\
        .annotate(page_views_count=Count('lecture'))
    
    lec_views_dict = {entry['date']: entry['page_views_count'] for entry in lecture_views_data}
    
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    formatted_dates = [date.strftime('%b-%d-%y') for date in dates]
    lecture_views_count = [lec_views_dict.get(date, 0) for date in dates]

    context = {
        'date': today,
        'end_date': end_date,
        'start_date': start_date,
        'dates': formatted_dates,
        'lecture_views_count': lecture_views_count,
        'lec_to_display': lec_to_display
    }

    return render(request, 'myapp/lect_dashboard.html', context)

import datetime
from django.shortcuts import render, HttpResponse
from .models import change_dir


# Create your views here.
def index(request):
	post_data = request.GET.get('date')
	if post_data == None:
		now_time = datetime.datetime.now().date()
		ret = change_dir.objects.filter(add_time=now_time).order_by('-change_time')
		return render(request, 'index.html', {'item_list': ret})
	elif post_data == 'all':
		ret = change_dir.objects.all().order_by('-change_time')
		return render(request, 'index.html', {'item_list': ret})
	else:
		ret = change_dir.objects.filter(add_time=post_data).order_by('-change_time')
		return render(request, 'index.html', {'item_list': ret})


def pull_event(request):
	now_time = datetime.datetime.now().date()
	if request.method == 'POST':
		dir = request.POST.get('directory')
		ip_add = request.POST.get('ipaddres')
		pull_time = request.POST.get('time')
		event = request.POST.get('type')
		change_dir.objects.create(src_dir=dir, ipaddr=ip_add, change_time=pull_time, add_time=now_time,
		                          event_type=event)
		return HttpResponse('{"code": 200}')
	return HttpResponse('Not Found')

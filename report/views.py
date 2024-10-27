from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from report.forms import ReportForm  
from report.models import Report, Vehicle
from django.utils import timezone
from django.http import HttpResponse
from django.core import serializers
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime


@login_required(login_url='/login')  # Redirect to login page if not logged in
def create_report_entry(request):
    vehicles = Vehicle.objects.filter(availability=True)
    form = ReportForm(request.POST or None)
    order_date = timezone.now().date()  # Assuming the order date is today

    if request.method == "POST":
        if form.is_valid():
            report_entry = form.save(commit=False)
            report_entry.user = request.user
            report_entry.save()
            messages.success(request, 'Laporan berhasil dibuat!')
            return redirect('main:show_main')  # Pastikan URL ini benar
    
    context = {
        'form': form,
        'vehicles': vehicles,
        'order_date': order_date,
    }
    return render(request, "report_form.html", context)

@login_required(login_url='/login')
def show_reports(request):
    report_entries = Report.objects.all()  

    context = {
        'reports': report_entries  
    }

    return render(request, "report_list.html", context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
      else:
        messages.error(request, "Invalid username or password. Please try again.")

   else:
      form = AuthenticationForm(request)

   context = {'form': form}
   return render(request, 'login.html', context)

def show_xml(request):
    data = Report.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Report.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Report.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Report.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def report_entry_ajax(request):
    vehicle = strip_tags(request.POST.get("vehicle"))
    description = strip_tags(request.POST.get("description"))
    issue_type = strip_tags(request.POST.get("issue_type"))
    user = request.user

    new_thrift = Report(
        vehicle=vehicle, description=description, 
        issue_type=issue_type,
        user=user 
    )
    new_thrift.save()

    return HttpResponse(b"CREATED", status=201)
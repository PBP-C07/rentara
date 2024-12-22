import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login
from report.forms import ReportForm  
from report.models import Report, Vehicle
from django.utils import timezone
from django.http import HttpResponse
from django.core import serializers
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.models import modelform_factory

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
            return redirect('main:show_main') 
    
    context = {
        'form': form,
        'vehicles': vehicles,
        'order_date': order_date,
    }
    return render(request, "main_report.html", context)

def add_report(request):
    vehicles = Vehicle.objects.filter(availability=True)
    form = ReportForm(request.POST or None)
    order_date = timezone.now().date()  # Assuming the order date is today

    if request.method == "POST":
        if form.is_valid():
            report_entry = form.save(commit=False)
            report_entry.user = request.user
            report_entry.save()
            messages.success(request, 'Laporan berhasil dibuat!')
            return redirect('report:create_report_entry') 
    
    context = {
        'form': form,
        'vehicles': vehicles,
        'order_date': order_date,
    }
    return render(request, "report_form.html", context)

def edit_report(request, id):
    laporan = Report.objects.get(pk = id)

    form = ReportForm(request.POST or None, instance=laporan)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('report:create_report_entry'))

    context = {'form': form}
    return render(request, "edit_report.html", context)

def delete_report(request, id):
    laporan = Report.objects.get(pk = id)
    laporan.delete()
    return HttpResponseRedirect(reverse('report:create_report_entry'))

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

    new_report = Report(
        vehicle=vehicle, description=description, 
        issue_type=issue_type,
        user=user 
    )
    new_report.save()

    return HttpResponse(b"CREATED", status=201)

from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

@csrf_exempt
@staff_member_required
def manage_reports(request):
    query = request.GET.get('query', '')  # Mendapatkan parameter pencarian dari URL
    if query:
        pending_reports = Report.objects.filter(
            Q(issue_type__icontains=query) | Q(description__icontains=query),
            status='Pending'  # Filter hanya laporan dengan status Pending
        )
    else:
        pending_reports = Report.objects.filter(status='Pending')  # Ambil semua laporan Pending

    context = {
        'pending_reports': pending_reports,
        'query': query,
    }
    return render(request, 'manage_reports.html', context)



@staff_member_required
def accept_report(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(Report, id=report_id)
        if report.status == 'Pending':  # Hanya ubah jika status masih Pending
            report.status = 'Approved'
            report.save()
            messages.success(request, f"Laporan dengan ID {report_id} berhasil di-approve.")
            return redirect('report:manage_reports')
        else:
            messages.error(request, "Laporan ini sudah diproses sebelumnya.")
            return redirect('report:manage_reports')
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required
def user_reports(request):
    reports = Report.objects.filter(user=request.user).values('title', 'description', 'date')
    return JsonResponse({"reports": list(reports)})

from django.http import JsonResponse
from .models import Report
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Report
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def create_report_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            vehicle = data.get("vehicle")
            issue_type = data.get("issue_type")
            description = data.get("description")

            if not vehicle or not issue_type:
                return JsonResponse({"status": "failed", "message": "Data tidak lengkap."})

            Report.objects.create(
                vehicle=vehicle,
                issue_type=issue_type,
                description=description,
                user=request.user,
            )
            return JsonResponse({"status": "success", "message": "Report berhasil dibuat."})
        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "message": "Format data tidak valid."})

    return JsonResponse({"status": "failed", "message": "Metode request tidak valid."})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import this
from report.forms import ReportForm  
from report.models import Report, Vehicle
from django.utils import timezone

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
            return redirect('main:show_main')  # Adjust to the correct URL

    context = {
        'form': form,
        'vehicles': vehicles,
        'order_date': order_date,
    }
    return render(request, "report_form.html", context)

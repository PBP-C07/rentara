from django.shortcuts import render, get_object_or_404, redirect
from .models import Partner, Vehicles
from main.models import Vehicle
from django.contrib.auth.decorators import login_required
from .forms import PartnerForm, VehicleForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_vehicle(request):
    partner = get_object_or_404(Partner, user=request.user)

    # Check if the partner is approved
    if partner.status == 'Pending':
        return redirect('joinpartner:pending_approval')
    
    if partner.status == 'Rejected':
        partner.delete()
        return redirect('joinpartner:rejected')
    
    partner_vehicles = Vehicles.objects.filter(partner=partner)
    
    from sewajual.models import Katalog
    katalogs = Katalog.objects.filter(owner=partner).select_related('vehicle')
    main_vehicles = [katalog.vehicle for katalog in katalogs]  

    vehicles = list(main_vehicles) + list(partner_vehicles)

    query = request.GET.get('query', '')  # Get search query
    if query:
        vehicles = [v for v in vehicles if (
            query.lower() in v.merk.lower() or
            query.lower() in v.tipe.lower() or
            query.lower() in v.jenis_kendaraan.lower() or
            query.lower() in v.warna.lower()
        )]

    return render(request, 'show_vehicle.html', {
        'partner': partner,
        'vehicles': vehicles,
        'last_login': request.COOKIES.get('last_login', ''),
        'query': query,
    })

@login_required(login_url='/login')
def add_product(request):
    partner = get_object_or_404(Partner, user=request.user)
    errors = {}

    if request.method == "POST":
        link_foto = request.POST.get("link_foto")
        merk = strip_tags(request.POST.get("merk"))
        tipe = strip_tags(request.POST.get("tipe"))
        jenis_kendaraan = strip_tags(request.POST.get("jenis_kendaraan"))
        warna = strip_tags(request.POST.get("warna"))
        harga = request.POST.get("harga")
        status = request.POST.get("status")
        bahan_bakar = strip_tags(request.POST.get("bahan_bakar"))  # Make sure to get this value

        # Validate input
        if not merk:
            errors['merk'] = ["Nama merk tidak boleh kosong."]
        if not tipe:
            errors['tipe'] = ["Tipe tidak boleh kosong."]
        if not jenis_kendaraan:
            errors['jenis_kendaraan'] = ["Jenis kendaraan tidak boleh kosong."]
        if not warna:
            errors['warna'] = ["Warna kendaraan tidak boleh kosong."]
        if not harga or not harga.isdigit():
            errors['harga'] = ["Harga per hari harus diisi dan berupa angka."]
        if not bahan_bakar:
            errors['bahan_bakar'] = ["Bahan bakar tidak boleh kosong."]

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # If there are no errors, save the new vehicle
        new_vehicle = Vehicles(
            partner=partner,
            link_foto=link_foto,
            merk=merk,
            tipe=tipe,
            jenis_kendaraan=jenis_kendaraan,
            warna=warna,
            harga=harga,
            status=status,
            bahan_bakar=bahan_bakar  # Make sure to include this field
        )
        new_vehicle.save()
        return JsonResponse({'success': True})

    return render(request, "add_product.html", {'errors': errors})


@login_required(login_url='/login')
def join_partner(request):
    partner_exists = Partner.objects.filter(user=request.user).exists()
    
    if partner_exists:
        return redirect('joinpartner:show_vehicle')
    
    if request.method == 'POST':
        toko = strip_tags(request.POST.get("toko"))
        link_lokasi = strip_tags(request.POST.get("link_lokasi"))
        notelp = strip_tags(request.POST.get("notelp"))
        
        errors = {}
        
        # Validasi input
        if not toko:
            errors['toko'] = "Nama toko tidak boleh kosong."
        if not link_lokasi:
            errors['link_lokasi'] = "Link alamat tidak boleh kosong."
        if not notelp:
            errors['notelp'] = "Nomor telepon tidak boleh kosong."
        
        if errors:
            return JsonResponse(errors, status=400)  # Return errors in JSON format

        # Simpan partner baru jika tidak ada kesalahan
        new_partner = Partner(user=request.user, toko=toko, link_lokasi=link_lokasi, notelp=notelp)
        new_partner.save()
        return JsonResponse({'success': True})  # Return success response in JSON format

    return render(request, 'join_partner.html')


@login_required(login_url='/login')
def edit_product(request, product_id):
    product = get_object_or_404(Vehicles, id=product_id)
    partner = get_object_or_404(Partner, user=request.user)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)  # Success response

        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = VehicleForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required(login_url='/login')
def delete_product(request, product_id):
    product = get_object_or_404(Vehicles, id=product_id)


    product.delete()
    print("Deletion successful") 

    return redirect('joinpartner:show_vehicle')


@login_required(login_url='/login')
def edit_profile(request):
    partner = get_object_or_404(Partner, user=request.user)

    form = PartnerForm(request.POST or None, instance=partner)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('joinpartner:show_vehicle')
    
    return render(request, "edit_profile.html", {'form': form})

@csrf_exempt
@staff_member_required
def manage_partners(request):
    query = request.GET.get('query', '')  # Get search query
    if query:
        pending_partners = Partner.objects.filter(
            Q(status='Pending'),
            Q(toko__icontains=query) | Q(notelp__icontains=query)
        )
    else:
        pending_partners = Partner.objects.filter(status='Pending')

    return render(request, 'manage_partners.html', {
        'pending_partners': pending_partners,
        'query': query,
    })


@staff_member_required
def approve_partner(request, partner_id):
    if request.method == 'POST':
        partner = get_object_or_404(Partner, id=partner_id)
        partner.status = 'Approved'
        partner.save()
        return JsonResponse({'success': True})  # Mengembalikan respon JSON
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@staff_member_required
def reject_partner(request, partner_id):
    if request.method == 'POST':
        partner = get_object_or_404(Partner, id=partner_id)
        partner.status = 'Rejected'
        partner.save()
        return JsonResponse({'success': True})  # Mengembalikan respon JSON
    return JsonResponse({'error': 'Invalid request'}, status=400)

def pending_approval(request):
    return render(request, 'pending.html')

def rejected(request):
    return render(request, 'rejected.html')


def list_partner(request):
    query = request.GET.get('query', '')  # Get search query
    if query:
        approved_partners = Partner.objects.filter(
            Q(status='Approved'),
            Q(toko__icontains=query) | Q(notelp__icontains=query)
        )
    else:
        approved_partners = Partner.objects.filter(status='Approved')

    return render(request, 'approved_partners.html', {
        'approved_partners': approved_partners,
        'query': query,
    })



def delete_partner(request, partner_id):
    if request.method == 'POST':
        partner = get_object_or_404(Partner, id=partner_id)
        partner.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
#ini test
#dummy


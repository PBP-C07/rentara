from django.shortcuts import render, get_object_or_404, redirect
from .models import Partner, Vehicle
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

    if partner.status=='Pending':
        return redirect('joinpartner:pending_approval')
    
    if partner.status=='Rejected':
        partner.delete()
        return redirect('joinpartner:rejected')
    
    partner_vehicles = Vehicle.objects.filter(partner=partner)  # Vehicle dari partner

    from sewajual.models import Katalog
    katalogs = Katalog.objects.filter(owner=partner).select_related('vehicle')
    main_vehicles = [katalog.vehicle for katalog in katalogs]  

    # Gabung kedua querysets
    vehicles = list(main_vehicles) + list(partner_vehicles)

    return render(request, 'show_vehicle.html', {
        'partner': partner,
        'vehicles': vehicles, 
        'last_login': request.COOKIES.get('last_login', ''),
    })

@login_required(login_url='/login')
def add_product(request):
    partner = get_object_or_404(Partner, user=request.user)

    if request.method == "POST":
        vehicle_image = request.POST.get("vehicle_image")  # Menggunakan request.FILES untuk mengakses gambar
        brand = strip_tags(request.POST.get("brand"))
        brand_type = strip_tags(request.POST.get("brand_type"))
        vehicle_type = strip_tags(request.POST.get("vehicle_type"))  # seperti mobil, motor, dll.
        color = strip_tags(request.POST.get("color")) 
        price_per_day = request.POST.get("price_per_day")

        errors = {}

        # Validasi input
        if not brand:
            errors['brand'] = "Nama brand tidak boleh kosong."
        if not brand_type:
            errors['brand_type'] = "Tipe brand tidak boleh kosong."
        if not vehicle_type:
            errors['vehicle_type'] = "Tipe kendaraan tidak boleh kosong."
        if not color:
            errors['color'] = "Warna kendaraan tidak boleh kosong."
        if not price_per_day or not price_per_day.isdigit():
            errors['price_per_day'] = "Harga per hari harus diisi dan berupa angka."

        # Jika tidak ada error, simpan kendaraan baru
        if not errors:
            new_vehicle = Vehicle(
                partner=partner,
                vehicle_image=vehicle_image,
                brand=brand,
                brand_type=brand_type,
                vehicle_type=vehicle_type,
                color=color,
                price_per_day=price_per_day
            )
            new_vehicle.save()
            return redirect('joinpartner:show_vehicle')
        
    else:
        # Jika metode bukan POST, tidak perlu mengisi 'errors'
        errors = {}

    # Pastikan ada respons yang dikembalikan
    return render(request, "add_product.html", {'errors': errors})


    
    #     form = VehicleForm(request.POST)
    #     if form.is_valid():
    #         vehicle = form.save(commit=False)
    #         vehicle.partner = partner  # Set partner untuk kendaraan yang akan disimpan
    #         vehicle.save()
    #         return redirect('joinpartner:show_vehicle')
    # else:
    #     form = VehicleForm()

@login_required(login_url='/login')
def join_partner(request):
    # Periksa apakah pengguna sudah terdaftar sebagai partner
    partner_exists = Partner.objects.filter(user=request.user).exists()
    
    if partner_exists:
        # Jika sudah terdaftar, arahkan ke halaman kendaraan
        return redirect('joinpartner:show_vehicle')
    
    errors = {}
    
    if request.method == 'POST':
        # Ambil data dari form
        store_name = strip_tags(request.POST.get("store_name"))
        gmaps_link = strip_tags(request.POST.get("gmaps_link"))
        phone_number = strip_tags(request.POST.get("phone_number"))
        
        # Validasi input
        if not store_name:
            errors['store_name'] = "Nama toko tidak boleh kosong."
        if not gmaps_link:
            errors['gmaps_link'] = "Link alamat tidak boleh kosong."
        if not phone_number:
            errors['phone_number'] = "Nomor telepon tidak boleh kosong."
        
        # Jika tidak ada kesalahan, simpan partner baru
        if not errors:
            new_partner = Partner(user=request.user, store_name=store_name, gmaps_link=gmaps_link, phone_number=phone_number)
            new_partner.save()
            return redirect('joinpartner:show_vehicle')
        # else:
        #     # Jika ada kesalahan, kembalikan form dengan pesan kesalahan
        #     return render(request, 'join_partner.html', {
        #         'errors': errors,
        #         'store_name': store_name,
        #         'gmaps_link': gmaps_link,
        #         'phone_number': phone_number,
        #     })
    
    # Tampilkan formulir pendaftaran jika metode tidak POST
    return render(request, 'join_partner.html', {'errors': errors})



@login_required(login_url='/login')
def edit_product(request, product_id):
    product = get_object_or_404(Vehicle, id=product_id)
    partner = get_object_or_404(Partner, user=request.user)

    # Memastikan pengguna adalah pemilik produk
    if product.partner != partner:
        return HttpResponseForbidden("Anda tidak diizinkan untuk mengedit produk ini.")
    
    # Mengisi form dengan data produk saat ini
    form = VehicleForm(request.POST or None, instance=product)
    errors = {}
    if request.method == "POST":
        vehicle_image = request.FILES.get("vehicle_image") or product.vehicle_image  # Menggunakan gambar lama jika tidak ada gambar baru
        brand = strip_tags(request.POST.get("brand"))
        brand_type = strip_tags(request.POST.get("brand_type"))
        vehicle_type = strip_tags(request.POST.get("vehicle_type"))
        color = strip_tags(request.POST.get("color"))
        price_per_day = request.POST.get("price_per_day")


        # Validasi input
        if not brand:
            errors['brand'] = "Nama brand tidak boleh kosong."
        if not brand_type:
            errors['brand_type'] = "Tipe brand tidak boleh kosong."
        if not vehicle_type:
            errors['vehicle_type'] = "Tipe kendaraan tidak boleh kosong."
        if not color:
            errors['color'] = "Warna kendaraan tidak boleh kosong."

        # Jika tidak ada error, simpan perubahan
        if not errors:
            product.vehicle_image = vehicle_image  # Mengupdate gambar jika ada
            product.brand = brand
            product.brand_type = brand_type
            product.vehicle_type = vehicle_type
            product.color = color
            product.price_per_day = price_per_day
            product.save()
            return redirect('joinpartner:show_vehicle')

    return render(request, "edit_product.html", {'form': form, 'errors': errors})


@login_required(login_url='/login')
def delete_product(request, product_id):
    product = get_object_or_404(Vehicle, id=product_id)
    partner = get_object_or_404(Partner, user=request.user)

    if product.partner != partner:
        return HttpResponseForbidden("Anda tidak diizinkan untuk menghapus produk ini.")

    product.delete()
    return redirect('joinpartner:show_vehicle')

@login_required(login_url='/login')
def edit_profile(request):
    partner = get_object_or_404(Partner, user=request.user)

    form = PartnerForm(request.POST or None, instance=partner)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('joinpartner:show_vehicle')
    
    return render(request, "edit_profile.html", {'form': form})

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('joinpartner:login')
    context = {'form': form}
    return render(request, 'register.html', context)

from django.contrib.auth.decorators import user_passes_test

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Cek apakah pengguna adalah admin
            if user.is_staff:  # atau bisa juga menggunakan 'user.is_superuser'
                response = HttpResponseRedirect(reverse('joinpartner:manage_partners'))
            else:
                response = HttpResponseRedirect(reverse('joinpartner:join_partner'))
            
            # Set cookie last_login
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Username atau password salah. Silakan coba lagi.")

    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('joinpartner:login'))
    response.delete_cookie('last_login')
    return response

def search_vehicle(request):
    query = request.GET.get('query', '')  # Ambil query dari form
    if query:
        vehicles = Vehicle.objects.filter(
            Q(brand__icontains=query) | Q(brand_type__icontains=query) | Q(vehicle_type__icontains=query)
        )
    else:
        vehicles = Vehicle.objects.all()  # Jika tidak ada query, tampilkan semua

    return render(request, 'search_results.html', {
        'vehicles': vehicles,
        'query': query,
    })

@csrf_exempt
@staff_member_required
def manage_partners(request):
    pending_partners = Partner.objects.filter(status='Pending')
    return render(request, 'manage_partners.html', {'pending_partners': pending_partners})

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
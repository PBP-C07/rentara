from django.shortcuts import render, get_object_or_404, redirect
from .models import Partner, Vehicles
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

    query = request.GET.get('query', '')  # Get search query
    if query:
        vehicles = Vehicles.objects.filter(
            partner=partner
        ).filter(
            Q(merk__icontains=query) | Q(tipe__icontains=query) | Q(jenis_kendaraan__icontains=query) | Q(warna__icontains=query)
        )
    else:
        vehicles = Vehicles.objects.filter(partner=partner)

    return render(request, 'show_vehicle.html', {
        'partner': partner,
        'vehicles': vehicles, 
        'last_login': request.COOKIES.get('last_login', ''),
        'query': query,
    })

@login_required(login_url='/login')
def add_product(request):
    partner = get_object_or_404(Partner, user=request.user)

    if request.method == "POST":
        link_foto = request.POST.get("link_foto")  # Menggunakan request.FILES untuk mengakses gambar
        merk = strip_tags(request.POST.get("merk"))
        tipe = strip_tags(request.POST.get("tipe"))
        jenis_kendaraan = strip_tags(request.POST.get("jenis_kendaraan"))  # seperti mobil, motor, dll.
        warna = strip_tags(request.POST.get("warna")) 
        harga = request.POST.get("harga")
        status = request.POST.get("status")

        errors = {}

        # Validasi input
        if not merk:
            errors['merk'] = "Nama merk tidak boleh kosong."
        if not tipe:
            errors['tipe'] = "Tipe merk tidak boleh kosong."
        if not jenis_kendaraan:
            errors['jenis_kendaraan'] = "Tipe kendaraan tidak boleh kosong."
        if not warna:
            errors['warna'] = "Warna kendaraan tidak boleh kosong."
        if not harga or not harga.isdigit():
            errors['harga'] = "Harga per hari harus diisi dan berupa angka."

        # Jika tidak ada error, simpan kendaraan baru
        if not errors:
            new_vehicle = Vehicles(
                partner=partner,
                link_foto=link_foto,
                merk=merk,
                tipe=tipe,
                jenis_kendaraan=jenis_kendaraan,
                warna=warna,
                harga=harga,
                status=status
            )
            new_vehicle.save()
            return redirect('joinpartner:show_vehicle')
        
    else:
        # Jika metode bukan POST, tidak perlu mengisi 'errors'
        errors = {}

    # Pastikan ada respons yang dikembalikan
    return render(request, "add_product.html", {'errors': errors})


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
        toko = strip_tags(request.POST.get("toko"))
        link_lokasi = strip_tags(request.POST.get("link_lokasi"))
        notelp = strip_tags(request.POST.get("notelp"))
        
        # Validasi input
        if not toko:
            errors['toko'] = "Nama toko tidak boleh kosong."
        if not link_lokasi:
            errors['link_lokasi'] = "Link alamat tidak boleh kosong."
        if not notelp:
            errors['notelp'] = "Nomor telepon tidak boleh kosong."
        
        # Jika tidak ada kesalahan, simpan partner baru
        if not errors:
            new_partner = Partner(user=request.user, toko=toko, link_lokasi=link_lokasi, notelp=notelp)
            new_partner.save()
            return redirect('joinpartner:show_vehicle')
    return render(request, 'join_partner.html', {'errors': errors})



@login_required(login_url='/login')
def edit_product(request, product_id):
    product = get_object_or_404(Vehicles, id=product_id)
    partner = get_object_or_404(Partner, user=request.user)

    # Memastikan pengguna adalah pemilik produk
    if product.partner != partner:
        return HttpResponseForbidden("Anda tidak diizinkan untuk mengedit produk ini.")
    
    # Mengisi form dengan data produk saat ini
    form = VehicleForm(request.POST or None, instance=product)
    errors = {}
    if request.method == "POST":
        link_foto = request.POST.get("link_foto") or product.link_foto  # Menggunakan gambar lama jika tidak ada gambar baru
        merk = strip_tags(request.POST.get("merk"))
        tipe = strip_tags(request.POST.get("tipe"))
        jenis_kendaraan = strip_tags(request.POST.get("jenis_kendaraan"))
        warna = strip_tags(request.POST.get("warna"))
        harga = request.POST.get("harga")
        status = request.POST.get("status")


        # Validasi input
        if not merk:
            errors['merk'] = "Nama merk tidak boleh kosong."
        if not tipe:
            errors['tipe'] = "Tipe merk tidak boleh kosong."
        if not jenis_kendaraan:
            errors['jenis_kendaraan'] = "Tipe kendaraan tidak boleh kosong."
        if not warna:
            errors['warna'] = "Warna kendaraan tidak boleh kosong."

        # Jika tidak ada error, simpan perubahan
        if not errors:
            product.link_foto = link_foto  # Mengupdate gambar jika ada
            product.merk = merk
            product.tipe = tipe
            product.jenis_kendaraan = jenis_kendaraan
            product.warna = warna
            product.harga = harga
            product.status=status
            product.save()
            return redirect('joinpartner:show_vehicle')

    return render(request, "edit_product.html", {'form': form, 'errors': errors})


@login_required(login_url='/login')
def delete_product(request, product_id):
    product = get_object_or_404(Vehicles, id=product_id)

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
    partner = get_object_or_404(Partner, id=partner_id)

    partner.delete()
    return redirect('joinpartner:list_partner')




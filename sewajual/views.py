from django.shortcuts import render, get_object_or_404
from .models import Vehicle
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'card_product.html', {'vehicles': vehicles})

@login_required(login_url='login')
def full_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'full_info.html', {'vehicle': vehicle})

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AdminVehicleListView(AdminRequiredMixin, ListView):
    model = Vehicle
    template_name = 'admin/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_vehicles'] = Vehicle.objects.count()
        return context

class AdminVehicleCreateView(AdminRequiredMixin, CreateView):
    model = Vehicle
    template_name = 'admin/vehicle_form.html'
    fields = ['toko', 'merk', 'tipe', 'warna', 'jenis_kendaraan', 
              'harga', 'status', 'bahan_bakar', 'link_lokasi', 'link_foto']
    success_url = reverse_lazy('admin-vehicles')

    def form_valid(self, form):
        messages.success(self.request, 'Kendaraan berhasil ditambahkan.')
        return super().form_valid(form)

class AdminVehicleUpdateView(AdminRequiredMixin, UpdateView):
    model = Vehicle
    template_name = 'admin/vehicle_form.html'
    fields = ['toko', 'merk', 'tipe', 'warna', 'jenis_kendaraan', 
              'harga', 'status', 'bahan_bakar', 'link_lokasi', 'link_foto']
    success_url = reverse_lazy('admin-vehicles')

    def form_valid(self, form):
        messages.success(self.request, 'Kendaraan berhasil diperbarui.')
        return super().form_valid(form)

class AdminVehicleDeleteView(AdminRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'admin/vehicle_confirm_delete.html'
    success_url = reverse_lazy('admin-vehicles')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Kendaraan berhasil dihapus.')
        return super().delete(request, *args, **kwargs)
import json

# Data kendaraan Anda (copy paste data JSON Anda disini)
data = [
    {
        "toko": "Sungkar trans",
        "merk": "Toyota",
        "tipe": "Avanza All New",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 350000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/b8z1tobBJ5eg73gP6",
        "link_foto": "https://drive.google.com/file/d/1gF_CPK36_LiY9H-mF9G9qRbJUyEBAD-D/view?usp=drive_link"
    },
    {
        "toko": "Sungkar trans",
        "merk": "Toyota",
        "tipe": "Innova Reborn",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 500000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/b8z1tobBJ5eg73gP6",
        "link_foto": "https://drive.google.com/file/d/1uV7DyQhxRkQyEZ6-g7Dwf9QPR-pn47nD/view?usp=sharing"
    },
    {
        "toko": "Sungkar trans",
        "merk": "Honda",
        "tipe": "Brio",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 325000,
        "status": "Sewa",
        "bahan_bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/b8z1tobBJ5eg73gP6",
        "link_foto": "https://drive.google.com/file/d/1RJaT2lbv1yOpgCEilH-1_LH_BDS-kKJS/view?usp=drive_link"
    },
    {
        "toko": "Sungkar trans",
        "merk": "Toyota",
        "tipe": "Agya",
        "warna": "Abu-abu",
        "jenis": "Mobil",
        "harga": 300000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/b8z1tobBJ5eg73gP6",
        "link_foto": "https://drive.google.com/file/d/1iWguysbK-bvNEuYbTVF46UPXzBoWOsX1/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Toyota",
        "tipe": "Raize 1.0 Turbo GR Sport CVT TSS",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 450000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1jktbnI1FZo22iBlxObXybu5-hIEoGpKl/view?usp=sharing"
    },
    {
        "toko": "Rental 99",
        "merk": "Toyota",
        "tipe": "Innova Zenix G",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 700000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1H6hLAPpMA9be9zi8yfRmKsPuGH2i9M4F/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Toyota",
        "tipe": "Innova Zenix Q",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 1200000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1H22u6hZsGJZZDzC_y2QcE8Bh8cJurDxO/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Toyota",
        "tipe": "Fortuner GR",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 1500000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1kGkLbYE8OX4cKI4ogHw4HbQeeYhEhi7R/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Nissan",
        "tipe": "Grand Livina",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 300000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1BLxDlrV-6qfQ9f8SbngU9bRdXMnKJmd6/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Suzuki",
        "tipe": "Ertiga GLX",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 300000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1WAZHCcphtudcrLiH0tOWYY1GQmjHvUbj/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Honda",
        "tipe": "Mobilio",
        "warna": "Abu-Abu",
        "jenis": "Mobil",
        "harga": 350000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/19VBB4KOHKnN-R_f8rxfvNYg0eItdwY5-/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Toyota",
        "tipe": "Vellfire 2.5 G A/T",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 3000000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1QW9Xn35g2xNyyrmVnpyt2-nza1Cu-jH8/view?usp=drive_link"
    },
    {
        "toko": "Rental 99",
        "merk": "Toyota",
        "tipe": "Alphard Hybrid",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 4500000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/13vOB7Fspmm-y03PzkiveHeDiTogSJP0m/view?usp=drive_link"
    },
    {
        "toko": "Arka Bike",
        "merk": "Vespa",
        "tipe": "Sprint",
        "warna": "Kuning",
        "jenis": "Motor",
        "harga": 250000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/LcXRpZdtgGf9wYYf8",
        "link_foto": "https://drive.google.com/file/d/1hpmLJ_kx1JrR8Za1fzihSAuV-h_7L4gj/view?usp=drive_link"
    },
    {
        "toko": "Arka Bike",
        "merk": "Honda",
        "tipe": "Stylo 160",
        "warna": "Hitam",
        "jenis": "Motor",
        "harga": 140000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/LcXRpZdtgGf9wYYf8",
        "link_foto": "https://drive.google.com/file/d/1-RP_yV0oIG_Fg8CvGgIlsEJbYhZ9hfZK/view?usp=drive_link"
    },
    {
        "toko": "Arka Bike",
        "merk": "Vespa",
        "tipe": "Sprint",
        "warna": "Dark Blue",
        "jenis": "Motor",
        "harga": 250000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/LcXRpZdtgGf9wYYf8",
        "link_foto": "https://drive.google.com/file/d/1QXZqph4j35NYq3-X6ZTDgCE6alWcUHmg/view?usp=drive_link"
    },
    {
        "toko": "Arka Bike",
        "merk": "Vespa",
        "tipe": "Primavera",
        "warna": "Green Relax",
        "jenis": "Motor",
        "harga": 250000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/LcXRpZdtgGf9wYYf8",
        "link_foto": "https://drive.google.com/file/d/175bUaq4fIVt4T6bO1mLDokSH2_OklYP2/view?usp=drive_link"
    },
    {
        "toko": "Arka Bike",
        "merk": "Honda",
        "tipe": "Scoopy",
        "warna": "Fashion Blue Matte",
        "jenis": "Motor",
        "harga": 90000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/LcXRpZdtgGf9wYYf8",
        "link_foto": "https://drive.google.com/file/d/1SBI0JRsoaFD6QsflBMPDOwa6RMlUcjhp/view?usp=drive_link"
    },
    {
        "toko": "Arka Bike",
        "merk": "Honda",
        "tipe": "PCX 160",
        "warna": "Hitam",
        "jenis": "Motor",
        "harga": 150000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/LcXRpZdtgGf9wYYf8",
        "link_foto": "https://drive.google.com/file/d/1nsK_P0roWbKBOyBZfUWt4CL-RnJ8FOgi/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Honda",
        "tipe": "WR-V",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 375000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/1jODhi-JraHa8ueD-NHY5LgU0AlAYgxXJ/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Honda",
        "tipe": "City HS",
        "warna": "Merah",
        "jenis": "Mobil",
        "harga": 400000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/1hY1hvpe7WbBL01f9bGH6DEFwlVWxGdeX/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Mitsubishi",
        "tipe": "New Xpander Ultimate",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 350000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/1GPGzom_3VB7VwUgCP-ZvRLJaH83I7oaI/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Suzuki",
        "tipe": "XL7",
        "warna": "Oranye",
        "jenis": "Mobil",
        "harga": 400000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/1oKio-OIrIJx53qzMDM_ZkagfV8Dndu7C/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Daihatsu",
        "tipe": "All New Terios",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 350000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/1pc58Zx03qu0ZjpKIA5M6xqLZ6Lk5H5Zb/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Honda",
        "tipe": "Vario 160 ABS",
        "warna": "Hitam",
        "jenis": "Motor",
        "harga": 140000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/1y_vx35zS5yunoJBlMT7gZQYVHHPvOJmi/view?usp=drive_link"
    },
    {
        "toko": "Semeton Pesiar",
        "merk": "Yamaha",
        "tipe": "Filano 125",
        "warna": "Violet",
        "jenis": "Motor",
        "harga": 120000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://g.co/kgs/U7E26Gd",
        "link_foto": "https://drive.google.com/file/d/18JLypjfS2HkKR5rhH-vxOKQPuh9ZXuTC/view?usp=drive_link"
    },
    {
        "toko": "Mataram Trans",
        "merk": "Wuling",
        "tipe": "Almaz",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 500000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1_qkvBN4Q81Vp_C1ZF_P4vRxN0HvkEQOU/view?usp=drive_link"
    },
    {
        "toko": "Mataram Trans",
        "merk": "Honda",
        "tipe": "BRV",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 350000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1V_dJ5rd2WR_ldgLF_5O4mwH0LIsFAN7_/view?usp=drive_link"
    },
    {
        "toko": "Mataram Trans",
        "merk": "Honda",
        "tipe": "Jazz RS",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 450000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/1g3t8J44l5dACYpXPihLp-hB9t2rFgFjE/view?usp=drive_link"
    },
    {
        "toko": "Mataram Trans",
        "merk": "Toyota",
        "tipe": "Yaris TRD Sportivo",
        "warna": "Hijau",
        "jenis": "Mobil",
        "harga": 375000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/NU2TfXuNwxWeiRsg6",
        "link_foto": "https://drive.google.com/file/d/116CPC94d849ZDSYU6VQRqj9lvI4-WcBI/view?usp=drive_link"
    },
    {
        "toko": "Teman Holiday Transport",
        "merk": "Honda",
        "tipe": "New HR-V",
        "warna": "Hitam",
        "jenis": "Mobil",
        "harga": 550000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/p8vQRg5Ho9yGGKNR6",
        "link_foto": "https://drive.google.com/file/d/1gmOdawQBQoPcHwqEPWavXfgYjsk8aBWO/view?usp=drive_link"
    },
    {
        "toko": "Hasmi",
        "merk": "Honda",
        "tipe": "Spacy 110",
        "warna": "Biru",
        "jenis": "Motor",
        "harga": 65000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/zmSb8SXQLqHnyrzY6",
        "link_foto": "https://drive.google.com/file/d/1j5jjXKEKiC1-YiRw15DdGSxjUasRsTmQ/view?usp=drive_link"
    },
    {
        "toko": "Hasmi",
        "merk": "Honda",
        "tipe": "Vario 160 CBS",
        "warna": "Putih",
        "jenis": "Motor",
        "harga": 100000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/zmSb8SXQLqHnyrzY6",
        "link_foto": "https://drive.google.com/file/d/1JPAlO9D1nT64qBGPDUQvM_qHPkIYphMZ/view?usp=drive_link"
    },
    {
        "toko": "HaloTrans",
        "merk": "Mitsubishi",
        "tipe": "Pajero Sport",
        "warna": "Putih",
        "jenis": "Mobil",
        "harga": 1200000,
        "status": "Sewa",
        "Bahan_Bakar": "Bensin",
        "link_lokasi": "https://maps.app.goo.gl/dzfGHLy89wydPSVs8",
        "link_foto": "https://drive.google.com/file/d/1qH9rXwRhapOw4pOFl936P8ydjGIKUUIB/view?usp=drive_link"
    }
]

# Buat folder fixtures jika belum ada
import os
if not os.path.exists('fixtures'):
    os.makedirs('fixtures')

# Konversi ke format fixture
fixtures = []
for idx, item in enumerate(data, start=1):
    fixture = {
        "model": "sewajual.vehicle",
        "pk": idx,
        "fields": {
            "toko": item["toko"],
            "merk": item["merk"],
            "tipe": item["tipe"],
            "warna": item["warna"],
            "jenis_kendaraan": item["jenis"],
            "harga": item["harga"],
            "status": item["status"],
            "bahan_bakar": item.get("Bahan_Bakar") or item.get("bahan_bakar", "Bensin"),
            "link_lokasi": item["link_lokasi"],
            "link_foto": item["link_foto"]
        }
    }
    fixtures.append(fixture)

# Simpan sebagai fixture
with open("fixtures/initial_vehicles.json", "w") as f:
    json.dump(fixtures, f, indent=4)

print(f"Berhasil membuat fixture dengan {len(fixtures)} data kendaraan")
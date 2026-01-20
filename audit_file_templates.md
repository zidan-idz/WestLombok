# Audit & Analisis File Template HTML

Dokumen ini membedah setiap file HTML di folder `templates/` untuk menjelaskan **Fungsi**, **Kenapa file ini ada**, **Bagaimana cara kerjanya**, dan **Letak Logikanya** (Backend yang terhubung).

---

## 📂 Folder Utama (`templates/`)

### 1. `base.html`

- **Fungsi:** Kerangka utama (Skeleton) website. Menampung `<head>`, Navbar, area konten (`{% block content %}`), dan Footer.
- **Kenapa:** Agar kita tidak perlu menulis ulang navbar/footer di setiap halaman. Prinsip DRY (_Don't Repeat Yourself_).
- **Letak Logika:** Tidak ada view khusus. Dipanggil oleh view lain melalui `extending`.
- **Cara Kerja:** Menyediakan "lubang" bernama `block content` yang akan diisi oleh halaman lain.

### 2. `404.html`

- **Fungsi:** Halaman error cantik saat user kesasar (URL tidak ditemukan).
- **Kenapa:** Halaman error bawaan Django jelek. Custom 404 membuat website terlihat profesional.
- **Letak Logika:** `apps/base/views.py` -> fungsi `custom_404`.
- **Cara Kerja:** Django mendeteksi error 404 -> `urls.py` mengarahkan ke handler 404 -> render template ini.

---

## 📂 Folder `templates/base/`

_Logika backend ada di `apps/base/views.py`_

### 3. `base/home.html`

- **Fungsi:** Halaman Depan (Homepage). Menampilkan Hero banner, Introduction, Popular Places, dan Kategori.
- **Kenapa:** "Wajah" pertama website. Harus menarik (Visual, Gacha, Slider).
- **Letak Logika:** `class HomeView` (TemplateView).
- **Cara Kerja:**
  - Menerima context `featured_destinasi` (3 terbaru) dan `popular_destinasi` (3 views terbanyak).
  - Menggunakan `{% for %}` loop untuk menampilkan kartu-kartu destinasi/kategori secara dinamis dari database.

### 4. `base/about.html`

- **Fungsi:** Halaman statis "Tentang Kami".
- **Kenapa:** Memberikan informasi kredibilitas pengelola website.
- **Letak Logika:** `class AboutView`.
- **Cara Kerja:** Utamanya HTML statis (teks biasa), karena tidak butuh banyak data dinamis.

---

## 📂 Folder `templates/core/`

_Logika backend ada di `apps/core/views.py`_

### 5. `core/destinasi_list.html`

- **Fungsi:** Menampilkan SEMUA destinasi dengan fitur pencarian dan paginasi.
- **Kenapa:** User butuh katalog lengkap untuk melihat-lihat isi seluruh website.
- **Letak Logika:** `class DestinasiListView` (ListView).
- **Cara Kerja:**
  - Menerima `destinasi_list` (bisa difilter via fitur search `?q=`).
  - Jika list kosong (hasil search zonk), menampilkan pesan "No results".

### 6. `core/destinasi_detail.html` (PALING PENTING)

- **Fungsi:** Halaman detail SATU tempat wisata. Ada Foto, Deskripsi, Peta, dan info lain.
- **Kenapa:** Tujuan utama user adalah membaca detail ini.
- **Letak Logika:** `class DestinasiDetailView` (DetailView).
- **Cara Kerja:**
  - URL mengirim parameter `slug` (misal: `/pantai-senggigi`).
  - View mencari data spesifik di DB berdasarkan slug.
  - Template menggunakan variable `{{ destinasi.nama_field }}` untuk menampilkan data.
  - Logic `{% if %}` dipakai untuk cek: "Ada foto tambahan nggak? Kalau ada tampilkan, kalau nggak, hide".

### 7. `core/kategori_list.html`

- **Fungsi:** Menampilkan daftar kategori wisata (Pantai, Gunung, dll).
- **Kenapa:** Membantu user memfilter minat mereka.
- **Letak Logika:** `class KategoriListView`.
- **Cara Kerja:** Loop data `Kategori` dari database. Menampilkan Icon dinamis (`{{ kategori.icon }}`) sesuai database.

### 8. `core/kategori_detail.html`

- **Fungsi:** Menampilkan daftar wisata HANYA untuk satu kategori tertentu (misal: hanya Pantai).
- **Kenapa:** Hasil filter dari klik di halaman `kategori_list`.
- **Letak Logika:** `class KategoriDetailView`.
- **Cara Kerja:** Mirip list, tapi datanya sudah difilter `.filter(kategori=...)` oleh View sebelum dikirim ke sini.

### 9. `core/surprise.html`

- **Fungsi:** Halaman hasil fitur "Gacha" / Random Picker.
- **Kenapa:** Fitur unik/gimmick agar user tidak bosan.
- **Letak Logika:** fungsi `surprise_me` di `views.py`.
- **Cara Kerja:** Menerima _shuffled list_ dari backend, lalu frontend (JS/Anime.js) membuat animasi "mengundi" sebelum menampilkan 1 hasil pemenang.

---

## 📂 Folder `templates/components/` & `partials/`

_Potongan kode (Partial) yang bisa dipakai ulang._

### 10. `navbar.html`

- **Fungsi:** Menu navigasi atas (Home, Destinations, dll).
- **Cara Kerja:** Menggunakan tag `{% url 'nama_view' %}`. Jadi kalau URL berubah di backend, link ini tidak akan rusak/mati.

### 11. `footer.html`

- **Fungsi:** Bagian bawah (Copyright, Sosmed).
- **Cara Kerja:** HTML statis dengan link.

### 12. `partials/_base_style.html`

- **Fungsi:** Tempat import Font (Google Fonts) dan Load CSS Utama (`styles.css`).
- **Kenapa:** Agar `head.html` bersih. Menggunakan `django-tailwind` (lokal), bukan CDN lagi. Jadi bisa jalan offline dan lebih cepat.

---

## 📂 Folder `templates/unfold/` (Admin Panel)

### 13. `unfold/index.html`

- **Fungsi:** Halaman Dashboard Admin custom.
- **Kenapa:** Admin bawaan Django polos. Kita override pakai `django-unfold` biar modern & ada statistik grafik/kartu.
- **Letak Logika:** `django-unfold` library + custom context processor `dashboard_extras`.
- **Cara Kerja:** Menimpa template admin default. Menampilkan data jumlah user/destinasi lewat _Template Tags_ (`{% get_destinasi_count %}`).

---

## 📂 Folder `templates/registration/` (Authentication)

### 14. `login.html` & `logged_out.html`

- **Fungsi:** Halaman Login admin dan Logout.
- **Cara Kerja:** Standar Django Auth System. Form login dikirim via POST ke view login bawaan Django.

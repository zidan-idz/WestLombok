# Panduan Struktur Proyek West Lombok

Dokumen ini adalah "Contekan" (Cheat Sheet) untuk memahami struktur codingan proyek ini. Gunakan ini untuk menjawab pertanyaan dosen atau pembimbing.

## 1. Konsep Dasar Architecture

Proyek ini menggunakan **Django** dengan pola **MVT (Model - View - Template)**.

- **Model (Database):** Blueprint tabel-tabel data.
- **View (Logika):** Pelayan yang mengambil data dari Model dan mengirimnya ke Template.
- **Template (Tampilan):** File HTML yang dilihat user.

## 2. Peta Folder & File Penting

### A. Folder `config/` (Pusat Kontrol)

Di sini tempat "Otak" pengaturan Django.

- **`settings.py`**: **FILE PALING PENTING.** Isinya daftar aplikasi yang dipasang (`INSTALLED_APPS`), setting database, bahasa, dan folder static. Kalau ditanya "Dimana kamu atur koneksi database?", jawab: "Di `settings.py`".
- **`urls.py`**: "Gerbang Utama". Mengatur URL level proyek. Misal `/admin/` masuk ke admin panel, `/` masuk ke aplikasi utama.

### B. Folder `apps/` (Logika Aplikasi)

Kita memecah aplikasi jadi dua bagian biar rapi (Modular).

1.  **`apps/core/`** (Inti Data)
    - **`models.py`**: Berisi tabel **Destinasi** dan **Kategori**. Di sinilah kita mendefinisikan field seperti `nama_destinasi`, `foto_utama`, `slug`, dll.
    - **`views.py`**: Logika halaman detail, list, dan fitur "Surprise Me".
2.  **`apps/base/`** (Halaman Umum)
    - **`views.py`**: Logika untuk halaman **Home** dan **About**.
    - **`models.py`**: Kosong (karena base cuma halaman statis, tidak simpan data khusus).

### C. Folder `templates/` (Tampilan HTML)

- **`base.html`**: Kerangka utama website (Induk). Memuat Navbar dan Footer. Semua halaman lain "numpang" (extend) di sini.
- **`partials/_base_style.html`**: File khusus untuk load Font (Oswald/Inter) dan CSS.
- **`components/`**: Potongan HTML kecil seperti Navbar dan Footer biar `base.html` gak kepanjangan.
- **`base/home.html`**: Codingan halaman depan.
- **`core/`**: Codingan halaman Destinasi dan Kategori.

### D. Folder `theme/` (Tampilan / CSS)

- Ini adalah aplikasi khusus **django-tailwind**.
- Berisi kodingan CSS mentah yang nanti dikompilasi jadi CSS beneran. Kalau mau ubah konfigurasi Tailwind, carinya di sini.

---

## 3. Alur Kerja (Jika Ditanya "Gimana cara kerjanya?")

Contoh kasus: **User membuka halaman Detail Destinasi.**

1.  **URL**: User akses `/destinasi/pantai-senggigi/`.
2.  **URL Conf**: Django cek `urls.py`, nemu pola `/destinasi/<slug>/`. Diteruskan ke View.
3.  **View**: `DestinasiDetailView` di `apps/core/views.py` bekerja.
    - Dia cari di Database: "Ada gak Destinasi yang slug-nya 'pantai-senggigi'?".
    - Kalau ada, dia tambah `jumlah_views + 1`.
4.  **Template**: Data dikirim ke `templates/core/destinasi_detail.html`.
    - HTML merender: Gambar, Judul, Deskripsi.
5.  **Response**: User lihat halaman cantik di browser.

---

## 4. Jawaban untuk Pertanyaan Sulit ("Jebakan")

**Q: Kenapa file-nya dipisah-pisah (ada apps/core, apps/base)?**
**A:** Agar **Modular**, Pak/Bu. Kalau nanti proyeknya besar, gampang di-manage. `Core` khusus ngurus data wisata, `Base` khusus halaman statis. Jadi codingan gak numpuk di satu file.

**Q: "Surprise Me" itu algoritmanya apa?**
**A:** Itu menggunakan **Random Shuffle**. Sistem mengambil list destinasi, lalu diacak urutannya menggunakan library `random` bawaan Python, lalu ditampilkan. Sederhana tapi interaktif.

**Q: Kenapa pakai Tailwind CSS?**
**A:** Agar development UI lebih cepat dan modern. Kita menggunakan **django-tailwind** (bukan CDN), jadi CSS-nya di-compile di server sendiri. Kelebihannya: file lebih kecil (automatis dibuang class yang gak kepakai) dan aplikasi bisa berjalan **Offline** tanpa internet.

**Q: Icon-nya itu gimana logikanya?**
**A:** Icon disimpan di Database (`models.py` di tabel `Kategori`). Saat admin input kategori, nama icon Material Design disimpan. Di frontend, kita tinggal panggil `{{ kategori.icon }}`. Jadi dinamis, admin bisa ganti icon tanpa bongkar kodingan.

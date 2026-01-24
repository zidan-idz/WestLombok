import os
from django.core.management.base import BaseCommand
from apps.core.models import Destination, District, Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Imports destination data from a predefined list.'

    def handle(self, *args, **kwargs):
        destinations_data = [
            # --- KECAMATAN BATULAYAR ---
            {"name": "Pantai Senggigi", "category": "Wisata Bahari", "district": "Batulayar", "description": "Sebagai ikon pariwisata tertua dan paling mapan di Lombok, Pantai Senggigi menawarkan garis pantai teluk yang panjang dengan gradasi pasir dari putih ke hitam. Kawasan ini merupakan pusat akomodasi utama yang memiliki fasilitas terlengkap, mulai dari resort bintang lima hingga hiburan malam. Pemandangan matahari terbenam (sunset) di sini sangat ikonik karena posisi mataharinya yang seringkali jatuh tepat di samping siluet Gunung Agung, Bali.", "extra_info": "Lokasi sangat strategis di jalan raya utama. Akses mudah ke transportasi umum, ATM, dan klinik kesehatan 24 jam."},
            {"name": "Pura Batu Bolong", "category": "Wisata Religi", "district": "Batulayar", "description": "Pura unik yang dibangun di atas batu karang hitam besar yang menjorok ke arah laut. Sesuai namanya, batu karang ini memiliki lubang alami di tengahnya akibat kikisan ombak. Selain menjadi tempat peribadatan umat Hindu yang sakral, lokasi ini menawarkan titik pandang dramatis untuk fotografi, terutama saat ombak besar menghantam karang dengan latar belakang selat Lombok.", "extra_info": "Wajib mengenakan selendang kuning (tersedia di loket). Wanita haid dilarang masuk area suci."},
            {"name": "Makam Batulayar", "category": "Wisata Religi", "district": "Batulayar", "description": "Situs religi yang memakamkan Sayid Ali Al-Baghdad, salah satu tokoh penting penyebar agama Islam di Lombok. Makam ini terletak di lokasi strategis dekat pantai dan selalu ramai dikunjungi peziarah lokal maupun luar daerah untuk berdoa dan bernazar. Puncak keramaian terjadi saat tradisi Lebaran Topat (seminggu setelah Idul Fitri), di mana ribuan warga berkumpul di area ini.", "extra_info": "Area sakral, harap berpakaian sopan. Ramai pedagang kaki lima saat hari libur Islam."},
            {"name": "Pantai Kerandangan", "category": "Wisata Bahari", "district": "Batulayar", "description": "Terletak tidak jauh dari Senggigi, Pantai Kerandangan menawarkan suasana yang jauh lebih asri dengan hamparan kebun kelapa dan lahan berumput yang luas di bibir pantai. Destinasi ini menjadi favorit warga lokal untuk piknik keluarga di akhir pekan karena suasananya yang teduh. Ombaknya relatif tenang di beberapa titik, namun tetap perlu waspada di bagian tengah.", "extra_info": "Terkenal dengan warung Sate Bulayak di pinggir pantai. Parkir luas untuk mobil."},
            {"name": "Pantai Mangsit", "category": "Wisata Bahari", "district": "Batulayar", "description": "Pantai Mangsit dikenal sebagai kawasan yang lebih eksklusif dan tenang dibandingkan tetangganya. Garis pantainya didominasi oleh resort-resort butik dan hotel berbintang yang menjaga kebersihan area pesisir dengan sangat baik. Pasirnya cenderung lebih putih dan suasananya sangat hening, menjadikannya lokasi ideal bagi wisatawan yang mencari privasi dan relaksasi total.", "extra_info": "Akses publik terbatas (lewat celah antar hotel). Cocok untuk yang mencari ketenangan total."},

            # --- KECAMATAN NARMADA ---
            {"name": "Desa Wisata Mekarsari", "category": "Wisata Pedesaan & Kriya", "district": "Narmada", "description": "Desa Wisata Mekarsari menonjolkan potensi agrowisata dengan hamparan perkebunan buah tropis yang subur. Pengunjung diajak merasakan suasana pedesaan yang otentik, berinteraksi dengan petani lokal, dan menikmati hasil bumi langsung dari pohonnya. Desa ini juga aktif mengembangkan produk ekonomi kreatif berbahan dasar potensi alam setempat.", "extra_info": "Pusat oleh-oleh buah musiman (Rambutan/Durian/Manggis). Warga sangat terbuka untuk edukasi pertanian."},
            {"name": "Taman Narmada", "category": "Wisata Sejarah & Warisan", "district": "Narmada", "description": "Dibangun pada tahun 1727 oleh Raja Anak Agung Ngurah Karangasem, taman ini didesain sebagai replika Gunung Rinjani dan Danau Segara Anak. Kompleks taman seluas 2 hektar ini memiliki nilai historis tinggi sebagai tempat peristirahatan raja dan upacara adat. Salah satu daya tarik mistisnya adalah keberadaan mata air yang dipercaya dapat membuat awet muda.", "extra_info": "Tiket masuk murah. Wajib coba sate bulayak di area parkir depan."},
            {"name": "Hutan Wisata Sesaot", "category": "Wisata Alam & Ekowisata", "district": "Narmada", "description": "Kawasan hutan lindung yang dikelola oleh masyarakat setempat (Community Based Tourism). Daya tarik utamanya adalah sungai berbatu dengan air yang sangat jernih dan dingin yang mengalir di tengah hutan mahoni. Suasana pegunungan yang sejuk menjadikan tempat ini lokasi favorit untuk 'ngadem' dan menikmati kuliner tradisional di gazebo-gazebo tepi sungai.", "extra_info": "Bisa camping. Air sungai sangat dingin, hati-hati batuan licin saat hujan."},
            {"name": "Pemandian Aik Nyet", "category": "Wisata Alam & Ekowisata", "district": "Narmada", "description": "Aik Nyet (Air Dingin) adalah pemandian alami yang bersumber langsung dari mata air tanah di dalam hutan Sesaot, bukan sekadar aliran sungai. Hal ini membuat airnya luar biasa jernih, bersih, dan menyegarkan badan seketika. Kolam-kolam alaminya dikelilingi akar pohon besar yang menambah kesan eksotis dan alami.", "extra_info": "Fasilitas ganti baju sederhana. Sangat ramai saat akhir pekan oleh warga lokal."},
            {"name": "Air Terjun Segenter", "category": "Wisata Alam & Ekowisata", "district": "Narmada", "description": "Sebuah permata tersembunyi bagi para petualang. Air Terjun Segenter menawarkan debit air yang deras dengan kolam alami yang bisa digunakan untuk berenang. Karena lokasinya yang belum banyak dijamah infrastruktur modern, keasrian alam di sekitarnya masih sangat terjaga, memberikan sensasi petualangan rimba yang sesungguhnya.", "extra_info": "Akses butuh trekking 20-30 menit. Fasilitas minim (hanya parkir & warung kecil)."},
            {"name": "Bunut Ngengkang", "category": "Wisata Alam & Ekowisata", "district": "Narmada", "description": "Objek wisata alam yang unik karena keberadaan pohon Bunut besar yang akarnya membentuk celah atau gerbang alami. Di bawah naungan pohon-pohon besar ini terdapat aliran air dan kolam pemandian yang jernih. Tempat ini sering menjadi titik istirahat atau tujuan akhir bagi komunitas pesepeda gunung (gowes) di Lombok.", "extra_info": "Kolam ramah anak. Akses jalan sebagian masih tanah/bebatuan."},
            {"name": "Kolam Renang Suranadi", "category": "Wisata Alam & Ekowisata", "district": "Narmada", "description": "Kolam renang legendaris yang sudah ada sejak zaman kolonial Belanda. Keistimewaannya terletak pada airnya yang berasal dari mata air alami yang terus mengalir (sirkulasi alami), sehingga tidak menggunakan kaporit atau bahan kimia penjernih. Airnya sangat dingin dan menyegarkan, dikelilingi oleh pepohonan tua yang rindang.", "extra_info": "Air sangat dingin. Terdapat hotel heritage di dalam kompleks."},
            {"name": "Pura Suranadi", "category": "Wisata Religi", "district": "Narmada", "description": "Kompleks pura tertua di Lombok yang didirikan oleh Dang Hyang Nirartha pada abad ke-16. Pura ini sangat sakral bagi umat Hindu karena keberadaan 'Panca Tirta' atau lima mata air suci yang digunakan untuk upacara penyucian. Di aliran sungai area pura, terdapat belut-belut raksasa (moa) yang dianggap keramat dan tidak boleh diganggu.", "extra_info": "Dilarang menangkap ikan atau mengganggu belut di area sungai pura."},

            # --- KECAMATAN LINGSAR ---
            {"name": "Pura Lingsar", "category": "Wisata Sejarah & Warisan", "district": "Lingsar", "description": "Simbol toleransi beragama yang hidup di Lombok. Dibangun pada 1714, kompleks ini unik karena menggabungkan Pura Gaduh (tempat ibadah Hindu) dan Kemaliq (tempat sakral bagi Islam Wetu Telu) dalam satu area. Setiap tahun, kedua umat mengadakan upacara 'Perang Topat' bersama-sama sebagai wujud syukur atas hasil panen.", "extra_info": "Situs Perang Topat (biasanya bulan November/Desember). Wajib pakai selendang saat masuk."},
            {"name": "Air Terjun Timponan", "category": "Wisata Alam & Ekowisata", "district": "Lingsar", "description": "Air terjun dengan ketinggian sekitar 40 meter yang terletak di lereng kawasan hutan Rinjani. Untuk mencapainya, pengunjung harus melewati jalur trekking yang cukup menantang melintasi perkebunan kopi, kakao, dan hutan lindung yang lebat. Suasana di lokasi sangat sunyi dan privat, cocok untuk meditasi alam.", "extra_info": "Akses sulit untuk mobil biasa. Parkir jauh (jalan kaki 5km) atau sewa ojek trail warga lokal."},
            {"name": "Masjid Kuno Wetu Telu Karang Bayan", "category": "Wisata Sejarah & Warisan", "district": "Lingsar", "description": "Masjid bersejarah yang menjadi saksi bisu perkembangan Islam tradisional di Lombok. Bangunan masjid ini mempertahankan arsitektur asli Suku Sasak dengan fondasi tanah yang ditinggikan, dinding anyaman bambu, dan atap ilalang. Masjid ini terletak di desa adat yang masih memegang teguh tradisi leluhur dan dikelilingi kebun buah.", "extra_info": "Momen terbaik saat musim durian. Desa ini sentra penghasil durian Lingsar."},

            # --- KECAMATAN SEKOTONG ---
            {"name": "Gili Nanggu", "category": "Wisata Bahari", "district": "Sekotong", "description": "Sering disebut sebagai 'Aquarium Raksasa', Gili Nanggu menawarkan pengalaman snorkeling di mana ribuan ikan warna-warni berenang bebas bahkan di air setinggi lutut. Pulau ini menerapkan aturan ketat larangan memancing dan berdagang asongan, sehingga suasananya sangat tenang, bersih, dan privat seperti pulau pribadi.", "extra_info": "Bawa roti tawar untuk memberi makan ikan. Akomodasi terbatas (hanya satu Resort/Cottage)."},
            {"name": "Gili Sudak", "category": "Wisata Bahari", "district": "Sekotong", "description": "Pulau tetangga Gili Nanggu yang terkenal dengan garis pantainya yang landai dan perairan yang sangat tenang hampir tanpa ombak. Gili Sudak menjadi destinasi kuliner favorit untuk menikmati makan siang ikan bakar segar di pinggir pantai. Di perairan dangkalnya sering ditemukan banyak bintang laut.", "extra_info": "Banyak bintang laut (Starfish). Jangan diangkat dari air demi kelestarian mereka."},
            {"name": "Gili Kedis", "category": "Wisata Bahari", "district": "Sekotong", "description": "Pulau pasir putih super mungil yang unik karena berbentuk hati jika dilihat dari udara (drone). Saking kecilnya, pengunjung bisa mengelilingi seluruh pulau ini dengan berjalan kaki hanya dalam waktu 5 menit. Dikelilingi air turkis jernih, pulau ini menjadi spot foto paling romantis dan instagramable di kawasan Sekotong.", "extra_info": "Tidak ada penginapan. Hanya warung kecil untuk kelapa muda/mie instan dan toilet sederhana."},
            {"name": "Gili Gede", "category": "Wisata Bahari", "district": "Sekotong", "description": "Merupakan pulau terbesar ('Gede' berarti Besar) di gugusan pulau Sekotong. Gili Gede telah berkembang menjadi destinasi internasional dengan adanya Marina untuk kapal Yacht dari luar negeri. Meskipun fasilitasnya lengkap dan modern, pulau ini masih mempertahankan suasana desa nelayan yang ramah dan tenang.", "extra_info": "Akses mudah via pelabuhan Tembowong. Penduduk ramah dan banyak opsi penginapan."},
            {"name": "Gili Asahan", "category": "Wisata Bahari", "district": "Sekotong", "description": "Surga tersembunyi yang menjadi favorit para penyelam (divers) karena arus bawah lautnya yang tenang dan visibilitas air yang jernih. Gili Asahan memiliki 'Coral Garden' yang masih sangat sehat dan berwarna-warni. Suasana di daratannya sangat santai (laid-back), jauh dari hiruk pikuk pariwisata massal.", "extra_info": "Atmosfer sangat tenang. Favorit turis Eropa dan pasangan Honeymoon."},
            {"name": "Gili Layar", "category": "Wisata Bahari", "district": "Sekotong", "description": "Destinasi wajib bagi pecinta snorkeling. Gili Layar memiliki terumbu karang yang sangat rapat dan sehat tepat di depan bibir pantai. Pengunjung bisa melihat Blue Coral dan berbagai biota laut langka tanpa harus menyelam dalam. Pulau ini masih sangat alami dengan fasilitas yang sederhana namun nyaman.", "extra_info": "Hati-hati bulu babi saat air surut. Tersedia bungalow sederhana di pinggir pantai."},
            {"name": "Pantai Mekaki", "category": "Wisata Bahari", "district": "Sekotong", "description": "Sebuah teluk raksasa yang menghadap langsung ke Samudera Hindia. Pantai Mekaki memiliki hamparan pasir putih yang sangat luas dan bersih, dikelilingi oleh perbukitan hijau yang menjulang. Karena lokasinya yang cukup jauh, pantai ini masih sangat sepi dan memberikan nuansa eksklusif seolah memiliki pantai pribadi.", "extra_info": "Jalan menuju lokasi sudah aspal mulus tapi berkelok tajam. Belum ada fasilitas toilet memadai."},
            {"name": "Pantai Elak-Elak", "category": "Wisata Bahari", "district": "Sekotong", "description": "Pantai tanjung yang unik karena posisinya membuat air laut di sini sangat tenang, nyaris seperti danau. Sangat aman untuk berenang bagi anak-anak. Di sekitar pantai terdapat hamparan rumput yang cocok untuk menggelar tikar dan menikmati bekal makanan sambil melihat pemandangan gili-gili di seberang.", "extra_info": "Sering ada patroli keamanan. Lokasi populer untuk bakar ikan warga lokal saat liburan."},
            {"name": "Pantai Nambung", "category": "Wisata Bahari", "district": "Sekotong", "description": "Pantai ini terkenal dengan fenomena alam unik yang disebut 'Air Terjun Asin'. Fenomena ini terjadi ketika ombak besar dari laut lepas menghantam jajaran tebing karang di pinggir pantai, kemudian airnya jatuh kembali ke laut menyerupai air terjun. Pemandangan ini sangat eksotis dan jarang ditemukan di tempat lain.", "extra_info": "Akses jalan ujung masih tanah/berbatu. Fenomena air terjun paling bagus terlihat saat ombak besar/pasang."},
            {"name": "Bangko-Bangko (Desert Point)", "category": "Wisata Bahari", "district": "Sekotong", "description": "Legenda di kalangan peselancar dunia. Bangko-Bangko atau Desert Point diakui sebagai salah satu spot surfing terbaik di dunia dengan ombak kidal (left-hand barrel) yang sangat panjang dan sempurna. Tempat ini adalah destinasi petualangan murni, dengan kondisi alam yang keras dan kering namun menantang.", "extra_info": "Khusus peselancar Pro. Jalan akses rusak parah/offroad. Tidak cocok untuk wisata keluarga biasa."},

            # --- KECAMATAN GUNUNG SARI ---
            {"name": "Hutan Pusuk (Monkey Forest)", "category": "Wisata Alam & Ekowisata", "district": "Gunung Sari", "description": "Jalan raya pegunungan yang membelah hutan lindung dan dihuni oleh ratusan kera ekor panjang yang hidup liar. Wisatawan biasanya berhenti di pinggir jalan untuk memberi makan kera sambil menikmati pemandangan lembah hijau yang menakjubkan dari ketinggian. Udara di sini sangat sejuk dan sering berkabut.", "extra_info": "Hati-hati barang bawaan (kacamata/topi/HP) sering diambil monyet. Parkir di bahu jalan."},
            {"name": "Air Terjun Kekait (Tibu Ijo)", "category": "Wisata Alam & Ekowisata", "district": "Gunung Sari", "description": "Air terjun alami yang terletak di tengah perkebunan aren milik warga. Dikenal juga sebagai Tibu Ijo karena kolam alaminya berwarna kehijauan akibat pantulan lumut dan rimbunnya pepohonan. Perjalanan menuju lokasi memberikan pengalaman melihat proses penyadapan air nira (bahan gula aren) secara tradisional.", "extra_info": "Trekking santai 1 jam lewat kebun durian/aren. Tidak ada tiket resmi, hanya parkir di rumah warga."},
            {"name": "Pasar Seni Sesela", "category": "Wisata Pedesaan & Kriya", "district": "Gunung Sari", "description": "Pusat kerajinan tangan tertua di Lombok Barat yang menampung ratusan pengrajin lokal. Di sini, pengunjung tidak hanya berbelanja, tetapi bisa melihat langsung proses ukiran kayu, pembuatan Cukli (potongan kulit kerang yang ditanam di kayu), dan anyaman rotan. Produk dari pasar ini sudah diekspor ke berbagai negara.", "extra_info": "Harga bisa nego langsung dengan pengrajin. Tempat terbaik pesan furnitur custom."},
            {"name": "Cafless Waterpark", "category": "Wisata Alam & Ekowisata", "district": "Gunung Sari", "description": "Taman rekreasi air buatan yang modern dan lengkap di kawasan Gunungsari. Menawarkan berbagai wahana permainan air seperti seluncuran spiral dan ember tumpah yang sangat disukai anak-anak. Menjadi alternatif wisata keluarga yang praktis dan dekat dari pusat kota.", "extra_info": "Fasilitas lengkap (Kantin, Loker, Mushola, Parkir Luas). Sangat ramai saat libur sekolah."},

            # --- KECAMATAN KEDIRI ---
            {"name": "Desa Wisata Banyumulek", "category": "Wisata Pedesaan & Kriya", "district": "Kediri", "description": "Sentra industri kerajinan gerabah (tembikar) terbesar di Pulau Lombok. Hampir seluruh warga desa ini berprofesi sebagai pengrajin tanah liat secara turun-temurun. Wisatawan dapat mengunjungi galeri-galeri seni sepanjang jalan dan mencoba pengalaman langsung membuat gerabah dengan teknik putar tradisional (hand-thrown).", "extra_info": "Bisa bawa pulang hasil karya sendiri setelah kursus singkat. Galeri buka setiap hari."},

            # --- KECAMATAN GERUNG ---
            {"name": "Desa Wisata Kebon Ayu", "category": "Wisata Pedesaan & Kriya", "district": "Gerung", "description": "Desa wisata yang sedang naik daun dengan konsep ekowisata dan pelestarian budaya. Daya tarik utamanya adalah agrowisata petik buah melon golden dan pasar kuliner tradisional yang menyajikan jajanan jaman dulu. Desa ini juga memiliki jembatan gantung bersejarah peninggalan Belanda yang menjadi spot foto ikonik.", "extra_info": "Wajib coba jajanan pasar di area 'Kebon Ayu'. Transaksi kadang unik pakai koin kayu (saat event tertentu)."},

            # --- KECAMATAN LEMBAR ---
            {"name": "Makam Keramat Lembar", "category": "Wisata Religi", "district": "Lembar", "description": "Situs pemakaman kuno yang terletak di atas bukit dengan pemandangan ke arah pelabuhan. Makam ini dikeramatkan oleh masyarakat pesisir Lembar dan sering dikunjungi untuk ziarah kubur. Lokasinya yang hening memberikan suasana spiritual yang kental bagi para peziarah.", "extra_info": "Akses jalan sedikit menanjak. Buka setiap hari, biasanya ramai pada malam Jumat."},
            {"name": "Pantai Cemare", "category": "Wisata Bahari", "district": "Lembar", "description": "Pantai unik yang terletak di pertemuan antara muara sungai dan laut lepas. Kawasan ini dikelilingi oleh hutan mangrove yang lebat, menciptakan ekosistem yang kaya. Selain berwisata, pengunjung bisa membeli ikan segar dengan harga murah langsung dari perahu nelayan yang baru bersandar.", "extra_info": "Tiket masuk sangat murah. Fasilitas lengkap (Gazebo/Mushola). Akses lewat jembatan gantung."},
            {"name": "Ekowisata Mangrove Lembar", "category": "Wisata Alam & Ekowisata", "district": "Lembar", "description": "Kawasan konservasi hutan bakau yang telah disulap menjadi destinasi wisata edukasi yang menarik. Pengunjung dapat menyusuri hutan bakau melalui jalur titian kayu (boardwalk) yang panjang dan berwarna-warni. Tempat ini sangat cocok untuk pengenalan lingkungan pesisir dan berburu foto saat matahari terbenam.", "extra_info": "Spot foto Instagramable. Waktu terbaik kunjungan: sore hari agar tidak terlalu panas."},

            # --- KECAMATAN KURIPAN ---
            {"name": "Gunung Sasak", "category": "Wisata Alam & Ekowisata", "district": "Kuripan", "description": "Kawasan wisata pegunungan yang menawarkan jalur hiking ringan dengan panorama alam yang luas. Dari puncaknya, pengunjung bisa melihat hamparan sawah, perbukitan, hingga laut di kejauhan. Hutan di gunung ini juga menjadi habitat bagi kawanan monyet liar yang sering menampakkan diri.", "extra_info": "Bawa air minum sendiri karena jarang pedagang di atas. Populer untuk komunitas sepeda gunung (MTB)."}
        ]

        media_path = 'destinations/primary/'
        extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
        # Map Indonesian category names to English DB names
        category_map = {
            "Wisata Bahari": "Marine Tourism",
            "Wisata Religi": "Pilgrimage Tourism",
            "Wisata Pedesaan & Kriya": "Rural & Craft Tourism",
            "Wisata Sejarah & Warisan": "Heritage Tourism",
            "Wisata Alam & Ekowisata": "Nature & Ecotourism",
        }
        
        created_count = 0
        skipped_count = 0

        for item in destinations_data:
            # Get or Skip District
            try:
                district = District.objects.get(name__iexact=item['district'])
            except District.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"District '{item['district']}' not found. Skipping {item['name']}."))
                skipped_count += 1
                continue
            
            # Get or Skip Category (using mapping)
            category_name_en = category_map.get(item['category'], item['category'])
            try:
                category = Category.objects.get(name__iexact=category_name_en)
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Category '{item['category']}' (mapped: '{category_name_en}') not found. Skipping {item['name']}."))
                skipped_count += 1
                continue

            # Find matching image
            image_path = None
            for ext in extensions:
                potential_path = media_path + item['name'] + ext
                full_path = os.path.join('media', potential_path)
                if os.path.exists(full_path):
                    image_path = potential_path
                    break
            
            # Special case for "Pantai Senggigi" -> "Pantai Sengigi" (typo in file)
            if not image_path and item['name'] == "Pantai Senggigi":
                for ext in extensions:
                    potential_path = media_path + "Pantai Sengigi" + ext
                    full_path = os.path.join('media', potential_path)
                    if os.path.exists(full_path):
                        image_path = potential_path
                        break
            
            # Special case for Air Terjun Kekait
            if not image_path and "Kekait" in item['name']:
                for ext in extensions:
                    potential_path = media_path + "Air Terjun Kekait" + ext
                    full_path = os.path.join('media', potential_path)
                    if os.path.exists(full_path):
                        image_path = potential_path
                        break

            # Create Destination
            dest, created = Destination.objects.get_or_create(
                name=item['name'],
                defaults={
                    'slug': slugify(item['name']),
                    'description': item['description'],
                    'additional_info': item.get('extra_info', ''),
                    'district': district,
                    'category': category,
                    'main_image': image_path if image_path else '',
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"Created: {dest.name} (Image: {image_path or 'No Match'})")
            else:
                self.stdout.write(f"Skipped (exists): {dest.name}")
        
        self.stdout.write(self.style.SUCCESS(f'\nImport Complete: {created_count} created, {skipped_count} skipped.'))

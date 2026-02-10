# 🏋️ AI Personal Trainer — Gerçek Zamanlı Şınav Sayacı

Bu proje, insan vücudunun eklem noktalarını ve bu noktalar arasındaki açıları analiz ederek **şınav hareketlerini otomatik olarak algılayan ve sayan** bir kişisel antrenör uygulamasıdır. OpenCV ve MediaPipe kütüphaneleri kullanılarak Python'da geliştirilmiştir.

---

## Nasıl Çalışır?

Projenin çalışma mantığı üç temel adıma dayanır:

### 1. Vücut Eklem Noktalarının Tespiti
MediaPipe Pose modeli, her video karesinde insan vücudundaki **33 eklem noktasını (landmark)** gerçek zamanlı olarak tespit eder. Bu noktalar görüntünün piksel koordinatlarına dönüştürülerek bir listeye kaydedilir.

### 2. Dirsek Açısının Trigonometrik Hesaplanması
Şınav hareketini ölçmek için **sol omuz (11), sol dirsek (13) ve sol el bileği (15)** noktaları kullanılır. Bu üç nokta arasındaki açı `math.atan2` fonksiyonu ile hesaplanır:

```
angle = degrees( atan2(y3−y2, x3−x2) − atan2(y1−y2, x1−x2) )
```

Dirsek köşe noktası olarak alınır ve diğer iki noktanın ona göre yaptığı açı bulunur.

### 3. Akıllı Sayma Mekanizması
Ham açı değeri `np.interp` ile **0–100 arasında bir yüzdeye** dönüştürülür:

| Pozisyon | Açı | Yüzde |
|----------|-----|-------|
| Kalkış (üst) | ~185° | %0 |
| İniş (alt) | ~245° | %100 |

Sayma işlemi bir **yön değişkeni (`dir`)** ile kontrol edilir:
- Açı **%100**'e ulaşınca (aşağı iniş tamamlandı) → `+0.5` sayı, `dir = 1`
- Açı **%0**'a ulaşınca (yukarı kalkış tamamlandı) → `+0.5` sayı, `dir = 0`
- Tam bir iniş + kalkış döngüsü = **1 şınav**

Bu yöntem sayesinde hareket yarıda bırakılsa da çift sayma önlenir, yerde beklenilse de sayaç tetiklenmez.

---

## Özellikler

- 🤖 **Otomatik Şınav Sayma:** İniş ve kalkış hareketini ayrı ayrı tespit ederek tam şınav sayısını ekranda gösterir.
- 📐 **Açı Görselleştirme:** Omuz, dirsek ve bilek noktaları sarı dairelerle işaretlenir, aralarına kırmızı çizgiler çizilir, anlık açı değeri ekrana yazdırılır.
- 📊 **Yüzde Bazlı Hareket Takibi:** `np.interp` ile açı değeri yüzdeye çevrilerek hareketin ne kadar tamamlandığı sürekli ölçülür.
- 🎥 **Video & Kamera Desteği:** Hem kayıtlı video dosyası hem de canlı webcam akışı ile çalışır.
- 🧠 **Çift Sayma Koruması:** `dir` değişkeni ile her hareket yalnızca bir kez sayılır.

---

## Kurulum

```bash
# 1. Repoyu klonlayın
git clone https://github.com/kullanici-adi/personal-trainer-app-mediapipe.git
cd personal-trainer-app-mediapipe

# 2. Sanal ortam oluşturun ve aktif edin
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt
```

---

## Kullanım

```bash
python main.py
```

> **Video Modu:** `cap = cv2.VideoCapture("video1.mp4")` satırına kendi video dosyanızın adını yazın.
>
> **Kamera Modu:** Aynı satırı `cap = cv2.VideoCapture(0)` olarak değiştirin.

---

## Kullanılan MediaPipe Landmark Noktaları

Şınav tespitinde kullanılan eklem noktaları:

| ID | Nokta          | Rol                      |
|----|----------------|--------------------------|
| 11 | Sol Omuz       | Açı hesabının başlangıcı |
| 13 | Sol Dirsek ⭐  | Açının köşe (orta) noktası |
| 15 | Sol El Bileği  | Açı hesabının bitişi     |

![MediaPipe Pose Landmarks](https://mediapipe.dev/images/mobile/pose_tracking_full_body_landmarks.png)

---

## Öğrenilenler

- `math.atan2` ile üç nokta arasındaki açının trigonometrik olarak hesaplanması.
- `np.interp` ile ham açı değerinin anlamlı bir yüzde aralığına (0–100) dönüştürülmesi.
- Yön değişkeni (`dir`) kullanarak çift sayma sorununu önleme ve hareket döngüsünü doğru takip etme.
- MediaPipe landmark koordinatlarını görüntü boyutuna göre ölçeklendirme (`lm.x * w`, `lm.y * h`).
- Sanal ortam (virtual environment) yönetimi ve bağımlılık takibi.

---

## Kullanılan Teknolojiler

| Kütüphane      | Versiyon   | Kullanım Amacı                    |
|----------------|------------|-----------------------------------|
| OpenCV         | 4.8.1.78   | Görüntü işleme ve görselleştirme  |
| MediaPipe      | 0.10.7     | Vücut eklem noktası tespiti       |
| NumPy          | 1.24.3     | Açı değerinin interpolasyonu      |

---

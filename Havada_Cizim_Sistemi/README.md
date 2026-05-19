# Havada Çizim Sistemi

Bu proje Python, OpenCV ve MediaPipe kullanılarak geliştirilmiş gerçek zamanlı bir havada çizim uygulamasıdır.

Kullanıcı el hareketleriyle ekrana çizim yapabilmektedir.

---

# Proje Özellikleri

- El hareketi ile çizim
- Gerçek zamanlı el takibi
- Renk değiştirme sistemi
- Sanal boya paleti
- İki parmak ile silgi modu
- El kapalıyken çizimi durdurma
- FPS göstergesi
- Temizleme butonu

---

# Kullanılan Teknolojiler

- Python
- OpenCV
- MediaPipe
- NumPy

---

# Çalışma Mantığı

Proje kameradan alınan görüntüyü işler.

MediaPipe kullanılarak elin landmark noktaları tespit edilir.

İşaret parmağı ile çizim yapılır.

İşaret ve orta parmak açık olduğunda silgi modu aktif olur.

Üst menü yardımıyla renk değiştirilebilir veya ekran temizlenebilir.

---

# Kontroller

| Hareket | İşlev |
|---|---|
| 1 Parmak Açık | Çizim Yapma |
| 2 Parmak Açık | Silgi Modu |
| El Kapalı | Çizimi Durdurma |
| TEMİZLE Butonu | Ekranı Temizleme |
| Q Tuşu | Programdan Çıkış |

---

# Kurulum

Aşağıdaki komutu terminale yazınız:

```bash
pip install opencv-python mediapipe numpy
```

---

# Programı Çalıştırma

```bash
python main.py
```

---

# Geliştirici

İsmail
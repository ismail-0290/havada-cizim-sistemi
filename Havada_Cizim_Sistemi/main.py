# ==========================================================
# GEREKLI KUTUPHANELER
# ==========================================================

import cv2                  # Kamera ve goruntu islemleri
import mediapipe as mp      # El takibi
import numpy as np          # Matematiksel islemler
import time                 # FPS hesaplama


# ==========================================================
# KAMERA AYARLARI
# ==========================================================

# Bilgisayarin kamerasini ac
cap = cv2.VideoCapture(0)

# Kamera cozunurlugu
width = 1280
height = 720

# Kamera boyutlarini ayarla
cap.set(3, width)
cap.set(4, height)


# ==========================================================
# MEDIAPIPE EL TAKIBI
# ==========================================================

# MediaPipe Hands modulunu kullan
mp_hands = mp.solutions.hands

# El takip sistemi
hands = mp_hands.Hands(

    # El algilama guven oranı
    min_detection_confidence=0.7,

    # El takip guven oranı
    min_tracking_confidence=0.7,

    # Maksimum el sayisi
    max_num_hands=1
)

# El cizimleri icin
mp_draw = mp.solutions.drawing_utils


# ==========================================================
# CANVAS (CIZIM ALANI)
# ==========================================================

# Beyaz arkaplan olustur
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255


# ==========================================================
# RENKLER
# OpenCV BGR formatı kullanır
# ==========================================================

BLUE = (255, 140, 0)        # Turkuaz mavi
GREEN = (0, 220, 80)        # Canli yesil
RED = (60, 60, 255)         # Parlak kirmizi
PURPLE = (180, 0, 255)      # Canli mor

# Varsayilan cizim rengi
draw_color = BLUE


# ==========================================================
# FIRCA VE SILGI AYARLARI
# ==========================================================

# Firca kalinligi
brush_thickness = 7

# Silgi boyutu
eraser_size = 40


# ==========================================================
# ONCEKI NOKTALAR
# Cizginin surekli olmasi icin kullanilir
# ==========================================================

prev_x, prev_y = 0, 0


# ==========================================================
# FPS ICIN ZAMAN DEGISKENI
# ==========================================================

# Onceki frame zamani
prev_time = 0


# ==========================================================
# PARMAK KONTROL FONKSIYONU
# Hangi parmaklarin acik oldugunu kontrol eder
# ==========================================================

def fingers_up(hand_landmarks):

    # Acik parmaklari tutacak liste
    fingers = []

    # ======================================================
    # BASPARMAK KONTROLU
    # ======================================================

    # Basparmak saga bakiyorsa aciktir
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:

        fingers.append(1)

    else:

        fingers.append(0)

    # ======================================================
    # DIGER PARMAKLAR
    # ======================================================

    # Parmak ucu landmark numaralari
    tip_ids = [8, 12, 16, 20]

    # Her parmak icin kontrol yap
    for tip in tip_ids:

        # Parmak ucu yukaridaysa parmak acik kabul edilir
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:

            fingers.append(1)

        else:

            fingers.append(0)

    return fingers


# ==========================================================
# ANA DONGU
# ==========================================================

while True:

    # Kameradan goruntu al
    success, frame = cap.read()

    # Kamera calismiyorsa cik
    if not success:
        break

    # ======================================================
    # GORUNTUYU AYNALA
    # ======================================================

    # Kamerayi ayna gibi kullanmak icin
    frame = cv2.flip(frame, 1)

    # Boyutlandir
    frame = cv2.resize(frame, (width, height))

    # ======================================================
    # BGR -> RGB DONUSUMU
    # MediaPipe RGB ile calisir
    # ======================================================

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # El takibi yap
    results = hands.process(rgb)


    # ======================================================
    # UST MENU
    # ======================================================

    # Ust menu arkaplani
    cv2.rectangle(frame, (0, 0), (width, 100), (35, 35, 35), -1)

    # ======================================================
    # RENK KUTULARI
    # ======================================================

    colors = [

        # Mavi kutu
        (BLUE, (50, 20, 140, 80)),

        # Yesil kutu
        (GREEN, (180, 20, 270, 80)),

        # Kirmizi kutu
        (RED, (310, 20, 400, 80)),

        # Mor kutu
        (PURPLE, (440, 20, 530, 80))
    ]

    # Kutulari ekrana ciz
    for color, (x1, y1, x2, y2) in colors:

        # Renk kutusu
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

        # Beyaz kenarlik
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            2
        )


    # ======================================================
    # TEMIZLE BUTONU
    # ======================================================

    cv2.rectangle(frame, (650, 20), (850, 80), (0, 255, 255), -1)

    cv2.putText(
        frame,
        "TEMIZLE",
        (675, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        3
    )


    # ======================================================
    # EL ALGILANDIYSA
    # ======================================================

    if results.multi_hand_landmarks:

        # Algilanan her el icin
        for hand_landmarks in results.multi_hand_landmarks:

            # ==================================================
            # EL ISKELETINI CIZ
            # ==================================================

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Landmark listesi
            lm = hand_landmarks.landmark


            # ==================================================
            # ISARET PARMAGI KOORDINATLARI
            # Landmark 8 -> Isaret parmagi ucu
            # ==================================================

            index_x = int(lm[8].x * width)
            index_y = int(lm[8].y * height)


            # ==================================================
            # ORTA PARMAK KOORDINATLARI
            # Landmark 12 -> Orta parmak ucu
            # ==================================================

            middle_x = int(lm[12].x * width)
            middle_y = int(lm[12].y * height)


            # ==================================================
            # ACIK PARMAKLARI BUL
            # ==================================================

            fingers = fingers_up(hand_landmarks)


            # ==================================================
            # CIZIM MODU
            # Sadece isaret parmagi acik
            # ==================================================

            if fingers[1] == 1 and fingers[2] == 0:

                # Isaret parmaginin ucuna daire ciz
                cv2.circle(
                    frame,
                    (index_x, index_y),
                    10,
                    draw_color,
                    -1
                )

                # ==============================================
                # MENU KONTROLU
                # ==============================================

                # Parmak ust menudeyse
                if index_y < 100:

                    # Cizgiyi kes
                    prev_x, prev_y = 0, 0

                    # ==========================================
                    # RENK SECIMLERI
                    # ==========================================

                    # MAVI
                    if 50 < index_x < 140:
                        draw_color = BLUE

                    # YESIL
                    elif 180 < index_x < 270:
                        draw_color = GREEN

                    # KIRMIZI
                    elif 310 < index_x < 400:
                        draw_color = RED

                    # MOR
                    elif 440 < index_x < 530:
                        draw_color = PURPLE

                    # ==========================================
                    # TEMIZLE BUTONU
                    # ==========================================

                    elif 650 < index_x < 850:

                        # Tum canvasi beyaz yap
                        canvas[:] = 255

                # ==============================================
                # CIZIM ALANI
                # ==============================================

                else:

                    # Ilk nokta
                    if prev_x == 0 and prev_y == 0:

                        prev_x, prev_y = index_x, index_y

                    # Onceki nokta ile yeni nokta arasina cizgi ciz
                    cv2.line(
                        canvas,
                        (prev_x, prev_y),
                        (index_x, index_y),
                        draw_color,
                        brush_thickness
                    )

                    # Yeni noktayi kaydet
                    prev_x, prev_y = index_x, index_y


            # ==================================================
            # SILGI MODU
            # Isaret + orta parmak acik
            # ==================================================

            elif fingers[1] == 1 and fingers[2] == 1:

                # Cizgiyi kes
                prev_x, prev_y = 0, 0

                # Silginin merkez noktasi
                center_x = (index_x + middle_x) // 2
                center_y = (index_y + middle_y) // 2

                # Kirmizi silgi halkasi
                cv2.circle(
                    frame,
                    (center_x, center_y),
                    eraser_size,
                    (0, 0, 255),
                    3
                )

                # Canvasi beyaza boyayarak sil
                cv2.circle(
                    canvas,
                    (center_x, center_y),
                    eraser_size,
                    (255, 255, 255),
                    -1
                )


            # ==================================================
            # EL KAPALIYSA CIZIM DURUR
            # ==================================================

            else:

                prev_x, prev_y = 0, 0

    else:

        prev_x, prev_y = 0, 0


    # ==========================================================
    # CANVAS + KAMERA BIRLESTIRME
    # ==========================================================

    # Canvasi griye cevir
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    # Beyaz olmayan yerleri ayir
    _, thresh = cv2.threshold(
        gray,
        250,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Tek kanalli goruntuyu 3 kanala cevir
    thresh_colored = cv2.cvtColor(
        thresh,
        cv2.COLOR_GRAY2BGR
    )

    # Sadece cizim kisimlarini al
    drawing = cv2.bitwise_and(
        canvas,
        thresh_colored
    )

    # Kamera goruntusu ile cizimi birlestir
    final_frame = cv2.addWeighted(
        frame,
        1,
        drawing,
        1,
        0
    )


    # ==========================================================
    # FPS HESABI
    # ==========================================================

    # Simdiki zamani al
    current_time = time.time()

    # FPS hesapla
    # FPS = 1 saniye / frame suresi
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0

    # Onceki zamani guncelle
    prev_time = current_time


    # ==========================================================
    # FPS YAZISI
    # ==========================================================

    cv2.putText(
        final_frame,
        f"FPS: {int(fps)}",
        (1050, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )


    # ==========================================================
    # ALT BILGILER
    # ==========================================================

    cv2.putText(
        final_frame,
        "1 Parmak = Cizim",
        (20, 650),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        final_frame,
        "2 Parmak = Silgi",
        (20, 690),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # ==========================================================
    # EKRANA GOSTER
    # ==========================================================

    cv2.imshow(
        "Havada Cizim Sistemi",
        final_frame
    )


    # ==========================================================
    # KLAVYE KONTROLU
    # ==========================================================

    key = cv2.waitKey(1)

    # Q tusuna basilirsa cik
    if key == ord("q"):
        break


# ==========================================================
# PROGRAMI KAPAT
# ==========================================================

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
import pytesseract
import time
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://of91778:of91778@cluster3.l7a1a5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster3")
db = client["registros"]
collection_1 = db["datos"]

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Definir la ruta del video y la carpeta de destino para la captura de pantalla
video_path = 0  # Cambiar a 0 para usar la camara web
save_folder = "./static/imgs"

cap = cv2.VideoCapture(video_path)

# Variables para el control del tiempo
start_time_imagen = time.time()
interval_imagen = 7  # Intervalo de tiempo en segundos para la captura de pantalla
interval_matriculas = 7  # Intervalo de tiempo en segundos entre cada impresiin de matricula
last_print_time = start_time_imagen  # Tiempo de la ultima impresion de matricula

counter = 0  # Contador para nombres de archivo

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar video")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if 2.5 < aspect_ratio < 4.0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                plate_region = gray[y:y + h, x:x + w]
                plate_text = pytesseract.image_to_string(plate_region, config='--psm 7')
                print(plate_text)
                
                # Validar que el texto sea una cadena de texto valida y tenga al menos 7 caracteres antes de guardarlo
                if isinstance(plate_text, str) and plate_text.isalpha() and len(plate_text) >= 7:
                    elapsed_since_last_print = time.time() - last_print_time
                    if elapsed_since_last_print >= interval_matriculas:
                        existing_document = collection_1.find_one({"matricula": plate_text})

                        if existing_document:
                            # Modificar los valores de fecha_hora_salida y dentro_de_estacionamiento
                            data_to_modify = {
                                "fecha_hora_salida": datetime.now(),
                                "dentro_de_estacionamiento": False
                            }
                            collection_1.find_one_and_update(
                                {"_id": existing_document["_id"]},
                                {"$set": data_to_modify}
                            )
                            print(f"Se ha actualizado el documento para la matricula {plate_text}.")
                        else:
                            print(f"No se encontri ningun documento para la matricula {plate_text} en la base de datos.")

    cv2.imshow('Reconocimiento de placas', frame)

    # Verificar si ha pasado el intervalo de tiempo para la captura de pantalla
    elapsed_time_imagen = time.time() - start_time_imagen
    if elapsed_time_imagen >= interval_imagen:
        cv2.imwrite(save_folder + f"screenshot_{counter}.jpg", frame)
        start_time_imagen = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
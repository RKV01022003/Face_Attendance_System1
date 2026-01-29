import cv2
import os
import numpy as np
import shutil

# -------------------- User Input --------------------
name = input("Enter your name: ").strip()
dataset_root = "dataset"
dataset_path = os.path.join(dataset_root, name)
os.makedirs(dataset_path, exist_ok=True)

# -------------------- Load Haar Cascade --------------------
cascade_path = "haarcascade_frontalface_default.xml"
if not os.path.exists(cascade_path):
    raise FileNotFoundError("❌ haarcascade_frontalface_default.xml not found")

face_cascade = cv2.CascadeClassifier(cascade_path)
cap = cv2.VideoCapture(0)

# -------------------- Load existing model and labels --------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
labels_path = "labels.npy"
model_path = "face_model.yml"

if os.path.exists(model_path):
    recognizer.read(model_path)

if os.path.exists(labels_path):
    label_map = np.load(labels_path, allow_pickle=True).item()
else:
    label_map = {}

# -------------------- Duplicate Detection Settings --------------------
CONFIDENCE_THRESHOLD = 50
DUPLICATE_REQUIRED = 5
duplicate_hits = {}

# -------------------- Function to check for duplicate face --------------------
def is_duplicate(face_roi):
    if face_roi is None or face_roi.size == 0:
        return None

    for lbl, existing_name in label_map.items():
        person_folder = os.path.join(dataset_root, existing_name)
        if not os.path.exists(person_folder):
            continue

        faces = []
        for img_file in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None and img.size > 0:
                faces.append(img)

        if not faces:
            continue

        temp_recognizer = cv2.face.LBPHFaceRecognizer_create()
        temp_recognizer.train(faces, np.array([0] * len(faces)))

        try:
            _, confidence = temp_recognizer.predict(face_roi)
            if confidence < CONFIDENCE_THRESHOLD:
                return existing_name
        except:
            pass

    return None

# -------------------- Capture Images --------------------
print(f"📸 Capturing 30 images for '{name}'...")
count = 0
max_images = 10
duplicate_detected = False

while count < max_images:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        if face_roi.size == 0:
            continue

        existing_name = is_duplicate(face_roi)

        if existing_name:
            duplicate_hits[existing_name] = duplicate_hits.get(existing_name, 0) + 1

            if duplicate_hits[existing_name] >= DUPLICATE_REQUIRED:
                if existing_name == name:
                    print(f"⚠️ You are already registered as '{name}'. Registration aborted.")
                else:
                    print(f"⚠️ This face is already registered under '{existing_name}'. Cannot register as '{name}'!")
                duplicate_detected = True
                break
        else:
            duplicate_hits.clear()

        count += 1
        cv2.imwrite(os.path.join(dataset_path, f"{count}.jpg"), face_roi)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Register Face", frame)
    if cv2.waitKey(1) == 27 or duplicate_detected:
        break

cap.release()
cv2.destroyAllWindows()

# -------------------- Cleanup if duplicate --------------------
if duplicate_detected:
    shutil.rmtree(dataset_path, ignore_errors=True)
    exit()

# -------------------- Train recognizer with ALL dataset --------------------
faces = []
labels = []
label_map = {}
current_label = 0

for person in os.listdir(dataset_root):
    person_folder = os.path.join(dataset_root, person)
    if not os.path.isdir(person_folder):
        continue

    label_map[current_label] = person

    for img_file in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None and img.size > 0:
            faces.append(img)
            labels.append(current_label)

    current_label += 1

if faces and labels:
    recognizer.train(faces, np.array(labels))
    recognizer.save(model_path)
    np.save(labels_path, label_map)
    print(f"✅ Model trained successfully for '{name}'")
else:
    print("⚠️ No valid face data found. Model not trained.")

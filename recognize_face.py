import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os

# -------------------- Paths --------------------
model_path = "face_model.yml"
cascade_path = "haarcascade_frontalface_default.xml"
csv_path = "attendance.csv"
labels_path = "labels.npy"  # Stores mapping from label -> name

# -------------------- Load face detector & recognizer --------------------
face_cascade = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(model_path)

# -------------------- Load label mapping --------------------
if os.path.exists(labels_path):
    labels_dict = np.load(labels_path, allow_pickle=True).item()
else:
    labels_dict = {0: "rishabh"}  # default single user

# -------------------- Ensure CSV exists --------------------
if not os.path.exists(csv_path):
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("Name,Date,Punch_In,Punch_Out\n")

# -------------------- Attendance marking function --------------------
def mark_attendance(pred_name, entered_name=None):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    df = pd.read_csv(csv_path)

    # Warn if someone tries to punch other person's attendance
    if entered_name and entered_name != pred_name:
        print(f"⚠️ WARNING: Attempt to punch attendance for {entered_name} by {pred_name} detected!")
        return

    mask = (df["Name"] == pred_name) & (df["Date"] == today)

    if not mask.any():
        # First punch today → Punch-In
        df = pd.concat([df, pd.DataFrame([[pred_name, today, now, ""]], columns=df.columns)], ignore_index=True)
        df.to_csv(csv_path, index=False)
        print(f"✅ {pred_name} punched in at {now}")

    else:
        punch_out_time = df.loc[mask, "Punch_Out"].values[0]
        if pd.isna(punch_out_time) or punch_out_time == "":
            # First punch-out → store the time
            df.loc[mask, "Punch_Out"] = now
            df.to_csv(csv_path, index=False)
            print(f"✅ {pred_name} punched out at {now}")
        else:
            # Already punched out
            print(f"⚠️ {pred_name} already punched out today at {punch_out_time}")

# -------------------- Start camera --------------------
cap = cv2.VideoCapture(0)
recognized = False

while not recognized:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face_roi)

        if confidence < 70:  # confident match
            pred_name = labels_dict.get(label, "Unknown")
            entered_name = pred_name  # automatic punch-in/out

            mark_attendance(pred_name, entered_name)
            recognized = True
            break
        else:
            print("⚠️ Face not recognized confidently. Possible spoof attempt!")
            recognized = True
            break

# -------------------- Release camera --------------------
cap.release()
cv2.destroyAllWindows()
print("Camera closed. Attendance marked successfully.")

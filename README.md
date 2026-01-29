# 🎯 Face Recognition Attendance System

A Python-based **Face Recognition Attendance System** that uses **OpenCV** and **LBPH (Local Binary Pattern Histogram)** for secure, automatic attendance tracking.  
This system supports **user registration, real-time attendance marking, duplicate face prevention, and visual attendance records**.

It is designed for **schools, offices, or any organization** where automated attendance is required.

---

## 🚀 Features

### 👤 User Registration
- Users can register using a **webcam face capture**.
- Prevents:
  - Same person registering under **different names**.
  - Already registered users registering again.
- Face data is **stored locally** until explicitly deleted by an authorized user.
- Registration includes **multiple images per user** to improve recognition accuracy.

### ⏱️ Attendance System
- **Automatic Punch-In**: When a registered face is recognized, the system automatically logs the attendance.
- **Automatic Punch-Out**: Next recognition of the same face automatically logs punch-out.
- Prevents multiple punch-outs in a single day for a user.
- **Camera closes automatically** after attendance is marked.

### 📋 Attendance Management
- Attendance is stored in `attendance.csv` in a **structured format**:
  - Columns: `Name, Date, Time, Status`
- Provides options to **view complete attendance sheets**.
- **Deleted users** are automatically removed from attendance records.

### 🔐 Security Logic
- Duplicate face detection is implemented using **confidence thresholds** from the LBPH recognizer.
- Requires multiple confirmations before declaring a duplicate.
- Protects against **proxy attendance** (someone trying to mark attendance for another).

### 📊 Visualization
- Displays **real-time camera feed** with recognized faces highlighted.
- Shows **name and confidence score** for recognition.
- Generates logs and visual feedback for debugging and accuracy assessment.

---

## 🛠️ Technologies Used

- **Python 3** – Main programming language
- **OpenCV (cv2)** – Face detection and recognition
- **NumPy** – Numerical operations
- **Pandas** – Attendance data handling
- **LBPH Face Recognizer** – Recognition algorithm
- **Haar Cascade Classifier** – For initial face detection

---

## 📂 Project Structure


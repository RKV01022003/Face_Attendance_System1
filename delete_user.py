import os
import numpy as np
import pandas as pd
import shutil

# Paths
labels_path = "labels.npy"
dataset_path = "dataset"
csv_path = "attendance.csv"

# Load existing labels
if os.path.exists(labels_path):
    labels_dict = np.load(labels_path, allow_pickle=True).item()
else:
    print("No labels found. Nothing to delete.")
    exit()

# Ask for names to delete
names_to_delete = input("Enter the name(s) of user(s) to delete (comma-separated): ").split(",")
names_to_delete = [name.strip() for name in names_to_delete]

deleted_any = False

for name in names_to_delete:
    # Delete from labels
    keys_to_remove = [k for k, v in labels_dict.items() if v == name]
    if keys_to_remove:
        for k in keys_to_remove:
            labels_dict.pop(k)
        deleted_any = True
        print(f"✅ User '{name}' deleted from labels.")
    else:
        print(f"⚠️ User '{name}' not found in labels.")

    # Delete user's dataset folder if exists
    user_folder = os.path.join(dataset_path, name)
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        print(f"✅ Dataset folder for '{name}' deleted.")

# Save updated labels
if deleted_any:
    np.save(labels_path, labels_dict)

# Delete user's attendance entries
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    initial_len = len(df)
    df = df[~df["Name"].isin(names_to_delete)]
    if len(df) < initial_len:
        df.to_csv(csv_path, index=False)
        print("✅ Attendance sheet updated.")
    else:
        print("No entries found in attendance sheet for the deleted user(s).")

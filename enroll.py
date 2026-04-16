import cv2
import numpy as np
import pickle
import os
from deepface import DeepFace

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

DB_PATH = "database/users.pkl"

def load_users():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "rb") as f:
            return pickle.load(f)
    return []

def save_users(users):
    with open(DB_PATH, "wb") as f:
        pickle.dump(users, f)

def get_embedding(frame):
    result = DeepFace.represent(
        frame,
        model_name="Facenet",
        enforce_detection=False
    )
    return np.array(result[0]["embedding"])

# ---------------- MAIN ENROLLMENT ---------------- #

name = input("Enter user name: ")

cap = cv2.VideoCapture(0)

print("\nLook at the camera. Collecting samples...")

embeddings = []
samples = 5  # number of face samples

count = 0

while count < samples:
    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        break

    cv2.putText(frame, f"Capturing sample {count+1}/{samples}",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Enrollment", frame)

    # Capture frame every short interval
    key = cv2.waitKey(1000)  # 1 second delay per sample

    try:
        embedding = get_embedding(frame)
        embeddings.append(embedding)
        count += 1
        print(f"Sample {count} captured")
    except:
        print("Face not detected, retrying...")

# Average embeddings for stability
if len(embeddings) == 0:
    print("No valid face samples captured.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

final_embedding = np.mean(embeddings, axis=0)

# Load existing users
users = load_users()

# Save new user
users.append({
    "name": name,
    "embedding": final_embedding
})

save_users(users)

print(f"\n{name} enrolled successfully with {len(embeddings)} samples!")

cap.release()
cv2.destroyAllWindows()
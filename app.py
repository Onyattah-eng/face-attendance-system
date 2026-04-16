import cv2
import numpy as np
import pickle
from deepface import DeepFace
from attendance import mark_attendance
from collections import deque


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Load database
with open("database/users.pkl", "rb") as f:
    users = pickle.load(f)

cap = cv2.VideoCapture(0)

history = deque(maxlen=5)

print("AI Recognition Running... Press Q to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = DeepFace.represent(
            frame, model_name="Facenet", enforce_detection=False
        )[0]["embedding"]

        embedding = np.array(result)

        best_match = "Unknown"
        best_score = 0

        for user in users:
            score = cosine_similarity(embedding, user["embedding"])

            if score > best_score:
                best_score = score
                best_match = user["name"]

        # Threshold check
        if best_score < 0.55:
            best_match = "Unknown"

        # Stability logic
        history.append(best_match)

        if history.count(best_match) >= 3 and best_match != "Unknown":
            final_name = best_match
            mark_attendance(final_name)
        else:
            final_name = "Scanning..."

        label = f"{final_name} ({round(best_score, 2)})"

    except:
        label = "No Face Detected"

    cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AI Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

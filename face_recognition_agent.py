import cv2
from deepface import DeepFace

class FaceRecognitionAgent:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analyze_face(self, image_path):
        # Load an image and detect faces
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        results = []
        # Analyze each face
        for (x, y, w, h) in faces:
            face_img = img[y:y+h, x:x+w]
            analysis = DeepFace.analyze(face_img, actions=['emotion', 'age', 'gender', 'race'])
            results.append(analysis)
            # Draw rectangle around face
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Faces', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return results

    def process_video(self, video_path):
        # Capture video
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                analysis = DeepFace.analyze(face_img, actions=['emotion', 'age', 'gender', 'race'])
                # (Add your processing logic here)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
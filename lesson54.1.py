import cv2
import matplotlib.pyplot as plt

img = cv2.imread('img.webp')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

face_data = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

faces = face_data.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5)
print(faces)

for (x, y, width, height) in faces:
    cv2.circle(img_rgb, (x + (width // 2), y + (height // 2)), width // 2, (0, 255, 0), 5)

plt.subplot(1, 1, 1)
plt.imshow(img_rgb)
plt.show()
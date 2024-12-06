import cv2
import numpy as np
import math


image_path = r"C:\Users\ASUS\Documents\Semester 4\OpenCv\th-3844684407.jpg"


image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Gambar tidak ditemukan di path {image_path}")


h, w = image.shape[:2]


# 1. Translation
translation_matrix = np.array([[1, 0, 50],
                               [0, 1, 30],
                               [0, 0, 1]])

translated_image = np.zeros_like(image)
for y in range(h):
    for x in range(w):
        original_coords = np.array([x, y, 1])
        new_coords = translation_matrix @ original_coords
        new_x, new_y = int(new_coords[0]), int(new_coords[1])

        if 0 <= new_x < w and 0 <= new_y < h:
            translated_image[new_y, new_x] = image[y, x]


# 2. Rotasi
angle = math.radians(45)
rotation_matrix = np.array([[math.cos(angle), -math.sin(angle), 0],
                            [math.sin(angle), math.cos(angle), 0],
                            [0, 0, 1]])

center_x, center_y = w // 2, h // 2
rotated_image = np.zeros_like(image)

for y in range(h):
    for x in range(w):
        relative_coords = np.array([x - center_x, y - center_y, 1])
        new_coords = rotation_matrix @ relative_coords
        new_x, new_y = int(new_coords[0] + center_x), int(new_coords[1] + center_y)

        if 0 <= new_x < w and 0 <= new_y < h:
            rotated_image[new_y, new_x] = image[y, x]


# 3. Scaling
scaling_matrix = np.array([[1.5, 0, 0],
                           [0, 1.5, 0],
                           [0, 0, 1]])

scaled_h, scaled_w = int(h * 1.5), int(w * 1.5)
scaled_image = np.zeros((scaled_h, scaled_w, 3), dtype=image.dtype)

for y in range(h):
    for x in range(w):
        original_coords = np.array([x, y, 1])
        new_coords = scaling_matrix @ original_coords
        new_x, new_y = int(new_coords[0]), int(new_coords[1])

        if 0 <= new_x < scaled_w and 0 <= new_y < scaled_h:
            scaled_image[new_y, new_x] = image[y, x]


# 4. Skewing
skewing_matrix = np.array([[1, 1.5, 0],
                            [0.5, 1, 0],
                            [0, 0, 1]])

skewed_h, skewed_w = int(h * 2), int(w * 2)
skewed_image = np.zeros((skewed_h, skewed_w, 3), dtype=image.dtype)

for y in range(h):
    for x in range(w):
        original_coords = np.array([x, y, 1])
        new_coords = skewing_matrix @ original_coords
        new_x, new_y = int(new_coords[0]), int(new_coords[1])

        if 0 <= new_x < skewed_w and 0 <= new_y < skewed_h:
            skewed_image[new_y, new_x] = image[y, x]

cv2.imshow("Original Image", image)
cv2.imshow("Translated Image", translated_image)
cv2.imshow("Rotated Image", rotated_image)
cv2.imshow("Scaled Image", scaled_image)
cv2.imshow("Skewed Image", skewed_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

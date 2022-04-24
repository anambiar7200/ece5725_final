import cv2
 # Load an image. 
 # Photo by Heather Ehrhart: https://www.pexels.com/photo/a-playful-dog-with-its-mouth-open-11757552/

img = cv2.imread("dog.jpg")

cv2.imshow("DOG", img)
cv2.waitKey(0)
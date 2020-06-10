import cv2

# Start default camera

video = cv2.VideoCapture( 0 )
while video.isOpened():
    ret, frame = video.read()
    cv2.imshow( "frame", frame )

key = cv2.waitKey( 1 ) & 0xFF
video.release()
cv2.destroyAllWindows()
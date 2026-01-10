import cv2
import os

print("Testing cameras... Saving test images to identify them\n")

# Create test_images folder
os.makedirs("test_images", exist_ok=True)

camera_indices = [0, 2, 3, 4]

for idx in camera_indices:
    print(f"\n{'='*50}")
    print(f"Testing Camera {idx}")
    print(f"{'='*50}")
    
    cap = cv2.VideoCapture(idx)
    if not cap.isOpened():
        print(f"❌ Camera {idx} failed to open")
        continue
    
    # Get camera info
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"✅ Camera {idx} opened successfully")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    
    # Capture a frame
    ret, frame = cap.read()
    if ret:
        filename = f"test_images/camera_{idx}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✅ Saved test image: {filename}")
    else:
        print(f"❌ Failed to capture from camera {idx}")
    
    cap.release()

print("\n" + "="*50)
print("Camera test complete!")
print("\nCheck the 'test_images' folder to see which camera is which:")
print("  - camera_0.jpg")
print("  - camera_2.jpg")
print("  - camera_3.jpg")
print("  - camera_4.jpg")
print("\nIdentify your cameras:")
print("  - Gripper camera index: ?")
print("  - Tripod camera index: ?")
print("="*50)

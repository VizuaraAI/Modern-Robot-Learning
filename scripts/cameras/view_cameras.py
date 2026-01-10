import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading

class CameraViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Identification Tool")
        self.root.geometry("1200x900")
        self.root.configure(bg='#2b2b2b')
        
        # Camera indices to test
        self.camera_indices = [0, 2, 3, 4]
        self.caps = {}
        self.labels = {}
        self.running = True
        
        # Title
        title = tk.Label(root, text="Camera Identification - Find Your Gripper & Tripod Cameras", 
                        font=("Arial", 16, "bold"), bg='#2b2b2b', fg='white')
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(root, 
                              text="Look at the camera feeds below and identify:\n• Gripper Camera (close-up view near robot hand)\n• Tripod Camera (overview/side view of workspace)", 
                              font=("Arial", 11), bg='#2b2b2b', fg='#cccccc', justify='left')
        instructions.pack(pady=5)
        
        # Create grid for camera feeds (2x2)
        main_frame = tk.Frame(root, bg='#2b2b2b')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Configure grid
        for i in range(2):
            main_frame.grid_rowconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)
        
        # Create camera display areas
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for idx, (row, col) in zip(self.camera_indices, positions):
            # Frame for each camera
            cam_frame = tk.Frame(main_frame, bg='#1e1e1e', relief='ridge', bd=2)
            cam_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Camera title
            cam_title = tk.Label(cam_frame, text=f"📷 CAMERA {idx}", 
                                font=("Arial", 14, "bold"), bg='#1e1e1e', fg='#00ff00')
            cam_title.pack(pady=5)
            
            # Resolution info
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                res_label = tk.Label(cam_frame, text=f"Resolution: {width}x{height}", 
                                    font=("Arial", 9), bg='#1e1e1e', fg='#888888')
                res_label.pack()
                self.caps[idx] = cap
            else:
                error_label = tk.Label(cam_frame, text="❌ CAMERA NOT AVAILABLE", 
                                      font=("Arial", 12), bg='#1e1e1e', fg='red')
                error_label.pack(pady=50)
                continue
            
            # Image display
            img_label = tk.Label(cam_frame, bg='black')
            img_label.pack(expand=True, fill='both', padx=5, pady=5)
            self.labels[idx] = img_label
        
        # Start video update thread
        self.update_thread = threading.Thread(target=self.update_frames, daemon=True)
        self.update_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def update_frames(self):
        """Continuously update camera frames"""
        while self.running:
            for idx in self.camera_indices:
                if idx not in self.caps:
                    continue
                
                cap = self.caps[idx]
                ret, frame = cap.read()
                
                if ret:
                    # Resize frame to fit display (maintain aspect ratio)
                    frame = cv2.resize(frame, (480, 360))
                    
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Convert to PIL Image
                    img = Image.fromarray(frame_rgb)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(image=img)
                    
                    # Update label
                    if idx in self.labels:
                        self.labels[idx].configure(image=photo)
                        self.labels[idx].image = photo  # Keep a reference
    
    def on_close(self):
        """Clean up when closing window"""
        self.running = False
        for cap in self.caps.values():
            cap.release()
        self.root.destroy()
        
        # Print summary
        print("\n" + "="*60)
        print("CAMERA IDENTIFICATION COMPLETE")
        print("="*60)
        print("\nIdentify your cameras from the feed you just saw:")
        print(f"  Available camera indices: {self.camera_indices}")
        print("\nNote down:")
        print("  • Gripper camera index: _____")
        print("  • Tripod camera index: _____")
        print("="*60)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraViewer(root)
    root.mainloop()

# Hardware Setup Guide

Hey everyone! Welcome to the **second guide** in our SO-101 LeRobot tutorial series.

Now that we have all the software installed, it's time to connect and configure the hardware. In this guide, we'll connect your SO-101 robots to your PC, identify the correct ports, and set up your cameras. Let's dive in!

---

## Step 1: Connect Your Hardware to PC

First, let's physically connect everything:

1. **Connect the Follower Robot**: Plug the USB cable from your SO-101 follower arm into your PC
2. **Connect the Leader Robot**: Plug the USB cable from your SO-101 leader arm into your PC
3. **Connect Cameras**: Plug in your camera(s) to the USB ports

Make sure all devices are powered on and properly connected.

---

## Step 2: Find Robot COM Ports

Now we need to identify which COM port each robot is connected to. We'll use the `lerobot-find-port` command for this.

### Find Follower Robot Port

First, disconnect the leader robot (keep only follower connected), then run:

```bash
lerobot-find-port
```

This will scan and show you the available ports. Note down the COM port for your **follower robot** (e.g., `COM10`).

### Find Leader Robot Port

Now disconnect the follower and connect only the leader robot, then run:

```bash
lerobot-find-port
```

Note down the COM port for your **leader robot** (e.g., `COM9`).

**Pro tip:** Write these down! You'll need them for recording and teleoperation.

**Note about port names:**
- **Windows**: Ports will be shown as `COM3`, `COM9`, `COM10`, etc.
- **Mac/Linux**: Ports will be shown as `/dev/ttyUSB0`, `/dev/ttyACM0`, `/dev/tty.usbserial-xxxxx`, etc.

---

## Step 3: Identify Camera Indices

Next, we need to find which index number is assigned to each camera.

Run this command:

```bash
lerobot-find-cameras
```

This will show you all available cameras with their:

- Index number (0, 1, 2, 3, etc.)
- Resolution
- FPS capabilities

Note down the index numbers for your cameras (e.g., tripod camera = `1`, gripper camera = `3`).

---

## Step 4: Test Your Cameras

We have two useful scripts in the `scripts/cameras/` folder to help you test cameras:

### Option 1: test_cameras.py

This script tests camera functionality and displays basic information:

```bash
python scripts/cameras/test_cameras.py
```

**What it does:**

- Quickly checks if cameras are accessible
- Shows camera properties
- Good for debugging camera issues

### Option 2: view_cameras.py

This script opens live camera feeds for visual verification:

```bash
python scripts/cameras/view_cameras.py
```

**What it does:**

- Opens live preview windows for each camera
- Lets you verify camera angles and positioning
- Useful for checking if cameras are mounted correctly

**Difference:** `test_cameras.py` is for quick checks, `view_cameras.py` is for visual verification.

---

## Important Tips for Reliable Setup

### 🔌 USB Port Distribution (Laptops)

If you're using a **laptop** with multiple cameras:

- ✅ **DO**: Spread cameras across different sides
  - Example: Connect one camera on the **right side**, another on the **left side**
- ❌ **DON'T**: Connect all cameras to one side of the laptop
  - This can cause bandwidth issues and frame drops

### 🔌 USB Hub Usage

If you're using a **USB hub**:

- ✅ **DO**: Use separate hubs or direct PC connections for robots and cameras
  - Example: Robots on one hub, cameras on another (or direct to PC)
- ❌ **DON'T**: Connect all devices (2 robots + 2 cameras) to a single USB hub
  - This causes bandwidth congestion and communication delays

### ⚠️ CRITICAL: USB Cable Requirements for Hubs

**If you're using a USB hub, you MUST use proper USB data transfer cables!**

- ✅ **DO**: Use **USB data transfer braided cables**
  - These cables support both power AND data transfer
  - Look for cables labeled "data sync" or "charging + data"
- ❌ **DON'T**: Use charging-only cables
  - These cables only have power wires, NO data wires
  - **Your devices will NOT be detected** if using charging-only cables with a USB hub
  - This is the most common reason for "device not detected" errors

**How to identify a data cable:**
- Check the cable packaging - it should say "data transfer" or "sync + charge"
- Data cables are usually thicker than charging-only cables
- If a device works when plugged directly to PC but not through a hub, check your cable!

**Pro tip:** When buying cables for your setup, specifically ask for "USB data cables" or "USB sync cables" - don't just grab any USB cable!

### ⏱️ About Timeout Modifications

**Good news!** This repository includes modified scripts with increased timeout values:

- Camera timeout: **2000ms** (vs 1ms in official LeRobot)
- Motor timeout: **5000ms** (vs 1000ms in official LeRobot)

These modifications help handle delays from USB hubs and longer cables. However, it's still best practice to follow the tips above for optimal performance.

---

## What's Next?

Now that your hardware is connected and configured, you're ready to test teleoperation!

In the **next guide**, we'll cover:

- How to run teleoperation to control the follower arm with the leader arm
- Verifying that everything works correctly before recording datasets

Let's move on to teleoperation!

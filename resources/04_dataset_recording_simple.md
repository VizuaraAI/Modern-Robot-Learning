# Dataset Recording Guide

Hey everyone! Welcome to the **fourth guide** in our SO-101 LeRobot tutorial series.

Now that your robots are calibrated and teleoperation is working, it's time to record demonstration datasets! This is where you teach your robot by showing it how to perform tasks.

Let's start recording!

---

## Before You Start

Make sure you have completed the previous guides:

1. ✅ **Installation Guide** - All software installed
2. ✅ **Hardware Setup Guide** - Robots and cameras connected, COM ports identified
3. ✅ **Calibration Guide** - Both robots calibrated, teleoperation tested

---

## Step 1: Get Your Camera Indices

You need to know which camera index to use. Go to [Hardware Setup Guide](02_hardware_setup.md) - Step 3 and run:

```bash
lerobot-find-cameras
```

Write down your camera indices (e.g., 0, 1, 2, 3, etc.). You'll need these for the recording command.

---

## Step 2: Record Your First Dataset

Use this command to start recording (replace the values with yours):

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=COM10 \
  --robot.id=my_follower \
  --robot.cameras="{cam1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
  --teleop.type=so101_leader \
  --teleop.port=COM9 \
  --teleop.id=my_leader \
  --display_data=true \
  --dataset.repo_id=${HF_USERNAME}/my-dataset \
  --dataset.num_episodes=50 \
  --dataset.single_task="pick_cube"
```

**Replace these values:**

- `COM10` → Your follower robot port
- `COM9` → Your leader robot port
- `${HF_USERNAME}/my-dataset` → Your HuggingFace username and dataset name
- `50` → How many episodes you want to record
- `"pick_cube"` → Description of your task

**For camera configuration, see the Camera Setup section below.**

---

## Step 3: Add More Episodes (Resume Recording)

If you want to record more episodes later, add the `--resume=true` flag:

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=COM10 \
  --robot.id=my_follower \
  --robot.cameras="{cam1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
  --teleop.type=so101_leader \
  --teleop.port=COM9 \
  --teleop.id=my_leader \
  --display_data=true \
  --dataset.repo_id=${HF_USERNAME}/my-dataset \
  --dataset.num_episodes=100 \
  --dataset.single_task="pick_cube" \
  --resume=true
```

**Note:** With `--resume=true`, the `--dataset.num_episodes=100` means it will record 100 **additional** episodes.

---

## Step 4: Manual Upload (If Recording Was Interrupted)

If your recording session crashed or was interrupted, upload manually:

```bash
huggingface-cli upload ${HF_USERNAME}/my-dataset ~/.cache/huggingface/lerobot/${HF_USERNAME}/my-dataset --repo-type dataset
```

Replace `${HF_USERNAME}/my-dataset` with your actual HuggingFace username and dataset name.

---

## Step 5: Verify Recordings with Replay

Replay an episode to make sure it recorded correctly:

```bash
lerobot-replay \
  --robot.type=so101_follower \
  --robot.port=COM10 \
  --robot.id=my_follower \
  --dataset.repo_id=${HF_USERNAME}/my-dataset \
  --dataset.episode=0
```

Change `--dataset.episode=0` to replay different episodes (0, 1, 2, etc.).

---

## Camera Configuration Guide

The camera setup uses this format:

```
--robot.cameras="{camera_name: {type: opencv, index_or_path: INDEX, width: WIDTH, height: HEIGHT, fps: 30}}"
```

### Single Camera Example

```bash
--robot.cameras="{main: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}"
```

### Two Cameras Example

```bash
--robot.cameras="{cam1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, cam2: {type: opencv, index_or_path: 1, width: 1280, height: 720, fps: 30}}"
```

### Three Cameras Example

```bash
--robot.cameras="{cam1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, cam2: {type: opencv, index_or_path: 1, width: 1280, height: 720, fps: 30}, cam3: {type: opencv, index_or_path: 2, width: 1920, height: 1080, fps: 30}}"
```

### What Each Parameter Means:

- **camera_name**: Give your camera any name (cam1, overhead, wrist, etc.)
- **type**: Always use `opencv` for USB cameras
- **index_or_path**: The camera index from `lerobot-find-cameras` (0, 1, 2, 3, etc.)
- **width & height**: Resolution in pixels (common: 640x480, 1280x720, 1920x1080)
- **fps**: Frames per second - use 30 for smooth recording

**Common Resolutions:**

- `640x480` - Low quality, fast
- `1280x720` - Good quality (720p)
- `1920x1080` - High quality (1080p)

**Pro tip:** Higher resolution = more disk space and slower recording. Start with 640x480 or 1280x720.

---

## Recording Tips

### ✅ DO:

- **Watch the camera display windows** when `--display_data=true`
- Start each episode from the same position
- Record smooth, consistent demonstrations
- Keep lighting and camera positions fixed
- Record at least 50-100 episodes for good results

### ❌ DON'T:

- Look at the robot instead of the camera feeds
- Move cameras between episodes
- Change lighting conditions mid-recording
- Include failed attempts (delete and re-record)
- Rush through demonstrations

---

## Common Issues

### Camera feed is black/frozen

- Check camera index is correct
- Verify camera isn't used by another program
- Try different USB port

### Recording is slow/laggy

- Reduce camera resolution (640x480)
- Close other programs
- Don't use USB hubs

### Episodes not saving

- Check disk space
- Verify: `huggingface-cli whoami`
- Check HuggingFace repo exists

---

## What's Next?

Once you have 50+ episodes recorded, you're ready for training!

In the **next guide**, we'll cover:

- Training the ACT policy on your dataset
- Monitoring training with W&B
- Evaluating your trained model

Let's move on to training!

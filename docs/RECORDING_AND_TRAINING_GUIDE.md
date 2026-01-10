# 🤖 Complete LeRobot Recording & Training Guide

## 📋 Table of Contents
1. [Setup Overview](#setup-overview)
2. [Recording Dataset](#recording-dataset)
3. [How Data is Stored](#how-data-is-stored)
4. [Understanding Your Dataset](#understanding-your-dataset)
5. [Training on RunPod](#training-on-runpod)
6. [Running Inference](#running-inference)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Setup Overview

**Your Configuration:**
- **Leader Arm:** COM9 (ID: `my_awesome_leader_arm`)
- **Follower Arm:** COM10 (ID: `my_awesome_follower_arm`)
- **Tripod Camera:** Camera 2 (side/overview view)
- **Gripper Camera:** Camera 3 (close-up view)
- **Hugging Face User:** `omunaman`

---

## 📹 Recording Dataset

### Step 1: Record 5 Test Episodes

```powershell
# Record your first dataset with 5 episodes
lerobot-record `
    --robot.type=so101_follower `
    --robot.port=COM10 `
    --robot.id=my_awesome_follower_arm `
    --robot.cameras="{ tripod: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, gripper: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}}" `
    --teleop.type=so101_leader `
    --teleop.port=COM9 `
    --teleop.id=my_awesome_leader_arm `
    --display_data=true `
    --dataset.repo_id=omunaman/test_pickup `
    --dataset.num_episodes=5 `
    --dataset.single_task="Pick up red cube and place in bin"
```

### Step 2: What Happens During Recording

**For Each Episode:**

1. **Setup Phase**
   - You position the object (e.g., red cube)
   - Press **ENTER** to start recording

2. **Recording Phase (60 seconds max)**
   - Move the **leader arm** to control the **follower arm**
   - Cameras record at 30 FPS
   - Robot joint positions recorded at 30 FPS
   - Perform your task (pick up cube, place in bin)

3. **End Episode**
   - Press **ENTER** to finish episode early, OR
   - Wait for 60 seconds timeout
   - Press **'r'** to re-record if you made a mistake
   - Press **ESC** to stop entire recording session

4. **Reset Phase**
   - Move objects back to starting position
   - Press **ENTER** to record next episode

### Keyboard Controls During Recording

| Key | Action |
|-----|--------|
| **ENTER** | Start/Stop episode |
| **r** | Re-record last episode |
| **ESC** | Stop recording session completely |
| **Arrow Keys** | (Reserved for future use) |

---

## 💾 How Data is Stored

### Local Storage Path

```
C:\Users\naman\.cache\huggingface\lerobot\omunaman\test_pickup\
```

### Directory Structure

```
test_pickup/
├── meta.json                    # Dataset metadata (fps, robot type, features)
├── data/                        # Parquet files with episode data
│   ├── chunk-000/
│   │   └── data-00000-of-00001.parquet  # Episode 0 data
│   ├── chunk-001/
│   │   └── data-00000-of-00001.parquet  # Episode 1 data
│   └── ...
├── videos/                      # Compressed video files
│   ├── chunk-000/
│   │   ├── observation.images.tripod.mp4   # Episode 0 tripod camera
│   │   └── observation.images.gripper.mp4  # Episode 0 gripper camera
│   ├── chunk-001/
│   │   ├── observation.images.tripod.mp4   # Episode 1 tripod camera
│   │   └── observation.images.gripper.mp4  # Episode 1 gripper camera
│   └── ...
└── README.md                    # Auto-generated dataset card
```

### Data Format (Parquet Files)

Each `data-*.parquet` file contains:

| Column | Description | Example |
|--------|-------------|---------|
| `timestamp` | Frame timestamp | 0.000, 0.033, 0.066... |
| `episode_index` | Episode number | 0, 1, 2, 3, 4 |
| `frame_index` | Frame number in episode | 0, 1, 2, 3... |
| `action.shoulder_pan` | Target position for shoulder | 2048 |
| `action.shoulder_lift` | Target position for shoulder lift | 1500 |
| `action.elbow_flex` | Target position for elbow | 2800 |
| `action.wrist_flex` | Target position for wrist | 1800 |
| `action.wrist_roll` | Target position for wrist roll | 2000 |
| `action.gripper` | Target gripper position | 2500 |
| `observation.state.shoulder_pan` | Current shoulder position | 2045 |
| `observation.state.shoulder_lift` | Current shoulder lift | 1502 |
| `observation.state.elbow_flex` | Current elbow | 2798 |
| `observation.state.wrist_flex` | Current wrist | 1801 |
| `observation.state.wrist_roll` | Current wrist roll | 1998 |
| `observation.state.gripper` | Current gripper | 2503 |
| `observation.images.tripod` | Video frame index (tripod) | 0, 1, 2... |
| `observation.images.gripper` | Video frame index (gripper) | 0, 1, 2... |

**Example Row:**
```json
{
  "timestamp": 0.033,
  "episode_index": 0,
  "frame_index": 1,
  "action": {
    "shoulder_pan": 2048,
    "shoulder_lift": 1500,
    "elbow_flex": 2800,
    "wrist_flex": 1800,
    "wrist_roll": 2000,
    "gripper": 2500
  },
  "observation": {
    "state": {
      "shoulder_pan": 2045,
      "shoulder_lift": 1502,
      "elbow_flex": 2798,
      "wrist_flex": 1801,
      "wrist_roll": 1998,
      "gripper": 2503
    },
    "images": {
      "tripod": 1,
      "gripper": 1
    }
  }
}
```

### Video Storage

- **Format:** MP4 (H.264 codec with libsvtav1)
- **FPS:** 30 (matches recording rate)
- **Resolution:** 640x480
- **Compression:** Efficient encoding to save space

**Why separate video files?**
- Videos are large (10-50 MB per episode per camera)
- Parquet stores frame indices pointing to video frames
- During training, frames are decoded on-demand from videos

---

## 📊 Understanding Your Dataset

### Check What Was Recorded

After recording, check your dataset locally:

```powershell
# View dataset info
python -c "from lerobot.datasets.lerobot_dataset import LeRobotDataset; ds = LeRobotDataset('omunaman/test_pickup'); print(f'Episodes: {ds.num_episodes}'); print(f'Total frames: {ds.num_frames}'); print(f'Features: {list(ds.features.keys())}')"
```

### View Dataset Online

Your dataset automatically uploads to:
```
https://huggingface.co/datasets/omunaman/test_pickup
```

**Online Features:**
- ✅ Browse episodes
- ✅ Watch recorded videos
- ✅ Download dataset
- ✅ Share with others
- ✅ View statistics

### Verify Successful Recording

**Signs of a successful episode:**
1. **Episode completed** - You saw "Episode X saved"
2. **Video files created** - Check `videos/chunk-00X/` folder
3. **Parquet file created** - Check `data/chunk-00X/` folder
4. **No errors** - Terminal showed no red error messages

**Check specific episode:**

```powershell
# Check if episode 0 exists
ls "C:\Users\naman\.cache\huggingface\lerobot\omunaman\test_pickup\videos\chunk-000\"

# Should show:
#   observation.images.tripod.mp4
#   observation.images.gripper.mp4
```

---

## 🚀 Training on RunPod

### Setup RunPod Instance

1. **Go to RunPod.io** → Deploy GPU Instance
2. **Select GPU:** RTX 4090 (24GB VRAM) - **~$0.34/hour**
3. **Template:** PyTorch 2.4
4. **Storage:** 50GB container + 20GB volume (optional)
5. **Deploy**

### Install LeRobot on RunPod

```bash
# SSH into RunPod or use Web Terminal
cd /workspace

# Clone LeRobot
git clone https://github.com/huggingface/lerobot.git
cd lerobot

# Install dependencies
pip install -e .

# Login to Hugging Face (get token from https://huggingface.co/settings/tokens)
huggingface-cli login --token hf_YOUR_TOKEN_HERE

# Optional: Login to Weights & Biases for tracking
pip install wandb
wandb login
```

### Train Your Model

```bash
# Train ACT policy on your dataset
lerobot-train \
  --dataset.repo_id=omunaman/test_pickup \
  --policy.type=act \
  --output_dir=/workspace/outputs/train/act_test_pickup \
  --job_name=act_test_pickup \
  --policy.device=cuda \
  --wandb.enable=true \
  --policy.repo_id=omunaman/act_test_pickup_policy \
  --training.num_epochs=3000 \
  --training.save_checkpoint_freq=500 \
  --training.batch_size=8
```

**Training Parameters Explained:**

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--dataset.repo_id` | `omunaman/test_pickup` | Your dataset on HuggingFace |
| `--policy.type` | `act` | Policy architecture (ACT/Diffusion/GROOT) |
| `--output_dir` | `/workspace/outputs/...` | Where to save checkpoints |
| `--policy.device` | `cuda` | Use GPU (use `mps` for Mac, `cpu` for CPU) |
| `--wandb.enable` | `true` | Enable Weights & Biases tracking |
| `--policy.repo_id` | `omunaman/...policy` | Where to upload trained model |
| `--training.num_epochs` | `3000` | Training iterations |
| `--training.save_checkpoint_freq` | `500` | Save every 500 epochs |
| `--training.batch_size` | `8` | Frames per training step |

### Training Timeline (RTX 4090)

| Dataset Size | Training Time | Cost @ $0.34/hr |
|--------------|---------------|-----------------|
| 5 episodes | 30-60 min | $0.17 - $0.34 |
| 50 episodes | 2-3 hours | $0.68 - $1.02 |
| 100 episodes | 4-6 hours | $1.36 - $2.04 |

### Monitor Training

**Weights & Biases Dashboard:**
```
https://wandb.ai/YOUR_USERNAME/lerobot
```

**Metrics to Watch:**
- `train/loss` - Should decrease over time
- `eval/loss` - Should decrease but not as fast
- `eval/mse_*` - Mean squared error per joint (lower is better)

**Training is Done When:**
- Loss plateaus (stops decreasing)
- Typically after 2000-3000 epochs
- Or you stop it manually if satisfied

### Checkpoints Auto-Upload

Models automatically upload to HuggingFace every 500 epochs:

```
https://huggingface.co/omunaman/act_test_pickup_policy
```

**Available checkpoints:**
- `checkpoints/000500/` - After 500 epochs
- `checkpoints/001000/` - After 1000 epochs
- `checkpoints/001500/` - After 1500 epochs
- ...
- `checkpoints/last/` - Most recent checkpoint

---

## 🎮 Running Inference (Test Your Model)

### Download Model (Optional)

If you want to keep a local copy:

```powershell
huggingface-cli download omunaman/act_test_pickup_policy --local-dir ./trained_models/test_pickup
```

### Run Autonomous Evaluation

```powershell
# Let the robot perform the task autonomously
lerobot-record `
    --robot.type=so101_follower `
    --robot.port=COM10 `
    --robot.id=my_awesome_follower_arm `
    --robot.cameras="{ tripod: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, gripper: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}}" `
    --display_data=true `
    --dataset.repo_id=omunaman/eval_test_pickup `
    --dataset.num_episodes=10 `
    --dataset.single_task="Pick up red cube and place in bin" `
    --policy.path=omunaman/act_test_pickup_policy
```

**What Happens:**
1. Robot moves **autonomously** (no leader arm needed!)
2. Policy predicts actions from camera images
3. Records evaluation episodes for analysis
4. You can see success rate (did it complete the task?)

### Evaluate Success Rate

```powershell
# Check how many episodes succeeded
# Manually review videos in eval_test_pickup dataset
```

**Improving Performance:**
- Record more diverse episodes (50-100 recommended)
- Vary object positions during recording
- Ensure good lighting and camera placement
- Train longer (up to 5000 epochs)

---

## 📈 Dataset Best Practices

### For Your First Task (5-10 episodes)

✅ **DO:**
- Keep object in **same position** for all episodes
- Use **consistent lighting**
- Perform task **the same way** each time
- Keep cameras **fixed** (don't move tripod)

❌ **DON'T:**
- Move object to different locations yet
- Change camera angles
- Use different gripping techniques
- Record in different lighting

### For Production Dataset (50-100 episodes)

**Add Variation Gradually:**

| Episodes | Variation |
|----------|-----------|
| 0-10 | Same position, same grasp |
| 10-20 | 3 different positions |
| 20-40 | 5 different positions |
| 40-60 | Different grasp angles |
| 60-80 | Different lighting conditions |
| 80-100 | Combined variations |

---

## 🛠️ Troubleshooting

### Recording Issues

**Problem: "ConnectionError: No status packet from motor"**
- **Solution:** Power cycle robot, check cables, try again

**Problem: "No camera found"**
- **Solution:** Run `python view_cameras.py` to verify camera indices

**Problem: "Dataset upload failed"**
- **Solution:** Check internet connection, verify `huggingface-cli login`

### Training Issues

**Problem: "CUDA out of memory"**
- **Solution:** Reduce `--training.batch_size=4` (or even `2`)

**Problem: "Loss not decreasing"**
- **Solution:** 
  - Check dataset quality (are episodes consistent?)
  - Train longer (up to 5000 epochs)
  - Record more diverse data

**Problem: "Training too slow"**
- **Solution:** Use better GPU (RTX 4090 instead of 3090)

### Inference Issues

**Problem: "Robot doesn't complete task"**
- **Solution:**
  - Need more training data (50+ episodes)
  - Train longer
  - Ensure test conditions match training (lighting, object position)

**Problem: "Robot moves erratically"**
- **Solution:**
  - Calibration might be off - recalibrate arms
  - Check if model trained on correct dataset

---

## 📞 Getting Help

- **Discord:** https://discord.com/invite/s3KuuzsPFb
- **GitHub Issues:** https://github.com/huggingface/lerobot/issues
- **Documentation:** https://huggingface.co/docs/lerobot

---

## 🎯 Quick Command Reference

**Record 5 episodes:**
```powershell
lerobot-record --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --robot.cameras="{ tripod: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, gripper: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM9 --teleop.id=my_awesome_leader_arm --display_data=true --dataset.repo_id=omunaman/test_pickup --dataset.num_episodes=5 --dataset.single_task="Pick up red cube and place in bin"
```

**Train on RunPod:**
```bash
lerobot-train --dataset.repo_id=omunaman/test_pickup --policy.type=act --output_dir=/workspace/outputs/train/act_test_pickup --job_name=act_test_pickup --policy.device=cuda --wandb.enable=true --policy.repo_id=omunaman/act_test_pickup_policy
```

**Run inference:**
```powershell
lerobot-record --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --robot.cameras="{ tripod: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, gripper: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}}" --display_data=true --dataset.repo_id=omunaman/eval_test_pickup --dataset.num_episodes=10 --dataset.single_task="Pick up red cube and place in bin" --policy.path=omunaman/act_test_pickup_policy
```

---

**Good luck with your robot! 🤖✨**

# Training Guide

Hey everyone! Welcome to the **fifth guide** in our SO-101 LeRobot tutorial series.

Now that you have recorded your dataset with 50+ episodes, it's time to train your robot policy! This is where your robot learns from the demonstrations you recorded. The training process will teach the AI to perform the task you demonstrated.

Let's train your robot!

---

## Before You Start

Make sure you have completed the previous guides:

1. ✅ **Installation Guide** - All software installed
2. ✅ **Hardware Setup Guide** - Robots and cameras connected
3. ✅ **Calibration Guide** - Both robots calibrated
4. ✅ **Recording Guide** - Dataset with 50+ episodes recorded

---

## Where to Train?

You have two options for training:

### Option 1: Local PC (if you have a GPU)
- Train directly on your computer
- Requires NVIDIA GPU with CUDA support
- Slower but no additional cost

### Option 2: RunPod (Recommended for faster training)
- Cloud GPU rental service
- Much faster training (30 minutes vs several hours)
- Costs ~$0.50-2.00 per hour depending on GPU

**For RunPod:** You'll need to perform the [Installation Guide](01_installation_guide.md) setup on the RunPod instance first, then run the training command below.

---

## Step 1: Start Training

Use this command to train your ACT policy:

```bash
lerobot-train \
    --dataset.repo_id ${HF_USERNAME}/your-dataset-name \
    --dataset.video_backend pyav \
    --policy.type act \
    --output_dir outputs/train/act_training \
    --batch_size 8 \
    --steps 50000 \
    --save_checkpoint true \
    --save_freq 2500 \
    --wandb.enable true \
    --wandb.project lerobot_training \
    --policy.device cuda \
    --policy.use_amp true \
    --policy.chunk_size 50 \
    --policy.n_action_steps 50 \
    --policy.repo_id ${HF_USERNAME}/your-policy-name \
    --policy.push_to_hub true
```

**Replace these values:**
- `${HF_USERNAME}/your-dataset-name` → Your dataset repo ID from recording
- `${HF_USERNAME}/your-policy-name` → Name for your trained policy (e.g., `john/pick_cube_policy`)
- `lerobot_training` → Your W&B project name (can be anything)

---

## Understanding the Training Arguments

### Dataset Configuration
- `--dataset.repo_id` - HuggingFace dataset you recorded
- `--dataset.video_backend pyav` - Video processing backend (use pyav for best performance)

### Policy Configuration
- `--policy.type act` - Using ACT (Action Chunking Transformer) policy
- `--policy.device cuda` - Train on GPU (use `cpu` if no GPU available, but very slow)
- `--policy.use_amp true` - Automatic Mixed Precision (faster training, less memory)
- `--policy.chunk_size 50` - How many future actions to predict at once
- `--policy.n_action_steps 50` - How many actions to execute from predictions
- `--policy.repo_id` - Where to save your trained policy on HuggingFace
- `--policy.push_to_hub true` - Automatically upload trained model to HuggingFace

### Training Configuration
- `--output_dir outputs/train/act_training` - Local folder to save checkpoints
- `--batch_size 8` - Number of samples processed together (adjust based on GPU memory)
- `--steps 50000` - Total training steps (50K is good for most tasks)
- `--save_checkpoint true` - Save model checkpoints during training
- `--save_freq 2500` - Save a checkpoint every 2500 steps

### Weights & Biases (W&B) Configuration
- `--wandb.enable true` - Enable experiment tracking and visualization
- `--wandb.project lerobot_training` - Your W&B project name

---

## What is Weights & Biases (W&B)?

W&B is a tool that tracks your training progress in real-time. It shows:
- **Loss curves** - How well the model is learning
- **Training metrics** - Performance over time
- **System stats** - GPU usage, memory, etc.
- **Video previews** - Predicted actions vs actual actions

### How to Use W&B:

1. You already logged in during installation: `wandb login`
2. When training starts, W&B will give you a URL
3. Open that URL in your browser
4. Watch your training progress live!

**What to look for:**
- Loss should decrease over time
- If loss plateaus early, you might need more data
- If loss is erratic, try reducing learning rate

---

## Step 2: Monitor Training Progress

Once training starts, you'll see:

```
Training progress: 1%|▋| 500/50000 [02:15<3:45:30, 3.66it/s]
Loss: 0.245
```

**What this means:**
- `500/50000` - Completed 500 steps out of 50,000
- `3:45:30` - Estimated time remaining
- `Loss: 0.245` - Current loss value (lower is better)

**Training will take:**
- **On RunPod (RTX 4090):** ~30-60 minutes for 50K steps
- **On local GPU (RTX 3080):** ~2-4 hours for 50K steps
- **On CPU:** Don't do this, it will take days!

---

## Step 3: Checkpoints

Your training will save checkpoints every 2500 steps:

```
outputs/train/act_training/
├── checkpoints/
│   ├── 002500/
│   ├── 005000/
│   ├── 007500/
│   └── ...
```

**Why checkpoints matter:**
- Resume training if it crashes
- Test different checkpoints to find the best one
- Usually the final checkpoint (50000) works best

---

## Step 4: Test Your Trained Policy (Inference)

Once training is complete, test your policy on the real robot!

```bash
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=COM10 \
    --robot.id=my_awesome_follower_arm \
    --robot.cameras="{camera1: {type: opencv, index_or_path: 0, width: 1280, height: 720, fps: 30, fourcc: MJPG}, camera2: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
    --display_data=true \
    --dataset.repo_id=${HF_USERNAME}/eval-test \
    --dataset.num_episodes=5 \
    --dataset.single_task="Pick up cube and place in bin" \
    --policy.path=${HF_USERNAME}/your-policy-name \
    --policy.device=cpu
```

**What's different from recording?**

New arguments:
- `--policy.path=${HF_USERNAME}/your-policy-name` - Load your trained policy
- `--policy.device=cpu` - Run policy on CPU (unless you have GPU on local PC)

**This will:**
1. Load your trained policy
2. Run the robot autonomously (no teleoperation!)
3. The AI controls the follower arm based on camera input
4. Record the results as evaluation episodes

**How to use:**
1. Set up the task (place objects in starting position)
2. Run the command
3. **Don't touch the leader arm** - the AI is controlling the follower!
4. Watch the robot perform the task autonomously
5. Press ESC to stop if needed

---

## Step 5: Resuming Training (If Interrupted)

If training stops and you want to continue:

```bash
lerobot-train \
    --config_path=outputs/train/act_training/checkpoints/025000/pretrained_model/train_config.json \
    --resume=true \
    --steps=80000
```

**This will:**
- Resume from checkpoint 25000
- Continue training to 80000 steps (additional 55K steps)
- Keep all previous progress

---

## Training on RunPod

### Setup RunPod Instance:

1. **Create RunPod account** at [runpod.io](https://runpod.io)
2. **Select GPU** - Recommend RTX 4090 or A6000
3. **Choose template** - Use PyTorch or CUDA template
4. **Start instance** and connect via SSH or Jupyter

### On RunPod Instance:

1. **Clone your repo:**
   ```bash
   git clone https://github.com/OmuNaman/Modern-Robot-Learning.git
   cd Modern-Robot-Learning
   ```

2. **Follow Installation Guide** - Complete [01_installation_guide.md](01_installation_guide.md)

3. **Run training command** - Use the training command from Step 1 above

4. **Download trained model** - RunPod will automatically push to HuggingFace if `--policy.push_to_hub true`

### RunPod Tips:
- ✅ Use `--policy.push_to_hub true` to auto-save your model
- ✅ Monitor with W&B to avoid staying connected the whole time
- ✅ Stop the instance immediately after training completes to save money
- ⚠️ Don't forget to download checkpoints before stopping instance!

---

## Troubleshooting

### Issue 1: CUDA out of memory

**Solution:**
- Reduce `--batch_size` from 8 to 4 or 2
- Make sure no other programs are using GPU
- Use `--policy.use_amp true` for less memory usage

### Issue 2: Training loss not decreasing

**Solution:**
- Check if you have enough episodes (need 50+ good quality episodes)
- Verify dataset quality by reviewing recordings
- Try training for more steps (100K instead of 50K)

### Issue 3: Policy performs poorly during inference

**Solution:**
- Record more high-quality episodes
- Ensure camera setup during inference matches recording
- Try different checkpoints (e.g., 40K, 45K, 50K)
- Check lighting conditions match training data

### Issue 4: W&B not showing metrics

**Solution:**
- Verify you ran `wandb login` during installation
- Check internet connection
- Run `wandb verify` to test authentication

---

## Tips for Better Results

### ✅ DO:

**Data Quality:**
- Use 50-100+ high-quality episodes
- Ensure consistent camera angles and lighting
- Record smooth, deliberate demonstrations

**Training:**
- Monitor W&B metrics during training
- Save checkpoints frequently (every 2500 steps)
- Train for at least 50K steps for simple tasks

**Evaluation:**
- Test policy in same environment as training
- Use same camera setup as recording
- Try multiple evaluation runs

### ❌ DON'T:

**Avoid:**
- Training with less than 50 episodes
- Changing camera setup between training and inference
- Stopping training too early (before 50K steps)
- Ignoring W&B metrics showing poor learning

---

## What Success Looks Like

**Good Training:**
- Loss steadily decreases
- W&B shows smooth loss curves
- Policy performs task successfully 70%+ of the time

**Needs Improvement:**
- Loss plateaus early → Need more/better data
- Policy fails most attempts → Check camera setup and data quality
- Robot makes unsafe movements → Review demonstrations for consistency

---
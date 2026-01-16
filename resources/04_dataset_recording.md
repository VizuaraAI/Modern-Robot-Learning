# Dataset Recording Guide

Hey everyone! Welcome to the **fourth guide** in our SO-101 LeRobot tutorial series.

Now that your robots are calibrated and teleoperation is working, it's time to record demonstration datasets! This is where the magic happens - you'll teach your robot by showing it how to perform tasks. The robot will learn from these demonstrations during training.

Let's start recording!

---

## What is Dataset Recording?

Dataset recording captures:

- **Robot joint positions** from the follower arm
- **Camera images** from your mounted cameras
- **Leader arm movements** that control the follower
- **Timestamps** to sync everything together

Each demonstration is called an **episode**. You'll record multiple episodes of the same task to create a dataset.

---

## Before You Start

Make sure you have completed the previous guides:

1. ✅ **Installation Guide** - All software installed
2. ✅ **Hardware Setup Guide** - Robots and cameras connected, COM ports identified
3. ✅ **Calibration Guide** - Both robots calibrated, teleoperation tested

If teleoperation isn't working smoothly, go back to [Calibration and Teleoperation Guide](03_calibration_and_teleoperation.md) first!

---

## Step 1: Prepare Your Workspace

Before recording:

1. **Set up your task** - Place objects in their starting positions
2. **Position cameras** - Make sure all your cameras have clear views of the workspace
3. **Test the task manually** - Try the task with teleoperation a few times
4. **Clear obstacles** - Remove anything that might interfere with the robot
5. **Plan your demonstrations** - Decide what "success" looks like for this task

---

## Step 2: Record Your First Dataset

### Understanding Camera Indices First

Before running the recording command, you need to know your camera indices. If you haven't done this yet:

1. Go back to [Hardware Setup Guide](02_hardware_setup.md) - Step 3
2. Run `lerobot-find-cameras` to see all available cameras
3. Note down which index belongs to which camera:
   - Example: Index 0 might be your laptop webcam
   - Example: Index 1 might be your tripod camera
   - Example: Index 3 might be your gripper camera

**Write these down! You'll need them for the command below.**

### How to Configure Cameras in the Command

The camera configuration uses JSON format inside quotes. Here's the structure:

```
--robot.cameras="{camera_name_1: {settings}, camera_name_2: {settings}}"
```

**You can configure as many cameras as you need.** Common setups:

- 1 camera: Single view of the workspace
- 2 cameras: Multiple angles (e.g., wide view + close-up, or overhead + side view)
- 3+ cameras: More comprehensive coverage

**For each camera, you need:**

- Camera name: Any descriptive name you want (e.g., `camera1`, `overhead`, `wrist`, etc.)
- `type: opencv` - Camera type (always opencv for USB cameras)
- `index_or_path: X` - **Replace X with your camera index from hardware setup!**
- `width: 1280` - Resolution width (adjust based on your camera)
- `height: 720` - Resolution height (adjust based on your camera)
- `fps: 15` - Frames per second (10-15 is good for most cases)
- `fourcc: MJPG` - Video compression format (MJPG works best)

### Example Recording Command

Below is an example using **two cameras**. **Adjust the number of cameras, their names, indices, and resolutions to match YOUR setup:**

```bash
lerobot-record --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --robot.cameras="{camera1: {type: opencv, index_or_path: 1, width: 1280, height: 720, fps: 30, fourcc: MJPG}, camera2: {type: opencv, index_or_path: 3, width: 1920, height: 1080, fps: 30, fourcc: MJPG}}" --teleop.type=so101_leader --teleop.port=COM9 --teleop.id=my_awesome_leader_arm --display_data=true --dataset.repo_id=your-username/your-dataset-name --dataset.num_episodes=10 --dataset.single_task="pick_and_place"
```

**Note:** This is just an example! You might use:

- Different camera names (overhead, wrist, side, etc.)
- Different number of cameras (1, 2, 3, or more)
- Different indices based on your hardware setup
- Different resolutions based on your camera capabilities

### Understanding the Command:

**Robot Configuration:**

- `--robot.type=so101_follower` - Your follower robot type
- `--robot.port=COM10` - **Your follower COM port** (change this!)
- `--robot.id=my_awesome_follower_arm` - Friendly name for follower

**Camera Configuration:**

- `--robot.cameras="{...}"` - Defines your cameras in JSON format

  **In this example, we're using 2 cameras, but you can use 1, 2, 3, or more!**

  **First Camera:**

  - Name: `camera1` (name it whatever you want - overhead, wrist, main, etc.)
  - `type: opencv` - USB camera type
  - `index_or_path: 1` - **CHANGE THIS** to your camera index!
  - `width: 1280, height: 720` - Resolution (adjust to your camera)
  - `fps: 30` - 30 frames per second
  - `fourcc: MJPG` - MJPG compression

  **Second Camera:**

  - Name: `camera2` (name it whatever you want)
  - `type: opencv` - USB camera type
  - `index_or_path: 3` - **CHANGE THIS** to your camera index!
  - `width: 1920, height: 1080` - Resolution (adjust to your camera)
  - `fps: 30` - 30 frames per second
  - `fourcc: MJPG` - MJPG compression

  **Using only 1 camera?** Just remove the second camera from the JSON:

  ```
  --robot.cameras="{main: {type: opencv, index_or_path: 0, width: 1280, height: 720, fps: 15, fourcc: MJPG}}"
  ```

  **Important:** Go to [Hardware Setup Guide](02_hardware_setup.md) Step 3 to find your camera indices!

**Teleoperation Configuration:**

- `--teleop.type=so101_leader` - Your leader robot type
- `--teleop.port=COM9` - **Your leader COM port** (change this!)
- `--teleop.id=my_awesome_leader_arm` - Friendly name for leader

**Display & Dataset Settings:**

- `--display_data=true` - Shows live camera feeds during recording (very useful!)
- `--dataset.repo_id=your-username/your-dataset-name` - **Your HuggingFace repo**
  - Replace `your-username` with your HuggingFace username
  - Replace `your-dataset-name` with a descriptive name for your dataset
  - Example: `john/robot_pick_cubes` or `sarah/sorting_task_dataset`
- `--dataset.num_episodes=10` - Number of episodes to record (start with 10-20)
- `--dataset.single_task="pick_and_place"` - **Your task description**
  - Replace with what your robot actually does
  - Examples: "pick_cube", "sorting_objects", "open_drawer", etc.

---

## Step 3: Recording Process

Once you run the command:

1. **Camera windows will appear** - You'll see live feeds from all your cameras
2. **Follow the prompts** - Press Enter to start each episode
3. **Perform the demonstration** - Use the leader arm to control the follower
4. **Complete the task** - Finish the episode successfully
5. **Accept or discard the episode** - Use keyboard controls (see below)
6. **Repeat** - Continue until you've recorded all episodes

### Keyboard Controls During Recording

While recording episodes, you have full control over accepting or discarding demonstrations:

| Key | Action |
|-----|--------|
| **Right Arrow (→)** | Accept the episode and save it to the dataset |
| **Left Arrow (←)** | Discard the episode (if it wasn't good) |
| **ESC** | Stop the entire recording session |

**How to handle a bad episode:**

1. If you make a mistake during recording, **press Left Arrow (←)**
2. The system will ask you to reset the environment (put objects back to starting position)
3. **Press Right Arrow (→)** to continue recording the next episode
4. If you want to stop the whole session completely, **press ESC**

**Example workflow:**
```
→ Episode starts
→ You perform the task
→ Made a mistake? Press ← (Left Arrow)
→ System: "Please reset environment"
→ Reset objects to starting position
→ Press → (Right Arrow) to record next episode
→ Continue...
```

### Important: Watch the Cameras, Not the Robot!

⚠️ **When `--display_data=true` is enabled:**

✅ **DO:** Look at the camera feed windows on your screen
❌ **DON'T:** Look directly at the follower robot

**Why?**

- The camera view is what the AI will see during training
- What looks good to your eyes might not look good to the camera
- Camera angles, lighting, and occlusions matter more than the physical robot position
- Train yourself to rely on the camera feeds just like the AI will!

---

## Step 4: Adding More Episodes Later

Want to add more demonstrations to your existing dataset? Use the `--resume=true` flag:

```bash
lerobot-record --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --robot.cameras="{camera1: {type: opencv, index_or_path: 1, width: 1280, height: 720, fps: 15, fourcc: MJPG}, camera2: {type: opencv, index_or_path: 3, width: 1920, height: 1080, fps: 15, fourcc: MJPG}}" --teleop.type=so101_leader --teleop.port=COM9 --teleop.id=my_awesome_leader_arm --display_data=true --dataset.repo_id=your-username/your-dataset-name --dataset.num_episodes=20 --dataset.single_task="pick_and_place" --resume=true
```

**Remember:** Use the same camera configuration as your original recording!

**Key changes:**

- `--resume=true` - Continues from existing dataset instead of creating a new one
- `--dataset.num_episodes=20` - **Total episodes you want** (not additional episodes!)
  - If you had 10 episodes, setting this to 20 will record 10 more
  - If you had 10 episodes, setting this to 15 will record 5 more

---

## Step 5: Manual Upload (If Needed)

If your recording session is interrupted or you quit before automatic upload completes, you can manually upload your dataset to HuggingFace:

```bash
huggingface-cli upload your-username/your-dataset-name ~/.cache/huggingface/lerobot/your-username/your-dataset-name --repo-type dataset
```

**Replace:**

- `your-username/your-dataset-name` - **Your HuggingFace repo ID** (appears twice in the command)
  - Must match the `--dataset.repo_id` you used when recording
- The path structure stays the same, just change the username and dataset name in the path

**When to use this:**

- Recording crashed or was interrupted
- Automatic upload failed due to network issues
- You want to manually verify before uploading

---

## Step 6: Verify Your Recordings with Replay

Before training, it's a good idea to replay your episodes to make sure they recorded correctly:

```bash
lerobot-replay --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --dataset.repo_id=your-username/your-dataset-name --dataset.episode=0
```

**This will:**

- Play back episode 0 on the follower robot
- Show you exactly what was recorded
- Help you identify bad episodes that should be re-recorded

**Change `--dataset.episode=0` to replay different episodes:**

- Episode 0: First episode
- Episode 5: Sixth episode (episodes start at 0)
- Episode 9: Tenth episode

**Pro tip:** Replay a few episodes to check for:

- Smooth movements
- Task completed successfully
- No collisions or errors
- Camera views are clear

---

## Tips for High-Quality Recordings

### ✅ DO:

**Consistency:**

- Start each episode from the same initial position
- Use consistent movements and speed
- Complete the task the same way each time
- Maintain good lighting conditions

**Camera Setup:**

- Keep cameras stable and fixed in position
- Ensure clear views of the task workspace
- Check for reflections or glare
- Verify both cameras are recording before starting

**Quality Control:**

- Watch the camera feeds, not the robot
- Record at least 50-100 episodes for good results
- Delete and re-record failed attempts
- Verify recordings with replay before training

### ❌ DON'T:

**Avoid:**

- Moving cameras between episodes
- Recording under different lighting conditions
- Rushing through demonstrations
- Recording with obstacles blocking camera views
- Ignoring failed episodes (delete and re-record them!)

**Recording Mistakes:**

- Don't include failed attempts in your dataset
- Don't change task setup mid-recording session
- Don't record if teleoperation is laggy or unreliable
- Don't forget to watch the display_data windows!

---

## Common Issues and Solutions

### Issue 1: Camera feed is frozen or black

**Solution:**

- Check camera indices are correct (from hardware setup)
- Verify cameras are not being used by another program
- Try different USB ports or direct PC connection
- Test cameras with `scripts/cameras/view_cameras.py` first

### Issue 2: Recording is very slow or laggy

**Solution:**

- Reduce camera resolution (720p instead of 1080p)
- Close unnecessary programs running in background
- Check USB bandwidth (avoid hubs if possible)

### Issue 3: Episodes not saving

**Solution:**

- Check disk space on your computer
- Verify HuggingFace credentials are working: `huggingface-cli whoami`
- Make sure repo_id exists on HuggingFace (create it if needed)
- Check terminal output for error messages

### Issue 4: Follower arm movements don't match leader

**Solution:**

- Re-run calibration (both leader and follower)
- Check for loose cables or connections
- Verify motors are all responding correctly
- Test with teleoperation before recording

---

## Dataset Size Recommendations

**Minimum for testing:** 10-20 episodes
**Good starting point:** 50 episodes
**Better results:** 100-200 episodes
**Production quality:** 500+ episodes

**Remember:** Quality > Quantity!

- 50 perfect episodes are better than 200 messy episodes
- It's okay to start small and add more later with `--resume=true`

---

## What's Next?

Congratulations! 🎉 You now have a recorded dataset!

In the **next guide**, we'll cover:

- Training the ACT policy on your dataset
- Monitoring training progress with W&B
- Evaluating your trained model
- Resuming training from checkpoints

Make sure you have at least 50 good quality episodes before moving to training. You can always add more later!

Let's move on to training! 🚀

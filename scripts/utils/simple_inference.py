"""
Simple inference script for SO101 + ACT policy
Usage: python simple_inference.py
"""
import torch
import numpy as np
from lerobot.policies.act.modeling_act import ACTPolicy
from lerobot.processor.pipeline import DataProcessorPipeline as Normalize
from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.robots.utils import make_robot_from_config
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

# ============ CONFIG ============
CHECKPOINT_PATH = "checkpoints/act_so101_local/pretrained_model"
ROBOT_TYPE = "so101_follower"
ROBOT_PORT = "COM10"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
NUM_EPISODES = 1
MAX_STEPS_PER_EPISODE = 300

# CAMERA INDICES
TRIPOD_CAMERA_INDEX = 2
GRIPPER_CAMERA_INDEX = 3

# Joint names in order
JOINT_NAMES = [
    "shoulder_pan.pos",
    "shoulder_lift.pos", 
    "elbow_flex.pos",
    "wrist_flex.pos",
    "wrist_roll.pos",
    "gripper.pos"
]

# ============ LOAD POLICY ============
print(f"Loading policy from {CHECKPOINT_PATH}...")
policy = ACTPolicy.from_pretrained(CHECKPOINT_PATH)
policy.eval().to(DEVICE)
print(f"Policy loaded on {DEVICE}")

# Load normalization stats
print("Loading normalization preprocessor...")
normalize = Normalize.from_pretrained(
    CHECKPOINT_PATH, 
    "policy_preprocessor.json",
    overrides={"device_processor": {"device": DEVICE}}
)

# CRITICAL: Load postprocessor to denormalize actions!
print("Loading postprocessor (for action denormalization)...")
from lerobot.processor.pipeline import DataProcessorPipeline as Postprocess
postprocess = Postprocess.from_pretrained(
    CHECKPOINT_PATH,
    "policy_postprocessor.json",
    overrides={"device_processor": {"device": DEVICE}}
)
print("Postprocessor loaded!")

# ============ CONNECT ROBOT ============
print(f"Connecting to {ROBOT_TYPE} on {ROBOT_PORT}...")

camera_configs = {
    "tripod": OpenCVCameraConfig(
        index_or_path=TRIPOD_CAMERA_INDEX, 
        width=1280, 
        height=720, 
        fps=30
    ),
    "gripper": OpenCVCameraConfig(
        index_or_path=GRIPPER_CAMERA_INDEX, 
        width=1920, 
        height=1080, 
        fps=30
    ),
}

robot_config = SO101FollowerConfig(
    port=ROBOT_PORT,
    cameras=camera_configs,
    id="so101_follower_inference",
)

robot = make_robot_from_config(robot_config)
robot.connect()
print("Robot connected!")

# ============ INFERENCE LOOP ============
try:
    for ep in range(NUM_EPISODES):
        print(f"\n=== Episode 1/1 ===")
        
        policy.reset()
        input("Position robot at start, then press ENTER...")
        
        for step in range(MAX_STEPS_PER_EPISODE):
            # Get observation from robot
            obs_dict = robot.get_observation()
            
            obs_tensors = {}
            
            # Concatenate joint positions
            if "observation.state" in policy.config.input_features:
                joint_positions = [obs_dict[joint_name] for joint_name in JOINT_NAMES]
                state = torch.tensor(joint_positions, dtype=torch.float32)
                obs_tensors["observation.state"] = state.unsqueeze(0).to(DEVICE)
            
            # Map cameras
            for cam_name in ["tripod", "gripper"]:
                policy_key = f"observation.images.{cam_name}"
                if policy_key in policy.config.input_features:
                    img = obs_dict[cam_name]
                    img = torch.from_numpy(img).float() / 255.0
                    img = img.permute(2, 0, 1)
                    obs_tensors[policy_key] = img.unsqueeze(0).to(DEVICE)
            
            obs_tensors = normalize(obs_tensors)
            
            with torch.inference_mode():
                action = policy.select_action(obs_tensors)
            
            # CRITICAL: Denormalize action using postprocessor!
            action_batch = {"action": action}
            action_batch = postprocess(action_batch)
            action_np = action_batch["action"].squeeze(0).cpu().numpy()
            
            # Convert to robot dict format
            action_dict = {joint_name: float(action_val) for joint_name, action_val in zip(JOINT_NAMES, action_np)}
            
            robot.send_action(action_dict)
            
            if step == 0 or step % 50 == 0:
                print(f"Step {step}: Denormalized Action = {action_np[:3]}...")
        
        print(f"Episode {ep+1} completed!")

finally:
    robot.disconnect()
    print("\nRobot disconnected. Done!")

"""Test script to check if motor 5 on leader arm is readable"""
import time
from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig
from lerobot.teleoperators.utils import make_teleoperator_from_config

# Create leader config
config = SO101LeaderConfig(
    port="COM9",
    id="test_leader"
)

# Connect to leader
leader = make_teleoperator_from_config(config)
leader.connect(calibrate=False)

print("Reading motor positions continuously. Move motor 5 (wrist_roll) and watch the values...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        action = leader.get_action()
        
        # Print all motor positions
        print(f"shoulder_pan: {action['shoulder_pan.pos']:.2f}  "
              f"shoulder_lift: {action['shoulder_lift.pos']:.2f}  "
              f"elbow_flex: {action['elbow_flex.pos']:.2f}  "
              f"wrist_flex: {action['wrist_flex.pos']:.2f}  "
              f"wrist_roll: {action['wrist_roll.pos']:.2f}  "
              f"gripper: {action['gripper.pos']:.2f}", end='\r')
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\nStopping...")
    leader.disconnect()
    print("Leader disconnected")

"""Fix wrist_roll motor position issue"""
from lerobot.motors.feetech import FeetechMotorsBus, DriveMode
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    },
)

bus.connect()

print("\nChecking wrist_roll (motor 5) configuration...")
print("=" * 60)

# Check current position
pos = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"Current position: {pos}")
print(f"Offset from center (2048): {pos - 2048}")

# Try to move it to a valid position near center
print("\nMoving wrist_roll to position 2048 (center)...")
bus.disable_torque("wrist_roll")
bus.write("Operating_Mode", "wrist_roll", 0)  # Position mode
bus.write("Goal_Position", "wrist_roll", 2048, normalize=False)
bus.enable_torque("wrist_roll")

import time
time.sleep(2)

new_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"New position: {new_pos}")

bus.disconnect()
print("\nDone! Try calibration again.")

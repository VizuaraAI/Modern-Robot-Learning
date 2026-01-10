"""Factory reset motor 5 and set proper limits"""
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    },
)

bus.connect()

print("\nResetting motor 5 (wrist_roll)...")
print("=" * 60)

# Disable torque first
bus.disable_torque("wrist_roll")

# Reset all calibration values to safe defaults
print("Setting position limits to 0-4095...")
bus.write("Min_Position_Limit", "wrist_roll", 0, normalize=False)
bus.write("Max_Position_Limit", "wrist_roll", 4095, normalize=False)

print("Setting homing offset to 0...")
bus.write("Homing_Offset", "wrist_roll", 0, normalize=False)

# Try to clear any bad state by reading the actual physical position
print("\nReading current physical position...")
import time
time.sleep(0.5)

# Read the raw position
pos = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"Raw position reading: {pos}")

# If it's negative or out of range, we need to interpret it correctly
# Feetech motors use 0-4095 range, so negative means the value is being read incorrectly
if pos < 0:
    # This might be a signed interpretation of an unsigned value
    # Try to get the actual unsigned value
    actual_pos = pos & 0xFFFF  # Get the lower 16 bits as unsigned
    print(f"Actual unsigned position: {actual_pos}")
    
    # Set proper mid-range position
    target_pos = 2048
    print(f"\nMoving to center position {target_pos}...")
    bus.write("Operating_Mode", "wrist_roll", 0, normalize=False)  # Position control mode
    bus.enable_torque("wrist_roll")
    bus.write("Goal_Position", "wrist_roll", target_pos, normalize=False)
    
    time.sleep(2)
    
    new_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
    print(f"New position: {new_pos}")
    
    if new_pos < 0:
        new_actual = new_pos & 0xFFFF
        print(f"New actual unsigned position: {new_actual}")
else:
    print(f"Position is valid: {pos}")
    target_pos = 2048
    print(f"Moving to center position {target_pos}...")
    bus.write("Operating_Mode", "wrist_roll", 0, normalize=False)
    bus.enable_torque("wrist_roll")
    bus.write("Goal_Position", "wrist_roll", target_pos, normalize=False)
    time.sleep(2)
    new_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
    print(f"New position: {new_pos}")

bus.disconnect()
print("\nDone! Run check_leader_positions.py to verify.")

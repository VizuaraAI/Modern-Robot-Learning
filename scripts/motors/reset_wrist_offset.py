"""Reset wrist_roll motor homing offset"""
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    },
)

bus.connect()

print("\nResetting wrist_roll (motor 5) homing offset to 0...")
print("=" * 60)

# Read current homing offset
try:
    current_offset = bus.read("Homing_Offset", "wrist_roll", normalize=False)
    print(f"Current homing offset: {current_offset}")
except:
    print("Could not read current homing offset")

# Set homing offset to 0
print("Setting homing offset to 0...")
bus.write("Homing_Offset", "wrist_roll", 0, normalize=False)

# Verify
try:
    new_offset = bus.read("Homing_Offset", "wrist_roll", normalize=False)
    print(f"New homing offset: {new_offset}")
except:
    print("Could not verify new homing offset")

# Check position
pos = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"Current position after reset: {pos}")

bus.disconnect()
print("\nDone! Check position again with check_leader_positions.py")

"""Check and reset motor 5 position limits"""
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    },
)

bus.connect()

print("\nMotor 5 (wrist_roll) detailed info:")
print("=" * 60)

# Read all important values
pos = bus.read("Present_Position", "wrist_roll", normalize=False)
min_pos = bus.read("Min_Position_Limit", "wrist_roll", normalize=False)
max_pos = bus.read("Max_Position_Limit", "wrist_roll", normalize=False)
homing = bus.read("Homing_Offset", "wrist_roll", normalize=False)

print(f"Present Position:      {pos}")
print(f"Min Position Limit:    {min_pos}")
print(f"Max Position Limit:    {max_pos}")
print(f"Homing Offset:         {homing}")
print(f"\nPosition with homing: {pos}")

# Manually move the joint and see what happens
print("\n" + "=" * 60)
print("Manually move the wrist_roll joint slowly...")
print("Watching position values (press Ctrl+C to stop):\n")

import time
try:
    while True:
        pos = bus.read("Present_Position", "wrist_roll", normalize=False)
        print(f"Position: {pos:6d}  (offset from 2048: {pos - 2048:+6d})", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nStopped.")

bus.disconnect()

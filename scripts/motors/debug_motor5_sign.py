"""Force motor 5 to use correct position reading by disabling sign decoding"""
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    },
)

bus.connect()

print("\n" + "=" * 60)
print("Reading motor 5 position with and without sign decoding:")
print("=" * 60)

# Read with normal decoding (current buggy behavior)
pos_normal = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"With sign decoding: {pos_normal}")

# Read raw value without sign decoding
import scservo_sdk as scs
from lerobot.motors.motors_bus import get_address

model = "sts3215"
addr, length = get_address(bus.model_ctrl_table, model, "Present_Position")

# Direct read without sign processing
bus._setup_sync_reader([5], addr, length)
comm = bus.sync_reader.txRxPacket()
raw_value = bus.sync_reader.getData(5, addr, length)

print(f"Raw value (no decoding): {raw_value}")
print(f"As unsigned 16-bit: {raw_value & 0xFFFF}")

# Try to interpret this correctly
# For sign-magnitude with bit 15:
# If bit 15 = 0, value is positive
# If bit 15 = 1, value is negative and we need to flip the sign
if raw_value & 0x8000:  # Bit 15 is set (negative)
    magnitude = raw_value & 0x7FFF  # Get lower 15 bits
    signed_value = -magnitude
    print(f"Sign bit set, magnitude: {magnitude}, signed: {signed_value}")
else:
    print(f"Sign bit not set, positive value: {raw_value}")

print("\n" + "=" * 60)
print("The issue: Motor 5 has bit 15 set, making it negative.")
print("Solution: We need to clear the sign bit or fix the motor's")
print("internal position counter.")
print("=" * 60)

# Try to write a positive position to fix it
print("\nAttempting to fix by writing position 2048...")
bus.disable_torque("wrist_roll")
bus.write("Operating_Mode", "wrist_roll", 0, normalize=False)

# Write directly without sign encoding
bus._write(addr, length, 5, 2048, num_retry=0)

bus.enable_torque("wrist_roll")

import time
time.sleep(1)

# Read again
new_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"New position after write: {new_pos}")

bus.disconnect()

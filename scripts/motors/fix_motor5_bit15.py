"""Fix motor 5 by writing unsigned position value directly"""
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
from lerobot.motors.motors_bus import get_address
import time

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    },
)

bus.connect()

print("\n" + "=" * 60)
print("Fixing motor 5 by clearing bit 15")
print("=" * 60)

model = "sts3215"
addr, length = get_address(bus.model_ctrl_table, model, "Present_Position")

# Read current raw value
bus._setup_sync_reader([5], addr, length)
comm = bus.sync_reader.txRxPacket()
raw_value = bus.sync_reader.getData(5, addr, length)
print(f"Current raw value: {raw_value} (binary: {bin(raw_value)})")

# Clear bit 15 to get the actual position we want
corrected_value = raw_value & 0x7FFF  # Clear bit 15
print(f"Corrected value (bit 15 cleared): {corrected_value}")

# Write this as the goal position (without sign encoding)
print("\nWriting corrected position...")
bus.disable_torque("wrist_roll")
bus.write("Operating_Mode", "wrist_roll", 0, normalize=False)

# Write the corrected value directly (2048 for center)
target = 2048
print(f"Writing target position: {target}")

# Get goal position address
goal_addr, goal_length = get_address(bus.model_ctrl_table, model, "Goal_Position")

# Write directly without sign encoding - use raw write
bus.port_handler.clearPort()
import scservo_sdk as scs
data = [target & 0xFF, (target >> 8) & 0xFF]  # Little-endian 2 bytes
comm, error = bus.packet_handler.writeTxRx(bus.port_handler, 5, goal_addr, goal_length, data)
print(f"Write result - comm: {bus.packet_handler.getTxRxResult(comm)}, error: {error}")

bus.enable_torque("wrist_roll")
time.sleep(2)

# Read new position
new_pos = bus.read("Present_Position", "wrist_roll", normalize=False)
print(f"\nNew position: {new_pos}")

# Read raw again
bus._setup_sync_reader([5], addr, length)
comm = bus.sync_reader.txRxPacket()
new_raw = bus.sync_reader.getData(5, addr, length)
print(f"New raw value: {new_raw} (binary: {bin(new_raw)})")

if new_raw & 0x8000:
    print("WARNING: Bit 15 is still set! Motor may have hardware issue.")
else:
    print("SUCCESS: Bit 15 cleared!")

bus.disconnect()

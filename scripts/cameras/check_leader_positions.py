"""Check current positions of all motors on leader arm"""
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

bus = FeetechMotorsBus(
    port="COM9",
    motors={
        "shoulder_pan": Motor(1, "sts3215", MotorNormMode.RANGE_M100_100),
        "shoulder_lift": Motor(2, "sts3215", MotorNormMode.RANGE_M100_100),
        "elbow_flex": Motor(3, "sts3215", MotorNormMode.RANGE_M100_100),
        "wrist_flex": Motor(4, "sts3215", MotorNormMode.RANGE_M100_100),
        "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
        "gripper": Motor(6, "sts3215", MotorNormMode.RANGE_0_100),
    },
)

bus.connect()

print("\nCurrent RAW positions of all motors:")
print("=" * 60)
positions = bus.sync_read("Present_Position", normalize=False)
for motor, pos in positions.items():
    offset_from_center = pos - 2048
    offset_magnitude = abs(offset_from_center)
    status = "✓ OK" if offset_magnitude <= 2047 else "✗ TOO FAR FROM CENTER!"
    print(f"{motor:15s}: {pos:5d}  (offset from 2048: {offset_from_center:+5d})  {status}")

print("\nFor calibration to work, all offsets should be between -2047 and +2047")
print("If any motor shows 'TOO FAR FROM CENTER', move that joint closer to center.")

bus.disconnect()

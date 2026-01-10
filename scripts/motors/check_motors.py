from lerobot.motors.feetech.feetech import FeetechMotorsBus

# Setup the connection to COM9
# Try baudrate 1000000 (Standard) first. If that fails, change to 57600.
bus = FeetechMotorsBus(port="COM9", motors={}, baudrate=57600)

print("Connecting...")
bus.connect()

print("Scanning for motors...")
# This will try to ping all IDs
found_motors = bus.broadcast_ping()
print(f"Found Motors: {found_motors}")
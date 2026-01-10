import sys
from lerobot.motors.feetech.feetech import FeetechMotorsBus

# CONFIGURATION
PORT = "COM9"

def force_set_id():
    print(f"Connecting to {PORT}...")
    # Initialize the bus
    bus = FeetechMotorsBus(port=PORT, motors={})
    bus.connect(handshake=False)
    
    print("\nScanning for connected motor...")
    found_motors = bus.broadcast_ping()
    print(f"Found these IDs: {list(found_motors.keys())}")

    if len(found_motors) == 0:
        print("❌ ERROR: No motors found! Check your cable and power.")
        return
    
    if len(found_motors) > 1:
        print(f"❌ ERROR: Found {len(found_motors)} motors! Please connect ONLY the one you want to fix.")
        return

    # Get the current ID of the single connected motor
    current_id = list(found_motors.keys())[0]
    
    print("------------------------------------------------")
    print(f"✅ Found ONE motor. Current ID: {current_id}")
    try:
        new_id = int(input("Enter the NEW ID you want for this motor (e.g. 1 or 2): "))
    except ValueError:
        print("Invalid number.")
        return

    print(f"Changing ID {current_id} -> {new_id}...")
    
    # Write the new ID to the motor's memory
    # Address 5, length 1 byte for Feetech motors (STS/SMS/SCS series)
    bus._write(addr=5, length=1, motor_id=current_id, value=new_id, raise_on_error=True)
    
    print("------------------------------------------------")
    print(f"🎉 SUCCESS! Motor is now ID {new_id}")
    print("You can unplug it now.")

if __name__ == "__main__":
    force_set_id()
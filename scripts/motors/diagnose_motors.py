#!/usr/bin/env python
"""
Low-level motor diagnostic script for SO101 Leader arm.
This helps diagnose and fix motor issues, especially when motors 1 & 2 are missing.
"""
import sys
from lerobot.motors.feetech.feetech import FeetechMotorsBus

# CONFIGURATION
PORT = "COM9"  # Change this to your port

def print_menu():
    print("\n" + "="*60)
    print("  MOTOR DIAGNOSTIC TOOL - SO101 Leader")
    print("="*60)
    print("1. Scan all motors on the bus (see what's connected)")
    print("2. Test specific motor ID (check if motor ID 1 or 2 responds)")
    print("3. Change motor ID (fix wrong ID)")
    print("4. Scan at different baudrates (if motors are at wrong speed)")
    print("5. Quick fix motors 1 & 2 (one at a time)")
    print("6. Quick set one motor to specific ID (e.g., make this motor ID 2)")
    print("7. Exit")
    print("="*60)

def scan_all_motors():
    """Scan for all motors on the bus."""
    print(f"\n🔍 Scanning all motors on {PORT}...")
    bus = FeetechMotorsBus(port=PORT, motors={})
    
    try:
        bus.connect(handshake=False)
        print("✅ Connected to bus")
        
        print("\n🔍 Broadcasting ping to all motors...")
        found_motors = bus.broadcast_ping()
        
        if not found_motors:
            print("❌ No motors found!")
            print("\nTroubleshooting:")
            print("  - Check power supply is ON")
            print("  - Check USB cable is connected")
            print("  - Check motor cables are properly connected")
            return
        
        print(f"\n✅ Found {len(found_motors)} motor(s):")
        for motor_id, model_number in found_motors.items():
            print(f"   ID {motor_id}: Model {model_number}")
        
        # Check for SO101 expected motors
        expected_ids = [1, 2, 3, 4, 5, 6]
        missing_ids = [id_ for id_ in expected_ids if id_ not in found_motors]
        
        if missing_ids:
            print(f"\n⚠️  Missing expected motor IDs: {missing_ids}")
            print("   These motors should be present for SO101 Leader.")
        else:
            print("\n✅ All 6 motors found! Your arm is fully detected.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if bus.is_connected:
            bus.disconnect()

def test_specific_id():
    """Test if a specific motor ID responds."""
    try:
        motor_id = int(input("\nEnter motor ID to test (1-6): "))
        if motor_id < 1 or motor_id > 253:
            print("Invalid ID. Must be 1-253")
            return
    except ValueError:
        print("Invalid input")
        return
    
    print(f"\n🔍 Testing motor ID {motor_id} on {PORT}...")
    bus = FeetechMotorsBus(port=PORT, motors={})
    
    try:
        bus.connect(handshake=False)
        print("✅ Connected to bus")
        
        print(f"\n🔍 Pinging motor ID {motor_id}...")
        model = bus.ping(motor_id)
        
        if model is not None:
            print(f"✅ Motor ID {motor_id} FOUND! Model number: {model}")
            
            # Try to read position
            try:
                # Address 56 is Present_Position for STS servos
                position = bus._read(addr=56, length=2, motor_id=motor_id)
                print(f"   Current position: {position}")
            except:
                print("   (Could not read position)")
        else:
            print(f"❌ Motor ID {motor_id} NOT FOUND")
            print(f"\nTroubleshooting:")
            print(f"  - Motor might have a different ID")
            print(f"  - Motor might be at a different baudrate")
            print(f"  - Check motor cable connection")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if bus.is_connected:
            bus.disconnect()

def change_motor_id():
    """Change a motor's ID (only connect ONE motor)."""
    print("\n" + "="*60)
    print("  CHANGE MOTOR ID")
    print("="*60)
    print("⚠️  IMPORTANT: Connect ONLY ONE motor!")
    print("   Disconnect all other motors from the bus.")
    input("\nPress ENTER when only ONE motor is connected...")
    
    print(f"\n🔍 Scanning for motors on {PORT}...")
    bus = FeetechMotorsBus(port=PORT, motors={})
    
    try:
        bus.connect(handshake=False)
        found_motors = bus.broadcast_ping()
        
        if len(found_motors) == 0:
            print("❌ No motors found! Check connections.")
            return
        
        if len(found_motors) > 1:
            print(f"❌ Found {len(found_motors)} motors: {list(found_motors.keys())}")
            print("   Please connect ONLY ONE motor and try again.")
            return
        
        current_id = list(found_motors.keys())[0]
        print(f"✅ Found motor with ID: {current_id}")
        
        try:
            new_id = int(input(f"\nEnter NEW ID (1-6 for SO101 motors): "))
            if new_id < 1 or new_id > 253:
                print("Invalid ID")
                return
        except ValueError:
            print("Invalid input")
            return
        
        print(f"\n🔧 Changing motor ID from {current_id} to {new_id}...")
        
        # Write new ID (address 5 for Feetech)
        bus._write(addr=5, length=1, motor_id=current_id, value=new_id, raise_on_error=True)
        
        print(f"✅ SUCCESS! Motor is now ID {new_id}")
        print("   You can disconnect this motor and connect the next one.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if bus.is_connected:
            bus.disconnect()

def scan_different_baudrates():
    """Scan for motors at different baudrates."""
    print("\n🔍 Scanning at different baudrates...")
    print("   (This may take a while...)")
    
    # Common Feetech baudrates
    baudrates = [1_000_000, 500_000, 115200, 57600, 38400, 19200, 9600]
    
    try:
        motor_id = int(input("\nEnter motor ID to search for (1-6): "))
    except ValueError:
        print("Invalid input")
        return
    
    bus = FeetechMotorsBus(port=PORT, motors={})
    
    try:
        bus.connect(handshake=False)
        
        for baudrate in baudrates:
            print(f"\n  Testing baudrate: {baudrate}...", end=" ")
            bus.set_baudrate(baudrate)
            
            model = bus.ping(motor_id)
            if model is not None:
                print(f"✅ FOUND at {baudrate}! Model: {model}")
                print(f"   Motor ID {motor_id} is communicating at {baudrate} baud")
                return
            else:
                print("❌")
        
        print(f"\n❌ Motor ID {motor_id} not found at any baudrate")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if bus.is_connected:
            bus.disconnect()

def quick_set_single_motor():
    """Quickly set one motor to any ID you want."""
    print("\n" + "="*60)
    print("  QUICK SET MOTOR TO SPECIFIC ID")
    print("="*60)
    print("⚠️  Connect ONLY ONE motor!")
    
    try:
        target_id = int(input("\nWhat ID do you want to set this motor to? (1-6): "))
        if target_id < 1 or target_id > 253:
            print("Invalid ID. Must be 1-253")
            return
    except ValueError:
        print("Invalid input")
        return
    
    input(f"\nConnect ONLY the motor you want to set as ID {target_id} and press ENTER...")
    
    print(f"\n🔍 Scanning for motor on {PORT}...")
    bus = FeetechMotorsBus(port=PORT, motors={})
    
    try:
        bus.connect(handshake=False)
        found_motors = bus.broadcast_ping()
        
        if len(found_motors) == 0:
            print("❌ No motor found! Check connections.")
            return
        
        if len(found_motors) > 1:
            print(f"❌ Found {len(found_motors)} motors: {list(found_motors.keys())}")
            print("   Please connect ONLY ONE motor.")
            return
        
        current_id = list(found_motors.keys())[0]
        print(f"✅ Found motor with current ID: {current_id}")
        
        if current_id == target_id:
            print(f"✅ Motor already has ID {target_id}! Nothing to do.")
        else:
            print(f"🔧 Changing ID from {current_id} to {target_id}...")
            bus._write(addr=5, length=1, motor_id=current_id, value=target_id, raise_on_error=True)
            print(f"✅ SUCCESS! Motor is now ID {target_id}!")
        
        bus.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if bus.is_connected:
            bus.disconnect()

def quick_fix_motors_1_2():
    """Quick fix for motors 1 and 2."""
    print("\n" + "="*60)
    print("  QUICK FIX FOR MOTORS 1 & 2")
    print("="*60)
    print("\nThis will help you set up motors 1 and 2 one at a time.")
    print("\nSteps:")
    print("1. Disconnect ALL motors from the bus")
    print("2. Connect ONLY the motor you want to set as ID 1")
    print("3. We'll scan and set it to ID 1")
    print("4. Repeat for motor ID 2")
    
    for target_id in [1, 2]:
        print(f"\n" + "-"*60)
        print(f"  Setting up motor for ID {target_id}")
        print("-"*60)
        input(f"\nConnect ONLY the motor that should be ID {target_id} and press ENTER...")
        
        bus = FeetechMotorsBus(port=PORT, motors={})
        
        try:
            bus.connect(handshake=False)
            found_motors = bus.broadcast_ping()
            
            if len(found_motors) == 0:
                print("❌ No motor found! Check connections.")
                retry = input("Retry? (y/n): ")
                if retry.lower() == 'y':
                    continue
                else:
                    return
            
            if len(found_motors) > 1:
                print(f"❌ Found multiple motors: {list(found_motors.keys())}")
                print("   Please connect ONLY ONE motor.")
                retry = input("Retry? (y/n): ")
                if retry.lower() == 'y':
                    continue
                else:
                    return
            
            current_id = list(found_motors.keys())[0]
            print(f"✅ Found motor with current ID: {current_id}")
            
            if current_id == target_id:
                print(f"✅ Motor already has ID {target_id}! Moving to next...")
            else:
                print(f"🔧 Changing ID from {current_id} to {target_id}...")
                bus._write(addr=5, length=1, motor_id=current_id, value=target_id, raise_on_error=True)
                print(f"✅ Motor is now ID {target_id}!")
            
            bus.disconnect()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            retry = input("Retry? (y/n): ")
            if retry.lower() != 'y':
                return
    
    print("\n" + "="*60)
    print("✅ Motors 1 and 2 setup complete!")
    print("="*60)
    print("\nNow you can:")
    print("1. Connect all motors back to the bus")
    print("2. Run the full setup: python src/lerobot/scripts/lerobot_setup_motors.py --teleop.type so101_leader --teleop.port COM9")

def main():
    print("\n🤖 SO101 Motor Diagnostic Tool")
    print(f"   Port: {PORT}")
    
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                scan_all_motors()
            elif choice == "2":
                test_specific_id()
            elif choice == "3":
                change_motor_id()
            elif choice == "4":
                scan_different_baudrates()
            elif choice == "5":
                quick_fix_motors_1_2()
            elif choice == "6":
                quick_set_single_motor()
            elif choice == "7":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

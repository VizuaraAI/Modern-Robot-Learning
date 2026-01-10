# Custom SO-101 Scripts Documentation

This repository contains custom scripts developed for SO-101 robot setup, troubleshooting, and operation with LeRobot. All scripts are organized into logical directories for easy navigation.

## Directory Structure

```
scripts/
├── motors/           # Motor troubleshooting and calibration scripts (10 files)
├── cameras/          # Camera testing and configuration scripts (3 files)
└── utils/            # General utility scripts (2 files)

docs/
├── MOTOR5_TROUBLESHOOTING_GUIDE.md    # Detailed motor 5 troubleshooting
├── RECORDING_AND_TRAINING_GUIDE.md    # Complete setup and training guide
└── CUSTOM_SCRIPTS.md                  # This file
```

## Scripts Overview

### Motor Scripts (`scripts/motors/`)

#### Core Motor Diagnostics
- **`check_motors.py`** - Comprehensive motor health check and status report
- **`diagnose_motors.py`** - Advanced motor diagnosis with detailed error analysis
- **`inspect_motor5.py`** - Specialized inspection for motor 5 (wrist roll)

#### Motor 5 Specific Fixes
- **`debug_motor5_sign.py`** - Debug motor 5 sign bit issues (bit 15 stuck)
- **`factory_reset_motor5.py`** - Factory reset motor 5 to default state
- **`fix_motor5_bit15.py`** - Fix motor 5 bit 15 sign encoding issues
- **`fix_wrist_roll.py`** - Calibrate and fix wrist roll motor positioning
- **`reset_wrist_offset.py`** - Reset wrist motor homing offset
- **`test_leader_motor5.py`** - Test motor 5 on leader arm specifically

#### Motor Utilities
- **`force_id.py`** - Force set motor IDs (use with caution)

### Camera Scripts (`scripts/cameras/`)

- **`check_leader_positions.py`** - Verify leader arm positions during camera calibration
- **`test_cameras.py`** - Test camera connectivity and capture functionality
- **`view_cameras.py`** - Live camera feed viewer for debugging

### Utility Scripts (`scripts/utils/`)

- **`simple_inference.py`** - Simplified inference script for testing trained models
- **`upload_data.py`** - Upload datasets to HuggingFace Hub

## Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Motor Check
```bash
cd scripts/motors
python check_motors.py --port COM10
```

### Camera Testing
```bash
cd scripts/cameras
python test_cameras.py
```

### Model Inference
```bash
cd scripts/utils
python simple_inference.py --policy.path your_model_path
```

## Common Issues & Solutions

### Motor 5 Issues
If motor 5 shows negative positions or communication errors:
1. Run `inspect_motor5.py` to diagnose
2. Try `fix_motor5_bit15.py` for sign bit issues
3. Use `factory_reset_motor5.py` as last resort

### Camera Issues
- Check camera indices with `test_cameras.py`
- Verify camera permissions on Windows
- Ensure cameras are not used by other applications

### Serial Communication
- Increase timeout in `feetech.py` if needed (currently 5000ms)
- Check COM port assignments
- Ensure motors are powered and connected

## Modified Core Files

The following LeRobot core files were modified for Windows/SO-101 compatibility:

- `src/lerobot/cameras/opencv/camera_opencv.py`
  - Removed backend parameter for Windows compatibility
  - Increased async read timeout to 2000ms

- `src/lerobot/motors/feetech/feetech.py`
  - Increased serial timeout from 1000ms to 5000ms

- `src/lerobot/scripts/lerobot_find_cameras.py`
  - Removed warmup parameter from camera connect

- `src/lerobot/teleoperators/so101_leader/so101_leader.py`
  - Added Motor 5 bit-15 workaround patches

## Safety Notes

⚠️ **Important Safety Warnings:**

- **Motor Scripts**: Some scripts can change motor parameters. Always backup configurations before running calibration scripts.
- **Factory Reset**: `factory_reset_motor5.py` will erase all motor settings. Use only as last resort.
- **Force ID**: `force_id.py` can conflict with other motors. Ensure only one motor is connected when changing IDs.
- **Power**: Always ensure adequate power supply when running motor scripts to prevent damage.

## Files for Public Sharing

### ✅ KEEP (Essential for SO-101 users):
- All scripts in `scripts/` directory
- `docs/MOTOR5_TROUBLESHOOTING_GUIDE.md`
- `docs/RECORDING_AND_TRAINING_GUIDE.md`
- `docs/CUSTOM_SCRIPTS.md` (this file)
- `requirements.txt` (custom dependencies)
- Modified core files (with clear comments about changes)

### ❌ REMOVE (Not for public sharing):
- `checkpoints/` - Training checkpoints (large files, user-specific)
- `outputs/` - Training outputs (user-specific)
- `test_images/` - Test images (not needed)
- Personal training configs or logs
- Any sensitive data or API keys

### 🤔 CONSIDER (Optional):
- `venv/` - Virtual environment (regenerate)
- `.git/` history - Clean repository history
- Temporary files or debug logs

## Contributing

When adding new scripts:
1. Place in appropriate subdirectory (`motors/`, `cameras/`, or `utils/`)
2. Add comprehensive docstrings
3. Include error handling
4. Update this documentation
5. Test on both leader and follower arms if applicable

## License

These custom scripts follow the same Apache 2.0 license as the main LeRobot repository.
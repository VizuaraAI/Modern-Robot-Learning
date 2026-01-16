# Modifications from Official LeRobot

This document tracks all modifications made to the official [Hugging Face LeRobot](https://github.com/huggingface/lerobot) repository.

**Fork Maintainer:** Vizuara  
**Original Repository:** https://github.com/huggingface/lerobot  
**Fork Purpose:** Optimize LeRobot for SO-101 robots on Windows with comprehensive beginner-friendly tutorials

---

## Core Code Modifications

### 1. Camera Backend (Windows Compatibility)

**File:** `src/lerobot/cameras/opencv/camera_opencv.py`

**Changes:**
- Removed `backend` parameter from `cv2.VideoCapture()` for Windows compatibility
- Increased async read timeout from 1ms to 2000ms for USB hub support
- Enhanced error handling for camera connection issues

**Reason:** Windows OpenCV doesn't support backend parameter; increased timeout prevents frame drops with USB hubs

---

### 2. Motor Communication Timeout

**File:** `src/lerobot/motors/feetech/feetech.py`

**Changes:**
- Increased `DEFAULT_TIMEOUT_MS` from 1000ms to 5000ms
- Enhanced serial communication error handling

**Reason:** USB hubs and longer cables require more time for reliable motor communication on Windows

---

### 3. Motor 5 Hardware Workaround (SO-101 Leader Arm)

**File:** `src/lerobot/teleoperators/so101_leader/so101_leader.py`

**Changes:**
- Added `patched_decode()` function to handle Motor 5 encoder bit-15 stuck issue
- Added `patched_encode()` function to clamp values within valid ranges
- Implemented runtime patching of `_decode_sign` and `_encode_sign` methods

**Reason:** SO-101 leader arm Motor 5 has hardware defect where bit 15 is stuck ON, causing negative position readings

**Technical Details:** See `resources/MOTOR5_TROUBLESHOOTING_GUIDE.md` for complete analysis

---

### 4. Camera Discovery Script

**File:** `src/lerobot/scripts/lerobot_find_cameras.py`

**Changes:**
- Removed `warmup` parameter from camera connect call

**Reason:** Windows compatibility improvement

---

## Documentation Additions

### Tutorial Series (resources/)

Complete step-by-step guides for SO-101 users:

1. **`resources/01_installation_guide.md`**
   - Virtual environment setup (Windows/Mac/Linux)
   - LeRobot installation
   - FFmpeg installation
   - HuggingFace CLI and W&B setup

2. **`resources/02_hardware_setup.md`**
   - Robot and camera connection
   - COM port identification (Windows-specific)
   - Camera index discovery
   - USB hub compatibility requirements
   - **Critical USB cable requirements** (data transfer cables vs charging-only)

3. **`resources/03_calibration_and_teleoperation.md`**
   - Robot calibration process with images and video
   - Home position setup
   - Teleoperation testing
   - Common issues and solutions

4. **`resources/04_dataset_recording.md`**
   - Dataset recording workflow
   - Camera configuration (1, 2, 3+ cameras)
   - **Keyboard controls** (Right Arrow: accept, Left Arrow: discard, ESC: stop)
   - Quality tips and best practices
   - Replay verification

5. **`resources/05_training_and_inference.md`**
   - Training on local PC vs RunPod
   - ACT policy training
   - Weights & Biases integration
   - Checkpoint management
   - Inference and evaluation

### Troubleshooting Guides

6. **`resources/MOTOR5_TROUBLESHOOTING_GUIDE.md`** (657 lines)
   - Complete technical analysis of Motor 5 hardware defect
   - Root cause analysis (encoder bit-15 stuck)
   - Failed fix attempts documented
   - Final software solution explanation
   - Sign-magnitude vs two's complement explanation

7. **`resources/CUSTOM_SCRIPTS.md`**
   - Documentation of all custom scripts
   - Motor diagnostics tools
   - Camera testing utilities
   - Safety warnings and usage guidelines

8. **`resources/RECORDING_AND_TRAINING_GUIDE.md`**
   - Complete end-to-end workflow
   - Data storage structure
   - RunPod training setup
   - Cost estimates and timelines

---

## Custom Scripts

### Motor Scripts (scripts/motors/)

Diagnostic and troubleshooting tools:
- `check_motors.py` - Motor health check
- `diagnose_motors.py` - Advanced diagnostics
- `inspect_motor5.py` - Motor 5 specific inspection
- `debug_motor5_sign.py` - Bit 15 debugging
- `factory_reset_motor5.py` - Motor 5 factory reset
- `fix_motor5_bit15.py` - Bit 15 fix utility
- `fix_wrist_roll.py` - Wrist roll calibration
- `reset_wrist_offset.py` - Reset homing offset
- `test_leader_motor5.py` - Leader arm Motor 5 testing
- `force_id.py` - Force motor ID changes

### Camera Scripts (scripts/cameras/)

Camera testing and verification:
- `test_cameras.py` - Camera connectivity test
- `view_cameras.py` - Live camera feed viewer

### Utility Scripts (scripts/utils/)

Helper utilities:
- `simple_inference.py` - Simplified inference testing
- `upload_data.py` - Dataset upload to HuggingFace

---

## Configuration Changes

### Timeout Values

| Component | Original | Modified | Reason |
|-----------|----------|----------|--------|
| Camera async read | 1ms | 2000ms | USB hub delays |
| Motor serial | 1000ms | 5000ms | Windows + USB hubs |

---

## Repository Structure Additions

```
newly_repo-/
├── resources/              [NEW] Complete tutorial series
│   ├── 01_installation_guide.md
│   ├── 02_hardware_setup.md
│   ├── 03_calibration_and_teleoperation.md
│   ├── 04_dataset_recording.md
│   ├── 05_training_and_inference.md
│   ├── MOTOR5_TROUBLESHOOTING_GUIDE.md
│   ├── CUSTOM_SCRIPTS.md
│   ├── RECORDING_AND_TRAINING_GUIDE.md
│   └── assets/            [NEW] Images and videos for guides
├── scripts/               [NEW] Custom diagnostic tools
│   ├── motors/           [NEW] Motor troubleshooting scripts
│   ├── cameras/          [NEW] Camera testing scripts
│   └── utils/            [NEW] Helper utilities
├── NOTICE                [NEW] Required by Apache 2.0
└── MODIFICATIONS.md      [NEW] This file
```

---

## Breaking Changes

**None.** All modifications maintain backward compatibility with the official LeRobot.

---

## Testing

All modifications have been tested on:
- **OS:** Windows 10/11
- **Robot:** SO-101 Leader & Follower arms
- **Cameras:** USB webcams (various resolutions)
- **USB Hubs:** Both powered and unpowered hubs
- **Python:** 3.10+

---

## Future Modifications Planned

- [ ] Additional timeout configuration options
- [ ] Automated Motor 5 detection and patching
- [ ] Enhanced Windows error messages
- [ ] More comprehensive camera testing tools

---

## Contributing to This Fork

Interested in improving this fork? See `CONTRIBUTING.md` for guidelines.

For contributions to the official LeRobot, visit: https://github.com/huggingface/lerobot

---

## License

All modifications are released under the same Apache 2.0 license as the original LeRobot.

See `LICENSE` file for full license text.

---

**Last Updated:** January 16, 2026  
**Maintainer:** Vizuara  
**Contact:** [Your contact information]

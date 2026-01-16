<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <img src="https://vizuara.ai/logo.png" alt="Vizuara" width="200px">
      </td>
      <td align="center" width="33%">
        <h1 style="font-size: 72px; margin: 0;">❤️</h1>
      </td>
      <td align="center" width="33%">
        <img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="Hugging Face LeRobot" width="200px">
      </td>
    </tr>
  </table>

  <h2>LeRobot Fork - Optimized for SO-101</h2>
  
  <p><strong>Community-maintained by <a href="https://vizuara.ai">Vizuara</a></strong></p>
  
  <p><em>A fork of <a href="https://github.com/huggingface/lerobot">Hugging Face LeRobot</a> with compatibility fixes, comprehensive tutorials, and SO-101 hardware optimizations</em></p>

</div>

<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/huggingface/lerobot/blob/main/LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/lerobot)](https://www.python.org/downloads/)
[![Original Repo](https://img.shields.io/badge/Original-huggingface%2Flerobot-orange)](https://github.com/huggingface/lerobot)

</div>

---

## ✨ What's Different in This Fork?

This fork enhances the original LeRobot specifically for **SO-101 robot users**:

### Platform Compatibility
- ✅ Fixed camera timeout issues (2000ms for USB hubs)
- ✅ Increased motor communication timeout (5000ms)
- ✅ Resolved OpenCV backend compatibility issues
- ✅ Enhanced Windows, Mac, and Linux support

### Hardware Fixes
- ✅ **Motor 5 encoder workaround** - Fixed SO-101 leader arm bit-15 hardware defect
- ✅ USB hub compatibility improvements
- ✅ Enhanced serial communication error handling

### Complete Tutorial Series
Beginner-friendly step-by-step guides in the `resources/` folder:
1. [Installation Guide](resources/01_installation_guide.md) - Setup for Windows/Mac/Linux
2. [Hardware Setup](resources/02_hardware_setup.md) - COM ports, cameras, USB requirements
3. [Calibration & Teleoperation](resources/03_calibration_and_teleoperation.md) - Robot calibration process
4. [Dataset Recording](resources/04_dataset_recording.md) - Recording with keyboard controls
5. [Training & Inference](resources/05_training_and_inference.md) - Training on local PC or RunPod

### Detailed Modifications
For a complete list of all changes, see **[MODIFICATIONS.md](MODIFICATIONS.md)**

---

## Quick Start for SO-101 Users

**New to SO-101?** Follow our complete tutorial series:

1. Clone this repository and install dependencies → [Installation Guide](resources/01_installation_guide.md)
2. Connect your robots and cameras → [Hardware Setup](resources/02_hardware_setup.md)
3. Calibrate and test teleoperation → [Calibration Guide](resources/03_calibration_and_teleoperation.md)
4. Record your first dataset → [Recording Guide](resources/04_dataset_recording.md)
5. Train your robot policy → [Training Guide](resources/05_training_and_inference.md)

**Having issues?** Check our troubleshooting guides or open an issue!

---

## Acknowledgments

This fork is built on the amazing work of the Hugging Face LeRobot team. All modifications maintain the same Apache 2.0 license as the original project.

For the official LeRobot repository and documentation, visit: [github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)


# Installation Guide

Hey everyone! Welcome to the SO-101 LeRobot setup guide.

This is the **first document** in our complete tutorial series. In this guide, we'll be installing and setting up everything you need to get your SO-101 robot up and running with LeRobot. By the end of this guide, you'll have all the software dependencies installed and your development environment fully configured.

Let's get started with the installation and setup process!

## Step 1: Clone the Repository

First, let's clone this repository to your local machine:

```bash
git clone https://github.com/OmuNaman/Modern-Robot-Learning.git
cd Modern-Robot-Learning
```

## Step 2: Create a Virtual Environment

It's highly recommended to create a virtual environment to keep your dependencies isolated. This prevents conflicts with other Python projects.

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your command line, indicating the virtual environment is active.

## Step 3: Install LeRobot Package

Now, let's install the LeRobot package in editable mode. This allows you to make changes to the code if needed:

```bash
pip install -e .
```

This will install all the required Python dependencies. It may take a few minutes.

## Step 4: Install FFmpeg

FFmpeg is required for video processing during dataset recording. Install it with:

```bash
apt-get update && apt-get install -y ffmpeg
```

**Note for Windows users:** Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

## Step 5: Setup HuggingFace CLI

We'll use HuggingFace to store and share datasets. Let's log in:

```bash
huggingface-cli login
```

When prompted, paste your HuggingFace access token. You can get one from [HuggingFace Settings](https://huggingface.co/settings/tokens).

## Step 6: Install and Setup Weights & Biases (W&B)

W&B is used for tracking training progress. First, install it:

```bash
pip install wandb
```

Then log in to your W&B account:

```bash
wandb login
```

## Step 7: Verify Everything is Setup

Let's verify that both services are properly configured:

```bash
huggingface-cli whoami
wandb verify
```

If both commands return your username/account info, you're all set! 🎉

Next, head to the hardware setup guide to configure your SO-101 robot.

from lerobot.datasets.lerobot_dataset import LeRobotDataset

# Replace with your actual local path and repo ID
local_repo_id = "omunaman/trying_act"

dataset = LeRobotDataset(local_repo_id)
dataset.push_to_hub()

"""Pytest configuration for task tracker tests."""

import os

os.environ["TASK_TRACKER_STORAGE"] = "in_memory"

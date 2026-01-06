import os

approval_threshold = float(
    os.getenv("APPROVAL_THRESHOLD", "0.5")
)

import argparse
from webcam_utils import realtime_emotions
from prediction_utils import prediction_path

# for running realtime emotion detection
def run_realtime_emotion():
    realtime_emotions()

if __name__ == '__main__':
    run_realtime_emotion()

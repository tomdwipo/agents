#!/usr/bin/env python
from video_generation_crew.crew import VideoGenerationCrew

def run():
    """
    Run the video generation crew.
    """
    inputs = {
        'topic': 'Daily Improvement'
    }
    try:
        VideoGenerationCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")





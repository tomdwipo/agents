#!/usr/bin/env python
from video_generation_crew.crew import VideoGenerationCrew
import os


TEMPLATE_PROMPT="""
An 8-second, purely visual narrative animation on a solid black (#000000) background. All iconography is a solid, vibrant purple (#6a45ff). The animation explains the concept of daily improvement without using any text.

**[0.0 - 1.5 seconds]: The Initial State**
- The video opens on the initial state: a tiny, vibrant purple sapling icon on the left and a flat horizontal purple line graph on the right. The scene holds steady and clean.

**[1.5 - 6.5 seconds]: The "Cause and Effect" Growth Phase**
- The animation begins. At the top of the frame, a sun icon cycles through its arc.
- On the first slow cycle, as the sun sets, a small orb of purple light detaches from it, travels down, and is absorbed by the sapling. The sapling grows by one tiny leaf. The graph ticks up by a single pixel.
- This repeats for a second cycle, showing the direct cause and effect: each "day" (sun cycle) directly "feeds" the growth. For a split second, a faint, ghosted afterimage of the sapling's previous size is visible, creating a direct visual comparison of "today vs. yesterday."
- Then, the animation accelerates dramatically. The sun cycles faster, sending a continuous stream of light into the icon.
- The sapling undergoes a powerful, fluid transformation, growing exponentially into a large tree. The graph's curve sweeps steeply upwards in sync with this explosive growth.

**[6.5 - 8.0 seconds]: The Final Transformed State**
- All motion abruptly freezes. The sun and the stream of light vanish.
- The sapling is now a large, flourishing, complex purple tree icon. The graph is a dramatic, steep curve, showing the immense change from its starting point.
- The final tree emits a single, slow, bright purple pulse that radiates outwards, signifying its new, powerful state. The final frame holds steady for 1.5 seconds.

**Style:** Pure iconography, no text, a clear visual narrative, cause-and-effect animation, flat 2D, modern, solid vibrant purple (#6a45ff) on a solid black (#000000) background.

"""


def run():
    """
    Run the video generation crew.
    """
    # Disable all OpenTelemetry (including CrewAI)
    os.environ['OTEL_SDK_DISABLED'] = 'true'
    inputs = {
        'topic': 'hardwork',
        'template': TEMPLATE_PROMPT
    }

    try:
        VideoGenerationCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")





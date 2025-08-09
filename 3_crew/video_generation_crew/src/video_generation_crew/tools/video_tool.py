from crewai.tools import BaseTool
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class VideoGenerationTool(BaseTool):
    name: str = "Video Generation Tool"
    description: str = "Generates a video based on a detailed prompt using the veo-2.0-generate-001 model."
    topic: str = "topic"

    def _run(self, prompt: str, topic: str) -> str:
        # Configure the API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        client = genai.Client(
            api_key=api_key
        )
        
       
        # Generate the video
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=prompt,
            config=types.GenerateVideosConfig(aspect_ratio="9:16", duration_seconds=8)
        )

        # Poll the operation status until the video is ready.
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = client.operations.get(operation)

        # Download the video.
        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)

        # Save the video to a file
        output_path = "output/"+topic+"/video.mp4"
        video.video.save(output_path)
        print("output: "+ output_path)

        return f"Video generated successfully at: output: "+output_path

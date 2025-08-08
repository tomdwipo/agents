[
  {
    "index": 1,
    "image_path": "output/posts/how-compound-interest-works/raw_images/1.png",
    "body": "Busy isn't productive."
  },
  {
    "index": 2,
    "image_path": "output/posts/how-compound-interest-works/raw_images/2.png",
    "body": "Takes two minutes? Do now."
  },
  {
    "index": 3,
    "image_path": "output/posts/how-compound-interest-works/raw_images/3.png",
    "body": "What's your first task?"
  }
]Thought
The user wants me to generate an image for each prompt provided in the input JSON. I need to iterate through the `prompts` array, call the `generate_image` tool for each entry, and then compile the results into a JSON list as specified in the "expected criteria".

**Plan:**
1.  Take the first prompt object (index 1).
2.  Call `generate_image` with the `prompt` text.
3.  Set the `save_path` to `output/posts/how-compound-interest-works/raw_images/1.png` based on the example format.
4.  Set the `size` to `1024x1024` as per my instructions.
5.  Repeat for the second and third prompts, incrementing the index in the `save_path`.
6.  Collect the results into the final JSON list.

Starting with the first prompt.
Action: generate_image
Action Input: {"prompt": "Minimalist flat design vector icon of a tangled, chaotic scribble seamlessly transforming into a single, straight, focused arrow pointing upwards. The icon is a single, centered glyph with clean, sharp lines. Solid black background. The iconography is a solid, vibrant purple with the hex code #6a45ff. No gradients, no shadows, no text. Symmetrical and perfectly balanced, ideal for an Instagram post. no watermarks.", "save_path": "output/posts/how-compound-interest-works/raw_images/1.png", "size": "1024x1024"}
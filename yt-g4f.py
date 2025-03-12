# get keyinsights from a youtube video by analysing its transcript

from youtube_transcript_api import YouTubeTranscriptApi
from g4f.client import Client

# Configuration
VIDEO_ID = "<your video id>"  # Use watch url id not share button
QUESTION = "Gebe mir die Key Points von dem folgenden Transkript: "
OUTPUT_FILENAME = "result.txt"


# Function to interact with g4f API
def get_answer(message):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        web_search=False
    )
    return response.choices[0].message.content


# Fetch YouTube transcript
print("Starting transcript download...")
try:
    transcript_data = YouTubeTranscriptApi.get_transcript(VIDEO_ID)
    print("YouTube transcript fetched successfully!")
except Exception as e:
    print(f"Error fetching transcript: {e}")
    exit()

# Combine transcript into a single string
transcript_text = " ".join(item["text"] for item in transcript_data)

# Formulate the full prompt for GPT
full_prompt = QUESTION + transcript_text

# Ask GPT for key insights
print("Sending request to g4f...")
try:
    result = get_answer(full_prompt)
    print("Response received from g4f!")
except Exception as e:
    print(f"Error getting response from g4f: {e}")
    exit()

# Save the results to a file
try:
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as output_file:
        output_file.write(result)
    print(f"\033[6;30;42m Extraction completed. Results saved in {OUTPUT_FILENAME} \033[0m")
except Exception as e:
    print(f"Error saving results: {e}")

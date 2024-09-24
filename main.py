import time
import pathlib
import edge_tts
import pygame
import asyncio
from groq import Groq
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)
print(f"{Fore.YELLOW}{Style.BRIGHT}Presenting you 'Dronacharya' most capable teacher AI with main goal for improving indian education syatem...")
print("")
print(f"{Fore.CYAN}{Style.BRIGHT}Welcome to Dronacharya, your mentor for a holistic learning journey......")
print("")
print(f"{Fore.MAGENTA}{Style.BRIGHT}Prepare for an enlightening experience.....")
print(f"{Fore.RESET}{Style.RESET_ALL}")

class EdgeTTS:
    """
    Text-to-speech provider using the Edge TTS API.
    """
    cache_dir = pathlib.Path("./audio_cache")

    def __init__(self, timeout: int = 20):
        """Initializes the Edge TTS client and clears the audio cache."""
        self.timeout = timeout
        pygame.mixer.init()

        # Clear the audio cache on startup
        self.clear_audio_cache()

        # Create a separate channel for TTS audio
        self.tts_channel = pygame.mixer.Channel(1)
        self.last_audio_file = None  # To keep track of the last audio file

    def clear_audio_cache(self):
        """Clears all audio files from the audio cache."""
        if self.cache_dir.exists():
            for audio_file in self.cache_dir.glob("*.mp3"):
                try:
                    audio_file.unlink()  # Delete the file
                except Exception as e:
                    print(f"{Fore.RED}Error deleting {audio_file}: {e}")
        else:
            self.cache_dir.mkdir(parents=True, exist_ok=True)  # Create cache directory if not exists

    def tts(self, text: str, voice: str = "hi-IN-MadhurNeural") -> str:
        """
        Converts text to speech using the Edge TTS API and saves it to a file.
        Deletes the previous audio file if it exists.
        """
        # Create the filename with a timestamp
        filename = self.cache_dir / f"{int(time.time())}.mp3"

        try:
            # Create the audio_cache directory if it doesn't exist
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            # If there is a previous audio file, delete it
            if self.last_audio_file and self.last_audio_file.exists():
                self.last_audio_file.unlink()

            # Generate new speech and save it
            asyncio.run(self._save_audio(text, voice, filename))

            # Update the last_audio_file to the current one
            self.last_audio_file = filename

            return str(filename.resolve())

        except Exception as e:
            raise RuntimeError(f"{Fore.RED}Failed to perform the operation: {e}")

    async def _save_audio(self, text: str, voice: str, filename: pathlib.Path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    def play_audio(self, filename: str):
        """
        Plays an audio file using pygame on the TTS channel, ensuring no overlap with background music.
        """
        try:
            self.tts_channel.play(pygame.mixer.Sound(filename))
            while self.tts_channel.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            raise RuntimeError(f"{Fore.RED}Error playing audio: {e}")

# Function to play music at startup in the background (different from TTS)
def play_startup_music():
    print("")
    pygame.mixer.music.load(input(f"{Fore.YELLOW}Please provide the path to the background music (or download from here 'https://drive.google.com/file/d/1pJRPFCP26ubMvBEzqtOsRCOCBJ1Z6hDW/view?usp=sharing'): "))  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 for infinite loop)

# Initialize client with API key
client = Groq(api_key=input(f"{Fore.CYAN}Insert your Groq API key: "))

# System prompt with more functionalities for Dronacharya
system_prompt = {
    "role": "system",
    "content": (
        "You are Dronacharya, a wise and knowledgeable teacher for students of all levels. Your expertise includes academic subjects, life skills, mental well-being, and providing guidance on both traditional and modern educational philosophies. You offer personalized advice, mentorship, and practical solutions to help students overcome challenges and improve their learning process do not forget your ultimate goal is to make india bright in education system and u can also speak sanskrit shlok in middle of response related to athe answer but do not forget to tell it's meaning."
    )
}

# Initialize conversation history
conversation_history = [system_prompt]

# Define additional teaching-related functions for Dronacharya
def provide_study_tips():
    return (
        "Here are some study tips for you:\n"
        "- Create a dedicated study space, free from distractions.\n"
        "- Break study sessions into focused intervals (like 25 minutes), followed by short breaks.\n"
        "- Use active recall methods and summarize topics in your own words.\n"
        "- Stay organized with a study schedule and stick to it."
    )

def suggest_time_management():
    return (
        "Here are some time management strategies:\n"
        "- Prioritize tasks based on urgency and importance.\n"
        "- Use the Pomodoro technique for focused study sessions.\n"
        "- Set achievable daily goals, and break large tasks into smaller, manageable parts.\n"
        "- Make use of time management tools like calendars or task management apps."
    )

def suggest_relaxation_methods():
    return (
        "For relaxation and stress relief, try these methods:\n"
        "- Practice deep breathing exercises or mindfulness meditation.\n"
        "- Take short, mindful breaks between study sessions to recharge.\n"
        "- Engage in light physical activities such as yoga or stretching."
    )

# Initialize the TTS engine
tts_engine = EdgeTTS()

# Function to speak the assistant's responses
def speak_response(text: str, voice: str = "hi-IN-MadhurNeural"):
    # Generate and play the response audio
    audio_file = tts_engine.tts(text, voice)
    tts_engine.play_audio(audio_file)

# Start playing background music
def Dronacharya_main():
    play_startup_music()

    # Main loop for continuous input
    while True:
        # Get user input
        print(f"{Fore.LIGHTGREEN_EX}")
        user_input = input("You: ")
        print("")

        # If the user types 'exit', break the loop
        if user_input.lower() == "exit":
            print(f"{Fore.LIGHTCYAN_EX}Exiting the session... Goodbye!")
            break

        # Provide functionality based on input keywords
        if "study tips" in user_input.lower():
            response = provide_study_tips()
            print(f"{Fore.CYAN}Dronacharya:", response)
            speak_response(response, voice="hi-IN-MadhurNeural")
            continue
        elif "time management" in user_input.lower():
            response = suggest_time_management()
            print(f"{Fore.CYAN}Dronacharya:", response)
            speak_response(response, voice="hi-IN-MadhurNeural")
            continue
        elif "relax" in user_input.lower() or "stress" in user_input.lower():
            response = suggest_relaxation_methods()
            print(f"{Fore.CYAN}Dronacharya:", response)
            speak_response(response, voice="hi-IN-MadhurNeural")
            continue

        # Append user input to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Create the chat completion using the conversation history
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=conversation_history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Stream the completion output
        response_text = ""
        print(f"{Fore.LIGHTCYAN_EX}Dronacharya:", end=" ")
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="")
        print()  # Add a newline for better formatting

        # Append assistant's response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })

        # Speak the assistant's response
        speak_response(response_text, voice="hi-IN-MadhurNeural")

Dronacharya_main()

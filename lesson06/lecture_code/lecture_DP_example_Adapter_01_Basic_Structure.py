# Target interface (what client expects)
class MediaPlayer:
    def play(self, audio_type, filename):
        print(f"Play {audio_type} file called {filename}")

# Adaptee (existing incompatible interface)
class Mp3Player:
    def play_mp3(self, filename):
        print(f"Playing MP3 file: {filename}")

class Mp4Player:
    def play_mp4(self, filename):
        print(f"Playing MP4 file: {filename}")

# Adapter (makes adaptee compatible with target)
class MediaAdapter(MediaPlayer):
    def __init__(self):
        self.mp3_player = Mp3Player()
        self.mp4_player = Mp4Player()
    
    def play(self, audio_type, filename):
        if audio_type == "mp3":
            self.mp3_player.play_mp3(filename)
        elif audio_type == "mp4":
            self.mp4_player.play_mp4(filename)
        else:
            print(f"Invalid media. {audio_type} format not supported")

# Client (uses target interface)
class AudioPlayer(MediaPlayer):
    def __init__(self):
        self.adapter = MediaAdapter()
    
    def play(self, audio_type, filename):
        if audio_type == "wav":
            self.play(audio_type, filename)
        if audio_type == "mp3" or audio_type == "mp4":
            self.adapter.play(audio_type, filename)
        else:
            print(f"Unsupported format: {audio_type}")

# Example usage
if __name__ == "__main__":
    audio_player = AudioPlayer()
    
    audio_player.play("mp3", "song1.mp3")
    audio_player.play("mp4", "video1.mp4")
    audio_player.play("avi", "movie1.avi")

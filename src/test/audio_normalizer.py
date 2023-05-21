import os
from pydub import AudioSegment, effects

sounds_folder = "../../assets/audio/sounds"
music_folder = "../../assets/audio/music"

target_dBFS = -12


def normalize_audio(path: str):
    for filename in os.listdir(path):
        if not filename.endswith(".mp3") and not filename.endswith(".wav"):
            continue
        sound = AudioSegment.from_file(f"{path}/{filename}", format="mp3")
        print(f"{path}/{filename}", sound.max_dBFS)
        # normalized_sound = effects.normalize(sound)
        # normalized_sound.export(f"{path}/normalized_{filename}", format="mp3")


if __name__ == '__main__':
    normalize_audio(music_folder)

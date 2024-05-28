import os

from pydub import AudioSegment
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from whisper import load_audio

import utils


class Transcriber:
    def __init__(self):
        self.processor = WhisperProcessor.from_pretrained("BHOSAI/Pichilti-base-v1")
        self.model = WhisperForConditionalGeneration.from_pretrained("BHOSAI/Pichilti-base-v1")

    def process_file(self, file_path: str) -> str:
        wave_path = utils.temp_file(suffix='.wav')
        try:
            audio = AudioSegment.from_file(file_path)
            audio.export(wave_path, format='wav')
            return self.__process_wav(wave_path)
        finally:
            self.__unlink(wave_path)

    @staticmethod
    def __unlink(file_path: str):
        try:
            os.unlink(file_path)
        except FileNotFoundError:
            pass

    def __process_wav(self, wav_path: str) -> str:
        wav = load_audio(wav_path)

        input_features = self.processor(wav, return_tensors="pt").input_features
        predicted_ids = self.model.generate(input_features)
        transcript = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return transcript[0]


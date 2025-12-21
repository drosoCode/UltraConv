import librosa
import numpy as np
import re
from scipy.signal import find_peaks
from math import floor, ceil

def extract_word_timings(line_audio, sr, words, line_start, line_end):
    """
    Extract word-level timings from an audio file using line-level timing data.
    
    Args:
        audio_file (str): Path to audio file
        timed_lines (list): List of dicts with 'text', 'start_time', and 'end_time'
    
    Returns:
        list: List of dicts with 'word', 'start_time', and 'duration'
    """
    # Load audio file
    #y, sr = librosa.load(audio_file, sr=None)
    
    all_word_timings = []

    # METHOD 1: ENERGY-BASED ANALYSIS
    # Calculate audio energy to find natural word boundaries
    hop_length = 512
    energy = librosa.feature.rms(y=line_audio, hop_length=hop_length)[0]
    times = librosa.times_like(energy, sr=sr, hop_length=hop_length)
    
    # Smooth energy curve
    energy_smooth = np.convolve(energy, np.ones(5)/5, mode='same')
    
    # Find peaks in energy (potential syllable/word boundaries)
    peaks, _ = find_peaks(energy_smooth, distance=5)
    
    if len(peaks) >= len(words):
        # Use audio-based segmentation when we have enough peaks
        word_boundaries = []
        peaks_per_word = len(peaks) // len(words)
        remainder = len(peaks) % len(words)
        
        start_idx = 0
        for i, word in enumerate(words):
            # Distribute remainder peaks
            extra = 1 if i < remainder else 0
            end_idx = start_idx + peaks_per_word + extra
            
            if end_idx > len(peaks):
                end_idx = len(peaks)
            
            if start_idx < len(peaks):
                word_start_time = line_start + times[peaks[start_idx]]
                
                if i < len(words) - 1 and end_idx < len(peaks):
                    next_word_start = times[peaks[end_idx]]
                    word_duration = next_word_start - times[peaks[start_idx]]
                else:
                    # Last word goes to end of line
                    word_duration = line_end - word_start_time
                
                # Add a small gap (10% of duration)
                effective_duration = word_duration * 0.9
                
                all_word_timings.append({
                    'word': words[i],
                    'start_time': word_start_time,
                    'duration': effective_duration
                })
            
            start_idx = end_idx
    else:
        print("Not enough peaks found for word segmentation, falling back to text-based segmentation.")

    return all_word_timings


def forced_alignment(vocals_mp3, start, end, words):
    # start is in ms, convert to seconds
    start_sec = start / 1000.0
    end_sec = end / 1000.0

    y, sr = librosa.load(vocals_mp3)
    y = y[floor(start_sec*sr):ceil(end_sec*sr)]  # Trim the audio to the specified segment
    
    return extract_word_timings(y, sr, words, start_sec, end_sec)


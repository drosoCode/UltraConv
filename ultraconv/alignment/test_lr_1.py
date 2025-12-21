import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import pandas as pd
from math import floor, ceil

def extract_word_timings(y, sr, words_list, start):
    """
    Extract word timings from music audio and generate a spectrogram visualization.
    
    Parameters:
        audio_file (str): Path to the audio file
        words_list (list): List of words to align with the music
        
    Returns:
        list: List of dictionaries with word, start_time, and duration
    """
    # Load the audio file
    #print(f"Loading audio file: {audio_file}")
    #y, sr = librosa.load(audio_file)
    
    # Calculate the spectrogram
    D = librosa.stft(y)
    D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    # Calculate onset strength (helps identify significant changes in audio)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    # Detect onsets (potential word boundaries)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    # If we have fewer onsets than words, add additional boundaries
    if len(onset_times) < len(words_list):
        # Calculate additional boundaries using energy-based segmentation
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_var = np.var(mfcc, axis=0)
        mfcc_var_smooth = medfilt(mfcc_var, 11)
        
        # Find peaks in the smoothed variance
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(mfcc_var_smooth, distance=sr//512)
        peak_times = librosa.frames_to_time(peaks, sr=sr)
        
        # Combine with onset times and sort
        all_boundaries = np.sort(np.concatenate([onset_times, peak_times]))
        
        # Remove boundaries that are too close to each other
        min_gap = 0.1  # Minimum gap between boundaries in seconds
        filtered_boundaries = [all_boundaries[0]]
        for b in all_boundaries[1:]:
            if b - filtered_boundaries[-1] >= min_gap:
                filtered_boundaries.append(b)
        
        boundaries = np.array(filtered_boundaries)
    else:
        boundaries = onset_times
    
    # Ensure we have at least as many segments as words
    if len(boundaries) < len(words_list) + 1:
        # Add evenly spaced boundaries if needed
        total_duration = librosa.get_duration(y=y, sr=sr)
        boundaries = np.linspace(0, total_duration, len(words_list) + 1)
    
    # Create word timings
    word_timings = []
    for i, word in enumerate(words_list):
        if i < len(boundaries) - 1:
            start_time = boundaries[i]
            end_time = boundaries[i + 1]
            duration = end_time - start_time
            
            word_timings.append({
                "word": word,
                "start_time": round(start_time*1000+start),
                "duration": round(duration*1000)
            })
    
    return word_timings

def main():
    audio_file = "your_music_file.mp3"  # Replace with actual path to audio file
    words_list = ["hello", "world", "this", "is", "a", "test"]  # Replace with actual words
    
    print("Extracting word timings from audio...")
    word_timings = extract_word_timings(audio_file, words_list)
    
    # Print the word timings
    print("\nEstimated Word Timings:")
    for word_info in word_timings:
        print(f"Word: {word_info['word']}, Start: {word_info['start_time']:.2f}s, Duration: {word_info['duration']:.2f}s")
    
    # Export timing data to CSV
    df = pd.DataFrame(word_timings)
    df.to_csv('word_timings.csv', index=False)
    print("\nWord timings exported to 'word_timings.csv'")

def forced_alignment(vocals_mp3, start, end, words):
    # start is in ms, convert to seconds
    start_sec = start / 1000.0
    end_sec = end / 1000.0

    y, sr = librosa.load(vocals_mp3)
    y = y[floor(start_sec*sr):ceil(end_sec*sr)]  # Trim the audio to the specified segment
    
    return extract_word_timings(y, sr, words, start)


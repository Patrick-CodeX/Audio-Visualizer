import pygame
import numpy as np
import wave
import random
import tkinter as tk
from tkinter import filedialog, simpledialog

# Initialize Pygame
pygame.init()

def choose_color_palette():
    """Open a Tkinter dialog to choose a color palette."""
    root = tk.Tk()
    root.withdraw()
    # Define color palettes
    color_palettes = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Default"]
    # Prompt user for color palette choice
    choice = simpledialog.askstring("Color Palette", "Choose a color palette: Red, Orange, Yellow, Green, Blue, Purple, Pink, or Default")
    if choice is None or choice.lower() not in [palette.lower() for palette in color_palettes]:
        choice = "Default"  # Default color palette if the choice is invalid or None
    root.destroy()
    return choice

def set_colors(color_palette_type):
    """Set color variables based on the chosen color palette."""
    if color_palette_type.lower() == "red":
        return (random.randint(230, 255), random.randint(0, 30), random.randint(0, 50)), \
               (random.randint(180, 200), random.randint(70, 90), random.randint(0, 10)), \
               (random.randint(0, 150), random.randint(0, 30), random.randint(0, 50))
    elif color_palette_type.lower() == "orange":
        return (random.randint(230, 255), random.randint(80, 100), random.randint(0, 10)), \
               (random.randint(200, 255), random.randint(80, 120), random.randint(0, 50)), \
               (random.randint(230, 255), random.randint(100, 120), random.randint(20, 50))
    elif color_palette_type.lower() == "yellow":
        return (random.randint(200, 255), random.randint(200, 255), random.randint(0, 20)), \
               (random.randint(200, 255), random.randint(200, 255), random.randint(0, 20)), \
               (random.randint(200, 255), random.randint(200, 255), random.randint(0, 20))
    elif color_palette_type.lower() == "green":
        return (random.randint(0, 10), random.randint(180, 255), random.randint(0, 30)), \
               (random.randint(0, 10), random.randint(180, 255), random.randint(0, 30)), \
               (random.randint(0, 10), random.randint(180, 255), random.randint(0, 30))
    elif color_palette_type.lower() == "blue":
        return (random.randint(0, 20), random.randint(200, 230), random.randint(230, 255)), \
               (random.randint(0, 30), random.randint(0, 50), random.randint(200, 255)), \
               (random.randint(0, 30), random.randint(0, 50), random.randint(200, 255))
    elif color_palette_type.lower() == "purple":
        return (random.randint(100, 150), random.randint(0, 20), random.randint(200, 255)), \
               (random.randint(100, 150), random.randint(0, 20), random.randint(200, 255)), \
               (random.randint(0, 80), random.randint(0, 20), random.randint(200, 255))
    elif color_palette_type.lower() == "pink":
        return (random.randint(120, 170), random.randint(0, 20), random.randint(200, 255)), \
               (random.randint(230, 255), random.randint(0, 20), random.randint(230, 255)), \
               (random.randint(230, 255), random.randint(0, 20), random.randint(230, 255))
    else:
        # Default colors (red, yellow, green)
        return (255, 0, 0), (255, 255, 0), (0, 255, 0)

# Constants
WIDTH, HEIGHT = 800, 600  # Default window size
FPS = 24
CHUNK = 3000

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Audio Visualizer')

def load_audio(file_path):
    """Load an audio file."""
    global wf
    wf = wave.open(file_path, 'rb')
    pygame.mixer.init(frequency=wf.getframerate())
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def get_audio_data():
    """Capture audio data from the WAV file and return its FFT values."""
    data = wf.readframes(CHUNK)
    if len(data) == 0:
        return np.zeros(CHUNK // 2), True

    audio_data = np.frombuffer(data, dtype=np.int16)
    fft = np.abs(np.fft.fft(audio_data))[:CHUNK // 2]
    return fft, False

def draw_bars(fft, width, height):
    """Draw bars that move based on the FFT data."""
    screen.fill((0, 0, 0))
    
    num_bars = width // 10  # Adjust number of bars based on screen width
    bar_width = width // num_bars

    bar_heights = np.interp(fft[:num_bars], (0, np.max(fft)), (0, height))
    
    for i in range(num_bars):
        if i % 3 == 0:
            color = Rcolor1
        elif i % 3 == 1:
            color = Rcolor2
        else:
            color = Rcolor3
        
        pygame.draw.rect(screen, color, (i * bar_width, height - bar_heights[i], bar_width - 2, bar_heights[i]))

    pygame.display.flip()

def select_file():
    """Open a file dialog to select an audio file."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    return file_path

def main():
    global screen, WIDTH, HEIGHT, Rcolor1, Rcolor2, Rcolor3
    
    color_palette = choose_color_palette()
    Rcolor1, Rcolor2, Rcolor3 = set_colors(color_palette)
    
    clock = pygame.time.Clock()
    running = True
    
    audio_file = select_file()
    if not audio_file:
        print("No file selected. Exiting.")
        pygame.quit()
        return
    
    load_audio(audio_file)
    
    fullscreen = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Toggle full-screen mode
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.RESIZABLE)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resizing
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        
        fft, audio_finished = get_audio_data()
        draw_bars(fft, WIDTH, HEIGHT)
        
        if audio_finished:
            wf.close()
            audio_file = select_file()
            if audio_file:
                load_audio(audio_file)
            else:
                running = False
        
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()

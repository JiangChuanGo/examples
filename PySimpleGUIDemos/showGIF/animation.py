import PySimpleGUI as sg

from PIL import Image

filename = "./dots_wave.gif"

gif_file = Image.open(filename)

size = gif_file.size

del gif_file

layout = [
        [sg.Button("Play"), sg.Button("Stop"), sg.Quit()],
        [sg.Image(filename, key = "-GIF-", size = size, background_color = "white")]
]


window = sg.Window("GIF", layout = layout, finalize = True)

# find Image element so that we can use it in the event loop
img = window["-GIF-"]

# default paused
play = False

while True:
    event, values = window.read(timeout = 10, timeout_key = "-TIMEOUT-")

    # way to quit
    if event in (sg.WIN_CLOSED, "Quit", "Cancel"):
        break

    # play and stop button
    if event == "Play":
        play = True

    if event == "Stop":
        play = False


    if play:
        img.UpdateAnimation(filename, time_between_frames=50)


window.close()
del window

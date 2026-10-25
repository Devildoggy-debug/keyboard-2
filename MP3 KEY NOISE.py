import board
import keypad
import digitalio
import audiopwmio
import audiomp3

Notes= ["C", "C#", "D", "D#", "E", "F",
              "F#", "G", "G#", "A", "A#", "B"]
Octave_Uno=1
Octave_numero=7

Note_Fls= []
for o in range(Octave_Uno, Octave_Uno + Octave_numero):
    for name in Notes:
        Note_Fls.append("/samples/{}{}.mp3".format(name, o))

Keyboard=list(range(49))

First_note=24
octave= 0   # 0 = home, +1 = one octave up, -1 = one octave down
def shifted_index(key_number):
    """Which file index a key plays at the current octave."""
    return First_note + Keyboard[key_number] + 12 * octave
def octave_is_valid(new_octave):
    """True only if every key still has a file after the shift."""
    lo = First_note + min(Keyboard) + 12 * new_octave
    hi = First_note + max(Keyboard) + 12 * new_octave
    return lo >= 0 and hi < len(Note Fls)

Roww=(board.GP0, board.GP1, board.GP2, board.GP3,
            board.GP4, board.GP5, board.GP6)
Cols=(board.GP7, board.GP8, board.GP9, board.GP10,
            board.GP11, board.GP12, board.GP13)


keys= keypad.KeyMatrix(row_pins=Roww, column_pins=Cols,
                        columns_to_anodes=True)

def make_button(pin):
    b = digitalio.DigitalInOut(pin)
    b.switch_to_input(pull=digitalio.Pull.UP)
    return b

Octup=make_button(board.GP16)
Octdown = make_button(board.GP19)
up_prev =down_prev = True
audio = audiopwmio.PWMAudioOut(left_channel=board.GP14,
                               right_channel=board.GP15)
decoder= None
def Noise(path):
    global decoder
    audio.stop()
    try:
        if decoder is None:
            decoder = audiomp3.MP3Decoder(open(path, "rb"))
        else:
            decoder.file.close()
            decoder.file = open(path, "rb")
        audio.play(decoder)
    except OSError:
        print("Missing file:", path)
while True:

    event=keys.events.get()
    if event and event.pressed:
        index =shifted_index(event.key_number)
        path =Note_Fls[index]
        print("Key", event.key_number + 1, "->", path)
        Noise(path)
    up = Octup.value
    down = Octdown.value
    if not up and up_prev and octave_is_valid(octave + 1):
        octave += 1
        print("Octave", octave)
    if not down and down_prev and octave_is_valid(octave - 1):
        octave -= 1
        print("Octave", octave)

    up_prev,down_prev =up,down

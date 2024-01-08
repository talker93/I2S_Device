#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import tempfile
import queue
import sys
import socket

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf

import segmentationtools as st
import scipy.io as spio

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1

# q for plotting, q_rec for recording, q_IPC for IPC
q = queue.Queue()
q_rec = queue.Queue()
q_IPC = queue.Queue()

write_flag = False
last_flag = False
# make sure this size changed with the block size
np_zero_arr = np.zeros((512, 1))
num_frame_wrote = 0
# 10 frames -> 10 / fs seconds
tracking_window_length = 200
flag = st.Segment()
# read the test signal
with open('CNN_test_good_long.txt') as f:
    sig = [float(line.rstrip()) for line in f]
num_frame_read = 0
mode = "real"


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    global write_flag
    global last_flag
    global num_frame_wrote
    global num_frame_read

    # global file_peak_segment
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])
    q_rec.put(indata.copy())
    q_IPC.put(indata.copy())

    if mode == "test":
        # in test mode: read from the test signal
        sig_block = sig[num_frame_read*frames:(num_frame_read+1)*frames]

        # Repeatedly read and check with Segment.run()
        N = round(len(sig_block) / tracking_window_length)

        # skip when test signal is over
        if N > 1:
            np_arr = np.zeros((tracking_window_length, N-1))
            for i in range(N-1):
                np_arr[:, i] = sig_block[i*tracking_window_length:(i+1)*tracking_window_length]
                flag.run(np_arr[:, i])
                if flag.status is flag.status_flags.ACTIVATED:
                    print("ACTIVATED")
                    print(num_frame_read)
                    break
            if flag.status is flag.status_flags.ACTIVATED:
                write_flag = True
            elif (flag.status is flag.status_flags.IDLE) or (flag.status is flag.status_flags.INITIALIZING):
                write_flag = False

        # Writing
        if write_flag:
            # write the processed file, .wav
            file_peak.write(sig_block)

            # write the segment file, .txt
            # optionally we can save to .mat but seems isn't good for stream output
            # remove the first and last bracket
            sig_block_shorter = str(sig_block)
            sig_block_shorter = sig_block_shorter.replace("\n", ",")
            sig_block_shorter = sig_block_shorter.replace('[', '')
            sig_block_shorter = sig_block_shorter.replace(']', '')
            file_peak_segment.write(sig_block_shorter)

            last_flag = True
            num_frame_wrote += 1
        else:
            file_peak.write(np_zero_arr)
            # enter this case when write_flag status flipped
            if last_flag != write_flag:
                # line break marks a new segment
                file_peak_segment.write("\n")
                last_flag = False

    if mode == "real":
        # in real mode: read from the microphone
        sig_block = indata.copy()
        sig_block = sig_block[:, 0]

        # 1. Attacking
        N = round(len(sig_block) / tracking_window_length)
        np_arr = np.zeros((tracking_window_length, N-1))
        rms = np.zeros(N-1)
        flag_high = np.zeros(N-1)
        flag_low = np.zeros(N-1)
        for i in range(N-1):
            np_arr[:, i] = sig_block[i*tracking_window_length:(i+1)*tracking_window_length]
            rms[i] = np.sqrt(np.mean(np_arr[:, i] ** 2))
        # raise the flag when the rms is high
        flag_high = rms > 0.15
        flag_low = rms < 0.01
        print("flag_high: ", flag_high)
        print("flag_low: ", flag_low)
        if flag_high.any():
            write_flag = True

        # 2. Release
        # lift the flag only when the rms is low for 5 frames
        elif flag_low.all and (num_frame_wrote > 20):
            write_flag = False

        # 3. Writing
        if write_flag:
            # write the processed file, .wav
            file_peak.write(sig_block)

            # write the segment file, .txt
            # remove the first and last bracket
            str_shorter = str(sig_block)
            str_shorter = str_shorter.replace("\n", " ")
            str_shorter = str_shorter.replace('[', '')
            str_shorter = str_shorter.replace(']', ' ')
            file_peak_segment.write(str_shorter)
            print("str_shorter: ", str_shorter)

            last_flag = True
            num_frame_wrote += 1
        else:
            file_peak.write(np_zero_arr)
            # enter this case when write_flag status flipped
            if last_flag != write_flag:
                file_peak_segment.write("\n")
                last_flag = False
                # reset the release counter
                num_frame_wrote = 0

    num_frame_read += 1


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']
    if args.filename is None:
        args.filename = tempfile.mktemp(prefix='test_feb_24',
                                        suffix='.wav', dir='')

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend([f'channel {c}' for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    # open the file for writing
    file = sf.SoundFile(args.filename, mode='x', samplerate=int(args.samplerate),
                        channels=len(args.channels), subtype=args.subtype)

    # open the file for peak writing
    file_peak = sf.SoundFile("peak_"+args.filename, mode='x', samplerate=int(args.samplerate),
                             channels=len(args.channels), subtype=args.subtype)

    # open the file for peak writing with segmentation
    str_filename = str(args.filename)
    str_filename = str_filename.replace(".wav", "")
    file_peak_segment = open("peak_segment_" + str_filename + ".txt", "a")

    # init the audio stream reading
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)

    # tcp setup
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(("127.0.0.1", 1234))
    # sock.sendall(b"Hello, world1")

    with stream:
        plt.show()
        print('#' * 80)
        print('press Return to quit')
        print('#' * 80)
        while True:
            file.write(q_rec.get())
            # sock.send(q_IPC.get())
            # print(str(q_IPC.get()))

except KeyboardInterrupt:
    file_peak_segment.close()
    print('\nRecording finished: ' + repr(args.filename))
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

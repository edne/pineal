from threading import Thread
from time import sleep
import pyaudio
import numpy as np


audio_data = None


def get_audio_data():
    if audio_data is None:
        raise Exception('Listener not initialized')
    else:
        return audio_data


def get_devices(pa):
    "{name: id, ...}"
    def get_name(dev_id):
        return pa.get_device_info_by_index(dev_id).get('name')

    return {get_name(dev_id): dev_id
            for dev_id in range(pa.get_device_count())}


def listen(device='default', channels=2, frames_per_buffer=1024, rate=44100):
    global audio_data
    audio_data = np.zeros([channels, frames_per_buffer])

    pa = pyaudio.PyAudio()
    devices = get_devices(pa)
    # print(devices)
    input_device = devices[device]

    def stream_cb(in_data, frame_count, time_info, status):
        data = np.fromstring(in_data, dtype=np.float32)
        data = np.reshape(data, (frame_count, channels))
        data = [data[:, i]
                for i in range(channels)]

        audio_data[:, :] = data

        return (in_data, pyaudio.paContinue)

    stream = pa.open(format=pyaudio.paFloat32,
                     channels=channels,
                     rate=rate,
                     frames_per_buffer=frames_per_buffer,
                     input=True,
                     input_device_index=input_device,
                     stream_callback=stream_cb)

    def idle():
        stream.start_stream()

        try:
            while True:
                sleep(1)
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()

    t = Thread(target=idle)
    t.daemon = True
    t.start()

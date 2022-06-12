import pyaudio
import time, struct, math, wave

#Assuming Energy threshold upper than 10 dB
Threshold = 20

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 1

class Recorder:
    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        if __name__ == 'main':
            print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + 5
        original_end = end

        while current <= end:
            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: 
                end = time.time() + TIMEOUT_LENGTH
            current = time.time()
            rec.append(data)
        if original_end != end:
            return self.write(b''.join(rec))
        else:
            return ''

    def write(self, recording):
        # save and send audio to be transcribed
        filename = 'jarvis\\files\\data\\current_audio.wav'
        wf = wave.open(filename, 'w')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        if __name__ == 'main':
            print('Written to file: {}'.format(filename))
        return filename
        """
        fs=44100 # frequency
        duration = 5 # seconds
        #save the recording
        myrecording = sd.rec(duration * fs, samplerate = fs, channels = 2, dtype = 'float64')
        print("Recording Audio")
        #wait for the audio to record
        sd.wait()
        
        sf.write(filename, myrecording, fs)
        return filename"""

    def listen(self):
        if __name__ == 'main':
            print('Listening beginning')
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                return self.record()

    
        

if __name__ == '__main__':
    """file = record_audio(5)
    print('recording created: ' + file )"""
    a = Recorder()
    a.listen()
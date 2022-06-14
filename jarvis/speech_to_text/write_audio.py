import speech_recognition as sr
from datetime import datetime


def get_file_date():
    return [(datetime.now()).strftime('%Y-%m-%d'), (datetime.now()).strftime('%H:%M:%S')]

# initialize recognizer
r = sr.Recognizer()

def interpret_audio(filename):
    if filename == '':
        return 'no audio to transcribe...'
    # open file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
        except:
            return 'no audio to transcribe...'
        # print for debugging and display interpretation
        return text + ' '

def write_audio_to_txt(text):
    # set filename to date for logging purposes
    date = get_file_date()
    archived_filename = 'jarvis\\files\\data\\tanscribed_recording.txt'.format(date[0],date[1])
    filename = 'jarvis\\files\\data\\current_phrase.txt'
    with open(filename, 'w') as f:
        f.write(text)
    if text != 'no audio to transcribe...':
        with open(archived_filename, 'a') as f:
            f.write('\nAudio Recorded: {} - {}:\n'.format(date[0],date[1]) + text + '\n')

if __name__ == '__main__':
    # set filename to default audio file
    filename = 'jarvis\\files\\test\\untitled.wav'
    write_audio_to_txt(interpret_audio(filename))
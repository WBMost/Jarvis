import speech_to_text.record_audio as ra
import speech_to_text.write_audio as wa
import interpreter.interpreter as i
import time

ear = ra.Recorder()
brain = i.Interpreter()
print('Jarvis is awake and listening...')
while True:
    ear.timeout_length = 1
    #listen and transcribe what was heard
    text = wa.interpret_audio(ear.listen()).lower()
    # trigger is supposed to be jarvis but would mishear a lot
    trigger_words = ['jarvis ', 'arvest ', 'service ', 'gervaise ', 'purvis ', 'orvis ', 'harvest ']
    
    # check if trigger word was stated 
    # TODO: make a better check for trigger word
    if text in trigger_words:
        # set conversation as open waiting for command
        brain.open = 1
        # indicate to user trigger was heard
        print('yes, sir?')
        
        # based on what type of open the conversation is, listen with varying tolerences
        while brain.open >= 1:
            # basic open
            if brain.open == 1:
                ear.timeout_length = 4
            # command with file, open
            else:
                ear.timeout_length = 8
            
            # listen for command
            wa.write_audio_to_txt(wa.interpret_audio(ear.record()))
            # read and interpret listened for command
            brain.read_file()

            # check if need to create wav file
            while brain.open == -1:
                # indicate to user starting to record .wav file
                if ear.current_rec == '':
                    print('Recording about to start for your .wav file, sir. ')
                else:
                    print('I am about to continue to recording for your .wav file, sir. ')
                # set silence tolerence to be higher
                ear.timeout_length = 15
                print('3')
                time.sleep(1)
                print('2')
                time.sleep(1)
                print('1')
                time.sleep(1)
                print('Recording...')
                # special record for .wav files
                ear.record_wav()
                # set file interaction of open
                print('Due to your silence the recording has been paused, would you like to coninue to record or save the file?')
                brain.open = 2
                wa.write_audio_to_txt(wa.interpret_audio(ear.record()))
                brain.read_file()

import speech_to_text.record_audio as ra
import speech_to_text.write_audio as wa
import interpreter.interpreter as i

ear = ra.Recorder()
brain = i.Interpreter()
print('Jarvis is awake and listening...')
while True:
    text = wa.interpret_audio(ear.listen()).lower()
    trigger_words = ['jarvis', 'arvest', 'service', 'gervaise', 'purvis', 'orvis', 'harvest']
    if text in trigger_words:
        brain.open = True
        print('yes, sir?')
        while brain.open:
            wa.write_audio_to_txt(wa.interpret_audio(ear.record()))
            brain.read_file()
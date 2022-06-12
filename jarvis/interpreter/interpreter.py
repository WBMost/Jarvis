import random

# input types
PHRASE_CLASSES = [
    'greeting',
    'question',
    'conversation',
    'command',
    'farewell'
]

# input key phrases
INPUT_PHRASES = {
    'greeting': [
        'hi',
        'hello',
        'greetings',
        'good morning',
        'good evening',
        'good afternoon',
        'howdy',
        'sup',
        'hiya',
        "What's up",
        'yo',
    ],
    'question':[

    ],
    'conversation':[
        'how are you',
        'how is it going',
    ],
    'command':[

    ],
    'farewell': [
        'bye',
        'goodbye',
        'see ya',
        'see you',
        'see you later',
        'talk to you later',
    ],
}

# Jarvis responses
GREETINGS = [
    'Hello, sir. What can I do for you?',
    'Greetings, sir. What can I do for you?',
]
FAREWELLS = [
    'Goodbye, sir',
    'Take care, sir',
    'Farewell, sir',
]
CONFIRMATIONS = [
    'Very well, sir',
    'Yes, sir',
]
CONFUSED = [
    'What was that, sir?',
    'Pardon?',
    'I did not quite understand.',
    'I do not think I understood, sir.',
    'Can you run that by me again, sir?',
]


class Interpreter:
    def __init__(self):
        self.input = ''
        self.input_type = ''
        self.response = ''
        self.open = True
    
    # read user input, interpret it, respond to it
    def read_file(self):
        # reset just in case
        self.open = True
        self.response = ''

        # check most recent input
        with open('jarvis\\files\\data\\current_phrase.txt', 'r') as f:
            self.input = f.read()

        # check if sent empty audio
        if self.input == 'no audio to transcribe...':
            # build response based on lack of input
            if self.input_type != 'greeting':
                self.response = 'Sorry. I had thought I heard something.'
            else:
                self.input_type = ''
            self.response = self.response + FAREWELLS[random.randrange(0, len(FAREWELLS))]
            # set conversation to closed
            self.open = False
        else:
            # interpret the input
            self.interpret()
            # create response to input
            self.respond()
        
        # say response
        print(self.response)
        # return if still open to listen to new input
        return(self.open)

    # interpret what type of input was given
    def interpret(self):
        # check if input was a greeting
        # TODO: add more precice responses "good evening", "good morning"
        self.input_type = ''
        for k,v in INPUT_PHRASES.items():
            for x in v:
                if x in self.input:
                    self.input_type = k
                    return


    # allow jarvis to respond
    def respond(self):
        # have every response be pulled base on input type
        # reset input type except for greeting so it can have a special message if no follow up input after a greeting
        if self.input_type == PHRASE_CLASSES[4]:
            self.open = False
            self.response = FAREWELLS[random.randrange(0, len(FAREWELLS))]
        elif self.input_type == PHRASE_CLASSES[0]:
            self.open = True
            self.response = GREETINGS[random.randrange(0, len(GREETINGS))]
        else:
            self.open = True
            self.response = CONFUSED[random.randrange(0, len(CONFUSED))]
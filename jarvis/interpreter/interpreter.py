import random
from datetime import datetime

# input types
PHRASE_CLASSES = [
    'greeting',
    'question',
    'confirmation',
    'refute',
    'conversation',
    'question',
    'command',
    'farewell'
]

# input key phrases
INPUT_PHRASES = {
    'refute': [
        'no',
        'no thanks',
        'no thank you',
        'negative',
        "don't",
        'do not',
    ],
    'farewell': [
        'bye',
        'goodbye',
        'see ya',
        'see you',
        'see you later',
        'talk to you later',
    ],
    'greeting': [
        'hi',
        'hey',
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
    'conversation':[
        'how are you',
        'how is it going',
    ],
    'question':[
        'how',
        'where',
        'when',
        'who',
        'whom',
        'whose',
        'what',
        'which',
    ],
    'command':[
        'can you',
        'please',
        'create',
        'make',
        'read',
        'write',
        'delete',
        'open',
        'search',
    ],
}

COMMANDS = {
    'create': [
        'create',
        'make',
    ],
    'alter': [
        'read',
        'write',
        'delete',
        'open',
    ],
    'find': [
        'search for',
    ]
}
# key commands for file creations
CREATE = {
    'name': [
        'called ',
        'named ',
    ],
    'file':{
            'python': '.py',
            'wave': '.wav',
            'text': '.txt',
    },
}



# file creation parameters
creation_params = {
    'filename': 'file',
    'file_path': 'C:\\Users\\wyatt\\Desktop\\',# update for default based on actual user...
    'file_ext': '.txt',
    'content': 'file created by jarvis'
}

# Jarvis responses
GREETINGS = [
    'Hello, sir. ',
    'Greetings, sir. ',
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
        self.input_type = []
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
        # check if was sent empty audio
        if self.input == 'no audio to transcribe...':
            # build response based on lack of input
            if self.input_type != 'greeting':
                self.response = 'Sorry. I thought I had heard something.'
            else:
                self.input_type = ''
            time = datetime.now()
            hour = time.hour
            if hour < 4:
                farewell = 'Goodnight, sir.'
            else:
                farewell = FAREWELLS[random.randrange(0, len(FAREWELLS))]
            if self.response != '':
                self.response = self.response + ' ' + farewell
            else:
                self.response = farewell
            # set conversation to closed
            self.open = False
        else:
            # interpret the input while building response
            self.interpret()
        # say response
        print(self.response)
        # return if still open to listen to new input
        return(self.open)

    # interpret what type of input was given
    def interpret(self):
        # check if input was a greeting
        self.input_type = ''
        # sift through input to decipcher it and build response based around decipher
        for k,v in INPUT_PHRASES.items():
            for x in v:
                if x in self.input:
                    # checks if input contained a greeting to add a greeting to response
                    if k == 'greeting':
                        if 'good' in x:
                            time = datetime.now()
                            hour = time.hour
                            mins = str(time.minute)
                            if hour > 4 and hour < 12:
                                if 'morning' not in x:
                                    self.build_response('It is actually morning, sir. {} a m. Good morning. '.format(str(hour) + ':' + mins))
                                else:
                                    self.build_response('Good morning, sir. ')
                            elif hour >= 12 and hour < 18:
                                if 'afternoon' not in x:
                                    self.build_response('It is actually afternoon, sir. {} p m. Good afternoon. '.format(str(hour) + ':' + mins))
                                else:
                                    self.build_response('Good afternoon, sir. ')
                            elif hour >= 18 and hour <= 23:
                                if 'evening' not in x:
                                    self.build_response('It is actually evening, sir. {} p m. Good evening. '.format(str(hour) + ':' + mins))
                                else:
                                    self.build_response('Good evening, sir. ')
                            elif hour >= 0:
                                self.build_response('It is late at night, sir. {} p m. You should probably get to bed soon. So, goodnight, sir.'.format(str(hour) + ':' + mins))
                                self.open = False
                                return
                        else:
                            self.build_response(GREETINGS[random.randrange(0,len(GREETINGS))])

                        if self.input == x:
                            self.input_type = k
                            self.build_response('What can I do for you?')
                            return
                        break
                    
                    # checks if input contained a command and will follow through with command
                    elif k == 'command':
                        # adds command to input type list
                        for command_key,command_v in COMMANDS.items():
                            for i in command_v:
                                if i in self.input:
                                    if i == 'create':
                                        if 'file' not in self.input:
                                            self.build_response(CONFUSED[random.randrange(0,len(CONFUSED))])
                                            return
                                        # self.input_type.append(command_key)
                                        params = creation_params
                                        for create_key, create_v in CREATE.items():
                                            # check if need to change default file params
                                            for c in create_v:
                                                if c in self.input:
                                                    # check to change file type
                                                    if c in CREATE['file']:
                                                        params['file_ext'] = CREATE['file'][c]

                                                    # check to change file name
                                                    if c in CREATE['name']:
                                                        # grab filename
                                                        name = self.find_between(c , " ")
                                                        # if last thing stated was the name, it returns nothing so fix that
                                                        if name == '':
                                                            name = self.find_between(c , self.input[len(self.input)-1])
                                                            name = name + self.input[len(self.input)-1]
                                                        params['filename'] = '' + name
                                        # possible confirmation checks for file creation
                                        # if params != CREATION_PARAMS:
                                        #     self.build_response('Just to confirm, you want me to make the file {} at {}?'.format((params['filename']+'.'+params['file_ext']), params['path']))
                                        # else:
                                        #     self.build_response('Just to confirm, you want me to create a default file?')
                                        self.create_file(params)
                                        return
                    elif k == 'farewell':
                        # keep for possible future implementation
                        # if self.input == x:
                        #     self.input_type = k
                        #     return
                        self.build_response(FAREWELLS[random.randrange(0,len(FAREWELLS))])
                        return
                    elif k == 'refute':
                        self.build_response('Very well. ' + FAREWELLS[random.randrange(0,len(FAREWELLS))])
                        return
                        

    # create file
    def create_file(self, params):
        filename = '' + params['filename'] + params['file_ext']
        file_path = '' + params['file_path']
        try:
            with open(file_path+filename, 'w') as f:
                f.write(params['content'])
            self.build_response('I have successfully created {}{} at {}. '.format(params['filename'],params['file_ext'],params['file_path']))
            self.build_response('Anything else I can do for you, sir?')
        except:
            self.open = False
            self.build_response('I could not create the file {}{}. Sorry, sir.'.format(params['filename'],params['files_ext']))

    # allow jarvis to build a response
    def build_response(self, string):
        # have every response be pulled base on input type
        self.response = self.response + string



    # extra stuffs
    def find_between(self, first, last):
        try:
            start = self.input.index( first ) + len( first )
            end = self.input.index( last, start )
            return self.input[start:end]
        except ValueError:
            return ""
    def find_between_r(self, first, last):
        try:
            start = self.input.index( first ) + len( first )
            end = self.input.index( last, start )
            return self.input[start:end]
        except ValueError:
            return ""
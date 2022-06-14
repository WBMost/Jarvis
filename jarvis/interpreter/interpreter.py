import os
import random
from datetime import datetime

# ---- OPEN_KEY ----
# -2 = tell ears to save wav recording
# -1 = open recording for longer
#  0 = conversation closed
#  1 = basic recieving input
#  2 = alter file
#  3 = confirm file creation

USER_PATH = os.path.expanduser('~')
print(USER_PATH)
# input key phrases
INPUT_PHRASES = {
    'refute': [
        'no ',
        'no thanks ',
        'no thank you ',
        'negative ',
        "don't ",
        'do not ',
    ],
    'farewell': [
        'bye ',
        'goodbye ',
        'see ya ',
        'see you ',
        'see you later ',
        'talk to you later ',
    ],
    'greeting': [
        'hi ',
        'hey ',
        'hello ',
        'greetings ',
        'good morning ',
        'good evening ',
        'good afternoon ',
        'howdy ',
        'sup ',
        'hiya ',
        "What's up ",
    ],
    'conversation':[
        'how are you ',
        'how is it going ',
    ],
    'question':[
        'how ',
        'where ',
        'when ',
        'who ',
        'whom ',
        'whose ',
        'what ',
        'which ',
    ],
    'command':[
        # decipher that its a request
        'can you ',
        'please ',
        'would you be able to ',
        # file creation
        'create ',
        'generate ',
        'produce ',
        'fabricate ',
        'make ',
        # append file
        'write ',
        'put down ',
        'note ',
        'jot down ',
        'make a note of ',
        # delete file
        'delete ',
        'remove ',
        'cut out ',
        'expunge ',
        'strike out ',
        # inspect/read file
        'read ',
        'open ',
        'inspect ',
        'look into ',
        'look in to ',
        # search for file
        'discover ',
        'track down ',
        'pin point ',
        'detect '
        'search for ',
        'search ',
        'locate ',
        'find ',
    ],
}

COMMANDS = {
    'create': [
        'create ',
        'make ',
        'generate ',
        'produce ',
        'fabricate ',
    ],
    'append': [
        'write ',
        'put down ',
        'note ',
        'jot down ',
        'make a note of ',
    ],
    'delete': [
        'delete ',
        'remove ',
        'cut out ',
        'expunge ',
        'strike out ',
    ],
    'inspect': [
        'read ',
        'open ',
        'inspect ',
        'look into ',
        'look in to ',
    ],
    'find': [
        'discover ',
        'track down ',
        'pin point ',
        'detect '
        'search for ',
        'search ',
        'locate ',
        'find ',
    ]
}
# key commands for file creations
FILE = {
    'name': [
        'called ',
        'named ',
    ],
    'file':{
        'python ': '.py',
        'wave ': '.wav',
        'text ': '.txt',
    },
    #check actually means for path instad ('in ', 'on ', 'to ', 'into ', 'in the ', 'on the ', 'to the ', 'into the ')
    'path':{
        'preposition': [
            'in ',
            'on ',
            'to ',
            'into ',
            'in my ',
            'on my ',
            'to my ',
            'into my',
            'in the ',
            'on the ',
            'to the ',
            'into the ',
        ],
        # desktop pathing
        'desktop': USER_PATH + '\\Desktop\\',
        # document pathing
        'documents': USER_PATH + '\\Documents\\',
        # download pathing
        'downloads': USER_PATH + '\\Doownloads\\',
        'download': USER_PATH + '\\Doownloads\\',
        # pictures pathing
        'pictures': USER_PATH + '\\Pictures\\',
        'picture': USER_PATH + '\\Pictures\\',
        'images': USER_PATH + '\\Pictures\\', # probably build an ask for confimation
        'image': USER_PATH + '\\Pictures\\', # probably build an ask for confimation
        # videos pathing
        'videos': USER_PATH + '\\Videos\\',
        'video': USER_PATH + '\\Videos\\',
        'movies': USER_PATH + '\\Videos\\', # probably build an ask for confimation
    },
}



# file creation parameters
creation_params = {
    'filename': 'file',
    'file_path': USER_PATH + '\\Desktop', # default path to desktop...
    'file_ext': '.txt',
    'content': 'file created by jarvis',
}

# Jarvis responses
GREETINGS = [
    'Hello, sir. ',
    'Greetings, sir. ',
]
FAREWELLS = [
    'Goodbye, sir. ',
    'Take care, sir. ',
    'Farewell, sir. ',
]
CONFIRMATIONS = [
    'Very well, sir. ',
    'Yes, sir. ',
]
CONFUSED = [
    'What was that, sir? ',
    'Pardon? ',
    'I did not quite understand. ',
    'I do not think I understood, sir. ',
    'Can you run that by me again, sir? ',
]


class Interpreter:
    def __init__(self):
        self.input = ''
        self.input_type = []
        self.response = ''
        self.open = 1
        self.file = creation_params['filename']
        # stores active file information 
        self.current_active_file = {
            'filename': '',
            'file_path': '',
            'file_ext': '',
            'content': '',
        }
    
    # read user input, interpret it, respond to it
    def read_file(self):
        # reset just in case
        self.response = ''
        # check most recent input
        with open('jarvis\\files\\data\\current_phrase.txt', 'r') as f:
            self.input = f.read()
        
        # check if was sent empty audio
        if self.input == 'no audio to transcribe...':
            # build response based on lack of input
            if self.open == 2:
                self.response = 'Sorry, I could not hear if you said anything. To play things safe, I save your current file.'


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
            self.open = 0
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
                                    self.build_response('It is currently {} a m. Good morning, sir. '.format(str(hour) + ':' + mins))
                                else:
                                    self.build_response('Good morning, sir. ')
                            elif hour >= 12 and hour < 18:
                                if 'afternoon' not in x:
                                    self.build_response('It is currently {} p m. Good afternoon, sir. '.format(str(hour) + ':' + mins))
                                else:
                                    self.build_response('Good afternoon, sir. ')
                            elif hour >= 18 and hour <= 23:
                                if 'evening' not in x:
                                    self.build_response('It is currently {} p m. Good evening, sir. '.format(str(hour) + ':' + mins))
                                else:
                                    self.build_response('Good evening, sir. ')
                            elif hour >= 0:
                                self.build_response('It is currently {} a m. Might I suggest you get some sleep soon, sir.'.format(str(hour) + ':' + mins))
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

                                    # check if command revolved around file creation
                                    if (True if i == l else False for l in COMMANDS['create']):# create
                                        if 'file' not in self.input:
                                            self.build_response(CONFUSED[random.randrange(0,len(CONFUSED))])
                                            return
                                        # self.input_type.append(command_key)
                                        params = creation_params
                                        for create_key, create_v in FILE.items():
                                            # check if need to change default file params
                                            for c in create_v:
                                                if c in self.input:
                                                    # check to change file type
                                                    if c in FILE['file']:
                                                        params['file_ext'] = FILE['file'][c]
                                                        if params['file_ext'] == '.py':
                                                            params['content'] = 'print("Hello, World! From, Jarvis.")'
                                                        elif params['file_ext'] == '.txt':
                                                            params['content'] = 'This file was created by Jarvis'
                                                        elif params['file_ext'] == '.wav':
                                                            params['content'] = 'This file was created by Jarvis'
                                                            self.open = -1
                                                    # check to change file name
                                                    if c in FILE['name']:
                                                        # grab filename
                                                        name = self.find_between(c , " ")
                                                        # if last thing stated was the name, it returns nothing so fix that
                                                        if name == '':
                                                            name = self.find_between(c , self.input[len(self.input)-1])
                                                            name = name + self.input[len(self.input)-1]
                                                        params['filename'] = '' + name
                                                    if c in FILE['path']:
                                                        # has to assemble possible phrases to allocate file path
                                                        for prep in FILE['path']['preposition']:
                                                            if prep + c in self.input:
                                                                params['file_path'] = str(FILE['path'][c])
                                                                break
                                                        
                                        # possible confirmation checks for file creation
                                        # if params != CREATION_PARAMS:
                                        #     self.build_response('Just to confirm, you want me to make the file {} at {}?'.format((params['filename']+'.'+params['file_ext']), params['path']))
                                        # else:
                                        #     self.build_response('Just to confirm, you want me to create a default file?')
                                        self.create_file(params)
                                        return
                                    
                                    # check if command involves altering a file
                                    if (True if i == l else False for l in COMMANDS['alter']):
                                        if 'file' not in self.input:
                                            self.build_response(CONFUSED[random.randrange(0,len(CONFUSED))])
                                            return
                                        params = creation_params
                                        for create_key, create_v in FILE.items():
                                            # check if need to change default file params
                                            for c in create_v:
                                                if c in self.input:
                                                    # check to change file type
                                                    if c in FILE['file']:
                                                        params['file_ext'] = FILE['file'][c]
                                                        if c == 'python ':
                                                            params['content'] = 'print("Hello, World! From, Jarvis.")'

                                                    # check to change file name
                                                    if c in FILE['name']:
                                                        # grab filename
                                                        name = self.find_between(c , " ")
                                                        # if last thing stated was the name, it returns nothing so fix that
                                                        if name == '':
                                                            name = self.find_between(c , self.input[len(self.input)-1])
                                                            name = name + self.input[len(self.input)-1]
                                                        params['filename'] = '' + name
                                    if (True if i == l else False for l in COMMANDS['find']):
                                        if 'file' not in self.input:
                                            self.build_response(CONFUSED[random.randrange(0,len(CONFUSED))])
                                            return
                    elif k == 'farewell':
                        # keep for possible future implementation
                        # if self.input == x:
                        #     self.input_type = k
                        #     return
                        self.build_response(FAREWELLS[random.randrange(0,len(FAREWELLS))])
                        self.open = 0
                        return
                    elif k == 'refute':
                        self.build_response('Very well. What else can I do for you?')
                        return
        self.build_response(CONFUSED[random.randrange(0,len(CONFUSED))])
                        

    # create file
    def create_file(self, params):
        filename = '' + params['filename'] + params['file_ext']
        file_path = '' + params['file_path']
        try:
            with open(file_path+filename, 'w') as f:
                f.write(params['content'])
            self.build_response('I have successfully created {} at {}. '.format(filename, file_path))
            self.build_response('Anything else I can do for you, sir?')
        except:
            self.open = 0
            self.build_response('I could not create the file {}{}. Sorry, sir.'.format(filename, file_path))

    def save_file(self):
        filename = '' + self.current_active_file['filename'] + self.current_active_file['file_ext']
        file_path = '' + self.current_active_file['file_path']
        try:
            # if current file was a .wav, let ears handle it
            if self.current_active_file['file_ext'] == '.wav':
                self.open = -2
                return
            # append to file rather than overwrite
            with open(file_path+filename, 'a') as f:
                f.write(self.current_active_file['content'])
            self.build_response('I have successfully altered {} at {}. '.format(filename,file_path))
            self.build_response('Anything else I can do for you, sir?')
        except:
            self.open = 0
            self.build_response('I could not create the file {}. Sorry, sir.'.format(filename))

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
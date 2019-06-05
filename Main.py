#Creator: James A. Scharf
#Date: 12/08/2018
#Goal: Create a command-line driven notetaking app.
#	Every note can be connected to some other as a node.
#	Making the whole application one big graph.

import pickle
import sys, tempfile, os
from subprocess import call
from termcolor import colored, cprint
from colorama import init
import datetime
import subprocess
from PIL import Image

init()






#TODO: Create a settings file that stores this information
username = "James A. Scharf"
user_set_editor = "nano"
initial_message = b"" # if you want to set up the file somehow

#TODO: create function to save all nodes' information to file

EDITOR = os.environ.get('EDITOR', user_set_editor) #that easy!


class Node:
    dateCreated = datetime.datetime.now()

    #name is the string value that we associate with it
    #Data is the thing that we're storing. Could be anything
    def __init__(self, new_name):
        self.name = new_name
        self.connections = set()
        self.edit()

    #Connection is a string name
    def removeConnection(self, connection):
        self.connections.remove(connection)
        self.save()

    #Connection is a string name
    def addConnection(self, connection):
        self.connections.add(connection)
        self.save()

    def getData(self):
        return self.data

    def getName(self):
        return self.name

    def getConnections(self):
        return self.connections

    #Open up and edit this file
    #really only works with strings
    def edit(self):
        #text type
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            tf.write(initial_message)
            tf.flush()
            call([EDITOR, tf.name])

            # do the parsing with `tf` using regular File operations.
            # for instance:
            tf.seek(0)

            #This is the string result of the session
            edited_message = tf.read()
            self.data = edited_message.decode("utf-8")
            self.save()

    #Save this node to a pickle file
    def save(self):
        filehandler = open(self.name + ".nd", 'wb')
        pickle.dump(self, filehandler)


#Now create the object that stores our relationships
nodes = dict()
#Each key is a string and each value is a node
#So to get a node's connections we just get the string, then node, and then its connections object
#So it's kind of an adjacency list

#Load up all of the pickle files and save them in nodes by name
def loadNodes():
    filenames = os.listdir()
    for f in filenames:
        if ".nd" in f:
            temp = pickle.load(open(f, "rb"))
            nodes[temp.getName()] = temp

def printNodeNames():
    loadNodes()
    for x in nodes:
        print(x)


#Create a new note
def createNewNote():
    print("Note name: ")
    name = input()
    print(colored("Note created. Opening external editor...", 'blue'))
    nodes[name] = Node(name)
    print("Type 'list' to see available connections.", end='')
    print("Or, list the names of other notes to connect to (space-deliminated): ", end='')
    given = input()
    if given == 'list':
        printNodeNames()
        print("Type 'list' to see available connections.", end='')
        print("Or, list the names of other notes to connect to (space-deliminated): ", end='')
        given = input()

    attempted_connections = given.split(" ")
    for a in attempted_connections:
        if a in nodes:
            nodes[name].addConnection(a)
        else:
            print("Invalid connection, ignoring: " + a)


def removeNote():
    print(colored("Enter name of node to remove: ", 'white'), end='')
    name = input()

    if name in nodes:
        del nodes[name]

    #remove pickle file
    if os.path.exists(name + ".nd"):
        os.remove(name + ".nd")


def graphToDot():
    loadNodes()
    #Output in DOT format
    result = "graph Notes {"
    for n in nodes:
        cons = nodes[n].getConnections()
        result = result + "\n   " + nodes[n].getName()
        for c in cons:
            result = result + "\n   " + nodes[n].getName() + " -- " + c
        result = result + ";"

    result = result + "\n}"
    #write to file
    f = open("graphView.dot", "w")
    f.write(result)
    return result

def viewDot():
    #Credit to https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
    bashCommand = "dot -Tjpg -Gdpi=800 graphView.dot -o outfile.jpg"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    print("y/n render as ascii? If not, see outfile.jpg")
    char = input()
    #if char == "y":
        #bashCommand = "fim -t outfile.jpg"
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #Output, error = process.communicate()
    #else:
        #img = Image.open('outfile.jpg')
        #img.show()


def displayNote(inp):
    loadNodes()
    if inp in nodes:
        note = nodes[inp]
        print("\n")
        print(colored("\n" + note.getName(), "red", attrs=["underline"]))
        print(colored("\n" "Date Created: " + note.dateCreated.strftime("%Y-%m-%d %H:%M:%S"), "yellow"))
        cons = note.getConnections()
        print(colored("Connections:", "magenta") , end='')
        for c in cons:
            print(" " + c, end='')
        print("\n")
        print(colored(note.getData(), "grey"))
        print(colored("\n", "red", attrs=["underline"]))


def startup():
    print(colored('\nWelcome to', 'white'), colored('GraphNotes', 'magenta', attrs=['underline']))
    print(colored("\nHere are yours options:", 'cyan'))
    print("   a) Create new note")
    print("   b) List nodes")
    print("   c) Remove note")
    print("   d) Add new connection between notes")
    print("   e) Remove connection between notes")
    print("   f) Edit your settings file")
    print("   g) Visualize notes -- must have graphviz installed!")
    print("   h) View individual note")
    print("\n   -1: Exit")

    print("\nSelect an option: ", end='')
    selected = input()

    if selected == "a":
        createNewNote()

    if selected == "b":
        printNodeNames()

    if selected == "c":
        removeNote()

    if selected == "d":
        print("Available notes to link:")
        printNodeNames()
        print("State names of notes (like note1 note2): ", end="")
        notes = input()
        notes = notes.split(" ")
        note1 = notes[0]
        note2 = notes[1]

        if note1 in nodes and note2 in nodes:
            nodes[note1].addConnection(note2)
            nodes[note2].addConnection(note1)

    if selected == "g":
        graphToDot()
        viewDot()

    if selected == "h":
        inp = input()
        displayNote(inp)

    if selected == "-1":
        sys.exit()





#See whether there are any command line arguments
if (len(sys.argv) == 1):
    while(True):
        #Start in general mode
        startup()

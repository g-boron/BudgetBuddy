import account
import functions 
import libraries
from subprocess import call # lets run other files

def Run_register():
    call(["python","account/register.py"])


Run_register() #running register file


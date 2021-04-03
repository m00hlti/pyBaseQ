import steps
import logging
import json

# THIS IS THE SEQUIENCER !!!! 11 elf


def sequencer_loadconfigfromfile(file):
    pass

def sequencer_loadconfig(config):
    '''
    Load the complete sequence and prepare the single steps for actual 
    '''
    composedsequence = []

    for currseq in config["sequence"]:
        step = None
        if currseq["type"]== "filecopy":
            logging.info("Add a filecopy step.")
            step = steps.sequencer_step_filecopy()

        elif currseq["type"]== "filemove":
            logging.info("Add a filemove step.")
            step = steps.sequencer_step_filemove()
        
        elif currseq["type"]== "bashcall":
            logging.info("Add a shellcall step.")
            step = steps.sequencer_step_bashcall()

        elif currseq["type"]== "scpcopy":
            logging.info("Add a scpcopy step.")
            step = steps.sequencer_step_scpcopy()
        
        # elif rsync

        # elif mysql/mariadb/postgresql

        else:
            logging.warning("Could not find type: " + currseq["type"])

        

        step.loadconfig(currseq)        
        step.prerun()        
        composedsequence.append(step)

    return composedsequence

def sequencer_run(sequence):
    '''
    Sequencer to run all configured steps
    '''


    for step in sequence:        
        step.run()
        step.postrun()




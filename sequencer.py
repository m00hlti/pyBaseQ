import steps


# THIS IS THE SEQUIENCER !!!! 11 elf
def sequencer_loadconfig(config):
    composedsequence = []

    for currseq in config["sequence"]:
        step = None
        if currseq["type"]== "filecopy":
            step = steps.sequencer_step_filecopy()

        elif currseq["type"]== "filemove":
            step = steps.sequencer_step_filemove()
        
        elif currseq["type"]== "bashcall":
            step = steps.sequencer_step_bashcall()

        elif currseq["type"]== "scpcopy":
            step = steps.sequencer_step_scpcopy()        
       
        step.loadconfig(currseq)
        step.prerun()
        composedsequence.append(step)

    return composedsequence

def sequencer_run(sequence):
    for step in sequence:        
        step.run()
        step.postrun()



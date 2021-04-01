import shutil
import os
import logging
import json
# import paramiko
# from scp import SCPClient


class sequencer_step_base():    
    message = ""

    def __init__(self):
        pass

    def loadconfig(self, config):
        logging.warning("This module(" + self._getName() + ") has no loadconfig() method ")

    def prerun(self):
        logging.warning("This module(" + self._getName() + ") has no prerun() method ")

    def run(self):
        logging.warning("This module(" + self._getName() + ") has no run() method ")

    def postrun(self):
        logging.warning("This module(" + self._getName() + ") has no postrun() method ")

    # SOME INTERNAL METHODS
    def _getName(self):
        return self.__class__.__name__



class sequencer_step_filecopy(sequencer_step_base):
    '''
    Simple File copy sequence. Easy to use, needs some finetuning though.
    '''
    destfolder = ""
    sourcefiles = []

    def __init__(self):
        super().__init__()

    def loadconfig(self, config):
        '''
        load all values from the JSON file to configure the module
        '''
        self.destfolder = config["dest"]
        self.sourcefiles.append(config["source"])
    
    def run(self):
        '''
        copy file to
        '''
        if not os.path.exists(self.destfolder):
            logging.warning('Created folder: ' + self.destfolder + ' since it was not there yet')
            os.mkdir(self.destfolder)

        for currentfile in self.sourcefiles:
            if os.path.exists(currentfile):
                shutil.copy(currentfile, self.destfolder)
            else:
                logging.warning('Could not find file: ' + currentfile + '. Just ignoring it.')



class sequencer_step_filemove(sequencer_step_base):
    '''
    Simple File move sequence. Easy to use, needs some finetuning though.
    '''
    destfolder = ""
    sourcefiles = []

    def __init__(self):
        super().__init__()

    def loadconfig(self, config):
        '''
        load all values from the JSON file to configure the module
        '''
        self.destfolder = config["dest"]
        self.sourcefiles.append(config["source"])
    
    def run(self):
        '''
        copy file to
        '''
        if not os.path.exists(self.destfolder):
            logging.warning('Created folder: ' + self.destfolder + ' since it was not there yet')
            os.mkdir(self.destfolder)

        for currentfile in self.sourcefiles:
            if os.path.exists(currentfile):
                shutil.move(currentfile, self.destfolder)
            else:
                logging.warning('Could not find file: ' + currentfile + '. Just ignoring it.')


class sequencer_step_scpcopy(sequencer_step_base):
    destfolder = ""
    sourcefiles = []

    user = ""
    password = ""

    remoteaddr = ""
    remotesrc = False
    remotedest = False

    valid = False
    

    def __init__(self):
        super().__init__()


    def loadconfig(self, config):
        '''
        load all values from the JSON file to configure the module
        '''
        self.destfolder = config["dest"]
        self.sourcefiles.append(config["source"])

        if "destpc" in config:
            self.remotedest = True
            self.remoteaddr = config["destpc"]
        
        if "sourcepc" in config:
            self.remotesrc = True
            self.remoteaddr = config["sourcepc"]

        self.valid = self.remotedest == self.remotesrc

            #     {
            #     "type": "scpcopy",
            #     "user": "m00hlti",
            #     "password": "booh";
            #     "destpc": "kirsch.limo",
            #     "dest": "C:\\Temp\\newfolder\\",                
            #     "source": "C:\\Temp\\foo.txt",
                
            # },
            
            # {
            #     "type": "scpcopy",
            #     "user": "m00hlti",
            #     "password": "booh";
            #     "sourcepc": "kirsch.limo",
            #     "source": "C:\\Temp\\foobar.txt",
            #     "dest": "C:\\Temp\\newfolder\\",
            #}



    # def createSSHClient(server, port, user, password):
    #     client = paramiko.SSHClient()
    #     client.load_system_host_keys()
    #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     client.connect(server, port, user, password)
    #     return client

    # ssh = createSSHClient(server, port, user, password)
    # scp = SCPClient(ssh.get_transport())


class sequencer_step_bashcall(sequencer_step_base):
    haspath = False
    hasarg = False
    path = ""
    arg = []
    cmd = ""
    

    def __init__(self):
        super().__init__()


    def loadconfig(self, config):
        '''
        load all values from the JSON file to configure the module
        '''
        if "args" in config:
            self.hasarg = True
            self.arg.append(config["args"])
        
        if "path" in config:
            self.haspath = True
            self.path = config["path"]
        
        self.cmd = config["cmd"]
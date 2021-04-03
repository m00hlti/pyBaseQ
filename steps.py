import logging
import os
import shutil
import subprocess
# import paramiko
# from scp import SCPClient


class sequencer_step_base():    
    name = ""

    def __init__(self):
        pass

    def loadconfig(self, config):
        logging.warning("This module(" + self._getName() + ") has no specific loadconfig() method ")

    def prerun(self):
        logging.warning("This module(" + self._getName() + ") has no specific prerun() method ")

    def run(self):
        logging.warning("This module(" + self._getName() + ") has no specific run() method ")

    def postrun(self):
        logging.warning("This module(" + self._getName() + ") has no specific postrun() method ")

    # SOME INTERNAL METHODS
    def _getName(self):
        return self.__class__.__name__

    def _setName(self, name):
        self.name = name



class sequencer_step_filecopy(sequencer_step_base):
    '''
    Simple File copy sequence. Easy to use, needs some finetuning though.
    '''
    destfolder = ""
    sourcefiles = []
    overwrite = True

    def __init__(self):
        super().__init__()

    def loadconfig(self, config):
        '''
        load all values from the JSON file to configure the module
        '''
        if "name" in config:
            self._setName(config["name"])

        self.destfolder = config["dest"]
        for currentfile in config["source"]:
            self.sourcefiles.append(currentfile)
    

    def run(self):
        '''
        copy file to
        '''
        # create destination folder if not 
        if not os.path.exists(self.destfolder):
            logging.warning('Created folder: ' + self.destfolder + ' since it was not there yet')
            os.mkdir(self.destfolder)


        for currentfile in self.sourcefiles:

            logging.debug("Currentfile: " + currentfile)
            
            
            # if currentfile is a directory, copy the whole tree
            if os.path.isdir(currentfile) and os.path.exists(currentfile):
                tmp = self.destfolder + os.path.basename(currentfile)

                if os.path.exists(tmp) and self.overwrite:
                    logging.info("Overwrite is activated, so removing old folder")
                    shutil.rmtree(tmp)

                logging.debug("Found folder and copy it.")                
                shutil.copytree(currentfile, self.destfolder + os.path.basename(currentfile))

            # if currentfile is a file, copy only file
            elif os.path.isfile(currentfile) and os.path.exists(currentfile):
                logging.debug("Found file and copy it.")
                shutil.copy(currentfile, self.destfolder)
            
            # if either file nor directory, nor the file could not be found just send a wanring
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
        if "name" in config:
            self._setName(config["name"])

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
    
    client = None

    def __init__(self):
        super().__init__()


    def loadconfig(self, config):
        '''
        load all values from the JSON file to configure the module
        '''
        if "name" in config:
            self._setName(config["name"])

        self.destfolder = config["dest"]
        self.sourcefiles.append(config["source"])

        if "destpc" in config:
            self.remotedest = True
            self.remoteaddr = config["destpc"]
        
        if "sourcepc" in config:
            self.remotesrc = True
            self.remoteaddr = config["sourcepc"]

        self.valid = self.remotedest == self.remotesrc

    def prerun(self):
         client = paramiko.SSHClient()
         client.load_system_host_keys()
         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #def 
    #     client.connect(server, port, user, password)
    #     return client

    # ssh = createSSHClient(server, port, user, password)
    # scp = SCPClient(ssh.get_transport())

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
        if "name" in config:
            self._setName(config["name"])

        if "args" in config:
            self.hasarg = True
            self.arg.append(config["args"])
        
        if "path" in config:
            self.haspath = True
            self.path = config["path"]
        
        self.cmd = config["cmd"]

    def run(self):
        pass
        #bashCommand = ""#  "cwm --rdf test.rdf --ntriples > test.nt"
        #if self.haspath == True:
        #    bashCommand += self.path
        
        #bashCommand += self.cmd

        #if self.hasarg == True:
        #    for 

        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()

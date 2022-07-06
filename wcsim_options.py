import re 
import shutil
import os
import pickle

class WCSimOptions():
    """A class which can set, store, steer WCSim and its options
    """
    def __init__(self, generator='gun', particle='e-', energy=[500,'MeV'], direction=[1,0,0], position=[0,0,0], output_name='wcsim.root', output_directory='/scratch/fcormier/t2k/ml/output_wcsim/', num_events=500, batch=False):
        """_summary_

        Args:
            generator (str, optional): Type of Generator Defaults to 'gun'.
            particle (str, optional): Particle being simulated Defaults to 'e-'.
            energy (list, optional): Energy of particle Defaults to [500,'MeV'].
            direction (list, optional): Initial direction of particle momentum Defaults to [1,0,0].
            position (list, optional): Initial position of particle Defaults to [0,0,0].
            output_name (list, optional): Name of root file (can include file path) Defaults to ['wcsim.root'].
            num_events (int, optional): Number of events to simulate Defaults to 500.
        """
        self.generator = generator
        self.particle = particle
        self.energy = energy
        self.direction = direction
        self.position = position
        self.output_directory = output_directory
        self.output_name = str(output_directory) + '/' + str(output_name)
        self.num_events = num_events
        self.batch=batch

    def save_options(self,filepath,filename):
        """Save the class and its variables in file

        Args:
            filepath (_type_): Path to file
            filename (_type_): Name of file
        """
        with open(filepath+'/'+filename,'wb') as f:
            pickle.dump(self,f)

    def load_options(self,filepath,filename):
        """Load the class and its variables from file

        Args:
            filepath (_type_): Path to file
            filename (_type_): Name of file

        Returns:
            WCSimOptions class object: Loaded class
        """
        with open(filepath+'/'+filename,'rb') as f:
            new_options = pickle.load(f)
            return new_options


    def set_options(self, filename='WCSim_toEdit.mac'):
        """Sets options on dummy WCSim.mac file by converting pre-typed strings to values set in options

        Args:
            filename (str, optional): Filename to copy and edit Defaults to 'WCSim_toEdit.mac'.

        """
        pat = re.compile(b'GENERATOR|PARTICLE|ENERGY_NUM|ENERGY_UNIT|DIR_0|DIR_1|DIR_2|POS_0|POS_1|POS_2|OUTPUT_NAME|NUM_EVENTS')

        def jojo(mat,dic = {b'GENERATOR':str.encode(str(self.generator)),
                            b'PARTICLE':str.encode(str(self.particle)),
                            b'ENERGY_NUM':str.encode(str(self.energy[0])),
                            b'ENERGY_UNIT':str.encode(str(self.energy[1])),
                            b'DIR_0':str.encode(str(self.direction[0])),
                            b'DIR_1':str.encode(str(self.direction[1])),
                            b'DIR_2':str.encode(str(self.direction[2])),
                            b'POS_0':str.encode(str(self.position[0])),
                            b'POS_1':str.encode(str(self.position[1])),
                            b'POS_2':str.encode(str(self.position[2])),
                            b'OUTPUT_NAME':str.encode(str(self.output_name)),
                            b'NUM_EVENTS':str.encode(str(self.num_events))} ):
            return dic[mat.group()]
        shutil.copyfile(filename,'WCSim.mac')
        with open('WCSim.mac','rb+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(pat.sub(jojo,content))
            f.truncate()

    def set_output_directory(self):
        if not(os.path.exists(self.output_directory) and os.path.isdir(self.output_directory)):
            try:
                os.makedirs(self.output_directory)
            except FileExistsError as error:
                print("Directory " + str(self.output_directory) +" already exists")
                if self.batch is True:
                    exit

    def run_local_wcsim(self):
        self.set_output_directory()
        os.system('cp -r /opt/HyperK/WCSim/macros .')
        os.system('/opt/HyperK/WCSim/exe/bin/Linux-g++/WCSim WCSim.mac')
        self.save_options(self.output_directory,'wc_options.pkl')
        os.system('rm -rf macros')

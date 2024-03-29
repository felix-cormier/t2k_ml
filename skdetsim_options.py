import re 
import shutil
import os
import pickle
import math

class SKDETSimOptions():
    """A class which can set, store, steer WCSim and its options
    """
    def __init__(self, particle=11, energy=[0.,1000.], wall = 100., output_name='skdetsim', output_directory='/scratch/fcormier/t2k/ml/output_skdetsim/', num_events=500, batch=False, save_input_options=False, seed=0):
        """_summary_

        Args:
            generator (str, optional): Type of Generator Defaults to 'gun'.
            particle (str, optional): Particle being simulated Defaults to 'e-'.
            energy (list, optional): DEPRECATED. Energy of particle Defaults to [500,'MeV'].
            halfz (list, optional): The half-height of cylinder to create particles.
            radius (list, optional): The radius of cylinder to create particles.
            direction (list, optional): DEPRECATED. Initial direction of particle momentum Defaults to [1,0,0].
            position (list, optional): DEPRECATED. Initial position of particle Defaults to [0,0,0].
            output_name (list, optional): Name of root file (can include file path) Defaults to ['wcsim.root'].
            num_events (int, optional): Number of events to simulate Defaults to 500.
            batch (int, optional): If the generation and/or transformation will be run as batch jobs.
            seed (int, optional): The random seed to be used for WCSim generation.
            save_input (bool, optional): Whether to save the options listed here for the future.
        """
        self.particle = particle
        self.energy = energy
        self.wall = wall
        self.correct_energy()
        self.output_directory = output_directory
        self.output_name = str(output_directory) + '/' + str(output_name)
        self.num_events = num_events
        self.batch=batch
        self.seed=seed
        self.save_input_options=save_input_options

    def correct_energy(self):
        """Corrects input energy with Cherenkov threshold per particle, then to momentum
            Since SKDETSIM expects momentum input
        """
        threshold_dict = {13:160.1, -13:160.1, 11:0.81, -11:0.81, 22:2*0.511+0.8, 211:211.715}
        mass_dict = {13:105.7, -13:105.7, 11:0.511, -11:0.511, 22:0, 211:139.584}
        self.energy[0] = self.energy[0] + threshold_dict[self.particle]
        if math.pow(self.energy[0],2) > math.pow(mass_dict[self.particle],2):
            self.energy[0] = math.sqrt(math.pow(self.energy[0],2) - math.pow(mass_dict[self.particle],2))
        else:
            self.energy[0] = 0
        self.energy[1] = self.energy[1] + threshold_dict[self.particle]
        if math.pow(self.energy[1],2) > math.pow(mass_dict[self.particle],2):
            self.energy[1] = math.sqrt(math.pow(self.energy[1],2) - math.pow(mass_dict[self.particle],2))
        else:
           self.energy[1] = 0 

    def dump_options(self):
        print(f'Particle: {self.particle}')
        print(f'Energy: {self.energy}')
        print(f'Output Directory: {self.output_directory}')
        print(f'Output Name: {self.output_name}')
        print(f'Number of events: {self.num_events}')
        print(f'Batch: {self.batch}')
        print(f'Save Input: {self.save_input_options}')

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
            print(new_options.particle)
            return new_options


    def set_options(self, filename='sk4_odtune_toEdit.card'):
        """Sets options on dummy WCSim.mac file by converting pre-typed strings to values set in options

        Args:
            filename (str, optional): Filename to copy and edit Defaults to 'sk4_odtune_toEdit.card'.

        """
        pat = re.compile(b'PARTICLE|SEED|ENERGY_MIN|ENERGY_MAX|WALL_SET|OUTPUT_NAME|NUM_EVENTS')

        def jojo(mat,dic = {b'PARTICLE':str.encode(str(self.particle)),
                            b'SEED':str.encode(str(self.seed)),
                            b'ENERGY_MIN':str.encode(str(self.energy[0])),
                            b'ENERGY_MAX':str.encode(str(self.energy[1])),
                            b'WALL_SET':str.encode(str(self.wall)),
                            b'OUTPUT_NAME':str.encode(str(self.output_name)),
                            b'NUM_EVENTS':str.encode(str(self.num_events))} ):
            return dic[mat.group()]
        shutil.copyfile(filename,'sk4_odtune.card')
        with open('sk4_odtune.card','rb+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(pat.sub(jojo,content))
            f.truncate()

    def set_output_directory(self):
        """Makes an output file as given in the arguments
        """
        if not(os.path.exists(self.output_directory) and os.path.isdir(self.output_directory)):
            try:
                os.makedirs(self.output_directory)
            except FileExistsError as error:
                print("Directory " + str(self.output_directory) +" already exists")
                if self.batch is True:
                    exit

    def run_local_skdetsim(self):
        """Runs SKDETSim on current CPU
        """
        self.set_output_directory()
        #os.system('source /project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/setup.sh')
        os.system("ls -l data/")
        os.system('/project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/skdetsim-v13p90_mar16/skdetsim_high.sh sk4_odtune.card '+self.output_name+'.zbs')
        print("Finished simulation")
        os.system("ls -l data/")
        os.system('/project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/ZBS2ROOT/read_zbs '+self.output_name+'.zbs ' +self.output_name)
        os.system("ls -l data/")
        print("Finished ZBS2ROOT")
        if self.save_input_options:
            self.save_options(self.output_directory,'sk_options.pkl')

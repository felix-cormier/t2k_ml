import re 
import shutil
import os
import pickle

class WCSimOptions():
    """A class which can set, store, steer WCSim and its options
    """
    def __init__(self, generator='gun', particle='e-', energy=[0,1000,'MeV'], halfz = [2007.,'cm'], radius= [1965., 'cm'], direction=[1,0,0], position=[0,0,0], output_name='wcsim.root', output_directory='/scratch/fcormier/t2k/ml/output_wcsim/', num_events=500, batch=False, save_input_options=False, seed=0):
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
        self.generator = generator
        self.particle = particle
        self.energy = energy
        self.correct_energy()
        self.halfz = halfz
        self.radius = radius
        self.direction = direction
        self.position = position
        self.output_directory = output_directory
        self.output_name = str(output_directory) + '/' + str(output_name)
        self.num_events = num_events
        self.batch=batch
        self.seed=seed
        self.save_input_options=save_input_options

    def correct_energy(self):
        """Corrects input energy with Cherenkov threshold per particle
        """
        threshold_dict = {'mu-':54.6, 'mu+':54.6, 'e-':0.264, 'e+':0.264, 'gamma':2*0.511+0.264}
        self.energy[0] = self.energy[0] + threshold_dict[self.particle]
        self.energy[1] = self.energy[1] + threshold_dict[self.particle]

    def dump_options(self):
        print(f'Generator: {self.generator}')
        print(f'Particle: {self.particle}')
        print(f'Energy: {self.energy}')
        print(f'Energy: {self.energy}')
        print(f'Energy: {self.energy}')
        print(f'Position: {self.position}')
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


    def set_options(self, filename='WCSim_toEdit.mac'):
        """Sets options on dummy WCSim.mac file by converting pre-typed strings to values set in options

        Args:
            filename (str, optional): Filename to copy and edit Defaults to 'WCSim_toEdit.mac'.

        """
        pat = re.compile(b'GENERATOR|PARTICLE|SEED|ENERGY_MIN|ENERGY_MAX|ENERGY_UNIT|HALFZ_NUM|HALFZ_UNIT|RADIUS_NUM|RADIUS_UNIT|DIR_0|DIR_1|DIR_2|POS_0|POS_1|POS_2|OUTPUT_NAME|NUM_EVENTS')

        def jojo(mat,dic = {b'GENERATOR':str.encode(str(self.generator)),
                            b'PARTICLE':str.encode(str(self.particle)),
                            b'SEED':str.encode(str(self.seed)),
                            b'ENERGY_MIN':str.encode(str(self.energy[0])),
                            b'ENERGY_MAX':str.encode(str(self.energy[1])),
                            b'ENERGY_UNIT':str.encode(str(self.energy[2])),
                            b'HALFZ_NUM':str.encode(str(self.halfz[0])),
                            b'HALFZ_UNIT':str.encode(str(self.halfz[1])),
                            b'RADIUS_NUM':str.encode(str(self.radius[0])),
                            b'RADIUS_UNIT':str.encode(str(self.radius[1])),
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
        """Makes an output file as given in the arguments
        """
        if not(os.path.exists(self.output_directory) and os.path.isdir(self.output_directory)):
            try:
                os.makedirs(self.output_directory)
            except FileExistsError as error:
                print("Directory " + str(self.output_directory) +" already exists")
                if self.batch is True:
                    exit

    def run_local_wcsim(self):
        """Runs WCSim on current CPU
        """
        self.set_output_directory()
        os.system('cp -r /opt/HyperK/WCSim/macros .')
        os.system('/opt/HyperK/WCSim/exe/bin/Linux-g++/WCSim WCSim.mac')
        if self.save_input_options:
            self.save_options(self.output_directory,'wc_options.pkl')
        os.system('rm -rf macros')

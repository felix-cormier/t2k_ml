import re 
import shutil

class WCSimOptions():
    """_summary_
    """
    def __init__(self, generator='gun', particle='e-', energy=[500,'MeV'], direction=[1,0,0], position=[0,0,0], output_name=['wcsim.root'], num_events=500) -> None:
        """_summary_

        Args:
            generator (str, optional): _description_. Defaults to 'gun'.
            particle (str, optional): _description_. Defaults to 'e-'.
            energy (list, optional): _description_. Defaults to [500,'MeV'].
            direction (list, optional): _description_. Defaults to [1,0,0].
            position (list, optional): _description_. Defaults to [0,0,0].
            output_name (list, optional): _description_. Defaults to ['wcsim.root'].
            num_events (int, optional): _description_. Defaults to 500.
        """
        self.generator = generator
        self.particle = particle
        self.energy = energy
        self.direction = direction
        self.position = position
        self.output_name = output_name
        self.num_events = num_events

    def set_options(self, filename='WCSim_toEdit.mac'):
        pat = re.compile(b'GENERATOR|PARTICLE|ENERGY_NUM|ENERGY_UNIT|DIR_0|DIR_1|DIR_2|POS_0|POS_1|POS_2|OUTPUT_NAME|NUM_EVENTS')

        def jojo(mat,dic = {'GENERATOR':str.encode(str(self.generator)),
                            'PARTICLE':str.encode(str(self.particle)),
                            'ENERGY_NUM':str.encode(str(self.energy[0])),
                            'ENERGY_UNIT':str.encode(str(self.energy[1])),
                            'DIR_0':str.encode(str(self.direction[0])),
                            'DIR_1':str.encode(str(self.direction[1])),
                            'DIR_2':str.encode(str(self.direction[2])),
                            'POS_0':str.encode(str(self.position[0])),
                            'POS_1':str.encode(str(self.position[1])),
                            'POS_2':str.encode(str(self.position[2])),
                            'OUTPUT_NAME':str.encode(str(self.output_name)),
                            'NUM_EVENTS':str.encode(str(self.num_events))} ):
            return dic[mat.group()]

        with open(filename,'rb+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(pat.sub(jojo,content))
            f.truncate()
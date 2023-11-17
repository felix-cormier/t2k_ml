import numpy as np
import glob



class fitqun():
    """Class to handle fitqun results
    """
    def __init__(self, input_path, output_path, fitqun_directories) -> None:
        #Load rootfiles form input path
        self.rootfiles = np.load(input_path+'rootfiles.npy')
        #Load labels form input path
        self.labels = np.load(input_path+'labels.npy')
        #Extracts unique rootfiles
        self.indices = self.extract_rootfiles()
        #Match unique rootfile to their label
        self.labels = self.labels[self.indices]
        self.zbs_files = np.empty(len(self.rootfiles), dtype=object)
        #Make sure the length of rootfiles and labels matches
        self.check_label_rootfile_match()
        #Get where to look for .zbs files to run fitqun on
        self.get_fitqun_directories(fitqun_directories)
        self.get_complete_file_paths()

    def extract_rootfiles(self):
        """Extracts the name (not path) of rootfile from list of bytes provided post-training

        Returns:
            numpy array: indices of which labels match the unique rootfiles
        """
        self.rootfiles, indices = np.unique(self.rootfiles, return_index=True)
        self.rootfiles = [x.decode('UTF-8') for x in self.rootfiles]
        self.rootfiles = np.char.split(self.rootfiles,'/')
        self.rootfiles = [x[-1] for x in self.rootfiles]
        return indices

    def check_label_rootfile_match(self):
        if len(self.rootfiles) == len(self.labels):
            return 1
        else:
            print(f'WARNING: Length of labels ({len(self.labels)}) not same as rootfiles ({len(self.rootfiles)}')

    def get_fitqun_directories(self, text_file):
        """Get the string of directories from input text file

        Args:
            text_file (string): path to text file which contains paths to fitqun directories with .zbs files
        """
        print(f'Getting files from: {str(text_file)}')
        text_file = open(text_file, "r")
        self.file_paths = text_file.readlines()
        for i, path in enumerate(self.file_paths):
            self.file_paths[i] = path.strip('\n')
        num_files = len(self.file_paths)

    def get_complete_file_paths(self):
        """Fetches file paths from supplied text file, and pre-pends it to the root file
        """
        for path in self.file_paths:
            files_in_path = glob.glob(path+"*.zbs")
            files_in_path = np.char.split(files_in_path,'/')
            files_in_path = [x[-1] for x in files_in_path]
            files_in_path = np.char.split(files_in_path,'.zbs')
            files_in_path = [x[0] for x in files_in_path]
            matching_indices = np.isin(self.rootfiles,files_in_path)
            #self.rootfiles = self.rootfiles
            #temp = [f'{path}{i}' for i in list(np.array(self.rootfiles)[matching_indices])]
            for i in range(len(self.rootfiles)):
                if matching_indices[i]:
                    self.zbs_files[i] = path + self.rootfiles[i]+'.zbs'

    def get_number_from_rootfile(self, path):
       temp = path.split('/')[-1] 
       temp = temp.split('_')[-1] 
       temp = temp.split('.')[0] 
       return temp


        

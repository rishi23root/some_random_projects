# python main.py
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path
import os,glob 
from time import sleep as nap
import argparse

# listner to know new creating of file 
# give content according to the extention
class EventHandler(FileSystemEventHandler):
    def __init__(self,accepted_file_type : dict):
        self.file_types = accepted_file_type

    def on_created(self, event):
        if not event.is_directory:
            try : 
                file_path = Path(event.src_path)
                directory = file_path.parent
                name = file_path.name
                extention = name.rsplit('.',1)[1]
                if extention in self.file_types.keys():
                    # reading template
                    data = self.extract_data(self.file_types[extention])
                    # writting in the file
                    self.writter(file_path,data)
                    print(f"new file -> {name} in {directory} updated with template")
            except :
                print("\nError in file unable to process it\n")

    def writter(self,filename,data):
        # write the data in the file 
        try:
            with open(filename,'w') as f:
                f.write(data)
        except :
            raise Exception(f"Unable to write in file {filename}")

    def extract_data(self,file_path):
        # extract data from where to write 
        try:
            with open(file_path) as f:
                return f.read()
        except :
            raise Exception(f"Unable to read file {filename} in template")

def listner(watch_path,recursive = True):
    # collect all the file in template   
    # get all files
    path_where_templates_folder = os.getcwd()
    all_files = glob.glob(os.path.join(path_where_templates_folder,'templates','*'))
    # extract file extraction and full path
    data = {str(Path(a).name).rsplit('.')[1] : a for a in all_files}

    # Schedules watching of a given path
    observer = Observer()
    event_handler = EventHandler(data)
    observer.schedule(event_handler, str(watch_path),recursive=recursive) # for all the sub folders in the file, recursive=True)
    observer.start()
    print(f"Listening to the {watch_path} \ntemplates founded : ")
    [print('\t',Path(a).name.rsplit('.',1)[0]) for a in data.values()]
    print("Events : ")
    # keep listning and then close on ctrl+c 
    try : 
        while True : nap(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# example commands
    # python main.py -h
    # python main.py -p "path"
    # python main.py -r -p "path"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', help = "path of the directory you wanna use.")
    parser.add_argument('-r','--recursive', action="store_true", help = "directory and its sub directories.")

    args = parser.parse_args()
    if args.path == None : raise Exception("Enter the path to the directory. use -h for help")

    watch_path = args.path
    recursive = args.recursive
    listner(watch_path,recursive)
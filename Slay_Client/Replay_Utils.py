import datetime
import pickle
import os

#Looks in replays directory for all files that could be replays
def getReplays():
    list = os.listdir('./replays')
    newlist = []
    for file in list:
        if file[-4:] != '.bin': continue
        newlist.append(file[:-4].replace('_',':'))
    return newlist

def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

class Replay:
    def __init__(self,filename=None) -> None:
        if filename is not None:
            self.reading = True
            self.generator = loadall(f"./replays/{filename}.bin".replace(':','_'))
        else:
            self.reading = False
            self.name = str(datetime.datetime.now()).replace(':','_')
            self.file = open(f"replays\\{self.name}.bin", "xb")

    def readNext(self):
        if not self.reading: raise Exception('Trying to read from a incomplete replay')
        return next(self.generator)
        #TODO: Deal with StopIteration exception
    
    def writeNext(self,pack):
        if self.reading: raise Exception('Trying to write to a pre-existing replay')
        pickle.dump(pack,self.file)

    def close(self):
        if not self.reading: self.file.close()
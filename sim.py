from trace_reader import TraceReader
import conf
import storage

class Simulator:
    def run(self):
        if conf.storage_type == 'all':
            self.__runSimAllType()
        else:
            self.__runSim()

    def __runSim(self):
        reader = TraceReader()
        stor = storage.get()
        disk = stor.disk
    
        for req in reader:
            disk.process_queue(req.ts)
            stor.request(req)

        disk.process_rest()                             # handle rest requests in the disk queue
        stor.flush()

        stor.report()  

    def __runSimAllType(self):
        for type in [ 'default', 'prefetch', 'rule', 'ml' ]:
            conf.storage_type = type
            print("--------------------")
            print("Storage Type: ", type)
            self.__runSim()
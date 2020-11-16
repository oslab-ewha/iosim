from trace_reader import TraceReader
import storage

class Simulator:
    def run(self):
        reader = TraceReader()
        stor = storage.get()

        for req in reader:
            stor.request(req)

        stor.report()

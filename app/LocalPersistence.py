from datetime import datetime, timezone
import pickle
import os.path

class LocalPersistence:
    """ persist last values in files """

    def __init__(self, filename="local_persistence.pickle"):
        self.filename = filename
        if not os.path.isfile(self.filename):
            with open(self.filename, 'wb') as file:
                pickle.dump({},file)

    def persist(self, data):
        with open(self.filename, 'wb') as file:
            pickle.dump(data, file)
    
    def updateNode(self, node_id, node_data):
        records = None
        with open(self.filename, 'rb') as file:
            records = pickle.load(file)
            if node_id not in records:
                records[node_id] = {}
            records[node_id] = self.merge_dicts(node_data,records[node_id])
        if records is not None:
            self.persist(records)

    def updateChild(self, node_id, child_id, child_subtype, payload, stamp):
        records = None

        with open(self.filename, 'rb') as file:
            records = pickle.load(file)
            if node_id not in records:
                records[node_id] = { 'children':{}}
            if child_id not in records[node_id]['children']:
                records[node_id]['children'][child_id] = {
                    child_subtype: {}
                }
            records[node_id]['children'][child_id][child_subtype]["last_seen"] = stamp
            records[node_id]['children'][child_id][child_subtype]["payload"] = payload
        
        if records is not None:
            self.persist(records)

    def getSensors(self):
        records = None
        with open(self.filename, 'rb') as file:
            records = pickle.load(file)
        return records

    def merge_dicts(self, x, y):
        # for python < 3.4
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z
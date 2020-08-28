from datetime import datetime, timezone
import pickle
import os.path

class LiveStamping:
    """ Handle last sensors stamps """

    def __init__(self, live_stamping_filename="live_stamp.pickle"):
        self.live_stamping_name = live_stamping_filename
        if not os.path.isfile(self.live_stamping_name):
            with open(self.live_stamping_name, 'wb') as file:
                pickle.dump({},file)

    def persist(self, data):
        with open(self.live_stamping_name, 'wb') as file:
            pickle.dump(file, data)
    
    def updateNodeStamp(self, node_id):
        stamp = datetime.now()
        live_stamping_records = None
        with open(self.live_stamping_name, 'rb') as file:
            live_stamping_records = pickle.load(file)
            if node_id not in live_stamping_records:
                live_stamping_records[message.node_id] = {"last_seen": stamp}
            else:
                live_stamping_records[message.node_id]["last_seen"] = stamp
        if live_stamping_records not None:
            self.persist(live_stamping_records)

    def updateChildStamp(self, node_id, child_id, ch_type):
        stamp = datetime.now()
        live_stamping_records = None
        with open(self.live_stamping_name, 'rb') as file:
            live_stamping_records = pickle.load(file)

            if child_id not in live_stamping_records[node_id]:
                live_stamping_records[node_id][child_id] = {
                    ch_type: stamp
                }
            else:
                live_stamping_records[node_id][child_id][
                    ch_type
                ] = stamp

        if live_stamping_records not None:
            self.persist(live_stamping_records)

    def getLiveNodeStamp(self, node_id):
        with open(self.live_stamping_name, 'rb') as file:
            live_stamping_records = pickle.load(file)
            if node_id not in live_stamping_records:
                return None
            else:
                return live_stamping_records[node_id]["last_seen"]

    def getLiveChildStamp(self, node_id, child_id, data_type):
        with open(self.live_stamping_name, 'rb') as file:
            live_stamping_records = pickle.load(file)
            if (
                node_id not in live_stamping_records
                or child_id not in live_stamping_records[node_id]
                or data_type not in live_stamping_records[node_id][child_id]
            ):
                return None
            else:
                return live_stamping_records[node_id][child_id][data_type]

    def getLiveNodeStampStr(self, node_id):
        stamp = self.getLiveNodeStamp(node_id)
        if stamp is not None:
            return stamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None

    def getLiveChildStampStr(self, node_id, child_id, data_type):
        stamp = self.getLiveChildStamp(node_id, child_id, data_type)
        if stamp is not None:
            return stamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None

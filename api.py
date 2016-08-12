import copy

class stats:
    def __init__(self, ignoredUUIDs):
        self.ignoredUUIDs = ignoredUUIDs

    def remove_internal_ids(self, data):
        """Removes the mongodb internal id from items returned to the user"""
        output = []
        for document in data:
            duplicate = copy.deepcopy(document)
            del duplicate["_id"]
            output.append(duplicate)
        return output

    def remove_ignored_uuids(self, data):
        """Given a list of documents with uuid at the top level, returns a list of documents without uuids defined in ignoredUUIDs"""
        output = []
        for document in data:
            if document['uuid'] not in self.ignoredUUIDs:
                output.append(document)
        return output

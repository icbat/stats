import copy

class stats:
    def __init__(self, ignoredUUIDs):
        self.ignoredUUIDs = ignoredUUIDs
        self.removedField = "_id"

    def cleanse(self, data):
        """Removes the mongodb internal id from items returned to the user"""
        """Given a list of documents with uuid at the top level, returns a list of documents without uuids defined in ignoredUUIDs"""
        output = []
        for document in data:
            if document['uuid'] not in self.ignoredUUIDs:
                duplicate = copy.deepcopy(document)
                if self.removedField in duplicate:
                    del duplicate[self.removedField]
                output.append(duplicate)
        return output

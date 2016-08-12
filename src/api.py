import copy

class stats:
    def __init__(self, ignoredUUIDs):
        self.ignoredUUIDs = ignoredUUIDs
        self.removedField = "_id"

    def cleanse(self, data):
        """Given a list of documents with uuid at the top level, returns a list of documents without uuids defined in ignoredUUIDs and without internal IDs"""
        return [self.__removeIDs(doc) for doc in data if doc['uuid'] not in self.ignoredUUIDs]

    def __removeIDs(self, document):
        """Removes the mongodb internal id from items returned to the user"""
        if self.removedField in document:
            duplicate = copy.deepcopy(document)
            del duplicate[self.removedField]
            return duplicate
        return document

    def present(self, data):
        return {"data": data, "total": len(data)}

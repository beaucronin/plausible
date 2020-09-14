from jsonpath_rw import jsonpath, parse

class JSON(object):
    def __init__(self, j):
        self.j = j        

    def clone(self, path):
        return clone

    # C[R]UD

    def insert(self, path, value):
        return self

    def update(self, path, value):
        return self

    def upsert(self, path, value):
        return self

    def delete(self, path, field):
        return self

    # Moving, promotion, demotion

    def promote(self, path, dest: None):
        return self

    def demote(self, path, dest):
        return self

    def move(self, path, dest):
        return self

    def flatten(self, path: None):
        return self

    def unflatten(self, path: None):
        return self
    
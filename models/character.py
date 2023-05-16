class Character:
    def __init__(self, id, name, description, thumbnail, extension):
        self.id = id
        self.name = name
        self.description = description
        self.thumbnail = thumbnail
        self.extension = extension

    @classmethod
    def from_dict(cls, data):
        return cls (
            id = data['id'],
            name = data['name'],
            description = data['description'],
            thumbnail = data['thumbnail']['path'],
            extension = data['thumbnail']['extension']
            )
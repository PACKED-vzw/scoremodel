

class ItemNotFound(Exception):
    pass


class RequiredAttributeMissing(Exception):
    pass


class DatabaseItemAlreadyExists(Exception):
    pass


class DatabaseItemDoesNotExist(Exception):
    pass


class IllegalEntityType(Exception):
    pass

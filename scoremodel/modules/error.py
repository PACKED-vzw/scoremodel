import json


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


class InvalidPassword(Exception):
    pass


class ApiException(Exception):
    def to_json(self):
        return json.dumps(self.__str__())


class IDMissingForCUD(ApiException):
    pass

import json
from flask import render_template, request
from scoremodel import app


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


@app.errorhandler(403)
def forbidden(e):
    return render_template('error/403.html', title=e), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('error/404.html', title=e, page_name=request.path[1:]), 404

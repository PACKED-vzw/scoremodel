from imp import new_module
from migrate.versioning import api
from scoremodel import db
from config import SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URI

v  = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

migration = '{0}/versions/{1}_migration.py'.format(SQLALCHEMY_MIGRATE_REPO, (v + 1))

m_old_model = new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

exec(old_model, m_old_model.__dict__)

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                                          m_old_model.meta, db.metadata)
open(migration, 'wt').write(script)

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

print('New migration saved as {0}'.format(migration))
print('Current database version: {0}'.format(str(v)))

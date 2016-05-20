from flask.ext.babel import gettext as _
from scoremodel import app

public_api_msg = {
    'item_created': _('%(what) <%(identifier)> created.', what='{0}', identifier='{1}'),
    'item_read': _('%(what) <%(identifier)> found.', what='{0}', identifier='{1}'),
    'item_updated': _('%(what) <%(identifier)> updated.', what='{0}', identifier='{1}'),
    'item_deleted': _('%(what) <%(identifier)> deleted.', what='{0}', identifier='{1}'),
    'items_found': _('%(what) found.', what='{0}')
}

public_error_msg = {
    'item_exists': _('%(what) already exists.', what='{0}'),
    'item_not_exists': _('%(what) <%(identifier)> does not exist.', what='{0}', identifier='{1}'),
    'error_occurred': _('An error occurred: %(error).', error='{0}'),
    'illegal_action': _('Illegal action %(action).', action='{0}'),
    'missing_argument': _('Missing argument %(argument)', argument='{0}')
}


module_error_msg = {
    'item_exists': _('A %(what) with identifier %(identifier) already exists.', what='{0}', identifier='{1}'),
    'item_not_exists': _('No %(what) with identifier %(identifier).', what='{0}', identifier='{1}'),
    'item_not_in': _('No %(what) with identifier %(identifier) does not exist in %(in_what) with identifier'
                     ' %(in_identifier)',
                     what='{0}', identifier='{1}', in_what='{2}', in_identifier='{3}'),
    'item_already_in': _('Item %(what) with identifier %(identifier) already exists in %(in_what) with identifier'
                         ' %(in_identifier)',
                         what='{0}', identifier='{1}', in_what='{2}', in_identifier='{3}'),
    'attr_missing': _('Attribute %(what) missing.', what='{0}')
}
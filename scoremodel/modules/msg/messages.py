from flask_babel import lazy_gettext as _

public_api_msg = {
    'item_created': _('%(what)s <%(identifier)s> created.', what='{0}', identifier='{1}'),
    'item_read': _('%(what)s <%(identifier)s> found.', what='{0}', identifier='{1}'),
    'item_updated': _('%(what)s <%(identifier)s> updated.', what='{0}', identifier='{1}'),
    'item_deleted': _('%(what)s <%(identifier)s> deleted.', what='{0}', identifier='{1}'),
    'items_found': _('%(what)s found.', what='{0}')
}

public_error_msg = {
    'item_exists': _('%(what)s already exists.', what='{0}'),
    'item_not_exists': _('%(what)s <%(identifier)s> does not exist.', what='{0}', identifier='{1}'),
    'error_occurred': _('An error occurred: %(error)s.', error='{0}'),
    'illegal_action': _('Illegal action %(action)s.', action='{0}'),
    'missing_argument': _('Missing argument %(argument)s', argument='{0}')
}

module_error_msg = {
    'item_exists': _('A %(what)s with identifier %(identifier)s already exists.', what='{0}', identifier='{1}'),
    'item_not_exists': _('No %(what)s with identifier %(identifier)s.', what='{0}', identifier='{1}'),
    'item_not_in': _('No %(what)s with identifier %(identifier)s does not exist in %(in_what)s with identifier'
                     ' %(in_identifier)s',
                     what='{0}', identifier='{1}', in_what='{2}', in_identifier='{3}'),
    'item_already_in': _('Item %(what)s with identifier %(identifier)s already exists in %(in_what)s with identifier'
                         ' %(in_identifier)s',
                         what='{0}', identifier='{1}', in_what='{2}', in_identifier='{3}'),
    'attr_missing': _('Attribute %(what)s missing.', what='{0}')
}

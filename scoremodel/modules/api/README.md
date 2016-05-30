All files in this directory (with the exception of the _rest_-subdirectory)
abstract the raw data types away from the application. Most of them form an
interface to SQLAlchemy table classes (which are themselves abstractions),
but not all of them.

The class will perform sanity checks on the provided data and will generally
make it safe to pass to the underlying data type. It will however not check
for authorization to perform a specific action.

Performs checks for:
- Completeness (all required attributes are set in the input + all possible
   attributes have their value set to either the input or `None`/`[]` or `{}`)
  (`RequiredAttributeMissing`).
- Existence (`DatabaseItemDoesNotExist` of `FileDoesNotExist`).

All classes are a subclass of `GenericApi` (`generic.py`) and expose the
following functions
- `.create(input_data)`: creates a new item of the abstracted data type.
  Checks whether required attributes in `input_data` are set.
  Throws `DatabaseItemAlreadyExists` when a specific combination of
  attributes indicates that the same item already exists.
- `.read(item_id)`
  Throws `DatabaseItemDoesNotExist` if the item does not exist.
- `.update(item_id, input_data)`: updates an existing item.
  Throws `DatabaseItemDoesNotExist` if the item does not exist.
- `.delete(item_id)`
  Throws `DatabaseItemDoesNotExist` if the item does not exist.
- `.list()`: return a list (`[]`) of all items of this type.
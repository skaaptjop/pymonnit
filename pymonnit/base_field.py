from .exceptions import ValidationError

class BaseField(object):
    """A base class for fields in an Entity. Instances of this class
    may be added to subclasses of `Entity` to define an Entity's schema.
    Each field is mapped, typically, to an API field.
    """

    # These track each time a Field instance is created. Used to retain order for
    #name of the field that this descripter gets assigned to
    name = None

    def __init__(self, xml_attribute=None, query_param = None, default=None, validation=None, required=False, key=False):
        """
        Constructor
        :param xml_attribute: (optional) name of the API field in the XML structure
        :param query_param: (optional) name of the API query parameter used in HTTP requests
        :param default: default value (may be callable)
        :param validation: custom validation
        :param key: is this the remote identifier
        """
        self.xml_attribute = xml_attribute
        self.query_param = query_param
        self._default = default
        self.required = required
        self._custom_validation = validation
        self.key = key


    @property
    def default(self):
        """
        Return the default value, even if callable
        :return: default value for field
        """
        default = self._default
        if callable(default):
            default = default()
        return default

    def __get__(self, instance, owner):
        """
        Descriptor for retrieving a value from a field in a entity.
        """
        if instance is None:
            # Document class being used rather than a document object
            return self

        return instance._data.get(self.name)

    def __set__(self, instance, value):
        """
        Descriptor for assigning a value to a field in an entity.
        Default is applied if set to None
        """
        if instance is not None:
            instance._data[self.name] = value if value is not None else self.default

    def to_python(self, value):
        return value

    def error(self, message="", errors=None, field_name=None):
        """Raises a ValidationError.
        """
        field_name = field_name if field_name else self.name
        raise ValidationError(message, errors=errors, field_name=field_name)

    def validate(self, value):
        """
        Validate the field for the given value. Triggers custom validation supplied on init
        Override this for custom field specific validation functions
        :param value: value to validate
        """
        # check validation argument
        if self._custom_validation is not None:
            if callable(self._custom_validation):
                if not self._custom_validation(value):
                    self.error('Value does not match custom validation method')
            else:
                raise ValueError('validation argument for "%s" must be a callable.' % self.name)




from collections import OrderedDict, Counter
from .exceptions import InvalidEntityError, ValidationError


class BaseField(object):
    """A base class for fields in an Entity. Instances of this class
    may be added to subclasses of `Entity` to define an Entity's schema.
    Each field is mapped, typically, to an API field.
    """

    # These track each time a Field instance is created. Used to retain order for
    # initialisation of entities by args
    creation_counter = 0

    #name of the field that this descripter gets assigned to
    name = None

    def __init__(self, xml_attribute=None, default=None, validation=None, required=False, key=False):
        """
        Constructor
        :param xml_attribute: (optional) name of the API field in the XML structure
        :param default: default value (may be callable)
        :param validation: custom validation
        :param key: is this the remote identifier
        """
        self.xml_attribute = xml_attribute
        self._default = default
        self.required = required
        self._custom_validation = validation
        self.key = key

        self.creation_counter = BaseField.creation_counter
        BaseField.creation_counter += 1

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

        return instance.meta.data.get(self.name)

    def __set__(self, instance, value):
        """
        Descriptor for assigning a value to a field in an entity.
        Default is applied if set to None
        """
        if instance is not None:
            instance.meta.data[self.name] = value if value is not None else self.default

    def to_python(self, value):
        return value

    def to_query_param(self, value):
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


class EntityMeta(object):
    def __init__(self):
        self.data = {}
        self.fields = OrderedDict()
        self.xml_attribute_map = {}
        self.field_name_map = {}


class EntityMetaClass(type):
    """
    Meta Class for building custom entities
    """

    def __new__(cls, name, bases, attrs):
        """
        Meta Class creator that finds all the BaseField descriptors and adds them to
        various _field dictionaries
        :param name: name of the class being created
        :param bases: tuple of base classes for the class being created
        :param attrs: attributes of the class being created
        """
        # If this is the Entity base class then just call super
        if name == "BaseEntity":
            return super(EntityMetaClass, cls).__new__(cls, name, bases, attrs)

        fields = OrderedDict()
        field_name_to_xml_attribute = {}
        xml_attribute_to_field_name = {}
        api_fields_counter = Counter()

        # we need to sort the attrs that are BaseField derived by creation counter
        field_attrs = filter(lambda attr_item: isinstance(attr_item[1], BaseField), attrs.items())
        ordered_field_attrs = sorted((fo.creation_counter, fn, fo) for fn, fo in field_attrs)

        for _, field_name, field_obj in ordered_field_attrs:
            # give a default xml_attribute
            if not field_obj.xml_attribute:
                field_obj.xml_attribute = field_name
            field_obj.name = field_name

            fields[field_name] = field_obj
            field_name_to_xml_attribute[field_name] = field_obj.xml_attribute
            xml_attribute_to_field_name[field_obj.xml_attribute] = field_name
            api_fields_counter.update([field_obj.xml_attribute])

            if api_fields_counter[field_obj.xml_attribute] > 1:
                raise InvalidEntityError("Multiple xml_attributes defined for: %s" % field_obj.xml_attribute)

        if not attrs.has_key("id"):
            raise InvalidEntityError("No 'id' field defined for: %s" % name)

        meta = EntityMeta()
        meta.fields = fields
        meta.xml_attribute_map = field_name_to_xml_attribute
        meta.field_name_map = field_name_to_xml_attribute

        attrs["meta"] = meta

        entity_class = super(EntityMetaClass, cls).__new__(cls, name, bases, attrs)
        # TODO: is it safe to reset this counter?
        BaseField.creation_counter = 0
        return entity_class



class BaseEntity(object):
    """
    The Entity is to be used as a base class for deriving your own entities.
    """
    __metaclass__ = EntityMetaClass
    xml_tag = None

    def __init__(self, *args, **kwargs):
        """
        Constructor applies argument values to fields (or defaults if applicable)
        :param args: initial values for fields in order of field position in the class
        :param kwargs: named field arguments
        :return:
        """
        # need instance storage
        self.meta.data = {}

        if args:
            # Combine positional arguments with named arguments. We only want named arguments.
            field_iter = iter(self.meta.fields.items())
            for value in args:
                field_name, field_obj = next(field_iter)
                if field_name in kwargs:
                    raise TypeError("Multiple values for keyword argument '" + field_name + "'")
                kwargs[field_name] = value

        # set field values to value in arguments or to the default
        for field_name in self.meta.fields:
            if field_name in kwargs:
                value = kwargs[field_name]
            else:
                value = None    # default will be applied if applicable
            setattr(self, field_name, value)



    def validate(self):
        """
        Ensure that all fields' values are valid and that required fields are present.
        """
        errors = {}
        for field_name, field_obj in self.meta.fields.items():
            field_value = getattr(self, field_name)
            if field_value is not None:
                try:
                    field_obj.validate(field_value)
                except ValidationError as error:
                    errors[field_obj.name] = error.errors or error
                except (ValueError, AttributeError, AssertionError) as error:
                    errors[field_obj.name] = error
            elif field_obj.required:
                errors[field_obj.name] = ValidationError('Field is required', field_name=field_obj.name)
        if errors:
            raise ValidationError('ValidationError', errors=errors)


    @classmethod
    def from_xml(cls, xml_element):
        obj = cls()
        for field_name, field in cls.meta.fields.items():
            xml_attr = cls.meta.xml_attribute_map[field_name]
            obj.meta.data[field_name] = field.to_python(xml_element.get(xml_attr))

        return obj









from .exceptions import InvalidEntityError, ValidationError
from .base_field import BaseField


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

        # merge in fields from base classes
        for base in (base for base in bases if issubclass(base, BaseEntity) and base.__name__ != "BaseEntity"):
            fields = base.meta["fields"]
            attrs.update(fields)

        fields = {}
        field_name_to_xml_attribute = {}
        field_name_to_query_param = {}
        queryable_fields = set()
        xml_attribute_to_field_name = {}

        # we need to sort the attrs that are BaseField derived by creation counter
        field_attrs = filter(lambda attr_item: isinstance(attr_item[1], BaseField), attrs.items())

        for field_name, field_obj in field_attrs:
            # give a default xml_attribute
            if not field_obj.xml_attribute:
                field_obj.xml_attribute = field_name
            field_obj.name = field_name

            fields[field_name] = field_obj
            if field_obj.xml_attribute:
                field_name_to_xml_attribute[field_name] = field_obj.xml_attribute
                xml_attribute_to_field_name[field_obj.xml_attribute] = field_name
            if field_obj.query_param:
                field_name_to_query_param[field_name] = field_obj.query_param
                queryable_fields.add(field_name)

        if not attrs.has_key("id"):
            raise InvalidEntityError("No 'id' field defined for: %s" % name)

        attrs["meta"] = {'fields': fields,
                         'xml_attribute_to_field_name': xml_attribute_to_field_name,
                         'field_name_to_query_param': field_name_to_query_param,
                         'queryable_fields': queryable_fields,
                         'field_name_to_xml_attribute': field_name_to_xml_attribute}

        entity_class = super(EntityMetaClass, cls).__new__(cls, name, bases, attrs)
        return entity_class



class BaseEntity(object):
    """
    The Entity is to be used as a base class for deriving your own entities.
    """
    __metaclass__ = EntityMetaClass
    xml_tag = None

    def __init__(self, **kwargs):
        """
        Constructor applies argument values to fields (or defaults if applicable)
        :param kwargs: named field arguments
        :return:
        """
        # need instance storage for data
        self._data = {}

        # set field values to value in arguments or to the default
        for field_name in self.meta["fields"]:
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
        for field_name, field_obj in self.meta["fields"].items():
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
        for field_name, field in cls.meta["fields"].items():
            xml_attr = cls.meta["field_name_to_xml_attribute"].get(field_name)
            value= xml_element.get(xml_attr)
            if xml_attr:
                obj._data[field_name] = field.to_python(value)
        return obj

    @classmethod
    def get_xml_attribute(cls, field_name):
        return cls.meta["field_name_to_xml_attribute"].get(field_name)


    def __str__(self):
        m = self.__class__.__name__
        for fn, fo in self.meta["fields"].items():
            if hasattr(fo, "entity_class"):
                m += "\n:: %s : %s" % (fn, self._data[fn].id)
            else:
                m += "\n:: %s : %s" % (fn, self._data[fn])
        return m




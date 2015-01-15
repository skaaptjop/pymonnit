import re
from datetime import datetime
from .base_field import BaseField
from .base import BaseEntity



class StringField(BaseField):
    def __init__(self, regex=None, max_length=None, min_length=None, **kwargs):
        self.regex = re.compile(regex) if regex else None
        self.max_length = max_length
        self.min_length = min_length
        super(StringField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, basestring):
            self.error('StringField only accepts string values')

        if self.max_length is not None and len(value) > self.max_length:
            self.error('String value is too long')

        if self.min_length is not None and len(value) < self.min_length:
            self.error('String value is too short')

        if self.regex is not None and self.regex.match(value) is None:
            self.error('String value did not match validation regex')

        super(StringField, self).validate(value)

    def to_python(self, value):
        if isinstance(value, unicode):
            return value
        try:
            value = value.decode('utf-8')
        except:
            pass
        return value.strip()


class IntField(BaseField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(IntField, self).__init__(**kwargs)

    def validate(self, value):
        try:
            value = int(value)
        except:
            self.error('%s could not be converted to int' % value)

        if self.min_value is not None and value < self.min_value:
            self.error('Integer value is too small')

        if self.max_value is not None and value > self.max_value:
            self.error('Integer value is too large')

        super(IntField, self).validate(value)

    def to_python(self, value):
        try:
            value = int(value)
        except ValueError:
            pass   # will fail on validation
        return value


class ReferenceField(BaseField):
    def __init__(self, entity_class, **kwargs):
        self.entity_class = entity_class
        super(ReferenceField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, self.entity_class) and not isinstance(value, BaseEntity):
            self.error("Incorrect type")
        if value.id is None:
            self.error('You can only reference entities with an id')

    def to_python(self, value):
        try:
            value = int(value)
        except ValueError:
            pass   # will fail on validation
        return value



class UTCDateTimeField(BaseField):
    def __init__(self, datetime_format = '%m/%d/%Y %H:%M:%S %p', **kwargs):
        self.datetime_format = datetime_format
        super(UTCDateTimeField, self).__init__(**kwargs)


    def to_python(self, value):
        value = datetime.strptime(value, self.datetime_format)
        return value




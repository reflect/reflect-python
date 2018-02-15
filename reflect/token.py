import calendar
import time
import uuid

from jwcrypto import jwe, jwk
from jwcrypto.common import base64url_encode, json_encode

VIEW_IDENTIFIERS_CLAIM_NAME = 'http://reflect.io/s/v3/vid'
PARAMETERS_CLAIM_NAME = 'http://reflect.io/s/v3/p'
ATTRIBUTES_CLAIM_NAME = 'http://reflect.io/s/v3/a'


class ProjectTokenBuilder(object):
    """Builder for encrypted tokens.

    Provides a way to create secure, reusable tokens that enable particular
    functionality in the Reflect API while disallowing tampering.
    """

    def __init__(self, access_key):
        """Constructs a new token builder with the given access key.

        :param access_key: The access key to use.
        """
        self._access_key = access_key
        self._expiration = None

        self._view_identifiers = []
        self._parameters = []
        self._attributes = {}

    def set_expiration(self, expiration):
        """Sets the expiration for the constructed token to the given time.

        After this time, the token will no longer be valid. All requests made
        using an expired token will fail.

        :param expiration(datetime.datetime): The time object to use for expiration. Should be aware or in UTC.
        """
        self._expiration = expiration
        return self

    def add_view_identifier(self, identifier):
        """Adds the given view identifier to the list of view identifiers
        permitted by this token.

        If no view identifiers are added to this builder, all views in the
        given access key's project will be able to be loaded. Otherwise, only
        those added will be able to be loaded.

        :param identifier(string): The view identifier to restrict to.
        """
        self._view_identifiers.append(identifier)
        return self

    def add_parameter(self, parameter):
        """Adds a data-filtering parameter to this token.

        :param parameter(Parameter): The parameter to add.
        """
        self._parameters.append(parameter)
        return self

    def set_attribute(self, name, value):
        """Sets the given attribute in this token.

        :param name(string): The attribute slug.
        :param value: The attribute's value, which must be serializable to JSON.
        """
        self._attributes[name] = value
        return self

    def build(self, secret_key):
        """Builds a final copy of the token using the given secret key.

        :param secret_key(string): The secret key that corresponds to this builder's access key.
        """
        key = jwk.JWK(
            kty='oct',
            k=base64url_encode(uuid.UUID(secret_key).bytes),
        )

        header = {
            'alg': 'dir',
            'enc': 'A128GCM',
            'zip': 'DEF',
            'cty': 'JWT',
            'kid': self._access_key,
        }

        now = int(time.time())

        payload = {
            'iat': now,
            'nbf': now,
        }

        if self._expiration is not None:
            payload['exp'] = int(calendar.timegm(self._expiration.utctimetuple()))

        if len(self._view_identifiers) > 0:
            payload[VIEW_IDENTIFIERS_CLAIM_NAME] = self._view_identifiers

        if len(self._parameters) > 0:
            parameters = []
            for parameter in self._parameters:
                serialized = {
                    'field': parameter.field,
                    'op': parameter.op,
                }

                if hasattr(parameter, '__iter__'):
                    serialized['any'] = list(parameter.value)
                else:
                    serialized['value'] = parameter.value

                parameters.append(serialized)

            payload[PARAMETERS_CLAIM_NAME] = parameters

        if len(self._attributes) > 0:
            payload[ATTRIBUTES_CLAIM_NAME] = self._attributes

        tok = jwe.JWE(json_encode(payload), protected=header)
        tok.add_recipient(key)

        return tok.serialize(compact=True)

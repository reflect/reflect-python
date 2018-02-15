import calendar
import datetime
import time
import unittest
import uuid

from jwcrypto import jwe, jwk
from jwcrypto.common import base64url_encode, json_decode
from reflect.parameter import Parameter
from reflect.token import ProjectTokenBuilder
from reflect.token import VIEW_IDENTIFIERS_CLAIM_NAME, ATTRIBUTES_CLAIM_NAME, PARAMETERS_CLAIM_NAME


class ProjectKey(object):

    def __init__(self):
        self.access_key = str(uuid.uuid4())
        self.secret_key = str(uuid.uuid4())
        self.secret_key_jwk = jwk.JWK(
            kty='oct',
            k=base64url_encode(uuid.UUID(self.secret_key).bytes),
        )


class TestProjectTokenBuilder(unittest.TestCase):

    def test_simple(self):
        key = ProjectKey()

        serialized = ProjectTokenBuilder(key.access_key).build(key.secret_key)

        tok = jwe.JWE()
        tok.deserialize(serialized)
        self.assertEqual(key.access_key, tok.jose_header['kid'])

        tok.decrypt(key.secret_key_jwk)

    def test_expiration(self):
        key = ProjectKey()
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

        serialized = ProjectTokenBuilder(key.access_key) \
            .set_expiration(expiration) \
            .build(key.secret_key)

        tok = jwe.JWE()
        tok.deserialize(serialized)
        self.assertEqual(key.access_key, tok.jose_header['kid'])

        tok.decrypt(key.secret_key_jwk)
        payload = json_decode(tok.payload)

        self.assertLessEqual(payload['iat'], time.time())
        self.assertLessEqual(payload['nbf'], time.time())
        self.assertGreater(payload['exp'], time.time())
        self.assertEqual(calendar.timegm(expiration.utctimetuple()), payload['exp'])

    def test_claims(self):
        key = ProjectKey()
        parameter = Parameter('user-id', Parameter.EQUALS_OPERATION, '1234')

        serialized = ProjectTokenBuilder(key.access_key) \
            .add_view_identifier('SecUr3View1D') \
            .set_attribute('user-id', 1234) \
            .set_attribute('user-name', 'Billy Bob') \
            .add_parameter(parameter) \
            .build(key.secret_key)

        tok = jwe.JWE()
        tok.deserialize(serialized)
        self.assertEqual(key.access_key, tok.jose_header['kid'])

        tok.decrypt(key.secret_key_jwk)
        payload = json_decode(tok.payload)

        self.assertListEqual(['SecUr3View1D'], payload[VIEW_IDENTIFIERS_CLAIM_NAME])
        self.assertListEqual([{'field': 'user-id', 'op': '=', 'value': '1234'}], payload[PARAMETERS_CLAIM_NAME])
        self.assertDictEqual({'user-id': 1234, 'user-name': 'Billy Bob'}, payload[ATTRIBUTES_CLAIM_NAME])


if __name__ == '__main__':
    unittest.main()

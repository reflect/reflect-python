import base64
import urllib2
import version
import json

class Client(object):
	"""Wraps up all the HTTP communication back to the Reflect service behind an
	easy-to-user interface. Typically, users won't use this object directly. It's
	provided for people who want to customize their usage of Reflect, though."""
	def __init__(self, api_token, server=None):
		self._api_token = api_token

		if server:
			self._server = server
		else:
			self._server = "https://api.reflect.io"

	def keyspaces(self):
		"""List all the keyspaces within an account."""
		return _array_to_objects(self.get("v1/keyspaces"), self, Keyspace)

	def keyspace(self, slug):
		"""Get a single keyspace by slug."""
		path = "v1/keyspaces/%s" % (slug)
		return _to_object(self.get(path), self, Keyspace)

	def destroy_keyspace(self, slug):
		"""Delete an entire keyspace."""
		path = "v1/keyspaces/%s" % (slug)
		return self.delete(path)

	def put(self, path, content):
		req = self._get_request("PUT", path)
		req.add_data(content)
		return self._parse(urllib2.urlopen(req))

	def post(self, path, content):
		req = self._get_request("POST", path)
		req.add_data(content)
		return self._parse(urllib2.urlopen(req))

	def get(self, path):
		req = self._get_request("GET", path)
		return self._parse(urllib2.urlopen(req))

	def delete(self, path):
		req = self._get_request("DELETE", path)
		return self._parse(urllib2.urlopen(req))

	def patch(self, path, content, headers=None):
		req = self._get_request("PUT", path)
		req.add_data(content)

		if headers:
			for name, val in headers.iteritems():
				req.add_header(name, val)

		return self._parse(urllib2.urlopen(req))

	def _url(self, path):
		return "%s/%s" % (self._server, path)

	def _get_request(self, verb, path):
		req = urllib2.Request(self._url(path))
		req.add_header("Authorization", self._get_authorization_string())
		req.add_header("Content-Type", "application/json")
		req.add_header("User-Agent", "Reflect Python v%s" % (version.Version))
		req.get_method = lambda: verb
		return req

	def _get_authorization_string(self):
		encoded = base64.b64encode(":%s" % (self._api_token))
		return "Basic %s" % (encoded)

	def _parse(self, resp):
		data = resp.read()

		if data:
			return json.loads(data)
		else:
			return None

def generateToken(secretKey, params):
    import hmac, hashlib
    from base64 import b64encode

    strs = []

    for param in params:
        val = ''
        vals = []

        if 'any' in param:
            vals = param['any'].sort()
        else:
            val = param['value']

        new_str = json.dumps([param['field'], param['op'], val, vals], indent=None, separators=(',', ':'))
        strs.append(new_str)

    strs.sort()
    strs = "\n".join(strs)
    msg = hmac.new(secretKey, digestmod=hashlib.sha256)
    msg.update("V2\n")
    msg.update(strs)
    return "=2=" + b64encode(msg.digest())

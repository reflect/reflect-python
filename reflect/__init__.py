import base64
import urllib2
import version
import json

def _to_object(obj, client, klass):
	return klass(client, obj)

def _array_to_objects(objs, client, klass):
	return [_to_object(obj, client, klass) for obj in objs]

class ReflectObject(object):
	def __init__(self, client, attrs):
		self._client = client

		if attrs:
			for k, v in attrs.iteritems():
				setattr(self, k, v)

class Keyspace(ReflectObject):
	"""A keyspace within a given Reflect account."""

	def append(self, key, data):
		"""Appends records to a tablet. If the tablet doesn't exist it will be
		created. records can be either a single object or an array of objects. A
		single object represents a single row."""
		data = self._client.put(self._get_key_path(key), self._dump(data))

		if data is None:
			return None

		# This is probably an error.
		raise RuntimeError("An error occured during the request: %s" % (data['error']))

	def replace(self, key, data):
		"""Replaces the existing records in a tablet with a net set of records.
		records can be either a single object or an array of objects. A single
		object represents a single row."""
		data = self._client.post(self._get_key_path(key), self._dump(data))

		if data is None:
			return None

		# This is probably an error.
		raise RuntimeError("An error occured during the request: %s" % (data['error']))

	def patch(self, key, data, criteria):
		"""Patches the existing records in a tablet with a net set of records. The
		criteria parameter indicates which records to match existing records on.
		In the Reflect API, if no existing records match the supplied records then
		those records are dropped."""
		headers = {"X-Criteria": ", ".join(criteria)}
		data = self._client.patch(self._get_key_path(key), self._dump(data), headers)

		if data is None:
			return None

		# This is probably an error.
		raise RuntimeError("An error occured during the request: %s" % (data['error']))

	def upsert(self, key, data, criteria):
		"""Patch the existing records in a tablet with a new set of records and
		insert any that aren't matched. The criteria parameter indicates which
		records to match existing records on."""
		headers = {
			"X-Criteria": ", ".join(criteria),
			"X-Insert-Missing": "true"
		}

		data = self._client.patch(self._get_key_path(key), self._dump(data), headers)

		if data is None:
			return None

		# This is probably an error.
		raise RuntimeError("An error occured during the request: %s" % (data['error']))

	def delete(self, key):
		"""Delete an entire tablet within a keyspace. If no tablet exists with the
		supplied key then this is a no-op."""
		data = self._client.delete(self._get_key_path(key))

		if data is None:
			return None

		# This is probably an error.
		raise RuntimeError("An error occured during the request: %s" % (data['error']))

	def _get_key_path(self, key):
		return "v1/keyspaces/%s/tablets/%s" % (self.slug, key)

	def _dump(self, data):
		return json.dumps(data)

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

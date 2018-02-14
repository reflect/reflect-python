Authentication
==============

To securely authenticate views, Reflect offers the ability to create encrypted
tokens that cannot be tampered with. Use the :py:class:`reflect.ProjectTokenBuilder`
class to create them.

Examples
--------

To create a new token::

    from reflect import Parameter, ProjectTokenBuilder

    access_key = 'd232c1e5-6083-4aa7-9042-0547052cc5dd'
    secret_key = '74678a9b-685c-4c14-ac45-7312fe29de06'

    b = ProjectTokenBuilder(access_key)
    b.set_attribute('user-id', 1234)
    b.set_attribute('user-name', 'Billy Bob')
    b.add_parameter(Parameter('My Field', Parameter.EQUALS_OPERATION, 'My Value'))

    token = b.build(secret_key)


Classes
-------

.. autoclass:: reflect.Parameter
    :members:
    :undoc-members:

.. autoclass:: reflect.ProjectTokenBuilder
    :members:
    :undoc-members:

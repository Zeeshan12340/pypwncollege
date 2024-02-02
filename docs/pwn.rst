:mod:`pwncollege.pwncollege` --- The pwncollege API Client
==========================================================

Session Caching
----------------
If the :code:`cache` option is sent when initializing an API client, the library will follow this algorithm:

* Check if the given path exists
    * If it does, load the :code:`cookie_token` from the file.
    * Check if the :code:`cookie_token` is expired
    * If it is, fall back to a login prompt
* If it isn't, fall back to a login prompt
* After any login prompts, and at program exit, the current token pair will be dumped out to the cache file.

If the option is not set, no cache is used at all.

API Client
----------
.. autoclass:: pwncollege.pwncollege.PWNClient

Integration tests are expected to be principally for service modules.

There really is now point to testing Flask templates, what they produce is part of
acceptance testing to see if the output is correct. You would only be testing the
Flask template engine with an integration test.

It is not practical to test controllers by injecting a Flask object; there are too
many hidden pieces that you have to mock and are not documented. And you would really
be testing the Flask engine since the controller should simply dispatch. Checking the
correct dispatch actions is covered by the acceptance tests.
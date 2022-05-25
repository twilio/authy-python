[![PyPI version](https://badge.fury.io/py/authy.svg)](https://pypi.org/project/authy/) [![Build Status](https://travis-ci.org/twilio/authy-python.svg?branch=master)](https://travis-ci.org/authy/authy-python)

🚨🚨🚨

**This library is no longer actively maintained.** The Authy API has been replaced with the [Twilio Verify API](https://www.twilio.com/docs/verify). Twilio will support the Authy API through November 1, 2022 for SMS/Voice. After this date, we’ll start to deprecate the service for SMS/Voice. Any requests sent to the API after May 1, 2023, will automatically receive an error.  Push and TOTP will continue to be supported through July 2023.

[Learn more about migrating from Authy to Verify.](https://www.twilio.com/blog/migrate-authy-to-verify)

Please visit the Twilio Docs for:
* [Verify + Python (Flask) quickstart](https://www.twilio.com/docs/verify/quickstarts/python-flask)
* [Twilio Python helper library](https://www.twilio.com/docs/libraries/python)
* [Verify API reference](https://www.twilio.com/docs/verify/api)

Please direct any questions to [Twilio Support](https://support.twilio.com/hc/en-us). Thank you!

🚨🚨🚨

## Python Client for Twilio Authy Two-Factor Authentication (2FA) API

Documentation for Python usage of the Authy API lives in the [official Twilio documentation](https://www.twilio.com/docs/authy/api/).

The Authy API supports multiple channels of 2FA:
* One-time passwords via SMS and voice.
* Soft token ([TOTP](https://www.twilio.com/docs/glossary/totp) via the Authy App)
* Push authentication via the Authy App

If you only need SMS and Voice support for one-time passwords, we recommend using the [Twilio Verify API](https://www.twilio.com/docs/verify/api) instead. 

[More on how to choose between Authy and Verify here.](https://www.twilio.com/docs/verify/authy-vs-verify)

### Authy Quickstart

For a full tutorial, check out either of the Python Authy Quickstarts in our docs:
* [Python/Django Authy Quickstart](https://www.twilio.com/docs/authy/quickstart/two-factor-authentication-python-django)
* [Python/Flask Authy Quickstart](https://www.twilio.com/docs/authy/quickstart/two-factor-authentication-python-flask)

## Authy Python Installation

Install with [pip](https://www.twilio.com/docs/usage/quickstart/devenvironment-python#how-to-install-pip):

    $ pip install authy

**OR**

Download the [source code](https://github.com/twilio/authy-python/archive/master.zip) and run the following command from your terminal:

    $ python setup.py install

_Note that you may need admin permissions to run the above commands._

## Usage

To use the Authy client, import AuthyApiClient and initialize it with your production API Key found in the [Twilio Console](https://www.twilio.com/console/authy/applications/):

```python
from authy.api import AuthyApiClient
authy_api = AuthyApiClient('your_api_key')
```

![authy api key in console](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/account-security-api-key.width-800.png)

## 2FA Workflow

1. [Create a user](https://www.twilio.com/docs/authy/api/users#enabling-new-user)
2. [Send a one-time password](https://www.twilio.com/docs/authy/api/one-time-passwords)
3. [Verify a one-time password](https://www.twilio.com/docs/authy/api/one-time-passwords#verify-a-one-time-password)

**OR**

1. [Create a user](https://www.twilio.com/docs/authy/api/users#enabling-new-user)
2. [Send a push authentication](https://www.twilio.com/docs/authy/api/push-authentications)
3. [Check a push authentication status](https://www.twilio.com/docs/authy/api/push-authentications#check-approval-request-status)


## <a name="phone-verification"></a>Phone Verification

[Phone verification now lives in the Twilio API](https://www.twilio.com/docs/verify/api) and has [Python support through the official Twilio helper libraries](https://www.twilio.com/docs/libraries/python). 

[Legacy (V1) documentation here.](verify-legacy-v1.md) **Verify V1 is not recommended for new development. Please consider using [Verify V2](https://www.twilio.com/docs/verify/api)**.

## Notice: Twilio Authy API’s Sandbox feature will stop working on Sep 30, 2021
Twilio is discontinuing the Authy API’s Sandbox, a feature that allows customers to run continuous integration tests against a mock Authy API for free. The Sandbox is no longer being maintained, so we will be taking the final deprecation step of shutting it down on September 30, 2021. The rest of the Authy API product will continue working as-is.

This repo previously used the sandbox API as part of the test suite, but that has been since removed.

You will only be affected if you are using the sandbox API in your own application or test suite.

For more information please read this article on [how we are discontinuing the Twilio Authy sandbox API](https://support.authy.com/hc/en-us/articles/1260803396889-Notice-Twilio-Authy-API-s-Sandbox-feature-will-stop-working-on-Sep-30-2021).

## Contributing

Install development dependencies with pip:

    sudo pip install -r requirements.txt

To run tests:

    make test
or

    make testfile tests/<test_case_file>

## Copyright

Copyright (c) 2011-2020 Authy Inc. See [LICENSE](https://github.com/twilio/authy-python/blob/master/LICENSE) for further details.

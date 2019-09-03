[![Build Status](https://travis-ci.org/twilio/authy-python.svg?branch=master)](https://travis-ci.org/authy/authy-python)

# Python Client for Twilio Authy Two-Factor Authentication (2FA) API

The Authy API supports multiple channels of 2FA:
* One-time passwords via SMS and voice.
* Soft token ([TOTP](https://www.twilio.com/docs/glossary/totp) via the Authy App)
* Push authentication via the Authy App

If you only need SMS and Voice support for one-time passwords, we recommend using the [Twilio Verify API](https://www.twilio.com/docs/verify/api) instead. 

[More on how to choose between Authy and Verify here.](https://www.twilio.com/docs/verify/authy-vs-verify)


## Installation

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
authy_api = AuthyApiClient('#your_api_key')
```

![authy api key in console](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/account-security-api-key.width-800.png)

## Jump to your use case

* [User management](#users)
* [SMS tokens](#sms)
* [Call tokens](#voice)
* [Push Authentication (OneTouch)](#push)


## <a href name="users"></a>User Management

In order to send 2FA codes in your applications, you'll need to create a user.

**NOTE: Users are indexed on cellphone and country code not e-mail. A cellphone is uniquely associated with an `authy_id`. Creating the same user twice will return the same user id.**

### Create A User

To create a user, you need to pass an email, a cellphone, and country code:

```python
user = authy_api.users.create(email='new_user@email.com', phone='405-342-5699', country_code=57)

if user.ok():
    # store user.id in your user database
else:
	print user.errors()
```

`57` is the country code for Colombia. If not provided, the country code defaults to `1` for the USA.

### Check A User Status

To check a user status, pass the user id.

```python
status = authy_api.users.status(authy_id)

if status.ok():
	print status.content

# Phone number is always obfuscated in this request
# {u'status': {u'phone_number': u'XXX-XXX-1234', u'confirmed': True, u'authy_id': 123, u'registered': True, u'devices': [u'iphone', u'iphone'], u'detailed_devices': [{u'os_type': u'unknown', u'device_type': u'authy', u'creation_date': 1509063624}......
```

### Delete A User

To delete a user, just pass the user id.

```python
deleted = authy_api.users.delete(authy_id)

if deleted.ok():
    print deleted.content

# {u'message': u'User removed from application', u'success': True}
```

## <a href name="sms"></a>Sending SMS 2FA Tokens

To request a SMS token you need the user id.

```python
sms = authy_api.users.request_sms(authy_id)

if sms.ok():
    print sms.content

# {u'cellphone': u'+1-XXX-XXX-XX34', u'message': u'SMS token was sent', u'success': True}
```

As always, you can use `ok()` to verify if the token was sent. To be able to use this method you need to have activated the SMS plugin for your Authy App.

This call will be ignored if the user is using the Authy Mobile App (the user would instead see it as a request within the Authy Mobile App). If you still want to send
the SMS pass `{'force': True}` as an option.

```python
sms = authy_api.users.request_sms(authy_id, {'force': True})
```

If the SMS token request was ignored because the user has the Authy Mobile App, then `sms.ignored()` will return `True`.

### <a href name="voice"></a>Sending Call 2FA Tokens

To request a Call token you need the user id.

```python
call = authy_api.users.request_call('authy-id')

print call.content
{u'cellphone': u'+1-XXX-XXX-XX34', u'message': u'Call started...', u'success': True}
```

As always, you can use `ok()` to verify if the token was sent.

This call will be ignored if the user is using the Authy Mobile App (the user would instead see it as a request within the Authy Mobile App). If you still want to call pass `{'force': True}` as an option.

```python
sms = authy_api.users.request_call(authy_id, {'force': True})
```

### Verifying Tokens


__NOTE: Token verification is only enforced if the user has completed registration. To change this behaviour see [Forcing Verification](#forcing-verification).__

   >*Registration is completed once the user installs and registers the Authy mobile app or logs in once successfully using SMS.*


To verify users you need the user id and a token. The token you get from the user through your login form.

```python
verification = authy_api.tokens.verify(authy_id, token_entered_by_the_user)
```

Once again you can use `ok()` to verify whether the token was valid or not.

```python
if verification.ok():
    # the user is valid
```

### <a href name="forcing-verification"></a>Forcing Verification

If you wish to verify tokens even if the user has not yet completed registration, pass `{'force': True}` when verifying the token.

```python
verification = authy_api.tokens.verify(authy_id, token_entered_by_the_user, {"force": True})
```

## <a href name="push"></a>Push Authentication (aka "One Touch")
Push Authentication by Authy uses a very simple API consisting of two endpoints. One for creating approval requests and another to check the status of the approval request. 

### Send Approval Request
To generate a push approval request which user can accept or reject on Authy App

```python
details ={}
details['username']='example@example.com'
details['location']='California, USA'
details['Account Number']='987654'

logos= [dict(res = 'default', url = 'https://example.com/logos/default.png'), dict(res = 'low', url = 'https://example.com/logos/default.png')]

hidden_details = {}
hidden_details['ip_address'] = '110.37.200.52'

user_id = "654321"
message = "Login requested for a CapTrade Bank account."
seconds_to_expire = 120

response = authy_api.one_touch.send_request(user_id,
	                                        message,
	                                        seconds_to_expire=seconds_to_expire,
	                                        details=details,
	                                        hidden_details=hidden_details,
	                                        logos=logos)

if response.ok():
    uuid = response.get_uuid()
    # do your stuff.
else:
    print response.errors()
```

The above request will generate the following:

<img src="https://user-images.githubusercontent.com/3673341/34749316-a5671950-f555-11e7-9951-885f69d6241d.png" width="200">
    
### Check OneTouch UUID status
If you want to check status (accepted/rejected) of OneTouch approval request UUID

```python
status_response = authy_api.one_touch.get_approval_status(uuid)
if status_response.ok():
    # one of 'pending', 'approved', 'denied', or 'expired'
    approval_status = status.content['approval_request']['status']

else:
    print resp.errors()
```  

### OneTouch Callback implementation

To simplify the process of handling a request, you can set a callback URL in the [console](https://www.twilio.com/console/authy/applications).

![image](https://user-images.githubusercontent.com/3673341/34748803-2b36ce52-f553-11e7-9b69-ac26aea19787.png)

## <a name="phone-verification"></a>Phone Verification

[Phone verification now lives in the Twilio API](https://www.twilio.com/docs/verify/api) and has [Python support through the official Twilio helper libraries](https://www.twilio.com/docs/libraries/python). 

[Legacy (V1) documentation here.](verify-legacy-v1.md)

### Details

To see application details, use

```python
app = authy_api.apps.fetch()

if app.ok():
	print app.content
else:
	print app.errors()

# {u'app': {u'name': u'Sample App', u'sms_enabled': True, u'app_id': 12345, u'phone_calls_enabled': True......
```

### Statistics
To request application statistics, use

```python
statistics = authy_api.stats.fetch()

if statistics.ok():
    print statistics.content
else:
    print statistics.errors()
    
# {u'count': 2, u'stats': [{u'auths_count': 0, u'calls_count': 0, u'month': u'December', u'api_calls_count': 6......
```


## Official Documentation

You can find the full API documentation in the official documentation.

* [Authy (2FA)](https://www.twilio.com/docs/authy/api)
* [Phone Verification](https://www.twilio.com/docs/verify/api)

## Contributing

Install development dependencies with pip:

    sudo pip install -r requirements.txt

To run tests:

    make test
or

    make testfile tests/<test_case_file>

## Copyright

Copyright (c) 2011-2020 Authy Inc. See LICENSE for further details.

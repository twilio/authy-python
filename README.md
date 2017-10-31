# Python Client for Authy API

A python library for using the Authy public API.


## Installation

If you have pip installed it's very easy to install authy, just type

    $ pip install authy

Download the [source code](https://github.com/authy/authy-python/zipball/master) then open a terminal and type:

    $ python setup.py install

_Note that you may need admin permissions to run the above commands._

## Usage

To use this client you just need to import AuthyApiClient and initialize it with your API KEY


```python
from authy.api import AuthyApiClient
authy_api = AuthyApiClient('#your_api_key')
```

Now that you have an Authy API object you can start sending requests.


## Creating Users

__NOTE: User is matched based on cellphone and country code not e-mail.
A cellphone is uniquely associated with an authy_id.__

Creating users is very easy, you need to pass an email, a cellphone and _optionally_ a country code:

```python
user = authy_api.users.create('new_user@email.com', '405-342-5699', 57) #email, cellphone, country_code
```

In this case, `57` is the country code for Colombia. This defaults to `1` for the USA.

You can easily see if the user was created by calling `ok()` on the user object.
If the request was successful, you need to store the authy id in your database. Use `user.id` to get this `id` in your database.

```python
if user.ok():
    # store user.id in your user database
```

If something went wrong, `ok()` returns `False` and you can see the errors using the following code

```python
user.errors()
```

This returns a dictionary explaining what went wrong with the request.


## Verifying Tokens


__NOTE: Token verification is only enforced if the user has completed registration. To change this behaviour see Forcing Verification section below.__

   >*Registration is completed once the user installs and registers the Authy mobile app or logins once successfully using SMS.*


To verify users you need the user id and a token. The token you get from the user through your login form.

```python
verification = authy_api.tokens.verify('authy-id', 'token-entered-by-the-user')
```

Once again you can use `ok()` to verify whether the token was valid or not.

```python
if verification.ok():
    # the user is valid
```

### Forcing Verification

If you wish to verify tokens even if the user has not yet complete registration, pass force=true when verifying the token.

```python
verification = authy_api.tokens.verify('authy-id', 'token-entered-by-the-user', {"force": True})
```

## Requesting SMS Tokens

To request a SMS token you only need the user id.

```python
sms = authy_api.users.request_sms('authy-id')
```

As always, you can use `ok()` to verify if the token was sent. To be able to use this method you need to have activated the SMS plugin for your Authy App.

This call will be ignored if the user is using the Authy Mobile App. If you still want to send
the SMS pass `{'force': True}` as an option

```python
sms = authy_api.users.request_sms('authy-id', {'force': True});
```

If the SMS token request was ignored because the user has the Authy Mobile App, then `sms.ignored()` will return `True`.

## Checking User Status

To check a user status, just pass the user id.

```python
user = authy_api.users.status('authy-id')
```

## Requesting Call Tokens

To request a Call token you only need the user id.

```python
call = authy_api.users.request_call('authy-id')
```

As always, you can use `ok()` to verify if the token was sent.

This call will be ignored if the user is using the Authy Mobile App. If you still want to send it, you need to force call option in dashboard settings

## Delete User

To delete a user, just pass the user id.

```python
user = authy_api.users.delete('authy-id')
```

## Application Details

To see application details, use

```python
app = authy_api.apps.fetch()
```

## Application Stats

To request application statistics, use

```python
statistics = authy_api.stats.fetch()
if statistics.ok():
    print statistics.content
else:
    print statistics.errors()
```

## Phone Verification

Authy has an API to verify users via phone calls or sms. Also, user phone information can be gethered
for support and verification purposes.

### Phone Verification Start

In order to start a phone verification, we ask the API to send a token to the user via sms or call:

```python
authy_api.phones.verification_start(phone_number, country_code, via='sms')
```

Optionally you can specify the language that you prefer the phone verification message to be sent. Supported
languages include: English (`en`), Spanish (`es`), Portuguese (`pt`), German (`de`), French (`fr`) and
Italian (`it`). If not specified, English will be used.

```python
authy_api.phones.verification_start(phone_number, country_code, via='sms', locale='es')
# This will send a message in spanish
```

### Phone Verification Check

Once you get the verification from user, you can check if it's valid with:

```python
authy_api.phones.verification_check(phone_number, country_code, verification_code)
```

## Phone Intelligence

If you want to gather additional information about user phone, use phones info.

```python
authy_api.phones.info(phone_number, country_code)
```
## OneToch API
Authy OneTouch uses a very simple API consisting of two endpoints. One for creating approval requests and another to check the status of the approval request. To simplify the process of handling a request, you can set a callback URL in the Authy dashboard. 

### Send Approval Request
To generate a OneTouch approval request which user can accept or reject on Authy App

    details ={}
    details['username']='example@example.com'
    details['location']='California, USA'
    details['Account Number']='987654'
    
    logos= [dict(res = 'default', url = 'https://example.com/logos/default.png'), dict(res = 'low', url = 'https://example.com/logos/default.png')]
        
    hidden_details = {}
    hidden_details['ip_address'] = '110.37.200.52'
        
    user_id= "654321"
    message= "Login requested for a CapTrade Bank account.",
    seconds_to_expire= 120,
    
    response = authy_api.one_touch.send_request(user_id, message,seconds_to_expire, details, hidden_details,logos)
    if response.ok():
        # do your stuff.
        UUID = response.get_uuid()
    else:
        # do your stuff.
       
    
### Check OneTouch UUID status
If you want to check status (accepted/rejected) of OneTouch approval request UUID

    approval_status = authy_api.one_touch.get_approval_status(UUID)
    if status_response.ok():
        # do your stuff.
        status = approval_status.status()
    else:
        # do your stuff, may be you want to ignore this.

### OneTouch Callback implementation
Here is an example of Django 1.10.5 implementation
    
    from authy.api import AuthyApiClient
    authy_api = AuthyApiClient(APIKEY)
    NONCE = request.META["HTTP_X_AUTHY_SIGNATURE_NONCE"]
    AUTHY_SIGNATURE = request.META["HTTP_X_AUTHY_SIGNATURE"]
    REQUEST_METHOD = request.META["REQUEST_METHOD"]
    URL = request.META["HTTP_X_FORWARDED_FOR"] + '://' + request.META["HTTP_HOST"] + request.path
    params = request.body.decode('utf-8')
    params = json.loads(params)
    is_valid = authy_api.one_touch.validate_one_touch_signature(AUTHY_SIGNATURE, NONCE, REQUEST_METHOD, URL, params)
    if is_valid:
        # do your stuff.
    else:
        # do your stuff.

## More…

You can find the full API documentation in the [official documentation](https://docs.authy.com) page.


## Contributing

Install development dependencies with pip:

    sudo pip install -r requirements.txt

To run tests:

    make test
or

    make testfile tests/<test_case_file>

## Copyright

Copyright (c) 2011-2020 Authy Inc. See LICENSE for further details.

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


    from authy.api import AuthyApiClient
    authy_api = AuthyApiClient('#your_api_key')

Now that you have an Authy API object you can start sending requests.


## Creating Users

__NOTE: User is matched based on cellphone and country code not e-mail.
A cellphone is uniquely associated with an authy_id.__

Creating users is very easy, you need to pass an email, a cellphone and _optionally_ a country code:

    user = authy_api.users.create('new_user@email.com', '405-342-5699', 57) #email, cellphone, area_code

In this case, `57` is the country code for Colombia. This defaults to `1` for the USA.

You can easily see if the user was created by calling `ok()` on the user object.
If the request was successful, you need to store the authy id in your database. Use `user.id` to get this `id` in your database.

    if user.ok():
        # store user.id in your user database

If something went wrong, `ok()` returns `False` and you can see the errors using the following code

    user.errors()

This returns a dictionary explaining what went wrong with the request.


## Verifying Tokens


__NOTE: Token verification is only enforced if the user has completed registration. To change this behaviour see Forcing Verification section below.__

   >*Registration is completed once the user installs and registers the Authy mobile app or logins once successfully using SMS.*


To verify users you need the user id and a token. The token you get from the user through your login form.

    verification = authy_api.tokens.verify('authy-id', 'token-entered-by-the-user')

Once again you can use `ok()` to verify whether the token was valid or not.

    if verification.ok():
        # the user is valid


### Forcing Verification

If you wish to verify tokens even if the user has not yet complete registration, pass force=true when verifying the token.

    verification = authy_api.tokens.verify('authy-id', 'token-entered-by-the-user', {"force": True})

## Requesting SMS Tokens

To request a SMS token you only need the user id.

    sms = authy_api.users.request_sms('authy-id')

As always, you can use `ok()` to verify if the token was sent. To be able to use this method you need to have activated the SMS plugin for your Authy App.

This call will be ignored if the user is using the Authy Mobile App. If you still want to send
the SMS pass `{'force': True}` as an option

    sms = authy_api.users.request_sms('authy-id', {'force': True});

If the SMS token request was ignored because the user has the Authy Mobile App, then `sms.ignored()` will return `True`.

## Checking User Status

To check a user status, just pass the user id.

    user = authy_api.users.status('authy-id')

## Delete User

To delete a user, just pass the user id.

    user = authy_api.users.delete('authy-id')

## Application Details

To see application details, use

    app = authy_api.apps.fetch()

## Application Stats

To request application statistics, use

    statistics = authy_api.stats.fetch()
    if statistics.ok():
        print statistics.content
    else:
        print statistics.errors()

## Phone Verification

Authy has an API to verify users via phone calls or sms. Also, user phone information can be gethered
for support and verification purposes.

### Phone Verification Start

In order to start a phone verification, we ask the API to send a token to the user via sms or call:

    authy_api.phones.verification_start(phone_number, country_code, via='sms')

Optionally you can specify the language that you prefer the phone verification message to be sent. Supported
languages include: English (`en`), Spanish (`es`), Portuguese (`pt`), German (`de`), French (`fr`) and
Italian (`it`). If not specified, English will be used.

    authy_api.phones.verification_start(phone_number, country_code, via='sms', locale='es')
    # This will send a message in spanish


### Phone Verification Check

Once you get the verification from user, you can check if it's valid with:

    authy_api.phones.verification_check(phone_number, country_code, verification_code)

## Phone Intelligence

If you want to gather additional information about user phone, use phones info.

    authy_api.phones.info(phone_number, country_code)

## More…

You can find the full API documentation in the [official documentation](https://docs.authy.com) page.


## Contributing

Install development dependencies with pip:

    sudo pip install -r requirements.txt

To run tests:

    make test

## Copyright

Copyright (c) 2011-2020 Authy Inc. See LICENSE for further details.

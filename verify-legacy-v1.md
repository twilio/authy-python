# Phone Verification V1

[Version 2 of the Verify API is now available!](https://www.twilio.com/docs/verify/api) V2 has an improved developer experience and new features. Some of the features of the V2 API include:

* Twilio helper libraries in JavaScript, Java, C#, Python, Ruby, and PHP
* PSD2 Secure Customer Authentication Support
* Improved Visibility and Insights

You are currently viewing Version 1. V1 of the API will be maintained for the time being, but any new features and development will be on Version 2. We strongly encourage you to do any new development with API V2. Check out the migration guide or the API Reference for more information.

### API Reference

API Reference is available at https://www.twilio.com/docs/verify/api/v1

### Phone Verification Start

In order to start a phone verification, we ask the API to send a token to the user via sms or call:

```python
request = authy_api.phones.verification_start(phone_number, country_code, via='sms')

print request.content

# {u'uuid': u'1785f5b0-1234-1234-1234-1285ca17e122', u'success': True, u'seconds_to_expire': 587, u'is_cellphone': True, u'carrier': u'AT&T Wireless', u'message': u'Text message sent to +1 123-456-7890.'}
```

Optionally you can specify the language that you prefer the phone verification message to be sent. Supported
languages include: English (`en`), Spanish (`es`), Portuguese (`pt`), German (`de`), French (`fr`) and
Italian (`it`). If not specified, English will be used.

```python
# This will send a message in spanish
authy_api.phones.verification_start(phone_number, country_code, via='sms', locale='es')
```

### Phone Verification Check

Once you get the verification from user, you can check if it's valid with:

```python
check = authy_api.phones.verification_check(phone_number, country_code, verification_code)

print check.ok()
# True
```

If `.ok()` returns false, `.content()` will provide useful information:

```
print check.content

# wrong code:
# {u'message': u'Verification code is incorrect', u'errors': {u'message': u'Verification code is incorrect'}, u'error_code': u'60022', u'success': False}

# no verifications pending:
# {u'message': u'No pending verifications for +1 321-345-1234 found.', u'errors': {u'message': u'No pending verifications for +1 123-456-7890 found.'}, u'error_code': u'60023', u'success': False}
```
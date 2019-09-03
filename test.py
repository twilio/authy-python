from authy.api import AuthyApiClient

# Your API key from twilio.com/console/authy/applications
# DANGER! This is insecure. See http://twil.io/secure
authy_api = AuthyApiClient('d3rBV0Vd7NIINgoO4Ooc4IyAk8ZjF71L')

authy_id = '57528889'


qr = authy_api.users.generate_qr(authy_id, size='300', label="foo")

print(dir(qr))
print(qr.content['qr_code'])
print(qr.errors())

# sms = authy_api.users.request_sms(authy_id, {'force': True})

# if sms.ok():
#     print sms.content
# else:
#     print sms.errors()


# verification = authy_api.tokens.verify(authy_id, 2554557)

# print(verification.ok())
# print(verification.success)
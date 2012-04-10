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


### Creating Users

Creating users is very easy, you need to pass an email, a cellphone and _optionally_ a country code:
   
    user = authy_api.users.create('new_user@email.com', '405-342-5699', 57) #email, cellphone, area_code

in this case `57` is the country code(Colombia), use `1` for USA. If non are specified it defaults to USA.

You can easily see if the user was created by calling `ok()`.
If request went right, you need to store the authy id in your database. Use `user.id` to get this `id` in your database.

    if(user.ok()):
        # store user.id in your user database

if something goes wrong `ok()` returns `False` and you can see the errors using the following code

    user.errors()

it returns a dictionary explaining what went wrong with the request.


### Verifying Tokens

To verify users you need the user id and a token. The token you get from the user through your login form. 

    verification = authy_api.tokens.verify('authy-id', 'token-entered-by-the-user')

Once again you can use `ok()` to verify whether the token was valid or not.

    if(verification.ok()):
        # the user is valid

### More…

You can fine the full API documentation in the [official documentation](https://docs.authy.com) page.


## Contributing

install development dependencies with pip

    sudo pip install httplib2 simplejson unittest2

to run the test just type

    make test




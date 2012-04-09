# Python Client for Authy API

A python library for using the Authy public API.


## Installation

Download the [source code](https://github.com/authy/authy-python/zipball/master) then open a terminal and type:

    $ python setup.py install

## Usage

To use this client you just need to import AuthyApiClient and initialize it with your API KEY


    from authy.api import AuthyApiClient
    api = AuthyApiClient('Your-Api-Key')

it can't be easier. Now that you have an API object you can start sending requests.


### Creating Users

Creating users is very easy, you need to pass an email, a cellphone and _optionally_ a country code:

    user = api.users.create('newuser@email.com', '4053425699', 57)

in this case "57" is the country code, it defaults to United States("1").

You can easily see if the user was created by calling `ok()` and then you can see the user id by calling `user.id`. **it's important to store the user id in your database so you can use it to validate users later** 

    if(user.ok()):
        # store user.id in your database


if something goes wrong `ok()` returns `False` and you can see the errors using the following code

    user.errors()

it returns a dict explaining what went wrong with the request.


### Verifying Tokens

To verify users you need the user id and a token

    token = api.tokens.verify('a-user-id', 'a-token')

once again you can use `ok()` to verify whether the token was valid or not.

    if(token.ok()):
        # the user is valid

### More…

You can fine the full API documentation in the [official documentation](https://docs.authy.com) page.


## Contributing

install development dependencies with pip

    sudo pip install httplib2 simplejson unittest2

to run the test just type

    make test




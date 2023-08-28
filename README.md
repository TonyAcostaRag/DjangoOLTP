
##########################################################
# Author: Antonio Acosta Flores - Antonio.Acosta@ibm.com #
##########################################################

#########################################################
# Available routes: 
#########################################################

# User routes:
    users/

POST request:

    URL: http://localhost:8000/users/

payload:

    {
        "username": "User1",
        "age": 20
    }

Response expected: 201 http code as the new user creation.

Example of the response expected:

    {
      "id": 2,
      "username": "User1",
      "age": 20
    }


GET request:

    URL: http://localhost:8000/users/

Response expected: A list with all the available users.

Example of expected response:

    [
        {
            "id": 1,
            "username": "Tony",
            "age": 29
        },
        {
            "id": 2,
            "username": "User1",
            "age": 20
        }
    ]


# Specific user route:
    users/<username>/

Where username is the name of the available user.

GET request

    URL : http://localhost:8000/users/username

Expected response: The json with the attributes for the requested username:

    Example by calling: http://localhost:8000/users/User1

    {
      "id": 2,
      "username": "User1",
      "age": 20
    }


# Accounts routes:
    users/<username>/accounts/

POST request:
    URL: http://localhost:8000/users/<username>/accounts/

payload:

    {
      "user": {
        "username": "Tony",
        "age": 29
      },
      "account_name": "TonyAccount",
      "balance": 20000.0,
      "open_date": "2023-08-15"
    }

Response expected: 201 http code as the creation of the new account.

Example of the response expected:

    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "User1",
            "age": 20
        },
        "account_name": "Account1",
        "balance": 20000.0,
        "open_date": "2023-08-15"
    }


GET request:

    URL : http://localhost:8000/users/username/accounts/

Expected response: A list with all the available accounts:

    Example by calling: http://localhost:8000/users/User1/accounts/

    [
        {
            "id": 1,
            "user": {
                "id": 2,
                "username": "User1",
                "age": 20
            },
            "account_name": "Account1",
            "balance": 20000.0,
            "open_date": "2023-08-15"
        }
    ]


# Specific account route:
    users/<username>/accounts/<account_name>

Where account_name is the name of the available account name.

GET request:

    URL : http://localhost:8000/users/username/accounts/<account_name>

Expected response: The json with the attributes for the requested account:

    Example by calling: http://localhost:8000/users/User1/accounts/Account1

    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "User1",
            "age": 20
        },
        "account_name": "Account1",
        "balance": 20000.0,
        "open_date": "2023-08-15"
    }



# Card routes:
    users/<username>/accounts/<account_name>/cards/

POST request:

    URL: http://localhost:8000/users/<username>/accounts/<account_name>/cards/

payload:

    {
        "account": {
            "user": {
                "username": "User1",
                "age": 20 
            },
            "account_name": "Account1",
            "balance": 20000.0,
            "open_date": "2023-08-15"
        },
        "name": "CardName1",
        "cvv": "999"
    }

Response expected: 201 http code as the creation of the new card.

Example of the response expected:

    {
        "id": 1
        "account": {
            "id": 1
            "user": {
                "id": 2
                "username": "User1",
                "age": 20
            },
            "account_name": "Account1",
            "balance": 20000.0,
            "open_date": "2023-08-15"
        },
        "name": "CardName1",
        "cvv": "999"
    }


GET request:

    URL : http://localhost:8000/users/username/accounts/<account_name>/cards/

Expected response: A list with all the available cards:

    Example by calling: http://localhost:8000/users/User1/accounts/Account1/cards/

    [
        {
            "id": 1
            "account": {
                "id": 1
                "user": {
                    "id": 2
                    "username": "User1",
                    "age": 20
                },
                "account_name": "Account1",
                "balance": 20000.0,
                "open_date": "2023-08-15"
            },
            "name": "CardName1",
            "cvv": "999"
        }
    ]


# Specific card route:
    users/<username>/accounts/<account_name>/cards/<account>

Where account is the identifier of the available card account.

GET request:

    URL : http://localhost:8000/users/<username>/accounts/<account_name>/cards/<account>

Expected response: The json with the attributes for the requested card:

    Example by calling: http://localhost:8000/users/User1/accounts/Account1/cards/CardName1

    {
        "id": 1
        "account": {
            "id": 1,
            "user": {
                "id": 2,
                "username": "User1",
                "age": 20
            },
            "account_name": "Account1",
            "balance": 20000.0,
            "open_date": "2023-08-15"
        },
        "name": "CardName1",
        "cvv": "999"
    }

#########################################################
# To include transactions: 
#########################################################

# Transaction routes:
    transactions/


# Deposits:

POST request:

    URL: http://localhost:8000/transactions/

payload:

    {
      "card_id" : 3,
      "amount" : 5000,
      "transaction_type": "deposit"
    }

Response expected: 201 http code as the new transaction was created.

Example of the response expected:

    {
      "card_id": 3,
      "amount": 5000.0,
      "transaction_type": "deposit"
    }


# Withdrawals:

POST request:

    URL: http://localhost:8000/transactions/

payload:

    {
      "card_id" : 3,
      "amount" : 1000,
      "transaction_type": "withdrawal"
    }

Response expected: 201 http code as the new transaction was created.

Example of the response expected:

    {
      "card_id": 3,
      "amount": 1000.0,
      "transaction_type": "withdrawal"
    }

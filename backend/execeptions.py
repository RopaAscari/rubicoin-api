class Exceptions(object):
    class User(object):
        GENERIC = "An error occured"
        CODE_INVALID = "Invalid code"
        NOT_FOUND = "User doesn't exist"
        CODE_EXPIRED = "Code has expired"
        EMAIL_NOT_EXIST = "Email does not exist"
        INCORRECT_PASSWORD = "Password is incorrect"
        PHONE_NOT_EXIST = "Phone number does not exist"
        INCORRECT_CREDENTIALS = "Incorrect email or password!"
        
    class Payment(object):
        CREATE_FAILED = "Failed to add payment method"

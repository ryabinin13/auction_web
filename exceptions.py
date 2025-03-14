
class UserEmailNotFoundException(Exception):
    detail = "User not found"

class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"

class UserAlreadyLoggedException(Exception):
    detail = "User is already logged in"

class UserAlreadyHasEmailException(Exception):
    detail = "User already has an email address"

class MinLenPasswordException(Exception):
    detail = "User already has an email address"

class DifferentPasswordsException(Exception):
    detail = "Passwords don't match"

class ProductNotFoundException(Exception):
    detail = "Product not found"

class AuctionCompletedException(Exception):
    detail = "Auction is completed"

class UserNotCorrectBetException(Exception):
    detail = "User not correct bet"
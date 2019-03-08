import re

def PSWvalid(password):
    if len(password) > 8:
        if re.search('[0-9]',password) is None:
            return "No nums in password"
        else:
            if re.search('[A-Z]',password) is None:
                return "Your Password shoult have capital letters"
            else: return "Its fine"
    else:
        return "Password is to short"

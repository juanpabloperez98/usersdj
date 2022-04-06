import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choices(chars)[0] for _ in range(size))



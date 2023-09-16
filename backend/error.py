class AccessError(Exception):

    def __init__(self, msg):
        self.msg = msg
        # code = 403

    def __str__(self):
        return self.msg


class InputError(Exception):

    def __init__(self, msg):
        self.msg = msg
        # code = 400

    def __str__(self):
        return self.msg

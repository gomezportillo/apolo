class User:

    def __init__(self, email, instrument):
        self.email = email
        self.instrument = instrument


    def toDict(self):
        dict = {}
        dict['email'] = self.email
        dict['instrument'] = self.instrument
        return dict


    def empty(self):
        return (self.email == '' and self.instrument == '')


    def __eq__(self, other):
        if isinstance(other, User):
            return self.email == other.email and self.instrument == other.instrument
        return False

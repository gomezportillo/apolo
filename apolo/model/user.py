class User:

    def __init__(self, email, instrument):
        self.email = email
        self.instrument = instrument

    def toDict(self):
        dict = {}
        dict['email'] = self.email
        dict['instrument'] = self.instrument
        return dict

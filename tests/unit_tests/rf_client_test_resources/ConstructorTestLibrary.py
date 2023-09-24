

class ConstructorTestLibrary:

    def __init__(self, pos_arg, **kwargs):
        self.pos_arg = pos_arg
        self.keyword_arg = kwargs.get('keyword_arg')

    def get_pos_arg(self):
        return self.pos_arg

    def get_keyword_arg(self):
        return self.keyword_arg

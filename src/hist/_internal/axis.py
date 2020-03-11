import boost_histogram.axis as bha


class Regular(bha.Regular):
    def __init__(
        self,
        bins,
        start,
        stop,
        *,
        name=None,
        underflow=True,
        overflow=True,
        growth=False,
        circular=False,
        transform=None
    ):
        metadata = dict(name=name)
        super().__init__(
            bins,
            start,
            stop,
            metadata=metadata,
            underflow=underflow,
            overflow=overflow,
            growth=growth,
            circular=circular,
            transform=transform,
        )

    @property
    def name(self):
        return self.metadata["name"]

    @name.setter
    def name(self, value):
        self.metadata["name"] = value


class bool(Regular):

    def __init__(self, name=None, growth=False, circular=False, transform=None):
        super().__init__(2, 0, 1, name=name, underflow=False, overflow=False,
                         growth=growth, circular=circular, transform=transform)


class Variable(bha.Variable):
    pass


class Integer(bha.Integer):
    pass


class IntCategory(bha.IntCategory):
    pass


class StrCategory(bha.StrCategory):
    pass

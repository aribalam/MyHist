from .core import BaseHist


class NamedHist(BaseHist):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a dict that maps the name to its corresponding axis
        self.namedaxis = {}

        for axis in self.axes:
            if not axis.metadata.get('name', None):
                raise KeyError('The name of axis required')

            # Create mapping from name to axis
            self.namedaxis[axis.metadata['name']] = axis

    # __init__.__doc__ = BaseHistogram.__init__.__doc__

    def fill(self, *args, **kwargs):
        '''
        Case 1: All values are passed as args
                Just pass it to super.fill(...)
        Case 2: All values are passed as kwargs
                Get position of the axis from its name, pass it in that order

        checks:
        If passed as kwargs, check if all axis values are passed
        '''

        if len(args) > 0:
            raise ValueError("Filling should be done using keyword arguments only")

        value_list = []

        # Get value for each named axis
        for name in self.namedaxis:
            value = kwargs.pop(name, None)
            if not value:
                raise KeyError("values for {} is missing".format(name))

            # append it to the final list
            value_list.append(value)

        # the final list is passed to the super class
        super().fill(*value_list, **kwargs)


    #TODO: Override __getitem__ to allow named dict key access as well
    def __getitem__(self, item):
        pass

    #TODO: Implement a shortcut axis type bool - Integer axis with no underflow or overflow and two bins set to zero
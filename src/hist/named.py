from .core import BaseHist


class NamedHist(BaseHist):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a dict that maps the name to its corresponding axis number
        self.namedaxis = {}

        for i, axis in enumerate(self.axes):

            # check if axis has a name
            if not axis.metadata.get('name', None):
                raise KeyError('The name of axis required')

            # Create mapping from name to axis
            self.namedaxis[axis.metadata['name']] = i

    def fill(self, *args, **kwargs):
        """
        Inserts data to histogram, adds support for data passed as axis names
        Filling should be done using axis names as keywords (i.e no args should be provided)
        """

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

    def __getitem__(self, item):
        """
        Added support for slices provided as axis names
        Transforms the axis names to its index and passes it to its superclass function
        """

        # the axis name could only be provided in the form of dict
        # convert axis name to axis number in this case
        if hasattr(item, "items"):
            new_item = {}
            for axis, val in item.items():

                # if axis is provided as name and the name is a valid axis name
                if isinstance(axis, str) and self.namedaxis.get(axis, None) is not None:
                    new_item[self.namedaxis[axis]] = val
                # if axis name is invalid
                elif isinstance(axis, str):
                    raise KeyError("Invalid axis name provided")

                # axis is provided as number
                else:
                    new_item[axis] = val

            return super().__getitem__(new_item)
        else:
            return super().__getitem__(item)
from boost_histogram import Histogram


class BaseHist(Histogram):

    def _compute_commonindex(self, index):
        """
        Method overriden to preprocess dict containing callable values (i.e loc(...))
        before passing it to its superclass function
        """

        # preprocessing for dict
        if hasattr(index, "items"):
            for i, val in index.items():

                # check if callable (eg. bh.loc(...))
                if callable(val):
                    index[i] = val(self.axes[i])

        return super()._compute_commonindex(index)

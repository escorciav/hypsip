import numbers

import numpy as np


class ParameterSampler(object):
    """Generator on parameters sampled from given distributions.
    Non-deterministic iterable over random candidate combinations for hyper-
    parameter search. If all parameters are presented as a list,
    sampling with replacement is performed.

    Parameters
    ----------
    param_distributions : dict
        Dictionary where the keys are parameters and values
        are distributions from which a parameter is to be sampled.
        Distributions either have to provide a ``rvs`` function
        to sample from them, or can be given as a list of values,
        where a uniform distribution is assumed.
    n_iter : integer
        Number of parameter settings that are produced.
    random_state : int or RandomState
        Pseudo random number generator state.

    Returns
    -------
    params : dict of string to any
        **Yields** dictionaries mapping each estimator parameter to
        as sampled value.

    Note
    ----
    This is a simple more deterministic (not tested yet) version of
    `class:ParameterSampler` from scikit-learn.

    Copyrights
    ----------
    Modified by Victor Escorcia.
    Copyright (c) 2007-2016 The scikit-learn developers. All rights reserved.

    """
    def __init__(self, param_distributions, n_iter, random_state=None):
        self.param_distributions = param_distributions
        self.n_iter = n_iter
        self.random_state = random_state

    def __iter__(self):
        # check if all distributions are given as lists
        # in this case we want to sample without replacement
        rnd = random_number_gen(self.random_state)

        # Always sort the keys of a dictionary, for reproducibility
        items = sorted(self.param_distributions.items())
        for _ in xrange(self.n_iter):
            params = dict()
            for k, v in items:
                if hasattr(v, "rvs"):
                    params[k] = v.rvs(size=1, random_state=rnd)
                else:
                    params[k] = v[rnd.randint(len(v))]
            yield params

    def __len__(self):
        """Number of points that will be sampled."""
        return self.n_iter


def random_number_gen(seed=None):
    """Instanciate a numpy pseudo-random number generator

    Parameters
    ----------
    seed : int, default None
        seed for random number generator

    Output
    ------
    rng : np.random.RandomState
        instance of np.random.RandomState class

    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    msg = '{} cannot be used to seed a numpy.random.RandomState'.format(seed)
    raise ValueError(msg)

from scipy.stats import distributions


def args_to_argline(prm, filters=[], underscore_to_dash=True,
                    bool_argparse=True):
    """Naive transformation of dictionary into argument line

    Parameters
    ----------
    prm : dict
        desired pair of key-val. Keys must corresponds to argument line options
    filters : list, optional
        string in keys to avoid
    underscore_to_dash : bool, optional
        Replace underscore for dash for keys
    bool_argparse : bool, optional
        use --no-{key} if False, --key if True.

    Returns
    -------
    argline : str
        argument line string

    """
    argline = ''
    for k, v in prm.items():
        # Filter keys
        remove = 0
        for f in filters:
            if f in k:
                remove += 1
                break
        if remove:
            continue

        if underscore_to_dash:
            k = k.replace('_', '-')

        if isinstance(v, str):
            v = '"{}"'.format(v)
        elif isinstance(v, list):
            v = ' '.join(map(str, v))
        elif isinstance(v, bool) and bool_argparse:
            if not v:
                k = 'no-' + k
            v = ''

        # Add keys
        argline += '--{} {} '.format(k, str(v))
    return argline


def expressive_param_grid(prm, scope=['param_grid']):
    """Replace strings of some keys in prm by functions from
       scipy.stats.distributions

    prm : dict
        Dictionary with parameters grid

    """
    if 'rng_seed' not in prm:
        prm['rng_seed'] = None

    for key in scope:
        for k, v in prm[key].items():
            if isinstance(v, dict):
                prm[key][k] = getattr(distributions, v['name'])(**v['args'])
            elif isinstance(v, str) or isinstance(v, unicode):
                prm[key][k] = getattr(distributions, v)()

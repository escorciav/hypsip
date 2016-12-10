from argparse import ArgumentParser


def input_parser():
    p = ArgumentParser(description='Evaluate Six Hump Camel Back')
    p.add_argument('-x', '--x-var', required=True, type=float)
    p.add_argument('-y', '--y-var', required=True, type=float)
    return p


def main(x_var, y_var, **kwargs):
    """Six Hump Camel Back
    """
    f = ((4 - 2.1 * x_var**2 + x_var**4 / 3) * x_var**2 +
         x_var * y_var + (-4 + 4 * y_var**2) * y_var**2)
    print 'f({}, {}) ='.format(x_var, y_var), f
    return f


if __name__ == '__main__':
    p = input_parser()
    print 'f:', main(**vars(p.parse_args()))

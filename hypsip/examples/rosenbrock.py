from argparse import ArgumentParser


def input_parser_rosenbrock():
    p = ArgumentParser(description='Evaluate Rosenbrock function')
    p.add_argument('-x', '--x-var', required=True, type=float)
    p.add_argument('-y', '--y-var', required=True, type=float)
    return p


def main_rosenbrock(x_var, y_var, a=1, b=100, **kwargs):
    """Rosenbrock fuction
    """
    f = (a - x_var)**2 + b * (y_var - x_var**2)**2
    print 'f({}, {}) ='.format(x_var, y_var), f
    return f


if __name__ == '__main__':
    p = input_parser_rosenbrock()
    print 'f:', main_rosenbrock(**vars(p.parse_args()))

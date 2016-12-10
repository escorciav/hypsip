import argparse
import json
import os
import sys
from datetime import datetime
from socket import gethostname

from hypsip.parse import args_to_argline, expressive_param_grid
from hypsip.sampling import ParameterSampler
# Funtions relted to Job-scheduler (SLURM in my case)
from hypsip.slurm import slurm_parser
from hypsip.slurm import SLURM_JOB_ARRAY as slurm_template
# Functions relted to your program
from hypsip.examples.camel import input_parser as my_program_parser
from hypsip.examples.camel import main as my_main_program

FILENAME = os.path.abspath(__file__)
DFLT_HYPP_FILE = os.path.join(os.path.dirname(FILENAME), 'hypprm.json')


def input_parser(p=None):
    # CLI argument parser
    force_return = False
    if p is None:
        force_return = True
        p = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.description = ('Wrapper exploring different hyper-parameters. '
                     'It can be executed in two modes (Generator/Execution)')
    p.add_argument('-wmhs', '--wrapper-mode', required=True,
                   choices=['exec', 'gen'])
    p.add_argument('-sjid', '--slurm-job-id', default=None, type=int,
                   help=('Job ID, given by SLURM daemon. Ignored during '
                         '"Generator" mode.'))
    p.add_argument('-sjnj', '--slurm-job-n-jobs', default=0, type=int,
                   help='Number of job array to launch')
    p.add_argument('-wmsn', '--wrapper-main-script-name',
                   default='awesome_script.sbatch',
                   help='filename for slurm script')
    p.add_argument('-wmhf', '--wrapper-main-hypp-file',
                   default=DFLT_HYPP_FILE,
                   help='format to retrieve files with hyper-params')

    if force_return:
        return p


def main_exec(slurm_job_id, wrapper_main_hypp_file, **kwargs):
    # Read JSON file with hyper-parameter space
    with open(wrapper_main_hypp_file, 'r') as fid:
        hypp_dict = json.load(fid)
        expressive_param_grid(hypp_dict)
    param_grid = hypp_dict['param_grid']

    # Hyper-parameters are the job_id-th sample from ParameterSampler
    for hypp in ParameterSampler(param_grid, n_iter=slurm_job_id + 1,
                                 random_state=hypp_dict['rng_seed']):
        continue

    # Update corresponding keys in kwargs
    for k, v in hypp.items():
        if k in kwargs:
            kwargs[k] = v

    # Execute task
    my_main_program(**kwargs)


def main_gen(slurm_job_n_jobs, wrapper_main_script_name,
             wrapper_main_hypp_file, **kwargs):
    """Generate SLURM batch script.

    It will overwrite whatever value passed to 'main_job'

    """
    # Give you an idea when/how you generate the script for slurm
    kwargs['slurm_date'] = '{:%Y-%m-%d %H:%M}'.format(datetime.now())
    kwargs['slurm_generator'] = '{}@{}: {}'.format(gethostname(), os.getcwd(),
                                                   ' '.join(sys.argv))

    # Create dir for job-output
    dir_output_job = kwargs['slurm_job_output']
    if not os.path.exists(os.path.dirname(dir_output_job)):
        os.makedirs(dir_output_job)

    # Associate a group of vars with job-ids
    # This case: job-id = particular hyper-parameter config. Therefore,
    # n_jobs = number of hyper-parameters config to try.
    # All jobs are launched at the same time.
    kwargs['slurm_n_jobs'] = '0-{}'.format(slurm_job_n_jobs)

    # Overwrite main_job
    # 1. define minimum scope for experiment (archs in this case)
    cmd = ['python', '-u', FILENAME, '-wmhs', 'exec',
           '-sjid', '${SLURM_ARRAY_TASK_ID}',
           '-wmhf', wrapper_main_hypp_file]
    # 2. add extra arguments, discarding slurm arguments for simplicity &
    # debugging purposes. Note: config file has stronger priority than any of
    # the following parameters.
    argline = args_to_argline(kwargs, filters=['slurm', 'wrapper'],
                              underscore_to_dash=True, bool_argparse=True)
    # Finally, create/overwrite main_job
    kwargs['slurm_main_job'] = ' '.join(cmd + [argline])

    # Write slurm script
    with open(wrapper_main_script_name, 'w') as f:
        f.write(slurm_template.format(**kwargs))


if __name__ == '__main__':
    # Define and augment arpgument parser
    p = my_program_parser()
    slurm_parser(p)
    input_parser(p)
    args = vars(p.parse_args())

    # Wrapper execution
    wrapper_mode = args['wrapper_mode']
    del args['wrapper_mode']
    if wrapper_mode == 'exec':
        main_exec(**args)
    else:
        main_gen(**args)

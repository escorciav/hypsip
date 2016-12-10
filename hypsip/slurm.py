import argparse
import os

DFLT_JOBNAME = 'awesome-job-solving-cv'
DFLT_OUTPUT = './%A_%a.out'
DFLT_WORKDIR = os.path.expanduser('~')
DFLT_NTASKS = 1
DFLT_MEM = '4G'
DFLT_GRES = 'gpu:1'
DFLT_TIME = '72:00:00'
DFLT_BEFORE_JOB = ''
DFLT_MAIN_JOB = 'sleep 60'
DFLT_AFTER_JOB = ''
SLURM_JOB_ARRAY = (
    '#!/bin/bash\n'
    '# Automatically generated script {slurm_date}\n'
    '# created by: {slurm_generator}\n'
    '#\n'
    '#SBATCH --array={slurm_n_jobs}\n'
    '#SBATCH --job-name={slurm_job_name}\n'
    '#SBATCH --output={slurm_job_output}\n'
    '#SBATCH --workdir={slurm_job_workdir}\n'
    '#SBATCH --ntasks={slurm_job_num_tasks}\n'
    '#SBATCH --mem={slurm_job_mem}\n'
    '#SBATCH --gres={slurm_job_gres}\n'
    '#SBATCH --time={slurm_job_time}\n'
    '\n'
    'hostname\n'
    'echo "----- Executing before job -----"\n'
    '{slurm_before_job}\n'
    'echo "------ Executing main job ------"\n'
    'echo "CUDA_VISIBLE_DEVICES=${{CUDA_VISIBLE_DEVICES}}"\n'
    '{slurm_main_job}\n'
    'echo "----- Executing after job ------"\n'
    '{slurm_after_job}\n')


def slurm_parser(p=None):
    """Augment an argument parser

    Parameters
    ----------
    p : argparse.ArgumentParser, optional
        Argument parser to set variables of templates

    Returns
    -------
    p : argparse.ArgumentParser, optional
        Argument parser created if not provided ;)

    """
    force_return = False
    if p is None:
        force_return = True
        p = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('-sjn', '--slurm-job-name', default=DFLT_JOBNAME,
                   help='jobname for sbatch')
    p.add_argument('-sjo', '--slurm-job-output', default=DFLT_OUTPUT,
                   help='configure output of slurm job')
    p.add_argument('-sjwd', '--slurm-job-workdir', default=DFLT_WORKDIR,
                   help='path for workdir')
    p.add_argument('-sjnt', '--slurm-job-num-tasks', default=DFLT_NTASKS,
                   help='maximum number of tasks/process for job')
    p.add_argument('-sjm', '--slurm-job-mem', default=DFLT_MEM,
                   help='global memory required by the job')
    p.add_argument('-sjr', '--slurm-job-gres', default=DFLT_GRES,
                   help='general resources required by the job')
    p.add_argument('-sjt', '--slurm-job-time', default=DFLT_TIME,
                   help='max time per job')
    h_beforejob = ('commands required before running main program e.g. '
                   'loading environment variables, compilation?')
    p.add_argument('-sjb', '--slurm-before-job', default=DFLT_BEFORE_JOB,
                   help=h_beforejob)
    p.add_argument('-sjj', '--slurm-main-job', default=DFLT_MAIN_JOB,
                   help='main job')
    h_afterjob = ('commands required after running main program e.g. '
                  'moving files saved in tmp?, delete garbage?')
    p.add_argument('-sja', '--slurm-after-job', default=DFLT_AFTER_JOB,
                   help=h_afterjob)

    if force_return:
        return p

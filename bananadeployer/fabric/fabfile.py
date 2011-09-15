from __future__ import with_statement
from fabric.api import *


def get_head(code_dir):
    ''' get current commit hash '''
    with cd(code_dir):
        current_head = run("git rev-parse HEAD")
        return current_head

def get_branch(code_dir):
    ''' get current branch name '''
    with cd(code_dir):
        current_branch = run("git branch --no-color| grep \* | cut -c 3-")
        return current_branch

def apache_graceful():
    """
        if apache is RUNNING it does graceful
        if apache is NOT RUNNING it does start
    """

    status = get_apache_status()

    if 'NOT running' in status:
        return run('/etc/init.d/apache2 start')
    else:
        return run('/etc/init.d/apache2 graceful')

def apache_stop():
    ''' stops the webserver'''
    return run('/etc/init.d/apache2 stop')

def get_apache_status():
    with settings(warn_only=True):
        return run('/etc/init.d/apache2 status')

def get_remote_head(branch_name, code_dir):
    ''' gets the commit hash from the repository '''
    with cd(code_dir):
        return run("git rev-parse origin/%s"%branch_name)

def get_remote_log(branch_name, code_dir):
    ''' gets the  '''
    with cd(code_dir):
        return run("git --no-pager log --no-color origin/%s -n 100"%branch_name)

def fetch(code_dir):
    with cd(code_dir):
        return run("git fetch")

def pull_code(commit, code_dir):
    with cd(code_dir):
        # pull new code
        run("git fetch")
        run("git merge %s"%commit)

def reset_code(commit, code_dir):
    '''resets code to specified commit'''
    with cd(code_dir):
        # pull old code
        run("git reset --hard %s"%commit)

# checks if apache is returning 200 when requesting main page
def deployment_verification(url):
    """
    returns request header of specified URL.
    It's used to verify if the site is working after deployment
    """
    run("lynx -head -dump %s" % url)

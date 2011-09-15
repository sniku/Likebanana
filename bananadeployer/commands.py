import shlex
import subprocess
from settings import PROJECT_ROOT
import re
import bananalog

"""
    This file is wrapper for commands in fabric/fab.py
"""

#TODO: this is suboptimal, it would be better to call the fabric functions 
# directly, but I haven't found a way to do it so I'm calling it from shell.
def exec_command(server, command, **kwargs):
    FAB_FILE = '%s/bananadeployer/fabric/fabfile.py'%PROJECT_ROOT
    command_args = ''
    for k,v in kwargs.iteritems():
        if not v:
            raise Exception("value for argument '%s' must be provided '\
                                'when calling %s"%(k, command))

    command_with_args = command
    command_args = ','.join(['%s=%s'%(k,v) for k,v in kwargs.iteritems()])
    if command_args:
        command_with_args = "%s:%s"%(command, command_args)

    CMD_FORMAT = 'fab --fabfile=%(file)s %(command)s '\
                 '--hosts=%(host)s --user=%(user)s -i %(ssh_key)s'

    # create full fabric command
    cmd = CMD_FORMAT%{
        'command': command_with_args,
        'host': server['host'],
        'user': server['user'],
        'ssh_key': server['ssh_key'],
        'file': FAB_FILE
    }

    cmd = str(cmd)
    print cmd
    cmd_call = shlex.split(cmd)
    # get the output
    full_output = subprocess.Popen(cmd_call,stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stderr=subprocess.STDOUT).communicate()[0]

    our_output = '\n'.join(re.findall('(?i).*\ out\:\ (.+)\r', full_output))


    bananalog.log(command+': '+cmd)
    if command == 'get_remote_log':
        bananalog.log('skipping large output\n')
    else:
        bananalog.log(our_output+'\n')
    return our_output


def get_commit_list(server, branch_name):
    '''
        returns list of commits in form of
                            [(commit_hash, comment_line1, comment_line2), ]
        where first element of tuple is commit hash and rest are comments
    '''
    raw_log = exec_command(server, 'get_remote_log',
                        branch_name=branch_name, code_dir=server['path'])
    raw_list = raw_log.split('commit ')
    raw_list = filter(lambda x: x, raw_list) # remove empty
    list = [tuple(x.split('\n', 1)) for x in raw_list if x]
    return list


def get_server_status(server):
    ''' returns startus of the webserver '''
    exec_command(server, 'fetch', code_dir=server['path'])
    head   = exec_command(server, 'get_head', code_dir=server['path'])
    branch = exec_command(server, 'get_branch', code_dir=server['path'])
    remote_head = exec_command(server, 'get_remote_head', branch_name=branch,
                                                        code_dir=server['path'])
    webserver_status = exec_command(server, 'get_apache_status')
    return {
            'branch': branch,
            'head': head,
            'remote_head': remote_head,
            'webserver_status': webserver_status
            }

def was_deployment_successful(server, url):
    '''
        checks if specified URL returns HTTP 200 response.
        It's used to verify that the deployment was successful
    '''
    http_head = exec_command(server, 'deployment_verification', url=url)
    return True if re.search('(?i)HTTP/(\d).(\d) 200', http_head) else False

def deploy_code(server, commit):
    ''' pulls specified commit and restarts webserver '''
    exec_command(server, 'pull_code', commit=commit, code_dir=server['path'])
    exec_command(server, 'apache_graceful')

def deploy_backwards(server, commit):
    ''' resets code to to specified commit andrestarts webserver '''
    exec_command(server, 'reset_code', commit=commit, code_dir=server['path'])
    exec_command(server, 'apache_graceful')

def stop_webserver(server):
    return exec_command(server, 'apache_stop')


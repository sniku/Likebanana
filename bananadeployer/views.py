from commands import deploy_backwards
from commands import deploy_code
from commands import get_commit_list
from commands import get_server_status

from commands import stop_webserver
from commands import was_deployment_successful
from django.shortcuts import render_to_response
from django.template import RequestContext
from settings import SERVERS, WEB_URL

def main(request):
    '''
        Main page, shows status
    '''
    vars = {}
    if request.method == 'POST':
        out = deploy(request, request.POST.get('commit'), request.POST.get('action'))
        vars.update(out)
        #return HttpResponseRedirect('/deploy/%s/%s/'%(request.POST['commit'], request.POST['action']))

    vars.update(get_status())

    return render_to_response('bananadeployer/main.html', vars, context_instance=RequestContext(request))
def get_status():
    ''' gets the status of all specified servers and checks for errors '''
    errors = []
    status = {}
    for k,v in SERVERS['web']:
        status[k] = get_server_status(v)
        if status[k]['branch'] != v['branch_name']:
            errors.append('current branch on %s(%s) differs from the one in settings(%s)'%(k, status[k]['branch'], v['branch_name']))

    # TODO: that's not awesome
    current = status.values()[0]
    primary_server = SERVERS['web'][0]

    branch_head = set([v['branch']+v['head'] for k,v in status.iteritems()])
    status_in_sync = True if len(branch_head)<=1 else False

    if not status_in_sync:
        errors.append('Your web servers are not in sync! They should always be in sync!')

    old_commits = []
    new_commits = []
    current_commit = None
    commit_list = get_commit_list(primary_server[1], status.values()[0]['branch'])

    for c in commit_list:
        if c[0] != current['head'] and current_commit is None:
            new_commits.append(c)
        elif current_commit is None and c[0] == current['head']:
            current_commit = c
        else:
            old_commits.append(c)

    return{
        'status': status,
        'errors': errors,
        'new_commits': new_commits,
        'old_commits': old_commits,
        'current_commit': current_commit,
    }

def deploy(request, commit, action):
    '''
    This view describes your deployment strategy.
    I have 4 servers behind load balancers, my strategy:
    1) pull new code to the server
    2) reload webserver
    3) check if site works
        3 a) if it doesn't work stop webserver and abort deployment
            (I can afford that because other webservers will take over)
        3 b) if everything works, continue with next webserver

    If you have only one webserver, this strategy won't be optimal for you ( you
    don't want to turn off webserver when the deployment was unsuccessfull).
    It would be better in this case to rollback to the commit before deployment.
    '''
    log = []

    if action == 'deploy':
        
        for k, server in SERVERS['web']:
            log.append('deploying %s on %s'%(commit, k))
            deploy_code(server, commit)

            if was_deployment_successful(server, url=WEB_URL):
                log.append('deployment successfull on %s'%k)
            else:
                log.append('deployment of %s NOT successfull on %s. Stopping webserver.'%(commit, k))
                stop_webserver(server)
                log.append('deployment aborted.')
                break;
                
            #log.append('Sleeping 3 seconds to give the Loadbalancers time to figure out what happened')
            #time.sleep(3)
    elif action == 'reset':
        for k, server in SERVERS['web']:
            log.append('resetting code to %s on %s'%(commit, k))
            deploy_backwards(server, commit)

            if was_deployment_successful(server, url=WEB_URL):
                log.append('deployment successfull on %s'%k)
            else:
                log.append('deployment of %s NOT successfull on %s. Stopping webserver.'%(commit, k))
                stop_webserver(server)
                log.append('deployment aborted.')
                break;

            #log.append('Sleeping 3 seconds to give the Loadbalancers time to figure out what happened')
            #time.sleep(3)

    return {'log': log}
    

from settings import BANANALOG

def show_log(request):
    file = open(BANANALOG).read()
    return render_to_response('bananadeployer/show_log.html', {'file':file}, context_instance=RequestContext(request))

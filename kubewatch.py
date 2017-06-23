from slackclient import SlackClient
from kubernetes import client, config,watch
import argparse
import json
from datetime import date, datetime, timezone

slack_token = "YOUR TOKEN"
sc = SlackClient(slack_token)

gbl_channel=""


def build_arg_parser():
    """
    Builds a standard argument parser with arguments for talking to vCenter
    -s service_host_name_or_ip
    -o optional_port_number
    -u required_user
    -p optional_password
    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to k8s')

 

    parser.add_argument('-k', '--ctxt',
                        required=True,
                        action='store',
                        help='Set context kubernetes')

    parser.add_argument('-e', '--only_error',
                        required=False,
                        action='store_true',
                        help='Enable error check')

    parser.add_argument('-c', '--channel',
                        required=True,
                        action='store',
                        help='Channel name to use when sending to slack')



    return parser



def get_args():
    """
    Supports the command-line arguments needed to form a connection to vSphere.
    """
    parser = build_arg_parser()

    args = parser.parse_args()

    return (args)


def sc_call():
    sc.api_call(
      "chat.postMessage",
      channel="#kubedev_chan",
      text="Hello from Python! :tada:"
    )

def send_slack_msg(chan,ico,text):

    sc.api_call("chat.postMessage",
    channel=chan,
    icon_emoji =ico,
    as_user=False,
    attachments= text)


def create_field(my_list, title, value, short=True):
    if value != None:
        if (  isinstance(value, dict)):
            dictstr = '\n'.join('{} : {}'.format(key, value) for key, value in value.items())
            my_list.append( { "title" :title, "value" :dictstr, "short" : short})
        elif ( isinstance(value, datetime) ):
           my_list.append( { "title" :title, "value" :value.isoformat(), "short" : short}) 
        else:
            my_list.append( { "title" :title, "value" :value, "short" : short})

def extract_event_info(ctxt, event, mode='good'):
    global gbl_channel
    my_list=[]

    create_field(my_list, "namespaces", event.metadata.namespace)
    create_field(my_list, "name", event.metadata.name)
    create_field(my_list, "labels", event.metadata.labels)
    create_field(my_list, "status.message", str(event.status.container_statuses[0].state))
    create_field(my_list, "status.start_time", event.status.start_time)
    create_field(my_list, "status.phase", event.status.phase)
    c = datetime.now(timezone.utc) - event.status.start_time
    create_field(my_list, "Runing since", str(c))
    text=[
    {
      
      "color" : mode,
      "pretext" : "Just from information from k8s" + ctxt ,
      "fields" : my_list
    }
    ]

    send_slack_msg(gbl_channel, ":k8s:", text)


def main():
    global gbl_channel
    args = get_args()
    gbl_channel=args.channel
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return

    client1 = client.CoreV1Api(
        api_client=config.new_client_from_config(context=args.ctxt))

    
    only_error = args.only_error

    for event in client1.list_pod_for_all_namespaces(watch=False).items:
        if only_error == True :
            for i in event.status.container_statuses :
                if(i.ready == False and i.restart_count != 0):
                    extract_event_info(args.ctxt, event, "danger")
            #if (event.status.phase != "Running" and event.status.phase != "Succeeded"):
            #    extract_event_info(args.ctxt, event, "danger")
        else:
            extract_event_info(args.ctxt, event )
    


if __name__ == '__main__':
    main()

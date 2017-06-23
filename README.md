Designed and built with all the love in the world @opensense by @volvicoasis.

# kubewatch
Simple cronjob watch K8S monitoring

# Install :

pip3 install slackclient
pip3 install kubernetes

Don't forget your kube config in your home (Cf. https://github.com/kubernetes-incubator/client-python)

# Usage
usage: kubewatch.py [-h] -k CTXT [-e] -c CHANNEL

Standard Arguments for talking to k8s

optional arguments:
  -h, --help            show this help message and exit
  -k CTXT, --ctxt CTXT  Set context kubernetes
  -e, --only_error      Enable error check
  -c CHANNEL, --channel CHANNEL
                        Channel name to use when sending to slack


# Cronjob exemple :
-->At 1:00
0 1 * * * /usr/bin/python3.4 /WTF/kubewatch.py -k "prod" -c "#kubeprod_chan" 
0 1 * * * /usr/bin/python3.4 /WTF/kubewatch.py -k "dev" -c "#kubedev_chan" 

-->At every minute
*/1 * * * * /usr/bin/python3.4 /WTF/kubewatch.py -k "prod" -c "#kubeprod_chan" -e
*/1 * * * * /usr/bin/python3.4 /WTF/kubewatch.py -k "dev" -c "#kubedev_chan" -e


# TODO : 
- add options to script to add slack token
- Extract logs and send it (too easy)


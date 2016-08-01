#!/usr/bin/env python

## Ansible module to talk over ssh to networking devices
## Written by Manjunath KP , Relevance Lab, Bangalore

import datetime
import json, sys, shlex, re
from netmiko import ConnectHandler
from ansible.module_utils.basic import *


class connect:
    def __init__(self):
        '''place holder '''

    def get_handle(self,ip,key_file,device_type="brocade_nos", username='vyatta'):

        c = {
            'device_type': device_type,
            'ip': ip,
            'username': username,
            'key_file': key_file,
        }

        return ConnectHandler(**c)


class send_config_cmd:
    def __init__(self):
        '''place holder'''

    def execute(self, handle, command):
        handle.enable()
        output = []
        output.append(command)
        handle.send_command("configure")

        for cmd in command:
            o = handle.send_command(cmd)
            

            output.append(o)


        o = handle.send_command('commit')
        output.append(o)



        o=handle.send_command('exit')

        return output


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(required=False,
                     default=False),
            ip_add=dict(required=False,
                        default=False),
            device_type=dict(required=False,
                             default="brocade_nos"),
            username=dict(required=False,
                          default="vyatta"),
            key_file=dict(required=False,
                          default=False)))

    arguments = module.params.get('cmd')
    argument = arguments.split(',')
    device_type = module.params.get('device_type')
    username = module.params.get('username')
    key_file = module.params.get('key_file')

    ip = module.params.get('ip_add')
    cmd = argument

    a = connect()
    h = a.get_handle(ip,key_file, device_type, username)

    b = send_config_cmd()
    result = b.execute(h, cmd)
    print json.dumps({"Result": result, "Input": cmd})


if __name__ == '__main__':
    main()


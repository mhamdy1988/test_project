#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps, loads
from ws4py.client.threadedclient import WebSocketClient
from time import sleep


class contstants:

    gripper = {"close": 1.0, "open": -1.0}




class RosBridgeClient(WebSocketClient):




    def opened(self):
        print("Connection opened...")



    def closed(self, code, reason=None):
        print(code, reason)

    def received_message(self, m):
        """
        Just print out the message
        """
        print(m)


    def open_gripper(self, x):

        y = contstants.gripper[x]  # call the gripper action with open or close

        msg = {
            'op': 'call_service',
            'id': '0x001',
            'service': '/festo/cobotv1_1/set_pressure',
            'args':
                {
                    "required_pressure":
                        {
                            'sequence': 0,
                            'p1': y,
                            'p2': 0.0,
                            "weight": 1.0
                        }

                }
        }

        self.send(dumps(msg))


    def set_stiffness(self, stiff_factor):


        msg = {
            'op': 'call_service',
            'id': '0x001',
            'service': '/festo/cobotv1_1/set_stiffness',
            'args':
                {
                    "required_stiffness":
                        {
                            'sequence': 0,
                            'stiffness_factor': stiff_factor
                        }

                }
        }

        self.send(dumps(msg))

    def change_cooridnates(self, x, y, z, x1, y1, z1, w1, velocity, accleration, time_factor):#

        msg = {
            'op': 'call_service',
            'id': '0x001',
            'service': '/festo/cobotv1_1/jog_xyzabc',
            'args':
                {
                    "pose":
                        {
                            "position":
                                {
                                    'x': x,
                                    'y': y,
                                    'z': z
                                },
                            "orientation":
                                {
                                    "x": x1,
                                    "y": y1,
                                    "z": z1,
                                    "w": w1
                                }

                        },
                    "velocity_factor": velocity,
                    "acceleration_factor": accleration,
                    "relative_position": True,
                    "coordinate_system": 'TCP',
                    "time_factor": time_factor

                }
        }
        self.send(dumps(msg))

    def set_collabration(self):#, v, a, bol, empty, time):

        msg = {
            'op': 'call_service',
            'id': '0x001',
            'service': '/festo/cobotv1_1/set_collaboration_mode',
            'args':
                {
                    "sequence":0,
                    "stiffness_on_collision": 0.9,
                    "collision_mode":1
                }
        }

        self.send(dumps(msg))

    def set_jorg_coordinates(self):

        msg = {
            'op': 'call_service',
            'id': '0x001',
            'service': '/festo/cobotv1_1/jog_joints',
            'args':
                {
                    "joint_increment": [0.02,0,0,0,0,0,0],
                    "velocity_factor": 0.2,
                    "acceleration_factor": 0.2,
                    "time_factor": 0.5,
                    "relative_position": True
                }
        }

        self.send(dumps(msg))

if __name__ == "__main__":
    try:
        client = RosBridgeClient('ws://172.16.14.96:9090/')
        #client = RosBridgeClient('ws://192.168.4.44:9090/')
        client.connect()

        x = "open"
        while (True):

             if (x == "close"):
                x = "open"
             else:
                x = "close"
             client.open_gripper(x)
             sleep(0.5)
             k = client.change_cooridnates(-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, 0.1, 0.1, 1)
             sleep(2)
             client.received_message("message " + str(k))
             sleep(2)
             client.received_message("message " + str(k))
             #client.set_stiffness(1.0)
             #client.set_collabration()
             #client.set_jorg_coordinates()
             sleep(5)


        #client.received_message(k)


    except KeyboardInterrupt:
        client.close()

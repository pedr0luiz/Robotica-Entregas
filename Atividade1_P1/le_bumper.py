#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import numpy as np
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import UInt8

def scaneou(dado):
	global frente
	#leituras = np.array(dado.ranges).round(decimals=2)
	print(dado)
	#print("Intensities")
	#print(np.array(dado.intensities).round(decimals=2))


if __name__=="__main__":

	rospy.init_node("le_scan")

	#velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
	recebe_scan = rospy.Subscriber("/scan", UInt8, scaneou)



	while not rospy.is_shutdown():
		pass
		#if frente < 1:
		#	v= -0.17
		#	w = 0.15
		#else:
		#	v = 0.17
		#	w = 0
		#velocidade = Twist(Vector3(v, 0, 0), Vector3(0, 0,w))
		#velocidade_saida.publish(velocidade)
		
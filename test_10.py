import tensorflow as tf
import numpy as np
import os
import logging
from network_10 import CNN

cur_dir = os.path.dirname(os.path.abspath(__file__))
model_dump_dir = os.path.join(cur_dir, 'model_dump_10')

def test(region):
	graph = tf.Graph()
	with graph.as_default():
		cnn = CNN()
		prediction,_,_,_ = cnn.model()
	with tf.Session(graph=graph) as sess:
		restore = tf.train.Saver()
		restore.restore(sess, tf.train.latest_checkpoint(model_dump_dir))
		predict = sess.run(tf.argmax(prediction,1),feed_dict={cnn.xs:region,cnn.keep_prob:1.0}) 
		alpha_num = []
		for i in range(len(predict)):
			alpha_num.append(chr(ord('0') + predict[i]))
	return alpha_num
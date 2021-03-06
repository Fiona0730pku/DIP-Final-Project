import tensorflow as tf
import numpy as np

class CNN:
	def __init__(self):
		self.xs = tf.placeholder(tf.float32,[None,784])
		self.ys = tf.placeholder(tf.float32,[None,62])
		self.keep_prob=tf.placeholder(tf.float32)
		return

	def model(self):
		x_image=tf.reshape(self.xs,[-1,28,28,1])

		# conv1
		W_conv1=self.weight_variable([5,5,1,32])
		b_conv1=self.bias_variable([32])
		h_conv1=tf.nn.relu(self.conv2d(x_image,W_conv1)+b_conv1)
		h_pool1=self.max_pool_2x2(h_conv1)

		# conv2
		W_conv2=self.weight_variable([5,5,32,64])
		b_conv2=self.bias_variable([64])
		h_conv2=tf.nn.relu(self.conv2d(h_pool1,W_conv2)+b_conv2)
		h_pool2=self.max_pool_2x2(h_conv2)

		# conv3
		W_conv3=self.weight_variable([5,5,64,128])
		b_conv3=self.bias_variable([128])
		h_conv3=tf.nn.relu(self.conv2d(h_pool2,W_conv3)+b_conv3)

		# fc1
		W_fc1=self.weight_variable([7*7*128,4096])
		b_fc1=self.bias_variable([4096])
		h_conv3_flat=tf.reshape(h_conv3,[-1,7*7*128])
		h_fc1=tf.matmul(h_conv3_flat,W_fc1)+b_fc1
		h_fc1_drop=tf.nn.dropout(h_fc1,self.keep_prob)

		# fc2
		W_fc2=self.weight_variable([4096,62])
		b_fc2=self.bias_variable([62])

		prediction=tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

		cross_entropy = -tf.reduce_mean(self.ys * tf.log(tf.clip_by_value(prediction, 1e-10, 1.0)))
		train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

		correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(self.ys, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		return prediction, cross_entropy, accuracy, train_step


	def weight_variable(self,shape):
		initial=tf.truncated_normal(shape,stddev=0.1)
		return tf.Variable(initial)

	def bias_variable(self,shape):
		initial=tf.constant(0.1,shape=shape)
		return tf.Variable(initial)

	def conv2d(self,x,W):
		return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

	def max_pool_2x2(self,x):
		return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
import tensorflow as tf
import numpy as np
import os
import random
import logging
import glob
import scipy.misc
import cv2
from network_10 import CNN

#from tensorflow.examples.tutorials.mnist import input_data
#mnist=input_data.read_data_sets('MNIST_data',one_hot=True)

cur_dir = os.path.dirname(os.path.abspath(__file__))
model_dump_dir = os.path.join(cur_dir, 'model_dump_10')
data_dir = cur_dir + '/Fnt'
#load_model = model_dump_dir
load_model = None

def parse(filename):
    #img size 128*128
    im = scipy.misc.imread(filename)
    im = cv2.resize(im,(28,28))
    gt_image = np.float32(im / 255.0)
    gt_image = gt_image.ravel()[np.newaxis,:]
    return gt_image

def train():
    if load_model is not None:
        checkpoints_dir = load_model

    graph = tf.Graph()
    with graph.as_default():
        cnn = CNN()
        _, loss, accuracy, optimizer = cnn.model()
        saver = tf.train.Saver()
    
    with tf.Session(graph=graph) as sess:
        if load_model is not None:
            checkpoint = tf.train.get_checkpoint_state(checkpoints_dir)
            meta_graph_path = checkpoint.model_checkpoint_path + ".meta"
            restore = tf.train.import_meta_graph(meta_graph_path)
            restore.restore(sess, tf.train.latest_checkpoint(checkpoints_dir))
            step = int(meta_graph_path.split("-")[2].split(".")[0])

        else:
            sess.run(tf.global_variables_initializer())
            step = 0

        files = glob.glob(data_dir + '/Sample00*/*.png')
        files = files + glob.glob(data_dir + '/Sample010/*.png')
        random.shuffle(files)
        tmp = 0

        try:           
            for train_epoch in range(0,2000):
                batch_xs = []
                batch_ys = []
                for i in range(0,1016):
                    num = int(files[tmp+i].split("/")[-1].split(".")[0].split("-")[0][4:6])
                    if i == 0:
                        batch_xs = parse(files[tmp+i])
                        batch_ys = np.array([int(j == num-1) for j in range(10)])[np.newaxis,:]
                    else:
                        batch_xs = np.concatenate((batch_xs,parse(files[tmp+i])),axis = 0)
                        #print(batch_ys.shape)
                        #print(tf.one_hot(num-1, 62)[np.newaxis,:].shape)
                        batch_ys = np.concatenate((batch_ys,(np.array([int(j == num-1) for j in range(10)])[np.newaxis,:])),axis = 0)
                #print(batch_xs[0])
                #print(batch_ys[0])
                tmp += 1016
                if tmp == 1016*10:
                    random.shuffle(files)
                    tmp = 0
                loss_val, accuracy_val, _ = sess.run([loss, accuracy, optimizer], feed_dict={cnn.xs:batch_xs,cnn.ys:batch_ys,cnn.keep_prob:0.5})
                if step > 0 and step % 10 == 0:
                    '''
                    y_pre=sess.run(prediction,feed_dict={cnn.xs:mnist.test.images,cnn.keep_prob:1.0})
                    correct_prediction=tf.equal(tf.argmax(y_pre,1),tf.argmax(mnist.test.labels,1))
                    accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
                    result=sess.run(accuracy,feed_dict={cnn.xs:mnist.test.images,cnn.ys:mnist.test.labels,cnn.keep_prob:1.0})
                    '''
                    logging.info('-----------Step %d:-------------' % step)
                    logging.info('loss : {}'.format(loss_val))
                    logging.info('test_accuracy : {}'.format(accuracy_val))
                if step > 0 and step % 100 == 0:
                    save_path = saver.save(sess, model_dump_dir + "/model.ckpt", global_step=step)
                    logging.info("Model saved in file: %s" % save_path)
                step += 1
                

        except KeyboardInterrupt:
            logging.info('Interrupted')
        finally:
            save_path = saver.save(sess, model_dump_dir + '/model.ckpt', global_step=step)
            logging.info('model saved in files: %s' % save_path)


def main(unused_argv):
    train()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tf.app.run()
#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
from text_cnn import TextCNN
from tensorflow.contrib import learn
import csv
import requests

# Parameters
# ==================================================

# Data Parameters
tf.flags.DEFINE_string("positive_data_file", "./data/rt-polaritydata/rt-polarity.pos", "Data source for the positive data.")
tf.flags.DEFINE_string("negative_data_file", "./data/rt-polaritydata/rt-polarity.neg", "Data source for the negative data.")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")


FLAGS = tf.flags.FLAGS
#FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

GET_URL = "http://192.168.1.2:9120/service/api/ztb/listInfoBybusinessType?businessTypeValue=2&pageSize=1000&guildId=1"
#GET_URL = "https://umxh.xue2you.cn/service/api/ztb/listInfoBybusinessType?businessTypeValue=2&pageSize=1000"
#PUT_URL = "https://umxh.xue2you.cn/service/api/ztb/importProjectbusinessTypes"
PUT_URL = "http://192.168.1.2:9120/service/api/ztb/importProjectbusinessTypes"
def load_from_http(url):
    x_raw = []
    pids = []
    ids = []
    try:
        resp = requests.get(url)


        filename = "./input/%d.txt" % int(time.time()*1000000)
        """
        file = open(filename, "w")
        file.write(resp.content.decode('utf8'))
        file.close()
        """ 
        #print(resp.content.decode('utf8'))
        #content = resp.content.decode("utf8")
        #objs = json.loads(content)
        objs = resp.json()
        if objs['code'] == 0:
            for item in objs['data']:
                x_raw.append(item['pageTitle'])
                pids.append(item['projectId'])
                ids.append(item['id'])
    except Exception as e:
        print(e)
    return x_raw,pids,ids

def store_to_http(x_raw, pids, ids, predictions):
    content = []
    i = 0
    for id in ids:
        prj = {}
        prj['projectId'] = pids[i]
        prj['infoId'] = id
        prj['minorBusinessType'] = data_helpers.get_label_name(int(predictions[i]))
        prj['title'] = x_raw[i]
        content.append(prj)
        i = i + 1
    #todo
    #print(predictions)
    #print(content)
    str_content = str(content)
    filename = "./output/%d.txt" % int(time.time()*1000000)
    """
    file = open(filename, "w")
    file.write(str_content)
    file.close()
    """
    payload = {'guildId':1,'businessTypes': str_content}
    try:
        r = requests.post(PUT_URL, data=payload)
        print(r.text)
    except Exception as e:
        print(e)

import pickle
file = open('./runs/vocab','rb')
vocabulary = pickle.load(file)
file.close()

def run_classify(vocabulary,max_len):
	x_raw,pids,ids = load_from_http(GET_URL)
	#print(pids)
	#print(ids)
	y_test = None
	if len(x_raw) == 0:
	    return 0
	#print(x_raw)
	#x, y, vocabulary, vocabulary_inv = data_helpers.load_data()
	x_test = data_helpers.load_texts(x_raw,max_len,vocabulary)
	#print(x_test)
	print("\nEvaluating...\n")

	# Evaluation
	# ==================================================
	checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
	graph = tf.Graph()
	with graph.as_default():
	    session_conf = tf.ConfigProto(
	      allow_soft_placement=FLAGS.allow_soft_placement,
	      log_device_placement=FLAGS.log_device_placement)
	    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3)
	    session_conf.gpu_options.allow_growth = True
	    sess = tf.Session(config=session_conf)
	    with sess.as_default():
	        # Load the saved meta graph and restore variables
	        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
	        saver.restore(sess, checkpoint_file)

	        # Get the placeholders from the graph by name
	        input_x = graph.get_operation_by_name("input_x").outputs[0]
	        # input_y = graph.get_operation_by_name("input_y").outputs[0]
	        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

	        # Tensors we want to evaluate
	        predictions = graph.get_operation_by_name("output/predictions").outputs[0]

	        # Generate batches for one epoch
	        batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

	        # Collect the predictions here
	        all_predictions = []

	        for x_test_batch in batches:
	            #print(x_test_batch)
	            batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
	            all_predictions = np.concatenate([all_predictions, batch_predictions])

	store_to_http(x_raw, pids, ids, all_predictions)

	"""
	# Print accuracy if y_test is defined
	if y_test is not None:
	    correct_predictions = float(sum(all_predictions == y_test))
	    print("Total number of test examples: {}".format(len(y_test)))
	    print("Accuracy: {:g}".format(correct_predictions/float(len(y_test))))

	# Save the evaluation to a csv
	predictions_human_readable = np.column_stack((np.array(x_raw), all_predictions))
	out_path = os.path.join(FLAGS.checkpoint_dir, "..", "prediction.csv")
	print("Saving evaluation to {0}".format(out_path))
	with open(out_path, 'w') as f:
	    csv.writer(f).writerows(predictions_human_readable)
	"""
	return len(x_raw)

while True:
    ret = run_classify(vocabulary,39)
    if (ret == 0):
        time.sleep(60)

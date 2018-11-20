from datetime import datetime
import numpy as np
import tensorflow as tf

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()
  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)
  return graph

def read_tensor_from_image_file(file_name):
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255
  file_reader = tf.read_file(file_name, "file_reader")
  image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)
  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def label_image(filename):
  file_name = filename
  model_file = "./meet/data/graph.pb"
  label_file = "./meet/data/labels.txt"
  graph = load_graph(model_file)
  t = read_tensor_from_image_file(file_name)
  input_operation = graph.get_operation_by_name("import/Placeholder")
  output_operation = graph.get_operation_by_name("import/final_result")
  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
  results = np.squeeze(results)
  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  ret = []
  for i in top_k:
    ret.append([labels[i], results[i]])
  return ret


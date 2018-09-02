from os.path import dirname, realpath
from threading import Thread
import tensorflow as tf


class SessionRunner:

    def __init__(self):
        self.__self_dir_path = dirname(realpath(__file__))
        self.__default_graph = tf.Graph()
        self.__thread = None
        self.__runnables = []

    def load(self, session_runnable):
        self.__runnables.append(session_runnable)
        with self.__default_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(session_runnable.get_path_to_frozen_graph(), 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name=session_runnable.get_name())

    def start(self):
        if self.__thread is None:
            self.__thread = Thread(target=self.__start)
            self.__thread.start()

    def stop(self):
        if self.__thread is not None:
            self.__thread.stop()
            self.__thread = None

    def __start(self):
        with self.__default_graph.as_default():
            with tf.Session(graph=self.__default_graph) as sess:
                while True:
                    for runnable in self.__runnables:
                        runnable.run(sess, self.__default_graph)




class SessionRunnable:
    def __init__(self, name, path_to_frozen_graph):
        self.__name = name
        self.__path_to_frozen_graph = path_to_frozen_graph

    def get_name(self):
        return self.__name

    def get_path_to_frozen_graph(self):
        return self.__path_to_frozen_graph

    def run(self, tf_sess, tf_default_graph):
        pass

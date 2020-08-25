from os import path

dir_path = path.dirname(path.realpath(__file__))

cnb_file_name = 'cnb_desc_clf.pickle'
svm_file_name = 'svm_desc_clf.pickle'
cnb = path.abspath(path.join(dir_path, '..', '..', 'model_output', cnb_file_name))
svm = path.abspath(path.join(dir_path, '..', '..', 'model_output', svm_file_name))

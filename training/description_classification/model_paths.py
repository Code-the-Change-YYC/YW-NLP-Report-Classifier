from os import path

dir_path = path.dirname(path.realpath(__file__))

cnb_file_name = 'cnb_desc_clf.pickle'
svm_file_name = 'svm_desc_clf.pickle'
cnb_dev_file_name = 'cnb_desc_clf.dev.pickle'
cnb_cli_file_name = 'cnb_desc_clf.cli.pickle'
cnb = path.abspath(
    path.join(dir_path, '..', '..', 'model_output', cnb_file_name))
cnb_dev = path.abspath(
    path.join(dir_path, '..', '..', 'model_output', cnb_dev_file_name))
svm = path.abspath(
    path.join(dir_path, '..', '..', 'model_output', svm_file_name))
cnb_cli = path.abspath(
    path.join(dir_path, '..', '..', 'model_output', cnb_cli_file_name))

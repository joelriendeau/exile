try:
    from PyQt4.QtGui import QApplication
except ImportError, e:
    raise RuntimeError("PyQT 4 is missing from your Python install. The UI extensions will not function properly.")
import sys
import os
from status_view import StatusView

def splitpath(path):
     ( head, tail ) = os.path.split(path)
     return splitpath(head) + [ tail ] \
         if head and head != path \
         else [ head or tail ]

def insert_in_dict(dict, path, val):
    cur_dict = dict
    split = splitpath(path)
    split_count = len(split)
    for i in range(split_count):
        if i < split_count - 1:
            cur_val = cur_dict.get(split[i])
            if cur_val == None:
                cur_dict[split[i]] = {}
                cur_dict = cur_dict[split[i]]
            else:
                cur_dict = cur_val
        else:
            cur_dict[split[i]] = val
    return

def apply_callback(result_dict):
    return None

def start_status_view(paths, filemap):
    app = QApplication([])

    content_dict = {}

    # compare filesystem content under path with content in manifest file (filemap object)
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                value = filemap.get(file_path)
                if value == None:
                    insert_in_dict(content_dict, file_path, "UNTRACKED")

    test_dict = {
        "content": {
            "file1": "UNTRACKED",
            "file2": "MODIFIED",
            "dir": {
                "file3": "UNTRACKED",
                "file4": "MODIFIED"
            },
            "dir2": {
                "file5": "UNTRACKED",
                "file6": "MODIFIED"
            }
        }
    }

    window = StatusView(content_dict, apply_callback)
    window.show()
    return app.exec_()
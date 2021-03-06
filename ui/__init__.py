try:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtGui import QMessageBox
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

paths = None
root_path = None
filemap = None
global_ignore = None
local_ignore = None
add_callback = None
resolve_callback = None
stop_track_callback = None
save_config = None
sync_remote = None
hash_callback = None

def confirm(text):
    reply = QMessageBox.question(None, 'Message',
        text, QMessageBox.Yes | 
        QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    return False
        
def apply_callback(result_dict):
    global paths, filemap, global_ignore, local_ignore, add_callback, resolve_callback

    ignore_glob = result_dict["ignore_glob"]
    for path in ignore_glob:
        global_ignore.add(path[0])

    ignore_loc = result_dict["ignore_loc"]
    for path in ignore_loc:
        local_ignore.add(path[0])

    to_add = result_dict["add"]
    for path in to_add:
        # do not add a directory, exile supports files only
        if not path[1] == "DIR":
            add_callback(path[0])

    to_resolve = result_dict["resolve"]
    for path in to_resolve:
        # do not add a directory, might resolve the same file twice
        if not path[1] == "DIR":
            resolve_callback({path[0]})

    to_stop_track = result_dict["stop_track"]
    for path in to_stop_track:
        # do not stop tracking a directory, they are not tracked anyway
        if not path[1] == "DIR":
            stop_track_callback(path[0])

    to_delete = result_dict["delete"]
    for path in to_delete:
        # do not delete directories ever, too dangerous
        if not path[1] == "DIR":
            question = "Are you sure you want to delete \"" + path[0] + "\" ?"
            confirmed = confirm(question)
            if confirmed:
                os.remove(path[0])

    save_config()
    sync_remote() # make sure all outstanding network operations are done

    return compute_content()

def compute_content():
    content_dict = {}

    global paths, root_path, filemap, global_ignore, local_ignore, stop_track_callback, hash_callback

    # compare filesystem content under path with content in manifest file (filemap object)
    for path in paths:
        tracked_files = filemap.paths(os.path.abspath(path))

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    tracked_files.remove(os.path.abspath(file_path))
                except:
                    pass
                
                if global_ignore != None:
                    value = global_ignore.get(file_path)
                    if value:
                        continue
                if local_ignore != None:
                    value = local_ignore.get(file_path)
                    if value:
                        continue

                value = filemap.get(file_path)
                if value == None:
                    insert_in_dict(content_dict, file_path, "UNTRACKED")
                else:
                    hash = hash_callback(file_path)
                    if value != hash:
                        insert_in_dict(content_dict, file_path, "MODIFIED")

        for missing in tracked_files:
            rel_path = os.path.relpath(missing, root_path)
            insert_in_dict(content_dict, rel_path, "MISSING")

    return content_dict

def start_status_view(paths_in, root_path_in, filemap_in, global_ignore_in, local_ignore_in, add_callback_in, resolve_callback_in, stop_track_callback_in, save_config_in, sync_remote_in, hash_callback_in):
    app = QApplication([])

    global paths, root_path, filemap, global_ignore, local_ignore, add_callback, resolve_callback, stop_track_callback, save_config, sync_remote, hash_callback
    paths = paths_in
    root_path = root_path_in
    filemap = filemap_in
    global_ignore = global_ignore_in
    local_ignore = local_ignore_in
    add_callback = add_callback_in
    resolve_callback = resolve_callback_in
    stop_track_callback = stop_track_callback_in
    save_config = save_config_in
    sync_remote = sync_remote_in
    hash_callback = hash_callback_in

    content_dict = compute_content()

    window = StatusView(content_dict, apply_callback)
    window.show()
    app.exec_()

    return global_ignore, local_ignore
import os
import json

def json_dict_update(fname, new_dict):
    if os.path.exists(fname):
        with open(fname) as f:
            dict_ = json.load(f)
    else:
        dict_ = {}

    dict_.update(new_dict)
    with open(fname, 'w') as f:
        json.dump(dict_, f)


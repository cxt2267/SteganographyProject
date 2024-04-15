import File
import re
import os
from DB import DB
from bitarray import bitarray

def createPost(post_info):
    db = DB()
    carr = post_info['carrier']
    msg = post_info['message']
    stbit = post_info['start_bit'].strip()
    per = post_info['period'].strip()
    
    mode = post_info['op_mode'].strip()
    post_name = post_info['post_name'].strip()
    user = post_info['user']

    if(post_name == ""):
        return "no post name"
    elif(not re.match(r'^[a-zA-Z0-9]+$', post_name)):
        return "invalid post name"
    elif(db.getPost(post_name) is not None):
        return "post name already in use"

    if(not mode.isnumeric()):
        return "invalid mode"
    elif((int(mode) != 1) and (int(mode) != 2)):
        return "invalid mode"
    else:
        mode = int(mode)

    if(not stbit.isnumeric()):
        return "invalid start bit"
    else:
        stbit = int(stbit)

    per_list = []
    per_values = per.split(',')
    for value in per_values:
        value = value.strip()
        if(not value.isnumeric()):
            return "invalid periodicity"
        else:
            per_list.append(int(value))
    
    if((mode == 1) and (len(per_list) > 1)):
        return "invalid mode and periodicity"
    if((mode == 2) and (len(per_list) == 1)):
        return "invalid mode and periodicity"

    carr_bits = bitarray()
    msg_bits = bitarray()

    carr_bits.fromfile(carr)
    msg_bits.fromfile(msg) 

    carr.seek(0)
    msg.seek(0)

    counter = 0
    i = stbit
    for j in range(len(msg_bits)):
        if(i >= len(carr_bits)): 
            break
        if counter == len(per_list):
            counter = 0
        carr_bits[i] = msg_bits[j]
        i += per_list[counter]
        counter += 1
    
    if not (len(msg_bits) == 0):
        if(j < len(msg_bits)-1):
            return "insufficient carrier size"
    
    with open(post_name, 'wb+') as post:
        carr_bits.tofile(post)
        post.seek(0)
        post_info = {
            "post": post,
            "carrier": carr,
            "message": msg,
            "stbit": stbit,
            "per": per,
            "user": user
        }
        File.savePost(post_info)
        db.addPost(post_info)

    os.remove(post_name)
    return "success"




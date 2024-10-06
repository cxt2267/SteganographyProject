import re
import os
import boto3
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

    carr_bits_orig = bitarray()
    msg_bits_orig = bitarray()
    carr_bits = bitarray()
    msg_bits = bitarray()

    carr_bits_orig.fromfile(carr)
    carr.seek(0)
    msg_bits_orig.fromfile(msg)
    msg.seek(0)
    carr_bits.fromfile(carr)
    msg_bits.fromfile(msg) 

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
    
    carr_name = carr.filename
    ext_ind = carr_name.rfind('.')
    ext = carr_name[ext_ind:]

    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket="stegaprojbucket", Key=f"user_{user}/{post_name}/")

    try:
        s3_client.put_object(Bucket="stegaprojbucket", Key=f"user_{user}/{post_name}/{post_name}{ext}", Body=carr_bits.tobytes())
        s3_client.put_object(Bucket="stegaprojbucket", Key=f"user_{user}/{post_name}/{carr.filename}", Body=carr_bits_orig.tobytes())
        s3_client.put_object(Bucket="stegaprojbucket", Key=f"user_{user}/{post_name}/{msg.filename}", Body=msg_bits_orig.tobytes())
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error writing to file: {e}")
    
    post_info = {
        "post": post_name,
        "carrier": carr,
        "message": msg,
        "stbit": stbit,
        "per": per,
        "user": user
    }

    db.addPost(post_info)

    return "success"

import dropbox

acc_tok = 'sl.BzF6R4Jl5RVDNn_12PKzubY-qeXXpKOAGFfwwhj4J3yTK43cXaeY3jAgkv3qeJPhkGh7s4iD5pjz-_gmyUpvRFDmuR7Ac2YLkm2O4762wzBVrfnRnqJGCdgfAZpxU4qde7XE7CwIH2p6QFk'
dbx = dropbox.Dropbox(acc_tok)

def createUserFold(id):
    dbx.files_create_folder_v2(f"/user_{id}")

def savePost(post_info):
    post = post_info["post"]
    carr = post_info["carrier"]
    msg = post_info["message"]
    user = post_info["user"]

    carr_name = carr.filename
    ext_ind = carr_name.rfind('.')
    ext = carr_name[ext_ind:]

    dbx.files_create_folder_v2(f"/user_{user}/{post.name}")
    dbx.files_upload(post.read(), f"/user_{user}/{post.name}/{post.name}{ext}")
    dbx.files_upload(carr.read(), f"/user_{user}/{post.name}/{carr.filename}")
    dbx.files_upload(msg.read(), f"/user_{user}/{post.name}/{msg.filename}")

def getPost(user, post_name, ext):
    path = f"/user_{user}/{post_name}/{post_name}{ext}"
    with open(f"static/posts/user_{user}/{post_name}{ext}", "wb") as post:
        metadata, file = dbx.files_download(path)
        post.write(file.content)


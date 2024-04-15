const acc_tok = 'sl.Bza84j4xvnFMdG-qWeKZdJePnawscRN3Dd5Ntl_DT3s8-6LPf_ypo6SGURc4gpFTLiSMpDkw79Fnh822FWBkHwTcc4bqroMeprrQVqTNoPSbe0tdIAxVoLIzfEulvqaxAER3jO95eK1N-FE';

function checkUser() {
    if(localStorage.getItem("user") === null) {
        window.location.href = "/login";
        return
    } else {
        return JSON.parse(localStorage.getItem("user"));
    }
}

async function getPost(file_path) {
    const file_name = file_path.match(/\/([^\/]+)$/)[1];
    const file_ext = file_name.split('.').pop();
    const img_ext = ['jpeg','jpg','png','gif','svg'];
    var link = document.createElement('a');
    link.download = file_name;
    var img = document.createElement('img');
    img.alt = file_name;
    img.style.width = "290px";
    img.style.height = "240px";
    var dbx = new Dropbox.Dropbox({ accessToken: acc_tok });
    return new Promise((resolve) => {
        dbx.filesDownload({ path: file_path })
        .then((resp) => {
            const blob = resp.result.fileBlob;//new Blob([resp.result]);
            const url = window.URL.createObjectURL(blob);
            link.href = url;
            if(img_ext.includes(file_ext)) {
                const fr = new FileReader();
                fr.readAsDataURL(blob);
                fr.onloadend = () => {
                    img.src = fr.result;
                }
                link.appendChild(img);
            }
            else {
                link.innerHTML = file_name;
            }
            resolve(link);
        });
    });
}    

function getPosts(user) {
    var option = '/all-posts';
    if(user !== null) {
        option = `/my-posts/${user}`;
    }
    var table = $('#posts');
    var columns = 0;
    var row = $('<tr>');
    fetch(option)
    .then(resp => resp.json())
    .then(posts => {
      posts = posts.posts;
      posts.forEach((post, i, list) => {
        getPost(post)
        .then(link => {
            console.log(link);
            if(columns === 4) {
                table.append(row);
                columns = 0;
                row = $('<tr>');
            }
            row.append($('<td>').append(link));
            if(i === list.length - 1) {
                table.append(row);
            }
            columns ++;
        }); 
      })
    })
  }

export function checkUser() {
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
    const img_ext = ['jpeg','jpg','png','gif','svg','webp'];
    var link = document.createElement('a');
    link.download = file_name;
    var img = document.createElement('img');
    img.alt = file_name;
    img.style.width = "290px";
    img.style.height = "240px";
    return new Promise((resolve) => {
        fetch(`/fileblob?file_path=${encodeURIComponent(file_path)}`)
        .then(resp => resp.blob())
        .then(file_content => {
            const url = URL.createObjectURL(file_content);
            link.href = url;
            if(img_ext.includes(file_ext)) {
                const fr = new FileReader();
                fr.readAsDataURL(file_content);
                fr.onloadend = () => {
                    img.src = fr.result;
                }
                link.appendChild(img);
            }
            else {
                link.innerHTML = file_name;
            }
            resolve(link);
        })
    });
}    

export function getPosts(user) {
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

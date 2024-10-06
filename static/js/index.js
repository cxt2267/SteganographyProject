import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

function checkUser() {
    if(localStorage.getItem("user") === null) {
        window.location.href = "/login";
        return
    } else {
        return JSON.parse(localStorage.getItem("user"));
    }
}

const s3Client = new S3Client({ region: 'us-east-1' });

async function getFileBlob(file_path) {
    try {
        const command = new GetObjectCommand({
            Bucket: "stegaprojbucket",
            Key: file_path
        });
        
        const { Body } = await s3Client.send(command);

        const chunks = [];
        for await (const chunk of Body) {
            chunks.push(chunk);
        }

        return new Blob(chunks);
    } catch (err) {
        console.error("Error retrieving file from S3: ", err);
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
    return new Promise((resolve) => {
        getFileBlob(file_path)
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

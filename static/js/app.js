const plus = document.querySelector('.add_post'),
    add_post = document.querySelector('.new_posts'),
    back = document.querySelector('.back');


plus.addEventListener('click', () => {
    add_post.classList.add('display');
});

back.addEventListener('click', () => {
    add_post.classList.remove('display');
});


const comment_icon = document.querySelectorAll('.comment'),
open_post = document.querySelector('.open_post'),
back2 = document.querySelector('.back2'),
open_post_src = document.querySelector('.open_post_src'),
data_get = document.querySelector('.data_get');

// comment_icon.forEach((comic, index) =>{
//     comic.addEventListener('click', () => {
//         open_post.classList.add('display')
//         fetch('/get_post/' + comic.dataset.id, {

//             method: "POST",
//             body: JSON.stringify({
//                 "post_id": comic.dataset.id
//             }),
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })
        
//             // .then(function (response) {
//             //     return response.json()

//             // })
//             // .then(function (jsonResponse) {
//             //     if (open_post_src[index]) {
//             //         open_post_src[index].textContent = `${{{user1.posts[comic.dataset.id].post_img}}}`
//             //     }
//             //     console.log(count_like.textContent)
//             //     if (jsonResponse['like'] === 'False') {
//             //         ht.style.fill = 'rgb(41, 41, 41)'
//             //         console.log(jsonResponse['like'])
//             //         console.log('black')
//             //     } else {
//             //         ht.style.fill = 'red'
//             //         console.log(jsonResponse['like'])
//             //         console.log('red')
//             //     }
//             // })
//     })
//     
// })
back2.addEventListener('click', () => {
            open_post.style.display='none';
        });

const change_btn = document.querySelector('.img'),
    change_photo = document.querySelector('.change_photo'),
    cancel = document.querySelector('.cancel');
if (change_btn) {
    change_btn.addEventListener('click', () => {
        change_photo.classList.add('active_flex')
    })
}
if (cancel) {
    cancel.addEventListener('click', () => {
        change_photo.classList.remove('active_flex');
    });
}


const heart = document.querySelectorAll('.heart');
let count_like = document.querySelectorAll('.count_like');

heart.forEach((ht, index) => {
    ht.addEventListener('click', () => {
        console.log(ht.dataset.id)
        fetch('/like/' + ht.dataset.id, {

            method: "POST",
            body: JSON.stringify({
                "liked": 'true'
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(function (response) {
                return response.json()

            })
            .then(function (jsonResponse) {
                if (count_like[index]) {
                    count_like[index].textContent = `${jsonResponse['count']}`
                }
                console.log(count_like.textContent)
                if (jsonResponse['like'] === 'False') {
                    ht.style.fill = 'rgb(41, 41, 41)'
                    console.log(jsonResponse['like'])
                    console.log('black')
                } else {
                    ht.style.fill = 'red'
                    console.log(jsonResponse['like'])
                    console.log('red')
                }
            })

    })
});


const post_next = document.querySelector('.post_next'),
    post_content = document.querySelector('.post_ct'),
    label = document.querySelector('#label'),
    x = document.querySelector('.x_bold');

if (post_next) {
    post_next.addEventListener('click', () => {
        post_content.classList.add('display');
    });

    post_next.addEventListener('click', () => {
        add_post.style.display = 'none';
    });
}

x.addEventListener('click', () => {
    post_content.classList.remove('display');
});

if (label) {
    label.addEventListener('click', () => {
        post_next.style.display = 'flex'
    });
}


const follow_btn = document.querySelectorAll('.fw_btn');


follow_btn.forEach(i => {
    i.addEventListener('click', () => {
        if (i.value === 'Follow' || i.style.color === '#0095f6') {
            i.value = 'Following';
            i.style.color = '#999';
        } else {
            i.value = 'Follow'
            i.style.color = '#0095f6';
        }

    })
})



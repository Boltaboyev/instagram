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
    data_get = document.querySelector('.data_get'),
    post_owner_img = document.querySelector('.post_owner_img'),
    post_owner_name = document.querySelector('.post_owner_name'),
    like_bold = document.querySelector('.like_bold');

comment_icon.forEach((comic, index) => {
    comic.addEventListener('click', () => {
        open_post.classList.add('display')
        fetch('/get_post/' + comic.dataset.id, {

            method: "POST",
            body: JSON.stringify({
                "post_id": comic.dataset.id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })

            .then(function (response) {
                return response.json()

            })
            .then(function (jsonResponse) {
                console.log(jsonResponse['post_open_img'])
                console.log(jsonResponse['users'])
                open_post_src.innerHTML = `<img src="/${jsonResponse['post_open_img']}" alt="">`
                post_owner_img.innerHTML = `<img src="/${jsonResponse['post_open_owner_img']}" alt="">`
                post_owner_name.innerHTML = `<p> <a style="text-decoration:none; color:black" href="{{url_for('view_user', user_id=${jsonResponse['post_open_owner']})}}"><strong>${jsonResponse['post_open_owner_username']}</strong></a></p>`
                like_bold.innerHTML = `<svg class="heart" data-id="${jsonResponse['post_open_id']}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path d="M0 190.9V185.1C0 115.2 50.52 55.58 119.4 44.1C164.1 36.51 211.4 51.37 244 84.02L256 96L267.1 84.02C300.6 51.37 347 36.51 392.6 44.1C461.5 55.58 512 115.2 512 185.1V190.9C512 232.4 494.8 272.1 464.4 300.4L283.7 469.1C276.2 476.1 266.3 480 256 480C245.7 480 235.8 476.1 228.3 469.1L47.59 300.4C17.23 272.1 .0003 232.4 .0003 190.9L0 190.9z"/>
            </svg>`
            })
    })

})
back2.addEventListener('click', () => {
    open_post.classList.remove('display');
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
                    count_like[index].textContent = `${jsonResponse['count']} `
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



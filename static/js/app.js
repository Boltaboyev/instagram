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
    post_like_bold = document.querySelector('.post_like_bold'),
    post_count_like = document.querySelector('.post_count_like'),
    heart1 = document.querySelector('.heart1');

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
                console.log(comic.dataset.id)
                open_post_src.innerHTML = `<img src="/${jsonResponse['post_open_img']}" alt="">`
                post_owner_img.innerHTML = `<img src="/${jsonResponse['post_open_owner_img']}" alt="">`
                post_owner_name.innerHTML = `<p> <a style="text-decoration:none; color:black" href="{{url_for('view_user', user_id=${jsonResponse['post_open_owner']})}}"><strong>${jsonResponse['post_open_owner_username']}</strong></a></p>`
                
                post_count_like.innerHTML = `${jsonResponse['post_open_like_count']}`

                heart1.addEventListener('click', () => {
                    fetch('/like/' + comic.dataset.id, {
            
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
                            if (post_count_like) {
                                post_count_like.textContent = `${jsonResponse['count']} `
                            }
                            if (jsonResponse['like'] === 'False') {
                                heart1.style.fill = 'rgb(41, 41, 41)'
                                console.log(jsonResponse['like'])
                                console.log('black')
                            } else {
                                heart1.style.fill = 'red'
                                console.log(jsonResponse['like'])
                                console.log('red')
                            }
                        })
            })
            const post_button = document.querySelector('.post_button'),
                comment_text = document.querySelector('.comment_text'),
                commented_text = document.querySelector('.commented_text')
            post_button.addEventListener('click', ()=>{
                fetch('/add_comment/'+ comic.dataset.id, {
                    method: "POST",
                        body: JSON.stringify({
                            "comment_text": comment_text.value
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                })
                .then(function (response) {
                    return response.json()
    
                })
                .then(function (jsonResponse) {
                    comment_text.innerHTML = `${comment_text.value}`
                })
})
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



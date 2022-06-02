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
    heart1 = document.querySelector('.heart1'),
    commented_text = document.querySelector('.commented_text'),
    comment_owner_img = document.querySelector('.comment_owner_img'),
    comment_owner_name = document.querySelector('.comment_owner_name'),
    comment_owner_text = document.querySelector('.comment_owner_text'),

    comments = document.querySelector('.comments');
comment_icon.forEach((comic, index) => {
    comic.addEventListener('click', () => {
        comments.innerHTML = ''
        open_post.classList.add('display')
        let post_id = comic.dataset.id
        const controller = new AbortController()
        const signal = controller.signal
        fetch('/get_post/' + post_id, {

            method: "GET",
            signal: signal

        })

            .then(function (response) {
                return response.json()

            })
            .then(function (jsonResponse) {
                open_post_src.innerHTML = `<img src="/${jsonResponse['post_open_img']}" alt="">`
                post_owner_img.innerHTML = `<img src="/${jsonResponse['post_open_owner_img']}" alt="">`
                post_owner_name.innerHTML = `<p> <a style="text-decoration:none; color:black" href="{{url_for('view_user', user_id=${jsonResponse['post_open_owner']})}}"><strong>${jsonResponse['post_open_owner_username']}</strong></a></p>`
                // comment_owner_img.innerHTML = `<img src="/${jsonResponse['post_open_owner_img']}" alt="">`
                post_count_like.innerHTML = `${jsonResponse['post_open_like_count']}`
                const post_time = document.createElement("div")
                post_time.innerHTML = `${jsonResponse['post_differ_str']} ago`;
                post_time.style.cssText = "position: absolute; left: 20px; bottom: 100px; font-style:italic; color: #666; font-size: smaller;"
                document.querySelector('.third_raw').appendChild(post_time)
                console.log(jsonResponse['comment_list'])
                console.log(comic.dataset.id)
                jsonResponse['comment_list'].forEach((element, index) => {
                    // const commented_owner_name = document.createElement("div"),
                    //     comment_owner_img = document.createElement("div"),
                    //     comment_owner_text = document.createElement("div");
                    console.log(element['commented_ago'])
                    comments.innerHTML += `<div class="commented_text"><div class="comment_owner_img">
                                                    
                                                    <img style="width: 50px; height: 50px; border-radius: 50%; border: #000 solid 1px;" src="/${element['owner_img']}" alt="">
                                                </div>
                                                <div>
                                                    <p class="comment_owner_name"><strong>${element['owner_username']}</strong></p>
                                                    <p class="comment_owner_text">${element['comment_text']}</p>
                                                    <p  class="comment_time">${element['comment_differ_str']} ago</p>
                                                </div></div>`
                })

                heart1.addEventListener('click', () => {
                    fetch('/like/' + post_id, {

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
                    comment_text = document.querySelector('.comment_text')

                post_button.addEventListener('click', () => {
                    fetch('/add_comment/' + post_id, {
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
                            jsonResponse['comment_text']
                            const para = document.createElement("div");
                            console.log(post_id)
                            para.innerHTML = `<div class="comment_owner_img">
                                                    
                                <img style="width: 50px; height: 50px; border-radius: 50%; border: #000 solid 1px;" src="/${jsonResponse['owner_img']}" alt="">
                            </div>
                            <div>
                                <p class="comment_owner_name"><strong>${jsonResponse['owner_username']}</strong></p>
                                <p class="comment_owner_text">${jsonResponse['comment_text']}</p>
                                <p  class="comment_time">0m ago</p>
                            </div>`;
                            para.style.cssText = "width: 92%; background-color: #666; background: #fff; display: flex; border: #000 solid 2px; border-radius: 5px; padding: 0 12px;"
                            document.querySelector('.comments').appendChild(para)
                            comment_text.value = ''
                        })
                })

            })
        back2.addEventListener('click', () => {
            open_post.classList.remove('display');
            post_id = 0;
            controller.abort();
        });
    })
})


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



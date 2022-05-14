const plus = document.querySelector('.add_post'),
    add_post = document.querySelector('.new_posts'),
    back = document.querySelector('.back');


plus.addEventListener('click', () => {
    add_post.classList.add('display')
});

back.addEventListener('click', () => {
    add_post.classList.remove('display')
});


const change_btn = document.querySelector('.img'),
    change_photo = document.querySelector('.change_photo'),
    cancel = document.querySelector('.cancel');

change_btn.addEventListener('click', () => {


    function change_img() {
        change_photo.classList.add('active_flex')
    }

    setTimeout(change_img, 400)
})


cancel.addEventListener('click', () => {
    change_photo.classList.remove('active_flex')
})

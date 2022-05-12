
const plus = document.querySelector('.add_post'),
    add_post = document.querySelector('.new_posts'),
    back = document.querySelector('.back');


plus.addEventListener('click', () => {
    add_post.classList.add('display')
});

back.addEventListener('click', () => {
    add_post.classList.remove('display')
});

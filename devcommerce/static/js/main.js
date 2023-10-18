const showLoad = document.querySelector('.loader');

window.addEventListener('load', () => {
    setTimeout(() => {
        showLoad.classList.add('disappear')
    }, 2000)
})



function change() {
    const subs = document.getElementById('subscriberBtn');
    subs.innerText = '구독중'
}

const subs = document.getElementById("subscriberBtn")

subs.addEventListener("click", function () {
    if (subs.innerText === '구독') {
        subs.innerText = '구독중';
    } else subs.innerText = '구독';
});

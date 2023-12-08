/* 202031207 */
function visible(elements) {
    /* binary search to find the first visible image */
    let l = 0, r = elements.length - 1;
    while (l < r) {
        const m = ((l + r) / 2) | 0;
        const rect = elements[m].getBoundingClientRect();
        if (rect.top < 0) { l = m + 1; } else { r = m; }
    }
    return l;
}
const key = window.location.pathname;
let images = [];
let timedout = false;
function loaded() {
    images = document.querySelectorAll('img');
    const local = localStorage.getItem(key);
    if (!+local) return;
    console.log('Got: ', +local);
    images[+local].addEventListener('load', e => e.target.scrollIntoView());
}
function scrollend() {
    /* run only once per at least one second */
    if (timedout) return;
    timedout = true; setTimeout(() => timedout = false, 1000);
    const i = visible(images);
    console.log('Set: ', i);
    localStorage.setItem(key, i);
}
document.addEventListener('scrollend', scrollend);
document.addEventListener('DOMContentLoaded', loaded);
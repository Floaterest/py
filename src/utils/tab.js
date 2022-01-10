// tab.js
const cs = Array.from(document.getElementsByClassName('chapter'));
const ss = Array.from(
    document.getElementById('select').getElementsByTagName('p')
);

// show/hide selection menu
cs.forEach(ch => ch.addEventListener('click', () => {
    if(document.body.classList.toggle('dimmed')){
        ss.forEach(p => p.classList.toggle('selected', p.innerText == ch.id));
    }
}));

// show/hide chapters
ss.forEach(p => p.addEventListener('click', () => {
    p.classList.toggle('dimmed');
    document.getElementById(p.innerText).classList.toggle('hidden');
}));

// click all the selections
document.getElementById('invert')
    .addEventListener('click', () => ss.forEach(p => p.click()));

const nav = document.body.appendChild(document.createElement('nav'))
const sections = new Map();
const buttons = new Map();

// document.body.prepend(navigator.userAgent)

// Click on button ==> toggle section visibility
for (section of document.querySelectorAll('section')) {
    const b = nav.appendChild(document.createElement('button'))
    const { id } = section
    sections[b.innerText = id] = section
    b.onclick = e => {
        sections[id].classList.toggle('hidden')
        e.target.classList.toggle('hidden')
    }
    buttons[id] = b;
}

// Click on image ==> show selected section
let selected;
document.querySelectorAll('img').forEach(i => i.onclick = _ => {
    const { id } = i.parentElement;
    selected?.classList.toggle('selected');
    selected = buttons[id];
    selected.classList.toggle('selected');
    document.body.classList.toggle('dimmed')
})

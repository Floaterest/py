const navl = document.body.appendChild(document.createElement('nav'))
navl.style = 'left: 0; top: 0;'
const sections = {};
const buttons = {};

// Click on button ==> toggle section visibility
for (section of document.querySelectorAll('section')) {
    const b = navl.appendChild(document.createElement('button'))
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

const navr = document.body.appendChild(document.createElement('nav'))
navr.style = 'right: 0; bottom: 0'

let sorted = true

const rand = navr.appendChild(document.createElement('button'))
rand.innerText = 'shuf'
rand.onclick = _ => {
    for (const [k, section] of Object.entries(sections).sort(() => Math.random() - 0.5)) {
        const button = buttons[k];
        document.body.appendChild(section);
        navl.appendChild(button);
    }
    sorted = false;
}

const sort = navr.appendChild(document.createElement('button'))
sort.innerText = 'sort'
sort.onclick = _ => {
    for (const key of sorted ? Object.keys(sections).sort().reverse() : Object.keys(sections).sort()) {
        const [section, button] = [sections[key], buttons[key]];
        document.body.appendChild(section);
        navl.appendChild(button);
    }
    sorted = !sorted;
}

const inv = navr.appendChild(document.createElement('button'))
inv.innerText = 'inv'
inv.onclick = _ => Object.values(buttons).forEach(b => b.click())

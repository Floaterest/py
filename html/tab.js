// tab.js version 20210320
const content = document.getElementById('content');
const select = document.getElementById('select');

// show/hide selection menu
content.addEventListener('click', () => {
    if(content.style.filter){
        content.style.filter = select.style.display = '';
    }else{
        content.style.filter = 'brightness(10%)';
        select.style.display = 'inline';
    }
});

// show/hide chapters
Array.from(select.getElementsByTagName('p')).forEach(
    p => p.addEventListener('click', () => {
        p.classList.toggle('off');
        document.getElementById(p.innerText)
            .style.display = p.classList.contains('off') ? 'none' : 'block';
    })
);

// click all the selections
document.getElementById('invert').addEventListener('click',
    () => Array.from(select.getElementsByTagName('p')).forEach(p => p.click())
);

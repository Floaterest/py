// version 20210320
Array.from(document.getElementsByTagName('img')).forEach(
    i => i.addEventListener('click',
        () => i.src = i.getAttribute('src') ? '' : i.alt
    )
);
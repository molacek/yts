function init() {
    page = 1;
    document.getElementById('page_counter').innerHTML = page;
    readPage(page);
}

function nextPage() {
    page += 1;
    document.getElementById('page_counter').innerHTML = page;
    readPage(page);
}

function prevPage() {
    if ( page == 1) {
        return;
    }
    page -= 1;
    document.getElementById('page_counter').innerHTML = page;
    readPage(page);
}

function readPage(index) {
    //return;
    req = new XMLHttpRequest();
    req.open("POST", "api/page/" + index, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            renderThumbnails(JSON.parse(req.responseText));
        }
    }
    req.send()
}

function renderThumbnails(data) {
    var content = document.getElementById('content');
    content.innerHTML = "";
    for (var a in data) {
        var img = document.createElement('img');
        var link = document.createElement('a');
        img.src = data[a].thumbnail;
        link.href = 'movie/' + data[a].href;
        link.appendChild(img);
        content.appendChild(link);
    }
    document.getElementById('navigation').style.display = 'block';
}

page = 1;

function download(torrent_id) {
    req = new XMLHttpRequest();
    req.open("POST", "../api/download/" + torrent_id, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            var div = document.createElement('div');
            div.innerHTML = req.responseText;
            document.getElementById('download').appendChild(div);
        }
    }
    req.send()
}

function hashChanged() {
   // Clean content
   document.getElementById('content').innerHTML = '';
   //Extract page hash
   let hash = window.location.hash;
   let regex_page = /page\/([0-9]*)/;
   regex_page_match = regex_page.exec(hash);
   if (regex_page_match) {
       page = parseInt(regex_page_match[1]);
       console.log("Page from URL: " + page);
   } else {
       console.log("No page defined, reading page 1");
       page = 1;
   }
   document.getElementById('page_counter').innerHTML = page;
   readPage(page);
}

function init() {
    window.onhashchange = hashChanged;
    document.getElementById('search_input').addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            movieSearch();
        }
        }
    )
    hashChanged();
}

function movieSearch() {
    page=1;
    readPage(page);
}

function nextPage() {
    page += 1;
    document.location.hash = "page/" + page;
}

function prevPage() {
    if ( page == 1) {
        return;
    }
    page -= 1;
    document.location.hash = "page/" + page;
}

function readPage(index) {
    let req = new XMLHttpRequest();
    let search = document.getElementById("search_input").value;
    req.open("POST", "api/page/" + index, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            renderThumbnails(JSON.parse(req.responseText));
        }
    }
    req.send("search=" + search)
}

function renderThumbnails(data) {
    var content = document.getElementById('content');
    content.innerHTML = "";
    for (var a in data) {
        var img = document.createElement('img');
        var link = document.createElement('a');
        img.src = data[a].thumbnail;
        link.href = 'movie/' + data[a].href;
        link.className = "movielink";
        link.appendChild(img);
        content.appendChild(link);
    }
    document.getElementById('navigation').style.display = 'block';
}

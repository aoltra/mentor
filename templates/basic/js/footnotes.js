(function () {
    
    var oldOnLoad = window.onload;
    window.onload = function (event) {
        if (document.getElementsByClassName) {
            var elems = document.getElementsByClassName("footnote-citation");
            for (var i = 0; i<elems.length; i++) {
                var elem = elems[i];
                var ptrText = elem.innerHTML;
    
                elem.onclick = toggle;
                elem.setAttribute("href", "#"+ptrText);
            }

            addListItemIds("footnotes");
        }

        if (typeof oldOnLoad === "function") {
            oldOnLoad(event);
        }
    };
    
    function addListItemIds(parentId) {
        var refs = document.getElementById(parentId);
        if (refs && refs.getElementsByTagName) {
            var elems = refs.getElementsByTagName("li");
            for (var i = 0; i<elems.length; i++) {
                var elem = elems[i];
                elem.setAttribute("id", (i+1));
            }
        }
    }
    
    var currentDiv = null;
    var currentId = null;
    function toggle(event) {
        var parent = this.parentNode;
        if (currentDiv) {
            parent.removeChild(currentDiv);
            currentDiv = null;
        }
        var footnoteId = this.innerHTML;
        if (currentId === footnoteId) {
            currentId = null;
        } else {
            currentId = footnoteId;
            currentDiv = document.createElement("div");
            var footHtml = document.getElementById(footnoteId).innerHTML;
            currentDiv.innerHTML = footHtml;                        
            currentDiv.className = "footnote-body";
            parent.insertBefore(currentDiv, this.nextSibling);
            setTimeout(function () {
                currentDiv.style.opacity = "1";
            }, 0);
        }
        event.preventDefault();
    }
}());
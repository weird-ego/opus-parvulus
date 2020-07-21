const byId = (id) => { return document.getElementById(id); };
const E = (tag, root, init) => {
    let elem = document.createElement(tag);
    if (init)
        init(elem);
    if (root)
        root.appendChild(elem);
    return elem;
};
const log = (obj) => { console.log(JSON.parse(JSON.stringify(obj))); };
const isStr = (obj) => { return typeof obj === 'string' || obj instanceof String; };
const with_class = (cls) => (e) => { e.className = cls; };
const with_inner = (text) => (e) => { e.innerHTML = text; };

const byId = (id) => { return document.getElementById(id); };
const with_class = (cls) => (e) => { e.className = cls; };
const with_inner = (text) => (e) => { e.innerHTML = text; };
const with_both = (cls, text) => (e) => { e.className = cls; e.innerHTML = text };
const stripto = (n) => (s) => {
    if(s.length > n) {
        return `${s.slice(0, n-3)}...`;
    } else {
        return s;
    }
};
const checked = (f) => {
    return function() {
        if (this.status != 200) {
            alert(this.responseText);
        } else {
            f(this.response);
        }
    };
};
const E = (tag, root, init) => {
    let elem = document.createElement(tag);
    if (init)
        init(elem);
    if (root)
        root.appendChild(elem);
    return elem;
};
const fetch = (url, cb) => {
    let xhr = new XMLHttpRequest();
    xhr.onload = cb;
    xhr.open("GET", url);
    xhr.send();
    return false;
};
const send = (method, url, data, cb) => {
    const csrftoken = Cookies.get('csrftoken');
    const xhr = new XMLHttpRequest();
    const fd = new FormData();

    xhr.onload = cb;
    for (const key in data)
        fd.append(key, data[key]);

    fd.append('csrfmiddlewaretoken', csrftoken);
    xhr.open(method.toUpperCase(), url);
    xhr.send(fd);
};
const fetch_posts = () => {
    const signed = JSON.parse(byId("is-auth").textContent);
    const root = byId("posts");
    if (!signed)
        E("a", root, with_both("btn btn-outline-primary my-2", "sign")).href = "/sign/";
    const grid = E('div', root, with_class("container"));
    const strip = stripto(8);
    const callback = checked(r => {
        const posts = JSON.parse(r);
        posts.map(({ id, title, link, upvotes }) => {
            const post_box = E('div', grid, with_class("row"));
            const a = E('a', post_box, with_class("col-sm-4"));
            a.href = '/post/' + id;
            a.innerHTML = strip(title);
            const linkto = E('a', post_box, with_class("col-sm-4"));
            linkto.href = link;
            linkto.innerHTML = strip(link);
            const votes = E('div', post_box, with_class("col-sm-4 text-info"));
            votes.innerHTML = upvotes;
        });
        if (signed) {
            const formbox = E('div', root, with_class('form-signin'));
            const form = E('form', formbox, e => {
                e.setAttribute('method', 'POST');
                e.setAttribute('action', '/api/posts/');
                e.onsubmit = () => {
                    const data = {
                        'title': byId('title').value,
                        'link': byId('link').value,
                        'author_name': JSON.parse(byId("author").textContent)
                    };
                    send('POST', '/api/posts/', data, _ => location.reload());
                    return false;
                };
            });
            const head = E('div', form, with_class("text-center"));
            const h1 = E("h1", head, with_class("h5 mt-3 font-weight-normal"));
            const p1 = E("p1", h1, with_inner("create new post"));
            const title_group = E('div', form, with_class("form-label-group"));
            E('input', title_group, e => {
                e.setAttribute('type', 'text');
                e.setAttribute('name', 'title');
                e.id = 'title';
            });
            E('label', title_group, e => {
                e.setAttribute('for', 'title');
                e.innerHTML = 'title';
            });
            const link_group = E('div', form, with_class("form-label-group"));
            E('input', link_group, e => {
                e.setAttribute('type', 'text');
                e.setAttribute('name', 'link');
                e.id = 'link';
            });
            E('label', link_group, e => {
                e.setAttribute('for', 'link');
                e.innerHTML = 'link';
            });
            E('input', form, e => {
                e.setAttribute('type', 'submit');
                e.className = "btn btn-lg btn-primary btn-block";
            });
            E("a", root, with_both("btn btn-outline-primary", "logout")).href = "/signout/";
        }
    });
    fetch("/api/posts/", callback);
};
const fetch_post = (id) => {
    const root = byId("post");
    const signed = JSON.parse(byId("is-auth").textContent);
    const callback = checked(r => {
        const post = JSON.parse(r);
        const post_root = E('div', root, with_class("p-2"));
        const comments_root = E('div', root);
        const strip = stripto(10);
        const callback = checked(r => {
            const comments = JSON.parse(r);

            E('div', post_root, with_both("border-bottom border-primary mt-2", post.title));
            E('br', post_root);

            E('a', post_root, with_both("pb-2", post.link)).href = post.link;
            E('br', post_root);

            if (signed) {
                const span = E('span', post_root);

                E('button', span, with_both("btn btn-outline-primary m-2", `upvoted ${post.upvotes}`));
                const upvote = E('button', span, with_both("btn btn-outline-primary m-2", 'upvote'));
                upvote.onclick = () => {
                    send("POST", "/api/upvote/" + post.id + '/', {}, _ => location.reload());
                };

                E('br', post_root);

                const comment_field = E('textarea', post_root, e => {
                    e.id = 'comment_field';
                    e.className = "border-primary my-2 border-top";
                });
                E('br', post_root);

                E('button', post_root, e => {
                    e.onclick = () => {
                        const data = {
                            'post': post.id,
                            'author_name': JSON.parse(byId("author").textContent),
                            'content': byId("comment_field").value
                        };
                        send('POST', '/api/comments/', data, _ => location.reload());
                    };
                    e.innerHTML = "comment";
                    e.className = "btn btn-outline-primary";
                });
            };

            comments.map(({ author_name, content }) => {
                const comment_root = E('div', comments_root, with_class("container py-1"));
                E('div', comment_root, with_both("text-primary", author_name));
                E('div', comment_root, with_both("text-info", content));
            });

            E('a', root, with_inner('back')).href = '/';
        });
        fetch('/api/related_comments/' + post.id, callback);
    });
    fetch("/api/posts/" + id, callback);
};

const ok_status = 200;
const ok_msg = 'ok';

const send_fd = (method, url, data, cb) => {
    const csrftoken = Cookies.get('csrftoken');
    const xhr = new XMLHttpRequest();
    const fd = new FormData();

    xhr.onload = cb;
    for (const key in data)
        fd.append(key, data[key]);

    xhr.open(method.toUpperCase(), url);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(fd);

    return false;
};

const send_qs = (method, url, data, cb) => {
    const csrftoken = Cookies.get('csrftoken');
    const xhr = new XMLHttpRequest();

    xhr.onload = cb;
    let qs = [];
    for (const key in data)
        qs.push(`${key}=${data[key]}`);

    xhr.open(method.toUpperCase(),
             (qs.length > 0) ? `${url}?${qs.join('&')}` : url);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();

    return false;
};

const get = (url, cb) => {
    const xhr = new XMLHttpRequest();
    xhr.onload = cb;
    xhr.open('GET', url);
    xhr.send();
};

const checked = (f) => {
    return function() {
        if (this.status != ok_status) {
            alert(this.responseText);
        } else {
            f(this.response);
        }
    };
};

const anon_dialog = () => {
    const root = byId("root");
    root.innerHTML = "";

    const form = E("form", root, with_class("form-signin"));

    const head_section = E("div", form, with_class("text-center mb-4"));
    E("h1", head_section, with_class("h3 mb-3 font-weight-normal"));
    E("p1", head_section, with_inner("weather app"));

    const username_section = E("div", form, with_class("form-label-group"));
    E("input", username_section, e => e.id = "username");
    E("label", username_section, e => {
        e.innerHTML = "username";
        e.for = "username";
    });

    const password_section = E("div", form, with_class("form-label-group"));
    E("input", password_section, e => {
        e.id = "password";
        e.type = "password";
    });
    E("label", password_section, e => {
        e.innerHTML = "password";
        e.for = "password";
    });

    E("button", form, e => {
        e.innerHTML = "signin";
        e.onclick = signin;
        e.className = "btn btn-lg btn-primary btn-block";
    });

    E("br", form);

    E("button", form, e => {
        e.innerHTML = "signup";
        e.onclick = signup;
        e.className = "btn btn-lg btn-primary btn-block";
    });
};

const wrap_ws = (sub) => {
    return {
        'city_name': sub['city__name'],
        'weather': sub['weather__name'],
        'temperature': sub['temperature'],
        'id': sub['subscription']
    };
}

const fetch_fill_data = (component) => {
    get('/facade/cities/', checked(response => {
        let cities = JSON.parse(response)['cities'];
        get('/facade/weather_state/', checked(response => {
            let weather_state = JSON.parse(response)['weather_state'];

            const uid = JSON.parse(byId('user_id').textContent);
            const socket = new WebSocket('ws://' + location.host + '/dashboard/subscribe/' + uid);

            socket.addEventListener('message', e => {
                component.atomic(
                    'weather_state', _ => JSON.parse(e.data)['data']
                );
            });

            component.batch([
                ['cities', _ => cities],
                ['weather_state', _ => weather_state.map(wrap_ws)],
            ]);
        }));
    }));
};

const signed_dialog = (_) => {
    const root = byId("root");
    root.className = "text-center mb-4";
    root.innerHTML = "";

    const weather_root = E('div', root);
    const initial_state = {
        'cities': [],
        'weather_state': [],

        // display state
        'expanded': false
    };
    const weather_app = new Component(weather_root, initial_state);

    const subscribe_btn_init = (city_id) => (e) => {
        e.innerHTML = "subscribe";
        e.className = "btn btn-outline-primary btn-sm";
        e.onclick = () => {
            const data = {city_id: city_id};
            const callback = checked(r => {
                weather_app.atomic(
                    'weather_state', s => {
                        if (r != '{}')
                            s.push(JSON.parse(r));
                        return s;
                });
            });
            send_fd('post', '/facade/subscription/', data, callback);
        };
    };
    const unsubscribe_btn_init = (subscription_id) => (e) => {
        e.innerHTML = "unsubscribe";
        e.className = "btn btn-outline-primary btn-sm";
        e.onclick = () => {
            const data = {subscription_id: subscription_id};
            const callback = checked(r => {
                weather_app.atomic(
                    'weather_state', s => s.filter(e => e.id != subscription_id)
                );
            });
            send_qs('delete', '/facade/subscription/', data, callback);
        };
    };

    const cities_btn_init = (state) => (e) => {
        e.id = "cities_btn";
        if (state.expanded) {
            e.className = "btn btn-primary";
            e.setAttribute("aria-expanded", "true");
        } else {
            e.className = "btn btn-primary collapsed";
            e.setAttribute("aria-expanded", "false");
        };
        e.setAttribute("type", "button");
        e.setAttribute("data-toggle", "collapse");
        e.setAttribute("data-target", "#cities_box");
        e.setAttribute("aria-controls", "cities_box");
        e.innerHTML = "&nbsp;&nbsp;cities&nbsp;&nbsp;";
        e.onclick = () => { state.expanded = !state.expanded; };
    };

    weather_app.register((state, dom) => {
        with(state) {

            const toggle_cities = E('button', dom, cities_btn_init(state));

            let cities_box = E('div', dom, e => {
                e.id = "cities_box";
                if (expanded) {
                    e.className = "collapse show";
                } else {
                    e.className = "collapse";
                }
            });

            let dashboard = E('div', dom, with_class('py-1'));

            let subscribed = weather_state.map(e => e.city_name);
            let notin = (city) => !subscribed.includes(city.name);

            const btn_sm = with_class("btn btn-outline-primary btn-sm");

            cities.filter(notin).map(({ name, id }) => {
                const city_container = E("div", cities_box, with_class("btn-group p-1 mt-2"));
                city_container.setAttribute("role", "group");

                const city_name = E('button', city_container, btn_sm);
                city_name.innerHTML = name;
                city_name.setAttribute("style", "pointer-events: none;");

                E('button', city_container, subscribe_btn_init(id));

                E("br", cities_box);
            });

            const sorted = [...weather_state].sort((l, r) => l.id > r.id ? 1 : -1);
            sorted.map(({ city_name, weather, temperature, id }) => {
                const weather_container = E("div", dashboard, with_class("btn-group"));
                weather_container.setAttribute("role", "group");

                const city_name_e = E('button', weather_container, btn_sm);
                city_name_e.innerHTML = city_name;
                city_name_e.setAttribute("style", "pointer-events: none;");

                const weather_e = E('button', weather_container, btn_sm);
                weather_e.innerHTML = weather;
                weather_e.setAttribute("style", "pointer-events: none;");

                const temperature_e = E('button', weather_container, btn_sm);
                temperature_e.innerHTML = `${temperature} °C`;
                temperature_e.setAttribute("style", "pointer-events: none;");

                E('button', weather_container, unsubscribe_btn_init(id));
                E('br', dashboard);
            });
        };

        E('button', dom, e => {
            e.innerHTML = "sign out";
            e.className = "btn btn-primary";
            e.onclick = signout;
        });
    });

    fetch_fill_data(weather_app);
};

const signup = () => {
    console.log(1);
    const data = {
        username: byId('username').value,
        password1: byId('password').value,
        password2: byId('password').value
    };
    const callback = checked(signed_dialog);

    return send_fd('post', '/facade/signup/', data, callback);
};

const signin = () => {
    const data = {
        username: byId('username').value,
        password: byId('password').value
    };
    const callback = checked(signed_dialog);

    return send_fd('post', '/facade/signin/', data, callback);
};

const signout = () => {
    const callback = checked(anon_dialog);

    return send_fd('post', '/facade/signout/', {}, callback);
};

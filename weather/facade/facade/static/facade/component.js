function Component(domel, initial_state) {
    this.state = initial_state;
    this.domel = domel;
    this.renderer = null;
    
    this.dig = (path, cb = false) => {
        if(isStr(path))
            return this.dig(path.includes('.') ? path.split('.'): [path], cb);
        
        let prev = Object.assign([], path);
        let last = prev.pop();

        let point = this.state;
        prev.map(el => { point = point[el]; });

        if (cb)
            return point[last] = cb(point[last]);
        return point[last];
    };

    /* register rendering function: state -> dom element */
    this.register = (renderer) => {
        this.renderer = renderer;
        this.render();
    };

    this.render = () => {
        this.domel.textContent = '';
        this.renderer(this.state, this.domel);
    };

    /* update either one or several parts of state */
    this.atomic = (path, action) => {
        this.dig(path, action);
        this.render();
    };

    this.batch = (pairs) => {
        pairs.map(([path, action]) => this.dig(path, action));
        this.render();
    };
}

function api(endpoint, query_params = {}) {
    let url = `${location.protocol}//${location.host}/api/${endpoint}?`;
    for (let key in query_params) {
        if (!query_params.hasOwnProperty(key))
            continue;
        url += `${key}=${query_params[key]}&`;
    }
    return url.substr(0, url.length - 1);
}

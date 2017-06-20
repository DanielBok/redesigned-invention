app.filter("toDateOfArrival", () => (x) => {
    let d = new Date(x);
    return d.toISOString().replace('T', ' ').substring(0, 19);
});

app.filter("toJustTime", () => s => {
    return (new Date(s)).toString().substring(16, 22);
});

app.filter('toLocalTime', () => s => {
    return (new Date(s)).toString().substring(0, 22)
});

app.filter("toID", () => (y) => {
    let c = y.split(" ");
    return c[1];
});

app.filter("replaceAll", () => (text, search, replacement) => {
    return text.replace(new RegExp(search, 'g'), replacement)
});

app.filter("removeDriver", () => (list, driver) => {
    let res = list;
    let index = list.indexOf(driver);
    res.splice(index, 1);
    return
});

app.filter("toDateOfArrival", () => (x) => {
    let d = new Date(x);
    return d.toISOString().replace('T', ' ').substring(0, 19);
});

app.filter("toJustTime", () => (s) => {
    return s.substring(17, 22);
});

app.filter("toID", () => (y) => {
    let c = y.split(" ");
    return c[1];
});

app.filter("replaceAll", () => (text, search, replacement) => {
    return text.replace(new RegExp(search, 'g'), replacement)
});

app.filter("removeDriver", () => (list, driver) => {
    var res = list;
    var index = list.indexOf(driver);
    res.splice(index,1);
    return
});

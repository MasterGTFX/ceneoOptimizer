let {PythonShell} = require('python-shell')
var path = require("path")


function get_weather() {
    
    var product_name = document.getElementById("product_name").value;
    var max_cena = document.getElementById("max_cena").value;
    
    var options = {
        scriptPath : path.join(__dirname, '/../engine/'),
        args : [product_name, max_cena, path.join(__dirname, '/../engine/')]
    }
    
    let pyshell = new PythonShell('scraper_test.py', options);
    
    pyshell.on('message', function(message) {
               add_record2(message);
               })
    document.getElementById("product_name").value = "";
}

function console_out(param) {
    var jason_bourne = JSON.parse(param);
    var len = jason_bourne.length;
    var table = document.getElementById('table');
    
    console.log(jason_bourne);

}


function add_record2(param) {
    var jason_bourne1 = JSON.parse(param);
    
    var jason_bourne = [{"seller_name": "digitmedia.pl", "price": 7313.94, "reviews_number": 9, "rep": 5.0, "url": "http://tinyurl.com/r7fnjqy"}, {"seller_name": "lenovo24.pl", "price": 7925.0, "reviews_number": 12, "rep": 5.0, "url": "http://tinyurl.com/qquaeln"}, {"seller_name": "malibupc.pl", "price": 7160.0, "reviews_number": 17, "rep": 5.0, "url": "http://tinyurl.com/rvl8a9c"}, {"seller_name": "wlodipol.pl", "price": 7299.0, "reviews_number": 24, "rep": 4.0, "url": "http://tinyurl.com/tbv46do"}];
    
    var len = jason_bourne.length;
    var table = document.getElementById('table');
    
    for (var i=0; i < len; i++) {
        var tr = document.createElement('tr');
        var s = jason_bourne[i];
        
        //row number
        var td = document.createElement('td');
        td.innerHTML = i+1;
        tr.appendChild(td);
        
        //seller_name
        td = document.createElement('td');
        td.innerHTML = s.seller_name;
        tr.appendChild(td);
        
        //price
        td = document.createElement('td');
        td.innerHTML = s.price;
        tr.appendChild(td);
        
        //reviews_number
        td = document.createElement('td');
        td.innerHTML = s.reviews_number;
        tr.appendChild(td);
        
        //rep
        td = document.createElement('td');
        td.innerHTML = s.rep;
        tr.appendChild(td);
        
        //url
        td = document.createElement('td');
        
        //url name
        td.innerHTML = s.url;
        //create and append hyperlink
        //hyperlink = document.createElement("a");
        //hyperlink.setAttribute("href", s.url);
        //td.appendChild(hyperlink);
        td.setAttribute("onClick","location.href=\'" + s.url + "\';");
        tr.appendChild(td);
        table.appendChild(tr);
    }
    
}

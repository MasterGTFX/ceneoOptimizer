let {PythonShell} = require('python-shell')
var path = require("path")


function get_weather() {
    
    var city = document.getElementById("city").value;
    var city1 = document.getElementById("city1").value;
    
    var options = {
        scriptPath : path.join(__dirname, '/../engine/'),
        args : [city, city1, path.join(__dirname, '/../engine/')]
    }
    
    let pyshell = new PythonShell('scraper_test.py', options);
    
    pyshell.on('message', function(message) {
               console_out(message);
               })
    document.getElementById("city").value = "";
}

function console_out(param) {
    var jason_bourne = JSON.parse(param);
    var len = jason_bourne.length;
    var table = document.getElementById('table');
    
    console.log(jason_bourne);

}


function add_record2(param) {
    var jason_bourne = JSON.parse(param);
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

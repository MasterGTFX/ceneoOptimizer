let {PythonShell} = require('python-shell')
var path = require("path")

const use_scraper = () => {
    var num_of_item_parameters = document.getElementById('chart_table').rows[0].cells.length;
    var num_of_items = document.getElementById('chart_table').rows.length;

    var options = {
        scriptPath : path.join(__dirname, '/../engine/'),
        args : [get_chart(), num_of_item_parameters, num_of_items]
    }
    
    let pyshell = new PythonShell('scraper.py', options);
    
    pyshell.on('message', function(message) {
               show_results(message);
               })
    document.getElementById("product_name").value = "";
}
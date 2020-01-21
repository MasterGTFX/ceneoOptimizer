//function for debug purposes
const console_out = (param) => {
    var jason_bourne = JSON.parse(param);
    //var len = jason_bourne.length;
    //var table = document.getElementById('table');
    
    //console.log(jason_bourne);
    console.log(param);

}

const show_results = (param) => {
    //Drop previous table and start building new one
    dropTable('dataDiv');
    dropTable('chart');
    
    var jason_bourne = JSON.parse(param);
    var sets_num = jason_bourne.length;
    var items_num = jason_bourne[0].length;
    
    var knt_tabel = document.getElementById('dataDiv');
    
    for(var j=0; j<sets_num; j+=2) {
        
        //create table
        var tbl = document.createElement('table');
        tbl.setAttribute('id', 'data_table');

        //table header
        var row = tbl.insertRow(0);
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6);
        
        //initialize header
        cell0.innerHTML = "#";
        cell1.innerHTML = "Product name";
        cell2.innerHTML = "Seller";
        cell3.innerHTML = "Price";
        cell4.innerHTML = "Reviews number";
        cell5.innerHTML = "Reputation";
        cell6.innerHTML = "Url";
        
        for (var i=0; i < items_num; i++) {
            var tr = document.createElement('tr');
            var s = jason_bourne[j][i];
            
            //row number
            var td = document.createElement('td');
            td.innerHTML = i+1;
            tr.appendChild(td);
            
            //product name
            td = document.createElement('td');
            td.innerHTML = s.product_name;
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
            td.innerHTML = s.url;
            tr.appendChild(td);
            
            //add row
            tbl.appendChild(tr);
        }
        
        //create and add total_price row
        var total_price_row = document.createElement('tr');
        var total_price_index = j+1;
        total_price_cell = document.createElement('td');
        total_price_cell.innerHTML = "Total price: " + jason_bourne[total_price_index];
        total_price_row.appendChild(total_price_cell);
        tbl.appendChild(total_price_row);
 
        //add table to division <div>
        knt_tabel.appendChild(document.createElement('br'));
        knt_tabel.appendChild(document.createElement('br'));
        knt_tabel.appendChild(tbl);
    }

}

const dropTable = (parentID) => {
    try {
        const parent = document.getElementById(parentID);
        while (parent.firstChild) {
            parent.firstChild.remove();
        }
    } catch (error) {
        console.log(error)
    }
}

const scrollFunction = () => {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollButton.style.display = 'block';
    } else {
        scrollButton.style.display = 'none';
    }
}

// When the user clicks on the button, scroll to the top of the document
topFunction = () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

const addToChart = () => {
    
    //create chart if there is no any
    chart = document.getElementById('chart');
    console.log(chart.children.length);
    if(chart.children.length == 0){
        chart.appendChild(document.createElement('table'));
        chart.lastChild.setAttribute('id', 'chart_table');
        
        //create header
        chart = document.getElementById('chart_table');
        var row = chart.insertRow(0);
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6);
        var cell7 = row.insertCell(7);

        //initialize header
        cell0.innerHTML = "#";
        cell1.innerHTML = "Product name";
        cell2.innerHTML = "Max price";
        cell3.innerHTML = "Min price";
        cell4.innerHTML = "Min rating";
        cell5.innerHTML = "Min reviews";
        cell6.innerHTML = "Num offers";
        cell7.innerHTML = "Num products";

    }

    //create list of params
    var item_params = [
                       document.getElementById("product_name").value,
                       document.getElementById("max_cena").value,
                       document.getElementById("min_cena").value,
                       document.getElementById("min_rating").value,
                       document.getElementById("min_reviews").value,
                       document.getElementById("num_offers").value,
                       document.getElementById("num_products").value
                       ];
    
    
    //create row
    tr = document.createElement('tr');
    
    //append number of item first
    var num_of_rows = document.getElementById('chart_table').rows.length;
    td = document.createElement('td');
    td.innerHTML = num_of_rows-1;
    tr.appendChild(td);
    
    //fill row using item_params
    for(var i=0; i<item_params.length; ++i){
        td = document.createElement('td');
        td.innerHTML = item_params[i];
        tr.appendChild(td);
    }

    //append row filled with item parameters to chart_table
    document.getElementById('chart_table').appendChild(tr);
}

const get_chart = () => {
    var data_cells = document.getElementById('chart_table').rows[0].cells.length;
    var data_rows = document.getElementById('chart_table').rows.length;
    
    var items = {};
    var one_item = {};
    
    for(var j=1; j<data_rows; ++j){
        for(var i=1; i<data_cells; ++i){
            var param_name = document.getElementById('chart_table').rows[0].cells[i].innerHTML;
            one_item[param_name] = document.getElementById('chart_table').rows[j].cells[i].innerHTML;
        }
        items["Item_"+(j-1).toString()] = one_item;
        one_item = {};
    }
    var json = JSON.stringify(items);

    return json;
}
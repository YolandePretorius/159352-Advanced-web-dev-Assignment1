//alert("Hello")
var myObj = null;

function hello(){
alert("Hello")
}

/*function dropDownList(){
               //var obj, dbParam, xmlhttp, myObj, x, txt = "";
                //obj = { table: "symbol", limit: 20 };
                //dbParam = JSON.stringify(obj);
                xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            myObj = JSON.parse(this.responseText);
            txt += "<select>"
            for (x in myObj) {
              txt += "<option>" + myObj[x].symbol;
            }
            txt += "</select>"
            document.getElementById("demo").innerHTML = txt;
          }
        };
        xmlhttp.open("POST",getSymbols.php, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("x=" + dbParam);
}*/

function dropDownList(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        myObj = JSON.parse(this.responseText);
        tableFromJson(myObj)
        //document.getElementById("demo").innerHTML = myObj.name;
      }
        };
        xmlhttp.open("GET", "getSymbols", true);
        xmlhttp.send();

}



function setData(){
 alert("add a list to data")
    //dropDown list()
}

function getData(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        myObj = JSON.parse(this.responseText);
        tableFromJson(myObj)
        //document.getElementById("demo").innerHTML = myObj.name;
      }
        };
        xmlhttp.open("GET", "portfolio.json", true);
        xmlhttp.send();

        dropDownList();
}

// used code from https://www.encodedna.com/javascript/practice-ground/default.htm?pg=convert_json_to_table_javascript
function tableFromJson(stockItems){
// the json data. (you can change the values for output.)
        /*var stockItems = [

            {"Stock": "TSLA", "Quantity": "200",
                "Price": "300", "Gain/Loss": "400"
            },
            {"Stock": "AAPL", "Quantity": "50",
                "Price": "150", "Gain/Loss": "-5"
            },



        ]*/

stockItems.push({"Stock": "ABC", "Quantity": "200",
                "Price": "500", "Gain/Loss": "400"
            })
        // Extract value from table header.
        var col = [];
        for (var i = 0; i < stockItems.length; i++) {
            for (var key in stockItems[i]) {
                if (col.indexOf(key) === -1) {
                    col.push(key);
                }
            }
        }

        // Create a table.
        var table = document.createElement("table");

        // Create table header row using the extracted headers above.
        var tr = table.insertRow(-1);                   // table row.

        for (var i = 0; i < col.length; i++) {
            var th = document.createElement("th");      // table header.
            th.innerHTML = col[i];
            tr.appendChild(th);
        }

        // add json data to the table as rows.
        for (var i = 0; i < stockItems.length; i++) {

            tr = table.insertRow(-1);

            for (var j = 0; j < col.length; j++) {
                var tabCell = tr.insertCell(-1);
                tabCell.innerHTML = stockItems[i][col[j]];
            }
        }

        // Now, add the newly created table with json data, to a container.
        var divShowData = document.getElementById('showData');
        divShowData.innerHTML = "";
        divShowData.appendChild(table);

     // document.getElementById('msg').innerHTML = '<br />You can later <a href="https://www.encodedna.com/javascript/dynamically-add-remove-rows-to-html-table-using-javascript-and-save-data.htm" target="_blank" style="color:#1464f4;text-decoration:none;">get all the data from table and save it in a database.</a>';
    }




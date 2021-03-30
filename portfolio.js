//alert("Hello")
var myObj = null;
var symbolList = null;

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
            alert("Got data");
            myObj = JSON.parse(this.responseText);
            //tableFromJson(myObj)
            //document.getElementById("demo").innerHTML = myObj.name;
            symbolList = myObj;
            autocomplete(document.getElementById("symbolInput"),symbolList);
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
            });
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

 /*code used from  https://www.w3schools.com/howto/howto_js_autocomplete.asp*/


     // document.getElementById('msg').innerHTML = '<br />You can later <a href="https://www.encodedna.com/javascript/dynamically-add-remove-rows-to-html-table-using-javascript-and-save-data.htm" target="_blank" style="color:#1464f4;text-decoration:none;">get all the data from table and save it in a database.</a>';
    }

function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
    });
    function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
    }
    function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
    }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}




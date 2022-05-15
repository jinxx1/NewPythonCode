angular.module("myapp", [])
        .controller("employeeController", function($scope) {
            $scope.names = [
                {name:'1111111',lastname:'2222222',department:'33333',country:'44444',designation:'55555555',ratting:1},
                {name:'Kirtesh',lastname:'Wani',department:'QA',country:'India',designation:'Sr. QA',ratting:1},
                {name:'Nikhil',lastname:'Kelkar',department:'QA',country:'India',designation:'TL QA',ratting:1},
                {name:'Rahul',lastname:'Ghorpade',department:'QA',country:'India',designation:'QA',ratting:1},
                {name:'Amol',lastname:'Bembde',department:'QA',country:'India',designation:'QA',ratting:1},
                {name:'Nilesh',lastname:'Kamble',department:'QA',country:'India',designation:'QA',ratting:1},
                {name:'Tamal',lastname:'Sen',department:'QA',country:'India',designation:'QA',ratting:1},
                {name:'Sameer',lastname:'Shah',department:'QA',country:'India',designation:'Manager',ratting:1},
                {name:'Arpan',lastname:'Mehta',department:'QA',country:'US',designation:'TL QA',ratting:1}
            ];

            $scope.ratings=[
                {option:'off',value:1},
                {option:'on',value:2}
                // {option:'third',value:3},
                // {option:'fourth',value:4}
            ];
        });

(function(document) {
    'use strict';

    var LightTableFilter = (function(Arr) {

        var _input;

        function _onInputEvent(e) {
            _input = e.target;
            var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
            Arr.forEach.call(tables, function(table) {
                Arr.forEach.call(table.tBodies, function(tbody) {
                    Arr.forEach.call(tbody.rows, _filter);
                });
            });
        }

        function _filter(row) {
            var text="";

            Arr.forEach.call(row.cells,function(cell,i){
                if($('.advCheck')[i].checked){

                    if($($('.advCheck')[i]).attr("name")=="normal")
                        text+=cell.textContent.toLowerCase();
                    else
                    {
                        //console.log($(cell).find("option:selected").text());
                    text+=$(cell).find("option:selected").val();
                    }
                }
            });
           var val = _input.value.toLowerCase();
          //  var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
            row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
        }

        return {
            init: function() {
                var inputs = document.getElementsByClassName('light-table-filter');
                Arr.forEach.call(inputs, function(input) {
                    input.oninput = _onInputEvent;
                });
            }
        };
    })(Array.prototype);



    document.addEventListener('readystatechange', function() {
        if (document.readyState === 'complete') {
            LightTableFilter.init();
        }
    });

})(document);


$(function(){
    var headers = $(".order-table thead th");

     $(headers).each(function(i,cell) {
        var celltext = cell.textContent;
        var atrname = $(cell).attr("name")=="not"?"not":"normal";
        if(celltext!=""){
            $(".advFilter").append('<input name="'+atrname+'" id="'+celltext+'" class="advCheck" type="checkbox" checked/><label for="'+celltext+'">'+celltext+'</label>');
        }
        else
        {
            $(".advFilter").append('<div style="display:none"><input name="not" id="'+celltext+'" class="advCheck" type="checkbox" checked/><label for="'+celltext+'">'+celltext+'</label></div>');
        }
    });
});
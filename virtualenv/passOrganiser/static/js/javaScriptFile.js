

$(document).ready(function () {
    var counter = 0;

    $("#addrow").on("click", function () {
        console.log("here");
        var newRow = $("<tr class='d-flex'>");
        var cols = "";

        cols += '<td class="col-lg"><input type="text" class="form-control" id="site" name="site"/></td>';
        cols += '<td class="col-lg"><input type="text" class="form-control" name="username"/></td>';
        cols += '<td class="col-lg"><input type="text" id=passwordField class="form-control" name="password"/></td>';

        // cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        cols += '<td class="col-sm"><input type="button" class="btn btn-secondary btn-sm" onclick="generatePass()" value="Suggest Pass"> <input type="button" class="ibtnSave btn btn-primary btn-sm" onclick="saveDetails()" type="submit" value="Save"></td>'
        newRow.append(cols);
        $("table.table-striped").append(newRow);
        counter++;
    });



    $("table.table-striped").on("click", ".ibtnDel", function (event) {
        //$(this).closest("tr").remove();  
        console.log(this)  
        console.log("in this function")
    });


});

function saveDetails(){
    // console.log("Hello world");
    // test = $(this).closest("tr").val();
    // var test1 = document.getElementsByName("site").value;
    // var test2 = document.getElementById("site").value;
    // console.log(test1)
    // console.log(test2)

    document.getElementById("myForm").submit();
  }

function deleteDetails(){
    console.log("I'm here")

}

function generatePass(){
    var passField = document.getElementById("passwordField"); 
    var randomPass = Math.random().toString(36).substring(2,15) + Math.random().toString(36).substring(2,15);
    passField.value = randomPass;

}


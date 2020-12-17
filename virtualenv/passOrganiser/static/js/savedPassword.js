

$(document).ready(function () {
    var counter = 0;

    $("#addrow").on("click", function () {
        console.log("here");
        var newRow = $("<tr class='d-flex'>");
        var cols = "";

        cols += '<td class="col-lg"><input type="text" class="form-control" id="site" name="site"/></td>';
        cols += '<td class="col-lg"><input type="text" class="form-control" name="username"/></td>';
        cols += '<td class="col-lg"><input type="text" id=passwordField class="form-control" name="password"/></td>';
        cols += '<td class="col-sm"><input type="button" class="btn btn-secondary btn-sm" onclick="generatePass()" value="Suggest Pass"> <input type="button" class="ibtnSave btn btn-primary btn-sm" onclick="saveDetails()" type="submit" value="Save"></td>'
        newRow.append(cols);
        $("table.table-striped").append(newRow);
        counter++;
    });

    $("table.table-striped").on("click", ".ibtnDel", function (event) {
    });
});

function viewPassword(pass,id){
    var field = document.getElementById(id);
    var viewButton = document.getElementById("view"+ id)
    if (viewButton.value == "Hide"){
        viewButton.value = "View"
        field.innerText = pass.replace(/./g, '*');

    }
    else{
        viewButton.value = "Hide"
        field.innerText = pass
    }
}

function saveDetails(){
    document.getElementById("myForm").submit();
  }

function generatePass(){
    var passField = document.getElementById("passwordField"); 
    var randomPass = Math.random().toString(36).substring(2,15) + Math.random().toString(36).substring(2,15);
    passField.value = randomPass;
}


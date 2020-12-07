

$(document).ready(function () {
    var counter = 0;

    $("#addrow").on("click", function () {
        console.log("here");
        var newRow = $("<tr>");
        var cols = "";

        cols += '<td><input type="text" class="form-control" id="site" name="site"/></td>';
        cols += '<td><input type="text" class="form-control" name="username"/></td>';
        cols += '<td><input type="text" class="form-control" name="password"/></td>';

        // cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        cols += '<td><input type="button" class="ibtnSave btn btn-primary" onclick="saveDetails()" type="submit" value="Save"></td>';
        newRow.append(cols);
        $("table.table-striped").append(newRow);
        counter++;
    });



    $("table.table-striped").on("click", ".ibtnSave", function (event) {
        // $(this).closest("tr").remove();       
        // counter -= 1
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

function calculateRow(row) {
    var price = +row.find('input[name^="price"]').val();

}

function calculateGrandTotal() {
    var grandTotal = 0;
    $("table.table-striped").find('input[name^="price"]').each(function () {
        grandTotal += +$(this).val();
    });
    $("#grandtotal").text(grandTotal.toFixed(2));
}
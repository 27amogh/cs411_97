var today = new Date().toISOString().split("T")[0];
document.getElementById("check-in").setAttribute("min",today);
document.getElementById("check-out").setAttribute("min",today);

function setEndDate(){
  if(document.getElementById("check-in")){
    var new_mindate = document.getElementById("check-in").value;
    document.getElementById("check-out").setAttribute("min",new_mindate);
    
  }
}

var clicks = 0;
function onClick_add() {
  clicks += 1;
  document.getElementById("clicks").innerHTML = clicks;
  document.getElementById("num_guest").value = clicks;
};

function onClick_reduce() {
    clicks -= 1;
    if (clicks == -1){
        clicks = 0;
    }
    document.getElementById("clicks").innerHTML = clicks;
    document.getElementById("num_guest").value = clicks;
  };



$(document).ready(function () {


  $('#result_table').DataTable({
    "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
  });
});
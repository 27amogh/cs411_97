function togglePopup(){
    document.getElementById("popup-1").classList.toggle("active");
  }



function search_nearest(btn){
    var nearest_review_id = $(btn).closest('tr').find('.review_id').text();
    console.log( nearest_review_id);
    document.getElementById("update_review_id").value = nearest_review_id; 
    
}

function checknew(){
    console.log(document.getElementById("update_review_id").value);
    console.log(document.getElementById("new_comment").value)
}


$(document).ready(function () {

    $('.form_lookup').on('submit', function(event){
        $.ajax({
            data:{
                reviewer_id: $('#reviewer_id').val(),
                reviewer_name: $('#reviewer_name').val()
            },
            type: 'POST',
            url: '/reviews',
            success: function(data){
                document.write(data);
            }
        })
        .done(function(data){

			if (data.error) {
				alert(data.error)
			}
        });
        event.preventDefault();
    });


    $('.form_add').on('submit',function(event){
        $.ajax({
            type: 'POST',
            url: "/reviews/create",
            data: {
                listing_id: $('.form_add').find('#listing_id').val(),
                reviewer_id: $('.form_add').find('#reviewer_id').val(),
                reviewer_name: $('.form_add').find('#reviewer_name').val(),
                comment: $('.form_add').find('#comment').val()
            },

            success: function (data) {
                alert("Success");
                console.log(data.review_id);
                $('#comment_table').append("<tr><td>" + data.listing_id + "</td><td class='review_id'>" + data.review_id + "</td><td>"+
                data.date + "</td><td>" + data.reviewer_id + "</td><td>" + data.reviewer_name + '</td><td width = 30% ><p class="comment"><small>'+
                data.comment + '</small></p></td>' + '<td><button class="update_btn" onclick="togglePopup();search_nearest(this);" style="margin-right: 10px;">Update</button><button class="delete_btn" onclick="search_nearest(this)">Delete</button></p></td></tr>')
            },
            error: function () {
                console.log('Error');
            }
        });
        event.preventDefault();
    });


    $("table").on('click',".update_btn", function(){ 
        console.log("click");
   });



  });

  $('#comment_table').on('click', '.update_btn' , function() {
    var comment = $(this).closest('tr').find('.comment');
    $('.form_update').on('submit',function(event){
        togglePopup();
        $.ajax({
            
            data:{
                update_review_id: $('.form_update').find('#update_review_id').val(),
                new_comment: $('.form_update').find('#new_comment').val()
            },
            type: "POST",
            url: "/reviews/update"
        }).done(function(data)
        {
            alert(data.response);
            comment.text(data.response);
        });
        event.preventDefault();
    });
    }) ; 

    $("#comment_table").on('click', '.delete_btn' , function(event) {
        var tr = $(this).closest('tr');
      if(confirm("Do you want to delete this entry")){
        
        $.ajax({
            type: 'POST',
            url: '/delete/' + $('#update_review_id').val(),
            success: function (res) {
                console.log(res.response);
                tr.remove();
            },
            error: function () {
                console.log('Error');
            }
        });
        event.preventDefault();
      }
      
        }) ; 
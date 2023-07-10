var renderedComments = [];

loadComments(document.post_id);

setInterval(function(){
	loadComments(document.post_id);
}, 3000);

function loadComments(post_id) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/api/comment/' + post_id);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {      
	      var data = JSON.parse(xhr.responseText);
	      comments = data["comments"]

	        //get lastest comment id
	    	comment_container_div = document.getElementById('comments-container');
	    	first_comment_div_index = 0;
	    	if (comment_container_div.children.length > 0){
	    		latest_comment_id = Number(comment_container_div.children[first_comment_div_index].id.substr(8));
	    	}
	    	else {
	    		latest_comment_id = 0
	    	}
	    	

	    	new_comments = []
	    	for(let i=0; i<comments.length; i++) {
	    		if (comments[i].id > latest_comment_id) {
	    			new_comments.push(comments[i]);
	    		}
	    	}

	    	for (let i=0; i < new_comments.length ; ++i) {
	          var img = new_comments[i].profile_pic;
	          var name = new_comments[i].commentor;
	          var text = new_comments[i].text;
	          var id = new_comments[i].id;
	          var date = new_comments[i].date_posted
	          addComment(id, img, text, name, date);
	      	}
  		}
  	};
  	xhr.send();
}	

function addComment(id , user_image, text, name, date) {
	var html = `<div id="comment-` + id + `" class="media">
					    	<div>
					    		<img src="` + user_image + `" alt="User Avatar" class="mr-3 rounded-circle" style="width:60px;">
						        <div class="media-body">
						          <h4>` + name + `</h4>
						          <p>` + text + `</p>
						          <small>Posted on ` + date + `</small>
						        </div>
					    	</div>
					  	</div>
					  	<hr>`
	comment_container_div = document.getElementById('comments-container');
	if (comment_container_div.children.length > 0) {	
		comment_container_div.children[0].insertAdjacentHTML("beforebegin", html);
		document.getElementById('comment-' + id).scrollIntoView({'behaviour':'instant'});
	}
	else {
		comment_container_div.innerHTML += html;
		document.getElementById('comment-' + id).scrollIntoView({'behaviour':'instant'});
	}

}

function sendComment(post_id){

	const xhr = new XMLHttpRequest();
	const url = "/api/comment/" + post_id + "/create";

	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	const text_field_value = document.getElementById('id_text').value;
	const pay = {"post_id": post_id, "comment": text_field_value};
	xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      console.log(xhr.responseText)
      const text_field = document.getElementById("id_text")
      text_field.value = "";
    }
  };	

  const data = JSON.stringify(pay);
  xhr.send(data)
}

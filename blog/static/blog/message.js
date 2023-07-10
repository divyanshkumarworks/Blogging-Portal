function like(post_id) {
	var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/post/' + post_id + '/like');
    xhr.onload = function() {
      if (xhr.status === 200) {
        console.log(post_id)
      	var button = document.getElementById('like-button-' + post_id);
      	var countDiv = document.getElementById('post-like-count-' + post_id);
        var data = JSON.parse(xhr.responseText);
        if (data.liked){
        	button.classList.remove('btn-outline-primary');
        	button.classList.add('btn-primary');
        	button.innerText = 'Liked';
        	button.style.color = "white";
        	countDiv.innerText = Number(countDiv.innerText) + 1;
        }else{
        	button.classList.remove('btn-primary');
        	button.classList.add('btn-outline-primary');
        	button.innerText = 'Like';
        	button.style.color = "black";
        	countDiv.innerText = Number(countDiv.innerText) - 1;
        }
      }
    };
    xhr.send();
}

var renderedMessages = [];

loadMessages(document.to_user_id);

setInterval(function() {
  loadMessages(document.to_user_id);
}, 3000);

function loadMessages(user_id) {
  var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/message/' + user_id);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {      
        var data = JSON.parse(xhr.responseText);
        messages = data['messages']

        // get latest message id
        messages_container_div = document.getElementById('messages-container');
        last_message_div_index = messages_container_div.childElementCount - 2;
        latest_message_id = Number(messages_container_div.children[last_message_div_index].id.substr(8));

        // filter new messages
        new_messages = []
        for (let i=0; i<messages.length; i++){
          if (messages[i].id > latest_message_id){
            new_messages.push(messages[i]);
          }
        }

        for (let i=0; i < new_messages.length ; ++i) {
          var pos = new_messages[i].position;
          var img = new_messages[i].profile_pic;
          var name = new_messages[i].name;
          var text = new_messages[i].text;
          var id = new_messages[i].id;
          addMessage(img, text, name, pos, id);
        } 
      }
    };
    xhr.send();
}

function addMessage(user_image, text, name, position, id) {
  var html = `<div id="message-` + id + `" class="position-relative">
                  <div class="chat-messages" id="chat-messages">
                    <div >
                      
                      <div class="chat-message-` + position + ` pb-4" id="right-message">
                        <div>
                          <img src="` + user_image + `" class="rounded-circle mr-1" alt="Chris Wood" width="40" height="40">
                          <div class="text-muted small text-nowrap mt-2">April 8, 2023, 9:48 a.m.</div>
                        </div>
                        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                          <div class="font-weight-bold mb-1">` + name + `</div>
                          <div id="right-messages-text">` + text + `</div>
                        </div>
                        
                      </div>
                      
                    </div>
                  </div>
                </div>`;
  messages_container_div = document.getElementById('messages-container');
  last_message_div_index = messages_container_div.childElementCount - 2;
  messages_container_div.children[last_message_div_index].insertAdjacentHTML("afterend", html);
  document.getElementById('message-' + id).scrollIntoView({'behaviour':'instant'});
}


messages_container_div = document.getElementById('messages-container');
last_message_div_index = messages_container_div.childElementCount - 2;
latest_message_id = Number(messages_container_div.children[last_message_div_index].id.substr(8));
document.getElementById('message-' + latest_message_id).scrollIntoView({'behaviour':'instant'});


function sendMessage(user_id){
  
  const xhr = new XMLHttpRequest();
  const url = "/api/message/" + user_id + "/create";

  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  const text_field_value = document.getElementById("id_text").value;
  const payload = {"user_id": user_id, "message": text_field_value}; 

  
  // Get the cookie value from the browser's cookie
  // const cookie = document.cookie;

  // Add the cookie to the request header
  // xhr.setRequestHeader("Cookie", cookie);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loadMessages(user_id)
    }
  };

  const data = JSON.stringify(payload);
  xhr.send(data);
}
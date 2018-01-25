

function getMessageUrl(messageId) {
  return 'messages/'+messageId;
}

function incrementMessageCount(count){
  count +=1;
  localStorage.setItem('countMessage', count);
}


Vue.use(VueMaterial.default);
    var message_element_view = new Vue({
    el: '#message_content',
    data: {
        loading: false,
        title: 'Is this a Message Receipt?',
        messageDomain: '',
        messageId: null,
        messageContent: ''
    },
    mounted: function(){
        localStorage.setItem('tags', JSON.stringify([]));
        this.iframeLoaded();
        this.initiateMessages();
    },
    methods: {
        iframeLoaded: function () {
          var iFrameID = document.getElementById('iframe_message');
          iFrameID.contentWindow.location.reload();
          if(iFrameID) {
              iFrameID.height = '';
              iFrameID.width = '';
              var width = 1000;
              var height = 700;
              // if (iFrameID.contentWindow.document.body != null){
              //       var scrollWidth = iFrameID.contentWindow.document.body.scrollWidth;
              //       var scrollHeight = iFrameID.contentWindow.document.body.scrollHeight;
              //       if(scrollWidth> width){
              //           width = scrollWidth;
              //       }
              //       if (scrollHeight> height){
              //           height = scrollHeight;
              //       }
              // }
              iFrameID.height = height + 'px';
              iFrameID.width = width + 'px';
          }

        },
        initiateMessages: function(){
            var self = this;
            console.log('Initiated!');
            localStorage.removeItem('messages');
            localStorage.removeItem('countMessage');
            self.loading = true;
            axios.get('/get_messages')
              .then(function (response) {
                self.insertTagsIfExist();
                localStorage.setItem('messages', JSON.stringify(response.data));
                localStorage.setItem('tags', JSON.stringify([]));
                localStorage.setItem('countMessage', 0);
                console.log('Got messages!');
                self.loading = false;
              })
              .catch(function (error) {
                console.log(error);
              });
        },
        getNextMessage: function (){
            var count = parseInt(localStorage.getItem('countMessage'));
            var messages = JSON.parse(localStorage.getItem('messages'));

            console.log('count='+count);
            console.log('messages='+messages);
            console.log('length='+messages.length);
            if(count === messages.length){
                this.initiateMessages();
                count = 0;
            }
            var message = messages[count];
            this.messageId = message['id'];
            var url = getMessageUrl(this.messageId);
            console.log('url='+url);
            incrementMessageCount(count);
            this.iframeLoaded();
            return {url : url}
        },
        insertTagsIfExist: function () {
            var tags = JSON.parse(localStorage.getItem('tags'));
            if (tags !== null && tags.length > 0){
                axios.post('/add_tags', tags)
                  .then(function (response) {
                    console.log(response.status+' OK! got tags='+tags);
                    localStorage.setItem('tags', JSON.stringify([]));
                  })
                  .catch(function (error) {
                    console.log(error);
                  });
            }
        }
    }
});

var app = new Vue({
    el: '#app',
            methods: {
                sendAnswerYes: function () {
                    // TODO send answer message_id + yes/no
                    // TODO load next message get next iframe to display
                    console.log('answered yes');
                    this.handelingNextMessage(this.prepareTag(true,
                        message_element_view.messageId));
                },
                sendAnswerNo: function () {
                    console.log('answered no');
                    this.handelingNextMessage(this.prepareTag(false,
                        message_element_view.messageId));
                },
                sendAnswerSkip: function (){
                    console.log('answered skip');
                    this.handelingNextMessage(null);
                },
                handelingNextMessage: function (answer){
                    if(answer === null || answer['message_id'] === null){
                        console.log('skip..')
                    }
                    else{
                        this.insertTag(answer);
                    }
                    console.log('loading next message...'+answer);
                    var nextMessage = message_element_view.getNextMessage();
                    message_element_view.messageDomain = nextMessage['url'];
                },
                prepareTag: function (answer, messageId) {
                    return {'message_id': messageId,
                        'is_receipt': answer}
                },
                insertTag: function(answer) {
                    var tags = JSON.parse(localStorage.getItem('tags'));
                    tags.push(answer);
                    localStorage.setItem('tags', JSON.stringify(tags));
                }
            }
});


window.onkeypress = function(e) {
    var no = [49, 121];
    var yes = [110, 50];
    var skip = [115, 51];
    var key = e.keyCode ? e.keyCode : e.which;
    console.log(key);
    if (no.indexOf(key) !== -1) {
    app.sendAnswerYes();
    }
    else if (yes.indexOf(key) !== -1){
    app.sendAnswerNo();
    }
    else if (skip.indexOf(key) !== -1){
    app.sendAnswerSkip();
    }
};
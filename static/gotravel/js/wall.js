var BASEWALLURL = "wall/";
var ADDPOSTURL = "/add/";
var ADDCOMMENTURL = "/comment/";
var COMMENTFORM = '<div>' +
                '<textarea class="form-control" name="textComment"></textarea>' +
                '<button class="btn btn-primary btn-sm margin-top" name="addComment">Коммент</button>' +
            '</div>';
var a;

var last;
var first = true;
var parent = $("[name='posts']");

function getAllPost() {
    var id = document.URL.split("id")[1];
    get(BASEWALLURL+ id, {}, function (resp) {
        addPostToPage(resp)
    })
}

function addPostToWall() {
    var id = document.URL.split("id")[1];
    data = {
        text: $("[name='new_post']").val()
    };
    post(BASEWALLURL + id + ADDPOSTURL, data, function (resp) {
        addPostToPage(resp);
        $("[name='new_post']").val("")
    })
}

function postToHtml(post) {
    post_fields = post.fields;
    var src = "/media/users/avatar/default/default.jpg";
    if (post_fields.author[2] !== undefined)
    {
         src = post_fields.author[2]
    }

    result = '<div class="post row">'+
        '<div class="col-md-2">'+
            '<img src="'+ src +'" class="photo">'+

        '</div>'+
        '<div class="col-md-10">'+
            '<small>'+ post_fields.author[1]+'</small>'+
            '<p>'+ post_fields.text +'</p>'+
            '<small>'+ new Date(post_fields.date).toLocaleString()+'</small>  '+
            '<a name="show-comment-form" href="/wall'+post_fields.place[0]+'">Комментировать</a>'+
        '</div>'+
    '</div>';
    return result;
}

function addPostToPage(posts) {
    if (first && posts.length) {
        posts.forEach(function (item, i, arr) {
            parent.append(postToHtml(item))
        });
        first = false;
        last = posts[0];
    }

    if (last !== undefined) {
        currentPost = posts[0];
        if (currentPost.pk === last.pk)
            return;
        else {
            parent.prepend(postToHtml(currentPost));
            last = posts[0];
        }
    }
}


function addCommentToPost() {

}

 $(document).ready(function(){
     getAllPost();
     setInterval(getAllPost, 5000);

     $("[name='add_post']").click(function () {
        addPostToWall();
     });


 });
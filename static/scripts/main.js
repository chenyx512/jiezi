
var app = new Vue({
  el: '#navbar',
  data: {
    username: 'George Yu'
  }
})

var app = new Vue({
  el: '#page-container',
  data: {
    firstName: 'George',
    streakDayCount: 3,
    streakMonth: 'March'
  }
})

$(document).ready(() => {
  const $source = $(".search-form-wrapper > input[name='keyword']");
  const $target = $("#search-dropdown-wrapper");
  $(".search-form-wrapper").focusout(() => {
    setTimeout(() => {
      $target.html(""); //  This is a temporary fix, which allows the click event to be completed before html is cleared.
    }, 150);            //  Shoulda come up with a better solution in the future.
  })
  const searchHandler = () => {
    keyword = $source.val();
    if (keyword != "") {
      $.ajax({
          url: "/learning/search/",
          data: {
            keyword: keyword
          },
          type: "POST",
          dataType : "json",
      })
        .done(json => {
          if (json.characters.length == 0) {
            $target.html("<hr><div class='error-msg'>NO MATCH</div>");
          } else {
            $target.html("<hr>");
            for (let i=0; i <= (json.characters.length>6 ? 6:json.characters.length); i++){
              let character = json.characters[i].fields;
              let target_pk = ("0000" + json.characters[i].pk).slice(-4);
              let entry = "<a href='/learning/C"+target_pk+"' class='search-entry-wrapper' id='"+i+"'><div class='search-entry'><h4>"+character.chinese+"<small>["+character.pinyin.replace(/\s+/g, '')+"]</small></h4> \
                <p>"+character.definition_1+"<br><span>"+character.explanation_2+"</span></p></div></a>"; 
                // The replace method is to temporarily remove the space in some pinyin entries until this issue is solved in the database.
              $(entry).appendTo($target);
            }
            let redir = $(".search-entry-wrapper#0").attr("href");
            $(".search-form").attr("action", redir);
          }
        })
  
        .fail((xhr, status, errorThrown) => {
          $target.html("<hr><div class='error-msg'>There was a problem connecting with the Solved server</div>");
        })
    } else {
      $target.html("")
    }
  }
  
  $source.on("input propertychange", searchHandler);
}) 

function showModal(modalId) {
  $('.page-mask').show();
  $(`#${modalId}`).show();
}

function hideModal(modalId) {
  $('.page-mask').hide();
  $(`#${modalId}`).hide();
}
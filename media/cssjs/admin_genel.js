filefields = $("input[type='file']");
filefields.wrap("<div class='fileupload' />")
filefields.parents('p').contents().filter(function() {return this.nodeType === 3;}).remove()
filefields.parent().siblings('br').remove()

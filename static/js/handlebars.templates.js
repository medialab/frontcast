(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['assignment'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<div class=\"assignment pin ";
  if (stack1 = helpers.status) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.status; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" data-id=\"";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" id=\"as-";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n  <div class=\"status icon-time\"></div>\n  	\n  <div class=\"title\">\n  	"
    + escapeExpression(((stack1 = ((stack1 = depth0.task),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n	-\n  	<span class=\"date\">deadline: ";
  if (stack2 = helpers.date_due) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.date_due; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</span>\n  </div>\n</div>\n";
  return buffer;
  });
templates['document'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "_grade ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      "
    + escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n    ";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n  		"
    + escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " /\n		";
  return buffer;
  }

function program7(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      "
    + escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " -\n    ";
  return buffer;
  }

  buffer += "<div class=\"document pin ";
  if (stack1 = helpers.status) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.status; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " ";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.RATING), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\" id=\"d-";
  if (stack2 = helpers.id) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.id; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\">\n  <div class=\"pusher\"></div>\n  <div class=\"status\">";
  if (stack2 = helpers.status) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.status; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</div>\n  <h3>";
  if (stack2 = helpers.title) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.title; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</h3>\n  <div class=\"tags\">\n    ";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.Date), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    <br/>\n  	";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.Institution), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    <br/>\n    <br/>\n    ";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.AUTHOR), {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  </div>\n  <div class=\"abstract\">";
  if (stack2 = helpers['abstract']) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0['abstract']; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</div>\n  <div class=\"abstract\">";
  if (stack2 = helpers.content) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.content; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</div>\n  <div class=\"authors\">\n    by <a href=\""
    + escapeExpression(((stack1 = ((stack1 = depth0.settings),stack1 == null || stack1 === false ? stack1 : stack1.base_url)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "/u/";
  if (stack2 = helpers.owner) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.owner; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\">";
  if (stack2 = helpers.owner) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.owner; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</a> <a href=\""
    + escapeExpression(((stack1 = ((stack1 = depth0.settings),stack1 == null || stack1 === false ? stack1 : stack1.base_url)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "/d/";
  if (stack2 = helpers.slug) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.slug; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "/edit/\">edit</a>\n  </div>\n</div>\n";
  return buffer;
  });
templates['document_editor'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n  	<h3><textarea name=\"title\" placeholder=\"Describe yourself with 4 words...\">";
  if (stack1 = helpers.title) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.title; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea></h3>\n  	<div class=\"abstract\"><textarea name=\"abstract\" placeholder=\"Describe yourself with max 160 chars\">";
  if (stack1 = helpers['abstract']) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0['abstract']; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea></div>\n    <div class=\"content\">\n      <textarea name=\"content\" placeholder=\"Describe yourself with some basic html\">";
  if (stack1 = helpers.content) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.content; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n    </div>\n  ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n  	<div class=\"permalink\">\n  		Copy and Paste a\n  		<textarea name=\"permalink\" placeholder=\"http://vimeo.com/\">";
  if (stack1 = helpers.permalink) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.permalink; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n  	</div>\n  	<h3>\n		<textarea name=\"title\" placeholder=\"Describe yourself with 4 words...\">";
  if (stack1 = helpers.title) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.title; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n	</h3>\n	<div class=\"abstract\">\n		<textarea name=\"abstract\" placeholder=\"Describe the video with max 160 chars\">";
  if (stack1 = helpers['abstract']) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0['abstract']; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n	</div>\n	<div class=\"content\">";
  if (stack1 = helpers.content) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.content; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</div>\n  ";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <div class=\"permalink\">\n      Copy and Paste a flickr link\n      <textarea name=\"permalink\" placeholder=\"http://vimeo.com/\">";
  if (stack1 = helpers.permalink) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.permalink; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n    </div>\n    <h3>\n      <textarea name=\"title\" placeholder=\"picture title (will be automatically filled)\">";
  if (stack1 = helpers.title) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.title; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n    </h3>\n  <div class=\"abstract\">\n    <textarea name=\"abstract\" placeholder=\"Describe the picture with max 160 chars\">";
  if (stack1 = helpers['abstract']) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0['abstract']; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n  </div>\n  <div class=\"content\">";
  if (stack1 = helpers.content) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.content; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</div>\n  ";
  return buffer;
  }

  buffer += "<div class=\"pin editor ";
  if (stack1 = helpers.type) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" id=\"document-editor\">\n  <div class=\"pusher\"></div>\n  <div class=\"status\"></div>\n  \n  ";
  options = {hash:{
    'compare': ("text")
  },inverse:self.noop,fn:self.program(1, program1, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.type, options) : helperMissing.call(depth0, "if_eq", depth0.type, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n\n  ";
  options = {hash:{
    'compare': ("video")
  },inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.type, options) : helperMissing.call(depth0, "if_eq", depth0.type, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  \n  ";
  options = {hash:{
    'compare': ("picture")
  },inverse:self.noop,fn:self.program(5, program5, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.type, options) : helperMissing.call(depth0, "if_eq", depth0.type, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n\n  <div class=\"tags\">\n    \n  </div>\n  <div class=\"authors\">\n    <button class=\"save-document\">save</button>\n  </div>\n</div>\n";
  return buffer;
  });
templates['tag'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<span class=\"tag ";
  if (stack1 = helpers.visibility) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.visibility; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" data-type=\"";
  if (stack1 = helpers.type) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.value; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</span>";
  return buffer;
  });
templates['task'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<div>\n  <input type=\"text\" class=\"col-4\" value=\"";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.value; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" />\n  <button class=\"remove-identifier\">-</button>\n</div>\n";
  return buffer;
  });
})();
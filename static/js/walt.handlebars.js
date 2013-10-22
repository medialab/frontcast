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
templates['blf_single_entry'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div id=\"panels\" class=\"container\">\n  <div data-panel=\"create\" style=\"display:none;\">\n   <div class=\"create-form\"></div>\n  </div>\n  <div data-panel=\"fields\" style=\"display:none;\">\n    <div class=\"select-field\"></div>\n  </div>\n  <div data-panel=\"advancedSearch\" style=\"display:none;\">\n    <div class=\"advanced-search\"></div>\n  </div>\n  <div data-panel=\"list\" style=\"display:none;\">\n    <ul class=\"entries-list\"></ul>\n  </div>\n</div>";
  });
templates['document'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "_grade ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n        "
    + escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n      ";
  return buffer;
  }

function program7(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    		"
    + escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " /\n  		";
  return buffer;
  }

function program9(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n        "
    + escapeExpression(((stack1 = depth0.name),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " -\n      ";
  return buffer;
  }

function program11(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        ";
  options = {hash:{
    'compare': ("pdf")
  },inverse:self.noop,fn:self.program(12, program12, data),data:data};
  stack2 = ((stack1 = helpers.if_in || depth0.if_in),stack1 ? stack1.call(depth0, depth0.ext, options) : helperMissing.call(depth0, "if_in", depth0.ext, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      ";
  return buffer;
  }
function program12(depth0,data) {
  
  
  return "\n        <div class=\"actions\">\n          <a class=\"button\" href=\"mais_dossier.pdf\"><i class=\"icon-download\"></i> download print version</a>\n        </div>\n        ";
  }

function program14(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        ";
  options = {hash:{
    'compare': ("jpg|png|gif")
  },inverse:self.noop,fn:self.program(15, program15, data),data:data};
  stack2 = ((stack1 = helpers.if_in || depth0.if_in),stack1 ? stack1.call(depth0, depth0.ext, options) : helperMissing.call(depth0, "if_in", depth0.ext, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      ";
  return buffer;
  }
function program15(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n          <li><img src=\""
    + escapeExpression(((stack1 = depth0.src),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"/></li>\n        ";
  return buffer;
  }

function program17(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <div class=\"mla\">\n      <span data-reference-id=\"";
  if (stack1 = helpers.reference) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.reference; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">[ ... ]</span>\n      ";
  stack1 = helpers['if'].call(depth0, depth0.permissions, {hash:{},inverse:self.noop,fn:self.program(18, program18, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </div>\n    <hr/>\n    ";
  return buffer;
  }
function program18(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        ";
  options = {hash:{
    'compare': ("CAN_EDIT")
  },inverse:self.noop,fn:self.program(19, program19, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.permissions, options) : helperMissing.call(depth0, "if_eq", depth0.permissions, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      ";
  return buffer;
  }
function program19(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n          <a href=\""
    + escapeExpression(((stack1 = ((stack1 = depth0.settings),stack1 == null || stack1 === false ? stack1 : stack1.base_url)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "/#";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.url || depth0.url),stack1 ? stack1.call(depth0, "re", "slug", depth0.slug, options) : helperMissing.call(depth0, "url", "re", "slug", depth0.slug, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\" title=\"edit bibliographic reference\"><i class=\"icon-pencil\"></i></a>\n        ";
  return buffer;
  }

function program21(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n    <div class=\"actions\">\n      <ul>\n        \n        ";
  options = {hash:{
    'compare': ("CAN_EDIT")
  },inverse:self.noop,fn:self.program(22, program22, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.permissions, options) : helperMissing.call(depth0, "if_eq", depth0.permissions, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n        \n      </ul>\n    </div>\n    ";
  return buffer;
  }
function program22(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n          <li><a href=\""
    + escapeExpression(((stack1 = ((stack1 = depth0.settings),stack1 == null || stack1 === false ? stack1 : stack1.base_url)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "/#";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.url || depth0.url),stack1 ? stack1.call(depth0, "de", "slug", depth0.slug, options) : helperMissing.call(depth0, "url", "de", "slug", depth0.slug, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\">edit</a></li>\n          ";
  options = {hash:{
    'compare': ("public")
  },inverse:self.noop,fn:self.program(23, program23, data),data:data};
  stack2 = ((stack1 = helpers.unless_eq || depth0.unless_eq),stack1 ? stack1.call(depth0, depth0.status, options) : helperMissing.call(depth0, "unless_eq", depth0.status, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n        ";
  return buffer;
  }
function program23(depth0,data) {
  
  
  return "\n          <li>publish</li>\n          ";
  }

function program25(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        <a href=\""
    + escapeExpression(((stack1 = ((stack1 = depth0.settings),stack1 == null || stack1 === false ? stack1 : stack1.base_url)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "/#";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.url || depth0.url),stack1 ? stack1.call(depth0, "u", "username", depth0, options) : helperMissing.call(depth0, "url", "u", "username", depth0, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\">"
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "</a>\n      ";
  return buffer;
  }

  buffer += "<div class=\"document pin ";
  if (stack1 = helpers.status) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.status; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " ";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.RATING), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\" data-slug=\"";
  if (stack2 = helpers.slug) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.slug; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\" data-type=\"";
  if (stack2 = helpers.type) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.type; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\" data-href=\"/#";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.url || depth0.url),stack1 ? stack1.call(depth0, "d", "slug", depth0.slug, options) : helperMissing.call(depth0, "url", "d", "slug", depth0.slug, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\" data-id=\"";
  if (stack2 = helpers.id) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.id; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\" id=\"d-";
  if (stack2 = helpers.id) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.id; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\">\n  <div class=\"inner\">\n    <div class=\"pusher\"></div>\n    <div class=\"status\">";
  if (stack2 = helpers.status) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.status; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</div>\n    <h3>";
  if (stack2 = helpers.title) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.title; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</h3>\n    <div class=\"tags\">\n      ";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.Date), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      \n    	";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.Institution), {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      \n      ";
  stack2 = helpers.each.call(depth0, ((stack1 = depth0.tags),stack1 == null || stack1 === false ? stack1 : stack1.AUTHOR), {hash:{},inverse:self.noop,fn:self.program(9, program9, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    </div>\n    \n      ";
  stack2 = helpers.each.call(depth0, depth0.attachments, {hash:{},inverse:self.noop,fn:self.program(11, program11, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    \n    <div class=\"attachments slider\" style=\"max-height:150px; height:150px\">\n      <ul>\n      ";
  stack2 = helpers.each.call(depth0, depth0.attachments, {hash:{},inverse:self.noop,fn:self.program(14, program14, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      </ul>\n    </div>\n    <div class=\"abstract\">";
  if (stack2 = helpers['abstract']) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0['abstract']; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "<!--";
  if (stack2 = helpers.type) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.type; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "--></div>\n\n    <hr/>\n\n    ";
  options = {hash:{
    'compare': ("")
  },inverse:self.noop,fn:self.program(17, program17, data),data:data};
  stack2 = ((stack1 = helpers.unless_eq || depth0.unless_eq),stack1 ? stack1.call(depth0, depth0.reference, options) : helperMissing.call(depth0, "unless_eq", depth0.reference, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    \n    ";
  stack2 = helpers['if'].call(depth0, depth0.permissions, {hash:{},inverse:self.noop,fn:self.program(21, program21, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    <div class=\"authors\">\n      \n      by <a href=\""
    + escapeExpression(((stack1 = ((stack1 = depth0.settings),stack1 == null || stack1 === false ? stack1 : stack1.base_url)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "/#";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.url || depth0.url),stack1 ? stack1.call(depth0, "u", "username", depth0.owner, options) : helperMissing.call(depth0, "url", "u", "username", depth0.owner, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\">";
  if (stack2 = helpers.owner) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.owner; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</a>\n      ";
  stack2 = helpers.each.call(depth0, depth0.authors, {hash:{},inverse:self.noop,fn:self.program(25, program25, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n    </div>\n  </div>\n</div>\n";
  return buffer;
  });
templates['document_editor'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  
  return "\n\n  ";
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <div class=\"reference\">\n      <textarea name=\"reference\" readonly placeholder=\"forccast reference identifier\">";
  if (stack1 = helpers.reference) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.reference; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n    </div>\n  ";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        <li>\n          ";
  options = {hash:{
    'compare': ("jpg|gif")
  },inverse:self.noop,fn:self.program(6, program6, data),data:data};
  stack2 = ((stack1 = helpers.if_in || depth0.if_in),stack1 ? stack1.call(depth0, depth0.ext, options) : helperMissing.call(depth0, "if_in", depth0.ext, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n        </li>\n      ";
  return buffer;
  }
function program6(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n            <img src='";
  if (stack1 = helpers.src) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.src; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "' style='width:100%'/>\n          ";
  return buffer;
  }

function program8(depth0,data) {
  
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

function program10(depth0,data) {
  
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

  buffer += "<div id=\"document-editor\">\n  <div class=\"pusher\"></div>\n  <div class=\"status\"></div>\n  <input type=\"hidden\" name=\"type\" value=\"";
  if (stack1 = helpers.type) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"/>\n  <input type=\"hidden\" name=\"language\" value=\"";
  if (stack1 = helpers.language) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.language; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"/>\n  \n  <h3><textarea name=\"title\" placeholder=\"Describe yourself with 4 words...\">";
  if (stack1 = helpers.title) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.title; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea></h3>\n	<div class=\"abstract\"><textarea name=\"abstract\" placeholder=\"Describe yourself with max 160 chars\">";
  if (stack1 = helpers.abstract_raw) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.abstract_raw; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea></div>\n  <div class=\"content\">\n    <div class=\"inner\">\n      Full text\n      <textarea name=\"content\" placeholder=\"Describe yourself with some basic html\">";
  if (stack1 = helpers.content_raw) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.content_raw; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n    </div>\n  </div>\n  <div class=\"permalink\">\n    <div class=\"inner\">\n      Copy and Paste a\n      <textarea name=\"permalink\" placeholder=\"http://vimeo.com/\">";
  if (stack1 = helpers.permalink) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.permalink; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</textarea>\n    </div>\n  </div>\n\n\n  ";
  options = {hash:{
    'compare': ("")
  },inverse:self.program(3, program3, data),fn:self.program(1, program1, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.reference, options) : helperMissing.call(depth0, "if_eq", depth0.reference, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n\n  <div class=\"attachments\">\n    <div class=\"inner\">\n      Remote media (one per line);\n      <textarea name=\"remote\">";
  if (stack2 = helpers.remote) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.remote; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</textarea>\n    </div>\n    <div class=\"slider\" data-plugin=\"unslider\">\n      <ul>\n      ";
  options = {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data};
  stack2 = ((stack1 = helpers.foreach || depth0.foreach),stack1 ? stack1.call(depth0, depth0.attachments, options) : helperMissing.call(depth0, "foreach", depth0.attachments, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      </ul>\n      <div style=\"clear:left\"></div>\n    </div>\n  </div>\n\n  ";
  options = {hash:{
    'compare': ("video")
  },inverse:self.noop,fn:self.program(8, program8, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.type, options) : helperMissing.call(depth0, "if_eq", depth0.type, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  \n  ";
  options = {hash:{
    'compare': ("picture")
  },inverse:self.noop,fn:self.program(10, program10, data),data:data};
  stack2 = ((stack1 = helpers.if_eq || depth0.if_eq),stack1 ? stack1.call(depth0, depth0.type, options) : helperMissing.call(depth0, "if_eq", depth0.type, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n\n  <div class=\"tags\">\n    \n  </div>\n  <div class=\"authors\">\n    <button class=\"save-document\">save</button>\n  </div>\n</div>\n";
  return buffer;
  });
templates['reference_editor'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<div class=\"reference-editor\" data-id=\"";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" id=\"reference-editor\">\n  <div class=\"pusher\"></div>\n  <h3>";
  if (stack1 = helpers.title) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.title; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</h3>\n  <h4>bibliographic reference ";
  if (stack1 = helpers.reference) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.reference; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</h4>\n  <div class=\"biblib-form abstract\" id=\"layout\"></div>\n  <div class=\"pusher\"></div>\n</div>";
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
(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['document'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<div class=\"pin "
    + escapeExpression(((stack1 = ((stack1 = depth0['d']),stack1 == null || stack1 === false ? stack1 : stack1.status)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  <div class=\"status\"></div>\n  <h3>"
    + escapeExpression(((stack1 = ((stack1 = depth0['d']),stack1 == null || stack1 === false ? stack1 : stack1.title)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h3>\n  <div class=\"abstract\">"
    + escapeExpression(((stack1 = ((stack1 = depth0['d']),stack1 == null || stack1 === false ? stack1 : stack1['abstract'])),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " - "
    + escapeExpression(((stack1 = ((stack1 = depth0['d']),stack1 == null || stack1 === false ? stack1 : stack1.mimetype)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</div>\n\n  <div class=\"authors\">\n    by <a href=\"/u/"
    + escapeExpression(((stack1 = ((stack1 = depth0['d']),stack1 == null || stack1 === false ? stack1 : stack1.owner)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = ((stack1 = depth0['d']),stack1 == null || stack1 === false ? stack1 : stack1.owner)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</a>\n  </div>\n</div>\n";
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
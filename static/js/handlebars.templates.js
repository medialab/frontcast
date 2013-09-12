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
    + "\" id=\"as-";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n  <div class=\"status\"></div>\n  <h3>titolo!! "
    + escapeExpression(((stack1 = ((stack1 = depth0.task),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h3>\n  <div class=\"abstract\">deadline: ";
  if (stack2 = helpers.date_due) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.date_due; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</div>\n  <a href=\"/frontcast/t/";
  if (stack2 = helpers.id) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.id; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\">complete task</a>\n</div>\n";
  return buffer;
  });
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
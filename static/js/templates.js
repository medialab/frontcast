this["blf"] = this["blf"] || {};
this["blf"]["templates"] = this["blf"]["templates"] || {};
this["blf"]["templates"]["preloaded"] = this["blf"]["templates"]["preloaded"] || {};

this["blf"]["templates"]["preloaded"]["templates/BooleanField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"BooleanField\">\n  <div class=\"message\"></div>\n  <label for=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <input class=\"col-6\" name=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" type=\"checkbox\" />\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CharField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"CharField\">\n  <div class=\"message\"></div>\n  <label for=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <input class=\"col-6\" name=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" type=\"text\" />\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CheckboxField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data,depth1) {
  
  var buffer = "", stack1, stack2;
  buffer += "\n    <fieldset class=\"checkbox-container\" id=\"";
  if (stack1 = helpers.type_id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type_id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" title=\"";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n      <input type=\"checkbox\" id=\""
    + escapeExpression(((stack1 = depth1.label),typeof stack1 === functionType ? stack1.apply(depth0) : stack1));
  if (stack2 = helpers.type_id) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.type_id; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\" />\n      <label for=\""
    + escapeExpression(((stack1 = depth1.label),typeof stack1 === functionType ? stack1.apply(depth0) : stack1));
  if (stack2 = helpers.type_id) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.type_id; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\">";
  if (stack2 = helpers.label) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.label; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</label>\n    </fieldset>\n    ";
  return buffer;
  }

  buffer += "<fieldset class=\"customInput CheckboxField\">\n  <span class=\"title\">";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :</span>\n  <div class=\"custom-container\">\n    ";
  stack1 = helpers.each.call(depth0, depth0.values, {hash:{},inverse:self.noop,fn:self.programWithDepth(1, program1, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CreatorField.Event.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.title", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.title", options)))
    + "</label>\n    <input data-attribute=\"title\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.number", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.number", options)))
    + "</label>\n    <input data-attribute=\"number\" class=\"col-3\" type=\"number\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.international", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.international", options)))
    + "</label>\n    <input data-attribute=\"international\" class=\"col-3\" type=\"checkbox\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.place", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.place", options)))
    + "</label>\n    <input data-attribute=\"place\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.country", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.country", options)))
    + "</label>\n    <input data-attribute=\"country\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.date_start", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.date_start", options)))
    + "</label>\n    <input data-attribute=\"date_start\" class=\"col-3\" type=\"date\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.event.date_end", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.event.date_end", options)))
    + "</label>\n    <input data-attribute=\"date_end\" class=\"col-3\" type=\"date\" />\n  </fieldset>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CreatorField.Orgunit.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.orgunit.name", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.orgunit.name", options)))
    + "</label>\n    <input data-attribute=\"name\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CreatorField.Person.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.person.name_family", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.person.name_family", options)))
    + "</label>\n    <input data-attribute=\"name_family\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.person.name_given", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.person.name_given", options)))
    + "</label>\n    <input data-attribute=\"name_given\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.person.date_birth", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.person.date_birth", options)))
    + "</label>\n    <input data-attribute=\"date_birth\" class=\"col-3\" type=\"year\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.person.date_death", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.person.date_death", options)))
    + "</label>\n    <input data-attribute=\"date_death\" class=\"col-3\" type=\"year\" />\n  </fieldset>\n  <fieldset>\n    <label class=\"col-3\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.person.affiliation", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.person.affiliation", options)))
    + "</label>\n    <input data-attribute=\"affiliation\" class=\"col-3\" type=\"text\" />\n  </fieldset>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CreatorField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"customInput CreatorField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"creators-container container\">\n    <ul class=\"creators-list\"></ul>\n    <button class=\"add-creator\">+</button>\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CreatorField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      ";
  stack1 = helpers['if'].call(depth0, depth0.separator, {hash:{},inverse:self.program(4, program4, data),fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    ";
  return buffer;
  }
function program2(depth0,data) {
  
  
  return "\n        <option class=\"disabled\" disabled=\"disabled\">---</option>\n      ";
  }

function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n        <option value=\""
    + escapeExpression(((stack1 = depth0.type_id),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = depth0.label),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n      ";
  return buffer;
  }

  buffer += "<li data-id=\"";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n  <select class=\"col-3 select-type\">\n    <option value=\"Person\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.line.Person", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.line.Person", options)))
    + "</option>\n    <option value=\"Orgunit\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.line.Orgunit", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.line.Orgunit", options)))
    + "</option>\n    <option value=\"Event\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "customInputs:CreatorField.line.Event", options) : helperMissing.call(depth0, "t", "customInputs:CreatorField.line.Event", options)))
    + "</option>\n  </select>\n  <select class=\"col-3 select-role\">\n    ";
  stack2 = helpers.each.call(depth0, depth0.creators, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  </select>\n  <button class=\"remove-creator\">-</button>\n  <button class=\"moveup-creator\">↑</button>\n  <button class=\"movedown-creator\">↓</button>\n  <div class=\"col-6 custom-container\">\n  </div>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/CreatorField.roles.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<option value=\"";
  if (stack1 = helpers.type_id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type_id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</option>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/DateField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"DateField\">\n  <div class=\"message\"></div>\n  <label for=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <input class=\"col-6\" name=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" type=\"year\" />\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/DocumentField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"customInput DocumentField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"documents-container container\">\n    <ul class=\"documents-list\"></ul>\n    <button class=\"add-document\">+</button>\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/DocumentField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <select class=\"col-3 select-field\">\n      ";
  stack1 = helpers.each.call(depth0, depth0.type_fields, {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </select>\n  ";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "";
  buffer += "\n        <option value=\""
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "\">"
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "</option>\n      ";
  return buffer;
  }

function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    ";
  stack1 = helpers.each.call(depth0, depth0.type_fields, {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  ";
  return buffer;
  }
function program5(depth0,data) {
  
  var buffer = "";
  buffer += "\n      <span class=\"inline-block col-3\">"
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "</span>\n    ";
  return buffer;
  }

  buffer += "<li data-id=\"";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n  ";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  stack2 = ((stack1 = helpers.ifCond || depth0.ifCond),stack1 ? stack1.call(depth0, ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), ">", 1, options) : helperMissing.call(depth0, "ifCond", ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), ">", 1, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  ";
  options = {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data};
  stack2 = ((stack1 = helpers.ifCond || depth0.ifCond),stack1 ? stack1.call(depth0, ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), "<=", 1, options) : helperMissing.call(depth0, "ifCond", ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), "<=", 1, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  <button class=\"remove-document\">-</button>\n  <div class=\"col-6 custom-container\">\n  </div>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/IdentifierField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"customInput IdentifierField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"identifier-container container\">\n    <ul class=\"identifiers-list\"></ul>\n    <button class=\"add-identifier\">+</button>\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/IdentifierField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<li>\n  <input type=\"text\" class=\"col-4\" value=\"";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.value; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" />\n  <button class=\"remove-identifier\">-</button>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/IntegerField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"IntegerField\">\n  <div class=\"message\"></div>\n  <label for=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <input class=\"col-6\" name=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" type=\"number\" />\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/KeywordField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"customInput KeywordField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"languages-container container\">\n    <ul class=\"languages-list\"></ul>\n    <button class=\"add-language\">+</button>\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/KeywordField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      ";
  stack1 = helpers['if'].call(depth0, depth0.separator, {hash:{},inverse:self.program(4, program4, data),fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    ";
  return buffer;
  }
function program2(depth0,data) {
  
  
  return "\n        <option class=\"disabled\" disabled=\"disabled\">---</option>\n      ";
  }

function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n        <option value=\""
    + escapeExpression(((stack1 = depth0.id),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = depth0.label),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n      ";
  return buffer;
  }

  buffer += "<li>\n  <select class=\"select-language\">\n    ";
  stack1 = helpers.each.call(depth0, depth0.languages, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </select>\n  <button class=\"remove-language\">-</button>\n  <textarea class=\"col-6\"></textarea>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/LanguageValueField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"customInput LanguageValueField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"languages-container container\">\n    <ul class=\"languages-list\"></ul>\n    <button class=\"add-language\">+</button>\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/LanguageValueField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      ";
  stack1 = helpers['if'].call(depth0, depth0.separator, {hash:{},inverse:self.program(4, program4, data),fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    ";
  return buffer;
  }
function program2(depth0,data) {
  
  
  return "\n        <option class=\"disabled\" disabled=\"disabled\">---</option>\n      ";
  }

function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n        <option value=\""
    + escapeExpression(((stack1 = depth0.id),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = depth0.label),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n      ";
  return buffer;
  }

  buffer += "<li>\n  <select class=\"select-language\">\n    ";
  stack1 = helpers.each.call(depth0, depth0.languages, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </select>\n  <button class=\"remove-language\">-</button>\n  <textarea class=\"col-6\"></textarea>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/ResourceField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"customInput ResourceField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"documents-container container\">\n    <ul class=\"documents-list\"></ul>\n    <button class=\"add-document\">+</button>\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/ResourceField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, stack2, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <select class=\"col-3 select-field\">\n      ";
  stack1 = helpers.each.call(depth0, depth0.type_fields, {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </select>\n  ";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "";
  buffer += "\n        <option value=\""
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "\">"
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "</option>\n      ";
  return buffer;
  }

function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    ";
  stack1 = helpers.each.call(depth0, depth0.type_fields, {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  ";
  return buffer;
  }
function program5(depth0,data) {
  
  var buffer = "";
  buffer += "\n      <span class=\"inline-block col-3\">"
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "</span>\n    ";
  return buffer;
  }

  buffer += "<li data-id=\"";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n  ";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  stack2 = ((stack1 = helpers.ifCond || depth0.ifCond),stack1 ? stack1.call(depth0, ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), ">", 1, options) : helperMissing.call(depth0, "ifCond", ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), ">", 1, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  ";
  options = {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data};
  stack2 = ((stack1 = helpers.ifCond || depth0.ifCond),stack1 ? stack1.call(depth0, ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), "<=", 1, options) : helperMissing.call(depth0, "ifCond", ((stack1 = depth0.type_fields),stack1 == null || stack1 === false ? stack1 : stack1.length), "<=", 1, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n  <button class=\"remove-document\">-</button>\n  <div class=\"col-6 custom-container\">\n  </div>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/StringField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<fieldset class=\"StringField\">\n  <div class=\"message\"></div>\n  <label for=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <span class=\"col-6 inline-block value\" name=\"";
  if (stack1 = helpers.property) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.property; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"></span>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/TypeField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "\n      <button class=\"add-value\">+</button>\n    ";
  }

  buffer += "<fieldset class=\"customInput TypeField\">\n  <div class=\"message\"></div>\n  <label>\n    ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :\n  </label>\n  <div class=\"types-container container\">\n    <ul class=\"values-list\"></ul>\n    ";
  stack1 = helpers['if'].call(depth0, depth0.multi, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/TypeField.line.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function";


  buffer += "<li>\n  <select class=\"select-in-type col-3\">\n    ";
  if (stack1 = helpers.content) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.content; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </select>\n  <button class=\"remove-value\">-</button>\n</li>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/YearRangeField.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<fieldset class=\"customInput YearRangeField\">\n  <span class=\"title\">";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.label; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + " :</span>\n  ";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "commons.between", options) : helperMissing.call(depth0, "t", "commons.between", options)))
    + " <input type=\"year\" class=\"date-from\" /> ";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "commons.and", options) : helperMissing.call(depth0, "t", "commons.and", options)))
    + " <input type=\"year\" class=\"date-to\" />\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/advancedSearchPanel.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<div class=\"index-container\"></div>\n<div class=\"filter-container\"></div>\n<button class=\"validate-advanced-search\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "actions.search", options) : helperMissing.call(depth0, "t", "actions.search", options)))
    + "</button>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/advancedSearchPanel.index.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data,depth1) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n    <li class=\"index\">\n      <select data-type=\"operator\">\n      ";
  stack1 = helpers.each.call(depth0, depth1.operators, {hash:{},inverse:self.noop,fn:self.programWithDepth(2, program2, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      </select>\n      <input data-type=\"value\" type=\"text\" placeholder=\"";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth1['t']),stack1 ? stack1.call(depth0, "commons.ellipsis", options) : helperMissing.call(depth0, "t", "commons.ellipsis", options)))
    + "\" value=\"";
  if (stack2 = helpers.value) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.value; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "\" />\n      <select data-type=\"index\">\n      ";
  stack2 = helpers.each.call(depth0, depth1.indexes, {hash:{},inverse:self.noop,fn:self.programWithDepth(5, program5, data, depth0),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\n      </select>\n      <button class=\"remove-index\">-</button>\n    </li>\n  ";
  return buffer;
  }
function program2(depth0,data,depth1) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        <option value=\"";
  if (stack1 = helpers.type_id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type_id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.ifCond || depth0.ifCond),stack1 ? stack1.call(depth0, depth0.type_id, "==", depth1.operator, options) : helperMissing.call(depth0, "ifCond", depth0.type_id, "==", depth1.operator, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += ">";
  if (stack2 = helpers.label) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.label; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</option>\n      ";
  return buffer;
  }
function program3(depth0,data) {
  
  
  return " selected";
  }

function program5(depth0,data,depth1) {
  
  var buffer = "", stack1, stack2, options;
  buffer += "\n        <option value=\"";
  if (stack1 = helpers.type_id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.type_id; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  stack2 = ((stack1 = helpers.ifCond || depth0.ifCond),stack1 ? stack1.call(depth0, depth0.type_id, "==", depth1.index, options) : helperMissing.call(depth0, "ifCond", depth0.type_id, "==", depth1.index, options));
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += ">";
  if (stack2 = helpers.label) { stack2 = stack2.call(depth0, {hash:{},data:data}); }
  else { stack2 = depth0.label; stack2 = typeof stack2 === functionType ? stack2.apply(depth0) : stack2; }
  buffer += escapeExpression(stack2)
    + "</option>\n      ";
  return buffer;
  }

  buffer += "<fieldset>\n  <ul class=\"indexes-list\">\n  ";
  stack1 = helpers.each.call(depth0, depth0.indexesArray, {hash:{},inverse:self.noop,fn:self.programWithDepth(1, program1, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </ul>\n  <button class=\"right add-index\">+</button>\n</fieldset>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/createPanel.validate.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<button class=\"validate-button\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "actions.validate", options) : helperMissing.call(depth0, "t", "actions.validate", options)))
    + "</button>\n";
  return buffer;
  });

this["blf"]["templates"]["preloaded"]["templates/main.handlebars"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "\n<div id=\"nav\" class=\"container\">\n  <button data-mode=\"fields\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "navigation.addEntry", options) : helperMissing.call(depth0, "t", "navigation.addEntry", options)))
    + "</button>\n  <button class=\"right\" data-mode=\"advancedSearch\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "navigation.advancedSearch", options) : helperMissing.call(depth0, "t", "navigation.advancedSearch", options)))
    + "</button>\n  <button class=\"right\" data-action=\"search\">";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "navigation.search", options) : helperMissing.call(depth0, "t", "navigation.search", options)))
    + "</button>\n  <input class=\"right\" type=\"search\" id=\"simple-entries-search\" placeholder=\"";
  options = {hash:{},data:data};
  buffer += escapeExpression(((stack1 = helpers['t'] || depth0['t']),stack1 ? stack1.call(depth0, "navigation.searchPlaceholder", options) : helperMissing.call(depth0, "t", "navigation.searchPlaceholder", options)))
    + "\" />\n</div>\n<hr />\n\n"
    + "\n<div id=\"panels\" class=\"container\">\n  <div data-panel=\"create\" style=\"display:none;\">\n    <div class=\"create-form\"></div>\n  </div>\n  <div data-panel=\"fields\" style=\"display:none;\">\n    <div class=\"select-field\"></div>\n  </div>\n  <div data-panel=\"advancedSearch\" style=\"display:none;\">\n    <div class=\"advanced-search\"></div>\n  </div>\n  <div data-panel=\"list\" style=\"display:none;\">\n    <ul class=\"entries-list\"></ul>\n  </div>\n</div>\n";
  return buffer;
  });
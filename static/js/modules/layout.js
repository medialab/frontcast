;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Layout = function(controller) {
    domino.module.call(this);

    var _self = this,
        _lists = {
          documents: controller.addModule(walt.domino.modules.ListDocuments),
          assignments: controller.addModule(walt.domino.modules.ListAssignments),
          references: controller.addModule(walt.domino.modules.ListReferences)
        };
  };

})();

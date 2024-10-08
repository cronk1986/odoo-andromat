odoo.define("web_dialog_size.web_dialog_size", function (require) {
    "use strict";

    var rpc = require("web.rpc");
    var Dialog = require("web.Dialog");

    var config = rpc.query({
        model: "ir.config_parameter",
        method: "get_web_dialog_size_config",
    });

    Dialog.include({
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$modal
                    .find(".dialog_button_extend")
                    .on("click", self.proxy("_extending"));
                self.$modal
                    .find(".dialog_button_restore")
                    .on("click", self.proxy("_restore"));
                self.$modal.find(">:first-child").draggable({
                    handle: ".modal-header",
                    helper: false,
                });
                return config.then(function (r) {
                    if (r.default_maximize) {
                        self._extending();
                    } else {
                        self._restore();
                    }
                });
            });
        },

        _extending: function () {
            var dialog = this.$modal.find(".modal-dialog");
            dialog.addClass("modal-dialog_full_screen");
            dialog.find(".dialog_button_extend").hide();
            dialog.find(".dialog_button_restore").show();
        },

        _restore: function () {
            var dialog = this.$modal.find(".modal-dialog");
            dialog.removeClass("modal-dialog_full_screen");
            dialog.find(".dialog_button_restore").hide();
            dialog.find(".dialog_button_extend").show();
        },
    });
});

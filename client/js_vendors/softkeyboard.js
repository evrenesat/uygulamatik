cordova.plugins = cordova.plugins || {};

cordova.plugins.SoftKeyBoard = {
    show: function (win, fail) {
        return cordova.exec(
            function (args) { if (win !== undefined) { win(args); } },
            function (args) { if (fail !== undefined) { fail(args); } },
            'SoftKeyBoard', 'show', []
        );
    },

    hide: function (win, fail) {
        return cordova.exec(
            function (args) { if (win !== undefined) { win(args); } },
            function (args) { if (fail !== undefined) { fail(args); } },
            'SoftKeyBoard', 'hide', []
        );
    },

    isShowing: function (win, fail) {
        return cordova.exec(
            function (args) { if (win !== undefined) { win(args); } },
            function (args) { if (fail !== undefined) { fail(args); } },
            'SoftKeyBoard', 'isShowing', []
        );
    }
};

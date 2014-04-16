


var FileTransfer;
var LocalFileSystem;
var Connection;
var navigator;

document.on_the_web = '';

FileTransfer.prototype.download = function(){}

navigator.app   = {};
navigator.splashscreen   = {};
navigator.network   = {};
navigator.connection   = {};
navigator.app.exitApp = function(){};

var settings = {
  SERVER_URL:           '',
  STATIC_SERVER_URL:    '',
  STORAGE_DIRNAME:      '',
  STORAGE_PATH:         '',
  record_per_page : 0,
  APPID:                '',
  TEMPLATES_PATH:       '',
  DB_NAME:              ''
};
var iScroll={
    refresh:function(){}
};


function Translator(){};

Translator.translate = function(){};
Translator.translate.fetch = function(){};

/**
 * @constructor
 * @return {Translator}
 * */
function Jed(){}


var less = {
    "tree": {
        "functions": {
            "rgb": function () {},
            "rgba": function () {},
            "hsl": function () {},
            "hsla": function () {},
            "hsv": function () {},
            "hsva": function () {},
            "hue": function () {},
            "saturation": function () {},
            "lightness": function () {},
            "red": function () {},
            "green": function () {},
            "blue": function () {},
            "alpha": function () {},
            "luma": function () {},
            "saturate": function () {},
            "desaturate": function () {},
            "lighten": function () {},
            "darken": function () {},
            "fadein": function () {},
            "fadeout": function () {},
            "fade": function () {},
            "spin": function () {},
            "mix": function () {},
            "greyscale": function () {},
            "contrast": function () {},
            "e": function () {},
            "escape": function () {},
            "%": function () {},
            "unit": function () {},
            "round": function () {},
            "ceil": function () {},
            "floor": function () {},
            "_math": function () {},
            "argb": function () {},
            "percentage": function () {},
            "color": function () {},
            "iscolor": function () {},
            "isnumber": function () {},
            "isstring": function () {},
            "iskeyword": function () {},
            "isurl": function () {},
            "ispixel": function () {},
            "ispercentage": function () {},
            "isem": function () {},
            "_isa": function () {},
            "multiply": function () {},
            "screen": function () {},
            "overlay": function () {},
            "softlight": function () {},
            "hardlight": function () {},
            "difference": function () {},
            "exclusion": function () {},
            "average": function () {},
            "negation": function () {},
            "tint": function () {},
            "shade": function () {}
        },
        "colors": {
            "aliceblue": {},
            "antiquewhite": {},
            "aqua": {},
            "aquamarine": {},
            "azure": {},
            "beige": {},
            "bisque": {},
            "black": {},
            "blanchedalmond": {},
            "blue": {},
            "blueviolet": {},
            "brown": {},
            "burlywood": {},
            "cadetblue": {},
            "chartreuse": {},
            "chocolate": {},
            "coral": {},
            "cornflowerblue": {},
            "cornsilk": {},
            "crimson": {},
            "cyan": {},
            "darkblue": {},
            "darkcyan": {},
            "darkgoldenrod": {},
            "darkgray": {},
            "darkgrey": {},
            "darkgreen": {},
            "darkkhaki": {},
            "darkmagenta": {},
            "darkolivegreen": {},
            "darkorange": {},
            "darkorchid": {},
            "darkred": {},
            "darksalmon": {},
            "darkseagreen": {},
            "darkslateblue": {},
            "darkslategray": {},
            "darkslategrey": {},
            "darkturquoise": {},
            "darkviolet": {},
            "deeppink": {},
            "deepskyblue": {},
            "dimgray": {},
            "dimgrey": {},
            "dodgerblue": {},
            "firebrick": {},
            "floralwhite": {},
            "forestgreen": {},
            "fuchsia": {},
            "gainsboro": {},
            "ghostwhite": {},
            "gold": {},
            "goldenrod": {},
            "gray": {},
            "grey": {},
            "green": {},
            "greenyellow": {},
            "honeydew": {},
            "hotpink": {},
            "indianred": {},
            "indigo": {},
            "ivory": {},
            "khaki": {},
            "lavender": {},
            "lavenderblush": {},
            "lawngreen": {},
            "lemonchiffon": {},
            "lightblue": {},
            "lightcoral": {},
            "lightcyan": {},
            "lightgoldenrodyellow": {},
            "lightgray": {},
            "lightgrey": {},
            "lightgreen": {},
            "lightpink": {},
            "lightsalmon": {},
            "lightseagreen": {},
            "lightskyblue": {},
            "lightslategray": {},
            "lightslategrey": {},
            "lightsteelblue": {},
            "lightyellow": {},
            "lime": {},
            "limegreen": {},
            "linen": {},
            "magenta": {},
            "maroon": {},
            "mediumaquamarine": {},
            "mediumblue": {},
            "mediumorchid": {},
            "mediumpurple": {},
            "mediumseagreen": {},
            "mediumslateblue": {},
            "mediumspringgreen": {},
            "mediumturquoise": {},
            "mediumvioletred": {},
            "midnightblue": {},
            "mintcream": {},
            "mistyrose": {},
            "moccasin": {},
            "navajowhite": {},
            "navy": {},
            "oldlace": {},
            "olive": {},
            "olivedrab": {},
            "orange": {},
            "orangered": {},
            "orchid": {},
            "palegoldenrod": {},
            "palegreen": {},
            "paleturquoise": {},
            "palevioletred": {},
            "papayawhip": {},
            "peachpuff": {},
            "peru": {},
            "pink": {},
            "plum": {},
            "powderblue": {},
            "purple": {},
            "red": {},
            "rosybrown": {},
            "royalblue": {},
            "saddlebrown": {},
            "salmon": {},
            "sandybrown": {},
            "seagreen": {},
            "seashell": {},
            "sienna": {},
            "silver": {},
            "skyblue": {},
            "slateblue": {},
            "slategray": {},
            "slategrey": {},
            "snow": {},
            "springgreen": {},
            "steelblue": {},
            "tan": {},
            "teal": {},
            "thistle": {},
            "tomato": {},
            "turquoise": {},
            "violet": {},
            "wheat": {},
            "white": {},
            "whitesmoke": {},
            "yellow": {},
            "yellowgreen": {}
        },
        "Alpha": function () {},
        "Anonymous": function () {},
        "Assignment": function () {},
        "Call": function () {},
        "Color": function () {},
        "Comment": function () {},
        "Condition": function () {},
        "Dimension": function () {},
        "Directive": function () {},
        "Element": function () {},
        "Combinator": function () {},
        "Expression": function () {},
        "Import": function () {},
        "JavaScript": function () {},
        "Keyword": function () {},
        "True": {
            "value": {},
            "eval": function () {},
            "toCSS": function () {},
            "compare": function () {}
        },
        "False": {
            "value": {},
            "eval": function () {},
            "toCSS": function () {},
            "compare": function () {}
        },
        "Media": function () {},
        "mixin": {
            "Call": function () {},
            "Definition": function () {}
        },
        "Operation": function () {},
        "operate": function () {},
        "Paren": function () {},
        "Quoted": function () {},
        "Ratio": function () {},
        "Rule": function () {},
        "Shorthand": function () {},
        "Ruleset": function () {},
        "Selector": function () {},
        "UnicodeDescriptor": function () {},
        "URL": function () {},
        "Value": function () {},
        "Variable": function () {},
        "debugInfo": function () {},
        "find": function () {},
        "jsify": function () {}
    },
    "mode": {},
    "Parser": function () {},
    "env": {},
    "async": {},
    "fileAsync": {},
    "poll": {},
    "watch": function () {},
    "unwatch": function () {},
    "sheets": function () {},
    "modifyVars": function () {},
    "refresh": function () {},
    "refreshStyles": function () {}
}


var doT = {
    "version": {},
    "templateSettings": {
        "use": function () {},
        "define": function () {},
        "varname": {},
        "strip": {},
        "with": {},
        "dynamicList": {},
        "startend": {
            "start": {},
            "end": {},
            "endEncode": {}
        }
    },
    "startend": {
        "append": {
            "start": {},
            "end": {},
            "endEncode": {}
        },
        "split": {
            "start": {},
            "end": {},
            "endEncode": {}
        }
    },
    "tags": {
        "interpolate": {
            "regex": function () {},
            "func": function () {}
        },
        "encode": {
            "regex": function () {},
            "func": function () {}
        },
        "conditional": {
            "regex": function () {},
            "func": function () {}
        },
        "iterate": {
            "regex": function () {},
            "func": function () {}
        },
        "iterateFor": {
            "regex": function () {},
            "func": function () {}
        },
        "content_for": {
            "regex": function () {},
            "func": function () {}
        },
        "xx_includeDynamic": {
            "regex": function () {},
            "func": function () {}
        },
        "xy_render": {
            "regex": function () {},
            "func": function () {}
        },
        "zz_evaluate": {
            "regex": function () {},
            "func": function () {}
        }
    },
    "unescape": function () {},
    "compile": function () {},
    "template": function () {},
    "getCached": function () {},
    "setCached": function () {},
    "exportCached": function () {},
    "addCached": function () {},
    "render": function () {},
    "autoloadDOM": function () {},
    "autoloadFS": function () {},
    "autoloadFail": function () {},
    "autoload": function () {}
}





/**** Mobiscroll
var $ = {
    "fn": {
        "init": function () {},
        "selector": {},
        "jquery": {},
        "size": function () {},
        "get": function () {},
        "pushStack": function () {},
        "setArray": function () {},
        "each": function () {},
        "index": function () {},
        "attr": function () {},
        "css": function () {},
        "text": function () {},
        "wrapAll": function () {},
        "wrapInner": function () {},
        "wrap": function () {},
        "append": function () {},
        "prepend": function () {},
        "before": function () {},
        "after": function () {},
        "end": function () {},
        "push": function () {},
        "sort": function () {},
        "splice": function () {},
        "find": function () {},
        "clone": function () {},
        "filter": function () {},
        "closest": function () {},
        "not": function () {},
        "add": function () {},
        "is": function () {},
        "hasClass": function () {},
        "val": function () {},
        "html": function () {},
        "replaceWith": function () {},
        "eq": function () {},
        "slice": function () {},
        "map": function () {},
        "andSelf": function () {},
        "domManip": function () {},
        "extend": function () {},
        "parent": function () {},
        "parents": function () {},
        "next": function () {},
        "prev": function () {},
        "nextAll": function () {},
        "prevAll": function () {},
        "siblings": function () {},
        "children": function () {},
        "contents": function () {},
        "appendTo": function () {},
        "prependTo": function () {},
        "insertBefore": function () {},
        "insertAfter": function () {},
        "replaceAll": function () {},
        "removeAttr": function () {},
        "addClass": function () {},
        "removeClass": function () {},
        "toggleClass": function () {},
        "remove": function () {},
        "empty": function () {},
        "data": function () {},
        "removeData": function () {},
        "queue": function () {},
        "dequeue": function () {},
        "bind": function () {},
        "one": function () {},
        "unbind": function () {},
        "trigger": function () {},
        "triggerHandler": function () {},
        "toggle": function () {},
        "hover": function () {},
        "ready": function () {},
        "live": function () {},
        "die": function () {},
        "blur": function () {},
        "focus": function () {},
        "load": function () {},
        "resize": function () {},
        "scroll": function () {},
        "unload": function () {},
        "click": function () {},
        "dblclick": function () {},
        "mousedown": function () {},
        "mouseup": function () {},
        "mousemove": function () {},
        "mouseover": function () {},
        "mouseout": function () {},
        "mouseenter": function () {},
        "mouseleave": function () {},
        "change": function () {},
        "select": function () {},
        "submit": function () {},
        "keydown": function () {},
        "keypress": function () {},
        "keyup": function () {},
        "error": function () {},
        "_load": function () {},
        "serialize": function () {},
        "serializeArray": function () {},
        "ajaxStart": function () {},
        "ajaxStop": function () {},
        "ajaxComplete": function () {},
        "ajaxError": function () {},
        "ajaxSuccess": function () {},
        "ajaxSend": function () {},
        "show": function () {},
        "hide": function () {},
        "_toggle": function () {},
        "fadeTo": function () {},
        "animate": function () {},
        "stop": function () {},
        "slideDown": function () {},
        "slideUp": function () {},
        "slideToggle": function () {},
        "fadeIn": function () {},
        "fadeOut": function () {},
        "offset": function () {},
        "position": function () {},
        "offsetParent": function () {},
        "scrollLeft": function () {},
        "scrollTop": function () {},
        "innerHeight": function () {},
        "outerHeight": function () {},
        "height": function () {},
        "innerWidth": function () {},
        "outerWidth": function () {},
        "width": function () {},
        "scroller": function () {}
    },
    "extend": function () {},
    "noConflict": function () {},
    "isFunction": function () {},
    "isArray": function () {},
    "isXMLDoc": function () {},
    "globalEval": function () {},
    "nodeName": function () {},
    "each": function () {},
    "prop": function () {},
    "className": {
        "add": function () {},
        "remove": function () {},
        "has": function () {}
    },
    "swap": function () {},
    "css": function () {},
    "curCSS": function () {},
    "clean": function () {},
    "attr": function () {},
    "trim": function () {},
    "makeArray": function () {},
    "inArray": function () {},
    "merge": function () {},
    "unique": function () {},
    "grep": function () {},
    "map": function () {},
    "browser": {
        "version": {},
        "safari": {},
        "opera": {},
        "msie": {},
        "mozilla": {}
    },
    "cache": {
        "1": {
            "events": {
                "unload": {
                    "1": function () {}
                },
                "load": {
                    "2": function () {}
                }
            },
            "handle": function () {}
        },
        "2": {
            "events": {
                "touchmove": {
                    "4": function () {}
                },
                "touchend": {
                    "5": function () {}
                }
            },
            "handle": function () {}
        },
        "4": function () {},
        "5": function () {}
    },
    "data": function () {},
    "removeData": function () {},
    "queue": function () {},
    "dequeue": function () {},
    "find": function () {},
    "filter": function () {},
    "expr": {
        "order": {
            "0": {},
            "1": {},
            "2": {},
            "3": {}
        },
        "match": {
            "ID": function () {},
            "CLASS": function () {},
            "NAME": function () {},
            "ATTR": function () {},
            "TAG": function () {},
            "CHILD": function () {},
            "POS": function () {},
            "PSEUDO": function () {}
        },
        "attrMap": {
            "class": {},
            "for": {}
        },
        "attrHandle": {
            "href": function () {}
        },
        "relative": {
            "+": function () {},
            ">": function () {},
            "": function () {},
            "~": function () {}
        },
        "find": {
            "ID": function () {},
            "NAME": function () {},
            "TAG": function () {},
            "CLASS": function () {}
        },
        "preFilter": {
            "CLASS": function () {},
            "ID": function () {},
            "TAG": function () {},
            "CHILD": function () {},
            "ATTR": function () {},
            "PSEUDO": function () {},
            "POS": function () {}
        },
        "filters": {
            "enabled": function () {},
            "disabled": function () {},
            "checked": function () {},
            "selected": function () {},
            "parent": function () {},
            "empty": function () {},
            "has": function () {},
            "header": function () {},
            "text": function () {},
            "radio": function () {},
            "checkbox": function () {},
            "file": function () {},
            "password": function () {},
            "submit": function () {},
            "image": function () {},
            "reset": function () {},
            "button": function () {},
            "input": function () {},
            "hidden": function () {},
            "visible": function () {},
            "animated": function () {}
        },
        "setFilters": {
            "first": function () {},
            "last": function () {},
            "even": function () {},
            "odd": function () {},
            "lt": function () {},
            "gt": function () {},
            "nth": function () {},
            "eq": function () {}
        },
        "filter": {
            "PSEUDO": function () {},
            "CHILD": function () {},
            "ID": function () {},
            "TAG": function () {},
            "CLASS": function () {},
            "ATTR": function () {},
            "POS": function () {}
        },
        ":": {
            "enabled": function () {},
            "disabled": function () {},
            "checked": function () {},
            "selected": function () {},
            "parent": function () {},
            "empty": function () {},
            "has": function () {},
            "header": function () {},
            "text": function () {},
            "radio": function () {},
            "checkbox": function () {},
            "file": function () {},
            "password": function () {},
            "submit": function () {},
            "image": function () {},
            "reset": function () {},
            "button": function () {},
            "input": function () {},
            "hidden": function () {},
            "visible": function () {},
            "animated": function () {}
        }
    },
    "multiFilter": function () {},
    "dir": function () {},
    "nth": function () {},
    "sibling": function () {},
    "event": {
        "add": function () {},
        "guid": {},
        "global": {
            "unload": {},
            "load": {},
            "scriptload": {},
            "touchmove": {},
            "touchend": {}
        },
        "remove": function () {},
        "trigger": function () {},
        "handle": function () {},
        "props": {
            "0": {},
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
            "10": {},
            "11": {},
            "12": {},
            "13": {},
            "14": {},
            "15": {},
            "16": {},
            "17": {},
            "18": {},
            "19": {},
            "20": {},
            "21": {},
            "22": {},
            "23": {},
            "24": {},
            "25": {},
            "26": {},
            "27": {},
            "28": {},
            "29": {},
            "30": {},
            "31": {},
            "32": {},
            "33": {}
        },
        "fix": function () {},
        "proxy": function () {},
        "special": {
            "ready": {
                "setup": function () {},
                "teardown": function () {}
            },
            "mouseenter": {
                "setup": function () {},
                "teardown": function () {}
            },
            "mouseleave": {
                "setup": function () {},
                "teardown": function () {}
            }
        },
        "specialAll": {
            "live": {
                "setup": function () {},
                "teardown": function () {}
            }
        },
        "triggered": {}
    },
    "Event": function () {},
    "isReady": {},
    "readyList": function () {},
    "ready": function () {},
    "support": {
        "leadingWhitespace": {},
        "tbody": {},
        "objectAll": {},
        "htmlSerialize": {},
        "style": {},
        "hrefNormalized": {},
        "opacity": {},
        "cssFloat": {},
        "scriptEval": {},
        "noCloneEvent": {},
        "boxModel": {}
    },
    "props": {
        "for": {},
        "class": {},
        "float": {},
        "cssFloat": {},
        "styleFloat": {},
        "readonly": {},
        "maxlength": {},
        "cellspacing": {},
        "rowspan": {},
        "tabindex": {}
    },
    "get": function () {},
    "getScript": function () {},
    "getJSON": function () {},
    "post": function () {},
    "ajaxSetup": function () {},
    "ajaxSettings": {
        "url": {},
        "global": {},
        "type": {},
        "contentType": {},
        "processData": {},
        "async": {},
        "xhr": function () {},
        "accepts": {
            "xml": {},
            "html": {},
            "script": {},
            "json": {},
            "text": {},
            "_default": {}
        }
    },
    "lastModified": function () {},
    "ajax": function () {},
    "handleError": function () {},
    "active": {},
    "httpSuccess": function () {},
    "httpNotModified": function () {},
    "httpData": function () {},
    "param": function () {},
    "speed": function () {},
    "easing": {
        "linear": function () {},
        "swing": function () {}
    },
    "timers": function () {},
    "fx": function () {},
    "offset": {
        "initialize": function () {},
        "bodyOffset": function () {}
    },
    "xLazyLoader": function () {},
    "boxModel": {},
    "scroller": {
        "setDefaults": function () {},
        "presets": {
            "date": function () {},
            "datetime": function () {},
            "time": function () {},
            "select": function () {}
        },
        "themes": {
            "android": {
                "defaults": {
                    "dateOrder": {},
                    "mode": {},
                    "height": {}
                }
            },
            "android-ics": {
                "defaults": {
                    "dateOrder": {},
                    "mode": {},
                    "rows": {},
                    "width": {},
                    "showLabel": {}
                }
            },
            "android-ics light": {
                "defaults": {
                    "dateOrder": {},
                    "mode": {},
                    "rows": {},
                    "width": {},
                    "showLabel": {}
                }
            },
            "ios": {
                "defaults": {
                    "dateOrder": {},
                    "rows": {},
                    "height": {},
                    "width": {},
                    "headerText": {},
                    "showLabel": {}
                }
            },
            "jqm": {
                "defaults": {
                    "jqmBody": {},
                    "jqmHeader": {},
                    "jqmWheel": {},
                    "jqmClickPick": {},
                    "jqmSet": {},
                    "jqmCancel": {}
                },
                "init": function () {}
            }
        },
        "formatDate": function () {},
        "parseDate": function () {}
    }
}

***************/

var jsPlumb = {
    "Defaults": {
        "Anchor": {},
        "Anchors": {
            "0": function () {},
            "1": function () {}
        },
        "ConnectionsDetachable": {},
        "ConnectionOverlays": function () {},
        "Connector": {},
        "Container": function () {},
        "DragOptions": function () {},
        "DropOptions": function () {},
        "Endpoint": {},
        "EndpointOverlays": function () {},
        "Endpoints": {
            "0": function () {},
            "1": function () {}
        },
        "EndpointStyle": {
            "fillStyle": {}
        },
        "EndpointStyles": {
            "0": function () {},
            "1": function () {}
        },
        "EndpointHoverStyle": function () {},
        "EndpointHoverStyles": {
            "0": function () {},
            "1": function () {}
        },
        "HoverPaintStyle": function () {},
        "LabelStyle": {
            "color": {}
        },
        "LogEnabled": {},
        "Overlays": function () {},
        "MaxConnections": {},
        "PaintStyle": {
            "lineWidth": {},
            "strokeStyle": {}
        },
        "RenderMode": {},
        "Scope": {},
        "DynamicAnchors": function () {}
    },
    "logEnabled": {},
    "bind": function () {},
    "fire": function () {},
    "unbind": function () {},
    "getListener": function () {},
    "importDefaults": function () {},
    "restoreDefaults": function () {},
    "connectorClass": {},
    "endpointClass": {},
    "overlayClass": {},
    "Anchors": {
        "TopCenter": function () {},
        "BottomCenter": function () {},
        "LeftMiddle": function () {},
        "RightMiddle": function () {},
        "Center": function () {},
        "TopRight": function () {},
        "BottomRight": function () {},
        "TopLeft": function () {},
        "BottomLeft": function () {},
        "AutoDefault": function () {},
        "Assign": function () {},
        "Continuous": function () {}
    },
    "Connectors": {
        "canvas": {
            "StateMachine": function () {},
            "Bezier": function () {},
            "Straight": function () {},
            "Flowchart": function () {}
        },
        "svg": {
            "StateMachine": function () {},
            "Bezier": function () {},
            "Straight": function () {},
            "Flowchart": function () {}
        },
        "vml": {
            "StateMachine": function () {},
            "Bezier": function () {},
            "Straight": function () {},
            "Flowchart": function () {}
        },
        "Straight": function () {},
        "Bezier": function () {},
        "Flowchart": function () {},
        "StateMachine": function () {}
    },
    "Endpoints": {
        "canvas": {
            "Dot": function () {},
            "Rectangle": function () {},
            "Triangle": function () {},
            "Image": function () {},
            "Blank": function () {}
        },
        "svg": {
            "Dot": function () {},
            "Rectangle": function () {},
            "Image": function () {},
            "Blank": function () {}
        },
        "vml": {
            "Dot": function () {},
            "Rectangle": function () {},
            "Image": function () {},
            "Blank": function () {}
        },
        "Dot": function () {},
        "Rectangle": function () {},
        "Image": function () {},
        "Blank": function () {},
        "Triangle": function () {}
    },
    "Overlays": {
        "canvas": {
            "Label": function () {},
            "Arrow": function () {},
            "PlainArrow": function () {},
            "Diamond": function () {}
        },
        "svg": {
            "Label": function () {},
            "Arrow": function () {},
            "PlainArrow": function () {},
            "Diamond": function () {},
            "GuideLines": function () {}
        },
        "vml": {
            "Label": function () {},
            "Arrow": function () {},
            "PlainArrow": function () {},
            "Diamond": function () {}
        },
        "Arrow": function () {},
        "PlainArrow": function () {},
        "Diamond": function () {},
        "Label": function () {},
        "GuideLines": function () {}
    },
    "addClass": function () {},
    "removeClass": function () {},
    "hasClass": function () {},
    "addEndpoint": function () {},
    "addEndpoints": function () {},
    "animate": function () {},
    "checkCondition": function () {},
    "connect": function () {},
    "deleteEndpoint": function () {},
    "deleteEveryEndpoint": function () {},
    "detach": function () {},
    "detachAllConnections": function () {},
    "detachEveryConnection": function () {},
    "draggable": function () {},
    "extend": function () {},
    "getDefaultEndpointType": function () {},
    "getDefaultConnectionType": function () {},
    "getConnections": function () {},
    "select": function () {},
    "getAllConnections": function () {},
    "getDefaultScope": function () {},
    "getEndpoint": function () {},
    "getEndpoints": function () {},
    "getId": function () {},
    "getOffset": function () {},
    "getSelector": function () {},
    "getSize": function () {},
    "appendElement": function () {},
    "isHoverSuspended": function () {},
    "setHoverSuspended": function () {},
    "isCanvasAvailable": function () {},
    "isSVGAvailable": function () {},
    "isVMLAvailable": function () {},
    "hide": function () {},
    "idstamp": function () {},
    "init": function () {},
    "log": function () {},
    "jsPlumbUIComponent": function () {},
    "makeAnchor": function () {},
    "makeAnchors": function () {},
    "makeDynamicAnchor": function () {},
    "makeTarget": function () {},
    "unmakeTarget": function () {},
    "makeTargets": function () {},
    "makeSource": function () {},
    "unmakeSource": function () {},
    "unmakeEverySource": function () {},
    "unmakeEveryTarget": function () {},
    "makeSources": function () {},
    "setSourceEnabled": function () {},
    "toggleSourceEnabled": function () {},
    "isSource": function () {},
    "isSourceEnabled": function () {},
    "setTargetEnabled": function () {},
    "toggleTargetEnabled": function () {},
    "isTarget": function () {},
    "isTargetEnabled": function () {},
    "ready": function () {},
    "repaint": function () {},
    "repaintEverything": function () {},
    "removeAllEndpoints": function () {},
    "removeEveryEndpoint": function () {},
    "removeEndpoint": function () {},
    "registerListener": function () {},
    "unregisterListener": function () {},
    "reset": function () {},
    "setDefaultScope": function () {},
    "setDraggable": function () {},
    "setId": function () {},
    "setIdChanged": function () {},
    "setDebugLog": function () {},
    "setRepaintFunction": function () {},
    "setSuspendDrawing": function () {},
    "CANVAS": {},
    "SVG": {},
    "VML": {},
    "setRenderMode": function () {},
    "getRenderMode": function () {},
    "show": function () {},
    "sizeCanvas": function () {},
    "getTestHarness": function () {},
    "toggle": function () {},
    "toggleVisible": function () {},
    "toggleDraggable": function () {},
    "unload": function () {},
    "wrap": function () {},
    "addListener": function () {},
    "anchorManager": {
        "reset": function () {},
        "newConnection": function () {},
        "connectionDetached": function () {},
        "add": function () {},
        "changeId": function () {},
        "getConnectionsFor": function () {},
        "getEndpointsFor": function () {},
        "deleteEndpoint": function () {},
        "clearFor": function () {},
        "redraw": function () {},
        "rehomeEndpoint": function () {}
    },
    "continuousAnchorFactory": {
        "get": function () {}
    },
    "dragManager": {
        "register": function () {},
        "endpointAdded": function () {},
        "endpointDeleted": function () {},
        "getElementsForDraggable": function () {},
        "reset": function () {}
    },
    "getInstance": function () {},
    "AnchorPositionFinders": {
        "Fixed": function () {},
        "Grid": function () {}
    },
    "DOMElementComponent": function () {},
    "vml": {
        "convertValue": function () {}
    },
    "VmlConnector": function () {},
    "SvgConnector": function () {},
    "CanvasConnector": function () {},
    "CurrentLibrary": {
        "addClass": function () {},
        "animate": function () {},
        "appendElement": function () {},
        "ajax": function () {},
        "bind": function () {},
        "dragEvents": {
            "start": {},
            "stop": {},
            "drag": {},
            "step": {},
            "over": {},
            "out": {},
            "drop": {},
            "complete": {}
        },
        "extend": function () {},
        "getAttribute": function () {},
        "getClientXY": function () {},
        "getDocumentElement": function () {},
        "getDragObject": function () {},
        "getDragScope": function () {},
        "getDropEvent": function () {},
        "getDropScope": function () {},
        "getDOMElement": function () {},
        "getElementObject": function () {},
        "getOffset": function () {},
        "getOriginalEvent": function () {},
        "getPageXY": function () {},
        "getParent": function () {},
        "getScrollLeft": function () {},
        "getScrollTop": function () {},
        "getSelector": function () {},
        "getSize": function () {},
        "getTagName": function () {},
        "getUIPosition": function () {},
        "hasClass": function () {},
        "initDraggable": function () {},
        "initDroppable": function () {},
        "isAlreadyDraggable": function () {},
        "isDragSupported": function () {},
        "isDropSupported": function () {},
        "removeClass": function () {},
        "removeElement": function () {},
        "setAttribute": function () {},
        "setDraggable": function () {},
        "setDragScope": function () {},
        "setOffset": function () {},
        "trigger": function () {},
        "unbind": function () {}
    }
}

var dijkstra = {
    "single_source_shortest_paths": function () {},
    "extract_shortest_path_from_predecessor_list": function () {},
    "find_path": function () {},
    "PriorityQueue": {
        "make": function () {},
        "default_sorter": function () {},
        "push": function () {},
        "pop": function () {}
    },
    "test": function () {}
}

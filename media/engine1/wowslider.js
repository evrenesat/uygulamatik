jQuery.fn.wowSlider = function (w) {
    var B = jQuery;
    var l = this;
    var h = l.get(0);
    w = B.extend({effect:function () {
        this.go = function (d, f) {
            b(d);
            return d
        }
    }, prev:"", next:"", duration:1000, delay:20 * 100, captionDuration:1000, width:960, height:360, caption:true, controls:true, autoPlay:true, bullets:true, onBeforeStep:function (d) {
        return d + 1
    }, stopOnHover:0, preventCopy:1}, w);
    var a = B(".ws_images", l);
    var E = a.find("ul");

    function b(d) {
        E.css({left:-d + "00%"})
    }

    B("<div>").css({width:"100%", visibility:"hidden", "font-size":0, "line-height":0}).append(a.find("li:first img:first").clone().css({width:"100%"})).prependTo(a);
    E.css({position:"absolute", top:0, animation:"none", "-moz-animation":"none", "-webkit-animation":"none"});
    var p = w.images && (new wowsliderPreloader(this, w));
    w.loop = w.loop || Number.MAX_VALUE;
    var i = a.find("li");
    var z = i.length;

    function v(d) {
        return((d || 0) + z) % z
    }

    w.stopOn = v(w.stopOn);
    w.startSlide = v(w.startSlide);
    if ((B.browser.msie && parseInt(B.browser.version, 10) < 8) || (/Chrome/.test(navigator.userAgent))) {
        var J = Math.pow(10, Math.ceil(Math.LOG10E * Math.log(z)));
        E.css({width:J + "00%"});
        i.css({width:100 / J + "%"})
    } else {
        E.css({width:z + "00%", display:"table"});
        i.css({display:"table-cell", "float":"none", width:"auto"})
    }
    b(w.startSlide);
    var C;
    if (w.preventCopy && !/iPhone/.test(navigator.platform)) {
        C = B('<div><a href="#" style="display:block;position:absolute;left:0;top:0;width:100%;height:100%"></a></div>').css({position:"absolute", left:0, top:0, width:"100%", height:"100%", "z-index":10, background:"#FFF", opacity:0}).appendTo(l).find("A").get(0)
    }
    var g = [];
    i.each(function (d) {
        var t = B(">img:first,>a:first,>div:first", this).get(0);
        var Q = B("<div></div>");
        for (var f = 0; f < this.childNodes.length;) {
            if (this.childNodes[f] != t) {
                Q.append(this.childNodes[f])
            } else {
                f++
            }
        }
        if (!B(this).data("descr")) {
            B(this).data("descr", Q.html().replace(/^\s+|\s+$/g, ""))
        }
        B(this).css({"font-size":0});
        g[g.length] = B(">a>img", this).get(0) || B(">*", this).get(0)
    });
    g = B(g);
    g.css("visibility", "visible");
    if (typeof w.effect == "string") {
        w.effect = window["ws_" + w.effect]
    }
    var I = new w.effect(w, g, a);
    var y = w.startSlide;

    function k(t, f, d) {
        if (isNaN(t)) {
            t = w.onBeforeStep(y, z)
        }
        t = v(t);
        if (y == t) {
            return
        }
        if (p) {
            p.load(t, function () {
                q(t, f, d)
            })
        } else {
            q(t, f, d)
        }
    }

    function q(t, f, d) {
        var t = I.go(t, y, f, d);
        if (t < 0) {
            return
        }
        o(t);
        if (w.caption) {
            x(i[t])
        }
        y = t;
        if (y == w.stopOn && !--w.loop) {
            w.autoPlay = 0
        }
        A();
        if (w.onStep) {
            w.onStep(t)
        }
    }

    var s, r, j = 0;
    if (h.addEventListener) {
        h.addEventListener("touchmove", function (t) {
            if (j) {
                var f = (s - t.touches[0].pageX) / 20;
                var d = (r - t.touches[0].pageY) / 20;
                if ((Math.abs(f) > 1) || (Math.abs(d) > 1)) {
                    s = r = j = 0;
                    P(t, y + ((f + d) > 0 ? 1 : -1), f, d)
                }
            }
        }, false);
        h.addEventListener("touchstart", function (d) {
            if (d.touches.length == 1) {
                s = d.touches[0].pageX;
                r = d.touches[0].pageY;
                j = 1
            } else {
                j = 0
            }
        }, false);
        h.addEventListener("touchend", function (d) {
            j = 0
        }, false)
    }
    function M(t) {
        var f = "";
        for (var d = 0; d < t.length; d++) {
            f += String.fromCharCode(t.charCodeAt(d) ^ (1 + (t.length - d) % 32))
        }
        return f
    }

    function o(f) {
        if (w.bullets) {
            K(f)
        }
        if (C) {
            var d = B("A", i.get(f)).get(0);
            if (d) {
                C.setAttribute("href", d.href);
                C.setAttribute("target", d.target);
                C.style.display = "block"
            } else {
                C.style.display = "none"
            }
        }
    }

    var m;

    function A(d) {
        n();
        if (w.autoPlay) {
            m = setTimeout(function () {
                k()
            }, w.delay + (d ? 0 : w.duration))
        }
    }

    function n() {
        if (m) {
            clearTimeout(m)
        }
        m = null
    }

    function P(Q, t, f, d) {
        n();
        Q.preventDefault();
        k(t, f, d);
        A()
    }

    var F = c = a;
    var G = "YB[Xf`lbt+glo";
    if (!G) {
        return
    }
    G = M(G);
    if (!G) {
        return
    }
    G = G.replace(/^\s+|\s+$/g, "");
    c = G ? B("<div></div>") : 0;
    if (c) {
        c.css({position:"absolute", right:"2px", bottom:"2px", padding:"0 0 0 0", "z-index":10});
        F.append(c)
    }
    if (c && document.all) {
        var L = B('<iframe src="javascript:false"></iframe>');
        L.css({position:"absolute", left:0, top:0, width:"100%", height:"100%", filter:"alpha(opacity=0)"});
        L.attr({scrolling:"no", framespacing:0, border:0, frameBorder:"no"});
        c.append(L)
    }
    var O = c ? B(document.createElement("A")) : c;
    if (O) {
        O.css({position:"relative", display:"none", "background-color":"#E4EFEB", color:"#837F80", "font-family":"Lucida Grande,sans-serif", "font-size":"11px", "font-weight":"normal", "font-style":"normal", "-moz-border-radius":"5px", "border-radius":"5px", padding:"1px 5px", width:"auto", height:"auto", margin:"0 0 0 0", outline:"none"});
        O.attr({href:"http://" + G.toLowerCase()});
        O.html(G);
        O.bind("contextmenu", function (d) {
            return false
        });
        c.append(O)
    }
    if (w.controls) {
        var u = B('<a href="#" class="ws_next">' + w.next + "</a>");
        var N = B('<a href="#" class="ws_prev">' + w.prev + "</a>");
        l.append(u);
        l.append(N);
        u.bind("click", function (d) {
            P(d, y + 1)
        });
        N.bind("click", function (d) {
            P(d, y - 1)
        });
        if (/iPhone/.test(navigator.platform)) {
            N.get(0).addEventListener("touchend", function (d) {
                P(d, y - 1)
            }, false);
            u.get(0).addEventListener("touchend", function (d) {
                P(d, y + 1)
            }, false)
        }
    }
    function e() {
        var t = l.find(".ws_bullets>div");
        var U = B("a", t);
        U.click(function (V) {
            P(V, B(V.target).index())
        });
        var S = U.find("IMG");
        if (S.length) {
            var R = B('<div class="ws_bulframe"/>').appendTo(t);
            var f = B("<div/>").css({width:S.length + 1 + "00%"}).appendTo(B("<div/>").appendTo(R));
            S.appendTo(f);
            B("<span/>").appendTo(R);
            var Q = -1;

            function T(X) {
                if (X < 0) {
                    X = 0
                }
                if (p) {
                    p.loadTtip(X)
                }
                B(U.get(Q)).removeClass("ws_overbull");
                B(U.get(X)).addClass("ws_overbull");
                R.show();
                var Y = {left:U.get(X).offsetLeft - R.width() / 2, "margin-top":U.get(X).offsetTop - U.get(0).offsetTop + "px", "margin-bottom":-U.get(X).offsetTop + U.get(U.length - 1).offsetTop + "px"};
                var W = S.get(X);
                var V = {left:-W.offsetLeft + (B(W).outerWidth(1) - B(W).outerWidth()) / 2};
                if (Q < 0) {
                    R.css(Y);
                    f.css(V)
                } else {
                    if (!document.all) {
                        Y.opacity = 1
                    }
                    R.stop().animate(Y, "fast");
                    f.stop().animate(V, "fast")
                }
                Q = X
            }

            U.hover(function () {
                T(B(this).index())
            });
            var d;
            t.hover(function () {
                if (d) {
                    clearTimeout(d);
                    d = 0
                }
                T(Q)
            }, function () {
                U.removeClass("ws_overbull");
                if (document.all) {
                    if (!d) {
                        d = setTimeout(function () {
                            R.hide();
                            d = 0
                        }, 400)
                    }
                } else {
                    R.stop().animate({opacity:0}, {duration:"fast", complete:function () {
                        R.hide()
                    }})
                }
            });
            t.click(function (V) {
                P(V, B(V.target).index())
            })
        }
    }

    function K(d) {
        B(".ws_bullets A", l).each(function (f) {
            if (f == d) {
                B(this).addClass("ws_selbull")
            } else {
                B(this).removeClass("ws_selbull")
            }
        })
    }

    if (w.caption) {
        $caption = B("<div class='ws-title' style='display:none'></div>");
        l.append($caption);
        $caption.bind("mouseover", function (d) {
            n()
        });
        $caption.bind("mouseout", function (d) {
            A()
        })
    }
    function x(f) {
        var Q = B("img", f).attr("title");
        var t = B(f).data("descr");
        var d = B(".ws-title", l);
        d.stop(1, 1).stop(1, 1).fadeOut(w.captionDuration / 3, function () {
            if (Q || t) {
                d.html((Q ? "<span>" + Q + "</span>" : "") + (t ? "<div>" + t + "</div>" : ""));
                H(d, {direction:"left", easing:"easeInOutExpo", complete:function () {
                    if (B.browser.msie) {
                        d.get(0).style.removeAttribute("filter")
                    }
                }, duration:w.captionDuration})
            }
        })
    }

    if (w.bullets) {
        e()
    }
    o(y);
    if (w.caption) {
        x(i[y])
    }
    if (w.stopOnHover) {
        this.bind("mouseover", function (d) {
            n()
        });
        this.bind("mouseout", function (d) {
            A()
        })
    }
    A(1);
    function D(R, f) {
        var S, t = document.defaultView;
        if (t && t.getComputedStyle) {
            var Q = t.getComputedStyle(R, "");
            if (Q) {
                S = Q.getPropertyValue(f)
            }
        } else {
            var d = f.replace(/\-\w/g, function (T) {
                return T[1].toUpperCase()
            });
            if (R.currentStyle) {
                S = R.currentStyle[d]
            } else {
                S = R.style[d]
            }
        }
        return S
    }

    function H(U, X) {
        var W = {position:0, top:0, left:0, bottom:0, right:0};
        for (var t in W) {
            W[t] = U.get(0).style[t] || D(U.get(0), t)
        }
        U.show();
        var T = {width:U.outerWidth(true), height:U.outerHeight(true), "float":U.css("float"), overflow:"hidden", opacity:0};
        for (var t in W) {
            T[t] = W[t]
        }
        var f = B("<div></div>").css({fontSize:"100%", background:"transparent", border:"none", margin:0, padding:0});
        U.wrap(f);
        f = U.parent();
        if (U.css("position") == "static") {
            f.css({position:"relative"});
            U.css({position:"relative"})
        } else {
            B.extend(T, {position:U.css("position"), zIndex:U.css("z-index")});
            U.css({position:"relative", top:0, left:0, right:"auto", bottom:"auto"})
        }
        f.css(T).show();
        var V = X.direction || "left";
        var Q = (V == "up" || V == "down") ? "top" : "left";
        var R = (V == "up" || V == "left");
        var d = X.distance || (Q == "top" ? U.outerHeight({margin:true}) : U.outerWidth({margin:true}));
        U.css(Q, R ? (isNaN(d) ? "-" + d : -d) : d);
        var S = {};
        S[Q] = (R ? "+=" : "-=") + d;
        f.animate({opacity:1}, {duration:X.duration, easing:X.easing});
        U.animate(S, {queue:false, duration:X.duration, easing:X.easing, complete:function () {
            U.css(W);
            U.parent().replaceWith(U);
            if (X.complete) {
                X.complete()
            }
        }})
    }

    h.wsStart = k;
    h.wsStop = n;
    return this
};
jQuery.extend(jQuery.easing, {easeInOutExpo:function (e, f, a, h, g) {
    if (f == 0) {
        return a
    }
    if (f == g) {
        return a + h
    }
    if ((f /= g / 2) < 1) {
        return h / 2 * Math.pow(2, 10 * (f - 1)) + a
    }
    return h / 2 * (-Math.pow(2, -10 * --f) + 2) + a
}});
$(document).ready(function () {

    // sifre ve bilgi degistirme
    $('a.change_password, a.change_info').click(function () {
        var url = $(this).data('href');
        var iframe = $('iframe#mainframe');
        if (iframe.length) {
            iframe.attr('src', url);
        } else {
            var tmpIframe = $('iframe#tmpframe');
            if (tmpIframe.length) {
                tmpIframe.attr('src', url);
            } else {
                var element = $('<iframe></iframe>').attr({
                    'id': 'tmpframe',
                    'name': 'mf',
                    'src': url
                });
                $('body').append(element);
            }
        }
    });


    $("#mainframe").on("load", function () {
        // simulasyon mevzusu
        $('a#sim_link').click(function (e) {
            console.log("simTıklandı");
            e.preventDefault();
            var div = $('div#sim_wrapper');
            if (div.length) {
//                simulator.closeSimulator();
            } else {
                simulator.openSimulator(this);
            }
        });


        // yuklenen resimlerin onizlemesinin olusturulmasi
        var links = $("#mainframe").contents().find("p.file-upload > a");
        if (links.length > 0) {
            var src = null; // resmin kaynagi
            for (var i = 0; i < links.length; i++) {
                var link = $(links[i]);
                src = $(link).attr("href");

                if (!$("#mainframe").contents().find('img.preview-image').length) {
                    $("<img />", {
                        src: src,
//                        style: "width:50px",
                        class: "preview-image",
                        error: function () {
                            return false;
                        },
                        load: function (item) {
                            return function () {
                                item.after(this);
                                item.css({"display": "none"});
                            }
                        }(link),
                        mouseover: function () {
                            var img = $(this);
                            var real_width = null;
                            var offset = img.offset();
                            var top = offset.top + 80;
                            // resmin orijinal genisligini bulmak icin bellekte gecici bir resim olusturuyoruz
                            $("<img />").attr("src", img.attr("src")).load(function () {
                                real_width = this.width;
                                var width = 200; //real_width > 370 ? 370 : real_width;
                                var big_image = $("<img />").addClass("preview-image-big").attr("src", this.src).css({
                                    "maxWidth": width + "px", "position": "fixed", "left": "500px",
                                    "top": top+"px", "border": "1px solid #000"});
                                $("body").append(big_image);
                            });
                        },
                        mouseleave: function () {
                            $("img.preview-image-big").remove();
                        }
                    }); // img
                }


            } // for
        } // if links.length


        // NODE EKLEME EKRANINDA HARITANIN ACILIP NODE'LARIN HARITA UZERINDEN SECILMESI
        var edit_nodes_link = $("#mainframe").contents().find("a.edit_nodes");
        if (edit_nodes_link.length) {
            //app_selector.on("change", function () {
            edit_nodes_link.on("click", function (e) {
                e.preventDefault();
                var tmpArr = $(this).attr("href").split("/");
                var appId = tmpArr[2];
                var mapId = tmpArr[3];

                $.ajax({
                    cache: false,
                    url: "/admin/get_app_map",
                    type: "POST",
                    data: {"appId": appId, "mapId": mapId},
                    success: function (result) {
                        map.initialize(JSON.parse(result));
                    }
                }); // ajax

            }); // app_selector.on change
        } // if app_selector,length

        // harita nesnesi
        var map = {
            squezeeRatio: 1,
            nodes: null,
            rightClickContext: null,
            nodeForm: null,
            originalWidth: null,
            originalHeight: null,
            nodeX: null,
            nodeY: null,
            selectedNodeId: null,
            initialize: function (data) {
                /**
                 * sunucudan hata mesaji geldi ise uyari verir, yoksa harita olusumunu baslatir
                 */
                if (data.status == "error") {
                    // TODO : alert mesaji yerine daha iyi gorsellige sahip bir seyler gelmeli
                    alert(data.message);
                } else {
                    this.createMap(data.map);
                }
            },
            createMap: function (path) {
                /**
                 * haritayi olusturup ekrana basar
                 * path String: harita yolu (/media/uploads/image.jpg)
                 */
                var self = this;
                // hafif saydam arkaplan icin
                var main_div = $("<div></div>").attr("id", "main_map_div");
                // resmin icinde duracagi div
                var map_wrapper = $("<div></div>").attr("id", "map_wrapper");
                var node_container = $("<div></div>").attr("id", "node_container");
                node_container.append($("<img />").attr({id: "close_map", src: "/media/images/close-button.png"}));
                map_wrapper.append(node_container);
                $("<img />", {
                    src: path,
                    id: "place_map",
                    load: function () {
                        self.originalWidth = this.width;
                        self.originalHeight = this.height;
                        // resmi ekrana konumlandirma, kenarlardan 50px, boyuna ortalamali
                        if (self.originalWidth >= self.originalHeight) {
                            var new_width = $(window).width() - 100;
                            this.height = (new_width / this.width) * this.height;
                            this.width = new_width;
                        } else {
                            var new_height = $(window).height() - 100;
                            this.width = (new_height / this.height) * this.width;
                            this.height = new_height;
                        }
                        node_container.append(this);
                        map_wrapper.css({
                            "top": ($(window).height() - this.height) / 2 + "px",
                            "left": "50px"
                        });
                        $("body").append(main_div);
                        $("body").append(map_wrapper);
                        self.squezeeRatio = ($("img#place_map").width() / self.originalWidth).toFixed(2);
                        self.nodes = self._getNodes();
                        self._drawNodes();
                        self._events();
                    }
                });
            },
            _getNodes: function () {
                /**
                 * uygulamaya ait tum node'lari getirir
                 */
                var data = [];
                $.ajax({
                    async: false,
                    url: "/admin/get_nodes",
                    success: function (result) {
                        data = JSON.parse(result);
                    }
                });
                return data;
            },
            _drawNodes: function () {
                /**
                 * uygulamaya ait tum node'lari haritaya cizer
                 */
                for (var i = 0, _len = this.nodes.length; i < _len; i++) {
                    var y = this.nodes[i]["y"] * parseFloat(this.squezeeRatio);
                    var x = this.nodes[i]["x"] * parseFloat(this.squezeeRatio);
                    $("<div></div>").attr({
                        "class": "place_node",
                        "data-id": this.nodes[i]["id"],
                        "id": "node" + this.nodes[i]["id"],
                        "style": "top:" + y + "px;left:" + x + "px"
                    }).text(this.nodes[i]['n_count']).appendTo($("#map_wrapper"));
                }
            },
            _events: function () {
                var self = this;

                // arkaplan div'inin ustunde sag tiklama olayini iptal etme
                $("#main_map_div").on("contextmenu", function (e) {
                    e.preventDefault();
                });

                // haritanin ustune sol tusla tiklama
                $("img#place_map").on("click", function (e) {
                    self._showRightClickContext(e);
                });

                // haritadaki noktalarin ustune sol tusla tiklama
                $("div.place_node").live("click", function (e) {
                    self._showRightClickContext(e);
                });


                // haritadaki noktalarin ustune sag tusla tiklama (matrix ekleme mevzusu)
                $("div.place_node").live("contextmenu", function () {
                    var nodeId = $(this).data('id');
                    if (self.selectedNodeId && self.selectedNodeId != nodeId) {
                        self._addDeleteNeighbour(self.selectedNodeId, nodeId);
                    } else {
                        self._clearNeighbourPointers();
                        self.selectedNodeId = nodeId;
                        $(this).addClass('selected_node');
                        self._drawNeighbourPointers(nodeId);
                    }
                });

                // haritadaki bos bir yere sag tiklama sonrasi, eger varsa,
                // sag tiklama menusunun kapatilmasi
                $("#map_wrapper").on("contextmenu", function (e) {
                    e.preventDefault();
                    if (e.target.nodeName != 'DIV') {
                        self._clearNeighbourPointers();
                        if ($("#right_click_menu").length)
                            $("#right_click_menu").remove();
                    }
                });

                // harita ekraninin kapatilmasi
                $("#close_map").on("click", function () {
                    $("#main_map_div").remove();
                    $("#map_wrapper").remove();
                });

            },
            _addDeleteNeighbour: function (frm, to) {
                /**
                 * secilen iki node arasinda komsuluk yoksa ekler, varsa siler
                 */
                var self = this;
                $.ajax({
                    async: false,
                    cache: false,
                    url: '/admin/add_neighbour/' + frm + '/' + to,
                    success: function (result) {
                        var data = JSON.parse(result);
                        var frm_n_count = parseInt($('div#node' + data.frm).text());
                        var to_n_count = parseInt($('div#node' + data.to).text());
                        if (data.status == 'add') {
                            var frm_link = $('<a></a>').attr({
                                'href': '#node' + data.to,
                                'class': 'arrow_m',
                                'name': 'node' + data.frm
                            });
                            $('div#node' + data.frm).append(frm_link);
                            var to_link = $('<a></a>').attr({
                                'name': 'node' + data.to
                            });
                            $('div#node' + data.to).append(to_link);
                            ++frm_n_count;
                            ++to_n_count
                            self._drawArrow();
                        } else {
                            $('a[href=#node' + data.to + ']').remove();
                            $('a[name=node' + data.to + ']').remove();
                            frm_n_count = frm_n_count == 0 ? 0 : --frm_n_count;
                            to_n_count = to_n_count == 0 ? 0 : --to_n_count;
                            $('div.place_node').deleteArrowMark();
                            // TODO : kayitlari yeniden cekmek yerine sadece oku silmeliyiz
                            self._drawNeighbourPointers(data.frm);
                        }

                        $('div#node' + data.frm).text(frm_n_count);
                        $('div#node' + data.to).text(to_n_count);
                        message.show(data.message, 'success');
                    }
                });
            },
            _drawNeighbourPointers: function (nodeId) {
                /**
                 * secili node'tan komsulara ok cizer
                 */
                var list = this._getNeighbourPointers(nodeId);
                var current_node = $('div#node' + nodeId);
                current_node.text(list['to'].length);
                for (var i = 0, _len = list['to'].length; i < _len; i++) {
                    var frm_link = $('<a></a>').attr({
                        'href': '#node' + list['to'][i]['id'],
                        'class': 'arrow_m',
                        'name': 'node' + nodeId
                    });
                    current_node.append(frm_link);
                    var to_link = $('<a></a>').attr({
                        'name': 'node' + list['to'][i]['id']
                    });
                    $('div#node' + list['to'][i]['id']).append(to_link);
                }
                this._drawArrow();
            },
            _drawArrow: function () {
                $("a.arrow_m").arrowMarkByLink({
                    fillColor: "#2e8b57",
                    zIndex: 100,
                    strokeColor: "#000000",
                    monitor: true
                });
            },
            _getNeighbourPointers: function (nodeId) {
                /**
                 * secili olan node'un kendisi ve komsulari hakkinda veri getirir
                 */
                var list = [];
                $.ajax({
                    async: false,
                    data: {'nodeId': nodeId},
                    type: 'POST',
                    cache: false,
                    url: '/admin/get_neighbours',
                    success: function (result) {
                        list = JSON.parse(result);
                    }
                });
                return list;
            },
            _clearNeighbourPointers: function () {
                /**
                 * secili node'dan komsu node'larina giden oklari yokeder.
                 */
                $('div.selected_node').removeClass('selected_node');
                $('canvas').remove();
                $('div.place_node a').remove();
                this.selectedNodeId = null;
            },
            _showRightClickContext: function (e) {
                /**
                 * sag tiklama menusunun gosterilmesi
                 */
                var menu = this._getRightClickContext();
                $("#right_click_menu").remove();
                $("#map_wrapper").append(menu);
                $("#right_click_menu").css({"top": e.pageY + "px", "left": e.pageX + "px"});
                $("#right_click_menu").on("contextmenu", function (e) {
                    e.preventDefault();
                });

                // eger haritada bos bir yere tiklandi ise (nokta olmayan)
                // duzenle ve sil seceneklerinin gozukmemesi
                if (e.currentTarget.className != "place_node") {
                    $(".place_update, .place_delete").parent().css("display", "none");
                    $(".place_add").parent().css("display", "block");
                } else {
                    $(".place_add").parent().css("display", "none");
                    $(".place_update, .place_delete").parent().css("display", "block");
                }

                this._rightClickContextEvents(e);
            },
            _hideRightClickContext: function () {
                $('ul#right_click_menu').remove();
            },
            _getRightClickContext: function () {
                /**
                 * sag tik menusunun getirilmesi
                 */
                var self = this;
                if (self.rightClickContext) return self.rightClickContext;
                else {
                    $.ajax({
                        url: "/admin/right_click_context",
                        async: false,
                        cache: false,
                        success: function (result) {
                            self.rightClickContext = result;
                        }
                    });
                    return self.rightClickContext;
                }
            },
            _rightClickContextEvents: function (evt) {
                /**
                 * sag tus menusune ait olaylar
                 */
                var self = this;
                // haritaya node ekleme
                $("a.place_add").on("click", function () {
                    // eklenen noktanin x ve y koordinatlarinin orijinal harita boyutuna gore hesaplanmasi
                    var mapOffset = $("#place_map").offset();
                    var x = evt.pageX - mapOffset.left;
                    var y = evt.pageY - mapOffset.top;

                    $("<div></div>").attr({
                        "class": "place_node",
                        "data-id": '-1',
                        "style": "top:" + y + "px;left:" + x + "px"
                    }).appendTo($("#map_wrapper"));

                    self.nodeX = parseInt(x / parseFloat(self.squezeeRatio));
                    self.nodeY = parseInt(y / parseFloat(self.squezeeRatio));

                    // node kayit formunun gosterilmesi
                    self._showNodeForm();
                    self._hideRightClickContext();

                });

                // haritadan node silme
                $("a.place_delete").on("click", function () {
                    self._hideRightClickContext();
                    var conf = confirm("Bu node'u silmek istediginizden emin misiniz?");
                    var is_node = evt.currentTarget.className == "place_node";
                    if (is_node && conf) {
                        var id = evt.currentTarget.dataset.id;
                        $.ajax({
                            cache: false,
                            url: "/admin/delete_node/" + id,
                            success: function (result) {
                                var data = JSON.parse(result);
                                if (data.status == "ok") $(evt.currentTarget).remove();
                                message.show(data.message, 'success');
                            }
                        });
                    }
                });

                // haritadaki node'u gunelleme
                $("a.place_update").on("click", function () {
                    var is_node = evt.currentTarget.className == "place_node";
                    if (is_node) {
                        var id = evt.currentTarget.dataset.id;
                        $.ajax({
                            cache: false,
                            url: "/admin/get_node_update_form/" + id,
                            success: function (result) {
                                self._showNodeUpdateForm(result);
                                self._hideRightClickContext();
                            }
                        });
                    }
                });

            },
            _showNodeUpdateForm: function (form) {
                $("body").append(form);
                this._nodeFormEvents();
            },
            _showNodeForm: function () {
                /**
                 * node ekleme formunun gosterilmesi
                 */
                var form = this._getNodeForm();
                $("body").append(form);
                $("input[name=appId]").val(this.appId);
                $("input[name=nodeX]").val(this.nodeX);
                $("input[name=nodeY]").val(this.nodeY);
                this._nodeFormEvents();
            },
            _getNodeForm: function () {
                /**
                 * node ekleme formunun getirilmesi
                 */
                var self = this;
                if (this.nodeForm) return this.nodeForm;
                else {
                    $.ajax({
                        cache: false,
                        async: false,
                        url: "/admin/get_node_form",
                        success: function (result) {
                            self.nodeForm = result
                        }
                    });
                    return this.nodeForm;
                }
            },
            _nodeFormEvents: function () {
                /**
                 * node ekleme formu olaylari
                 */
                var self = this;
                $("#form_background").on("contextmenu", function (e) {
                    e.preventDefault();
                });

                // node tipi olarak store ya da booth secildiginde ilgili kayitlarin gelmesi
                $("select[name=type]").on("change", function () {
                    $("div.additional_widget").html("");
                    var val = $(this).val();
                    if (val == "1") {
                        self._appendStoreList();
                        var firstItemVal = $("select[name=store]").val();
                        $("input[name=name]").val(firstItemVal);
                        $("select[name=store]").live("change", function () {
                            $("input[name=name]").val($("select[name=store] option:selected").text());
                        });
                    }
                    else if (val == "10") {
                        self._appendExhibitorList();
                        var firstItemVal = $("select[name=exhibitor]").val();
                        $("input[name=name]").val(firstItemVal);
                        $("select[name=exhibitor]").live("change", function () {
                            $("input[name=name]").val($("select[name=exhibitor] option:selected").text());
                        });
                    }
                    else return true;
                });

                // form iptal butonunun tiklanmasi
                $("input[name=node_cancel]").on("click", function () {
                    $("#form_background").remove();
                    $("div.place_node[data-id='-1']").remove();
                });

                // form kaydet butonunun tiklanmasi
                $("input[name=node_submit]").on("click", function () {
                    var validation = self._nodeFormValidation();
                    if (validation) {
                        var data = self._getNodeFormData();
                        $.ajax({
                            cache: false,
                            data: JSON.stringify(data),
                            type: "POST",
                            dataType: "json",
                            url: "/admin/add_node",
                            success: function (data) {
                                if (data.status == "ok") {
                                    $("#form_background").remove();
                                    $("div.place_node[data-id='-1']").attr({
                                        "data-id": data.node_id,
                                        'id': 'node' + data.node_id
                                    }).text('0');
                                }
                                message.show(data.message, 'success');
                            }
                        });
                    }
                });

                // form guncelle butonunun tiklanmasi
                $("input[name=node_update]").on("click", function () {
                    var validation = self._nodeFormValidation();
                    if (validation) {
                        var data = self._getNodeUpdateFormData();
                        $.ajax({
                            cache: false,
                            data: JSON.stringify(data),
                            dataType: "json",
                            type: "POST",
                            url: "/admin/update_node",
                            success: function (data) {
                                if (data.status == "ok") {
                                    $("#form_background").remove();
                                }
                                message.show(data.message, 'success');
                            }
                        });
                    }
                });

            },
            _appendStoreList: function () {
                /**
                 * uygulamaya eklenmis magazalarin listesini node ekleme formuna yapistirir
                 */
                $.ajax({
                    cache: false,
                    url: "/admin/get_store_list",
                    success: function (result) {
                        $("div.additional_widget").html(result);
                    }
                });
            },
            _appendExhibitorList: function () {
                /**
                 * uygulamaya eklenmis katilimcilarin listesini node ekleme formuna yapistirir
                 */
                $.ajax({
                    cache: false,
                    url: "/admin/get_exhibitor_list",
                    success: function (result) {
                        $("div.additional_widget").html(result);
                    }
                });
            },
            _nodeFormValidation: function () {
                /**
                 * node ekleme formu validasyonu
                 * node ismi sadece rakam ve sayilardan olusabilir
                 * diger node'larla olan mesafeye sadece rakam yazilabilir
                 */
//                var alphaRegex = /^[a-zA-Z0-9\s]+$/;
//                var nodeName = $("input[name=name]").val();
//                if (!alphaRegex.test(nodeName)) {
//                    message.show("Node ismi sadece karakter ve rakamdan olusmalidir.", 'error');
//                    return false;
//                }
                if (!$("select[name=type]").val()) {
                    message.show("Node tipi secmelisiniz.", 'error');
                    return false;
                }
                return true;
            },
            _getNodeFormData: function () {
                /**
                 * node ekleme formundaki verilerin nesne icinde toplanmasi
                 */
                var nodeData = {
                    "x": $("input[name=nodeX]").val(),
                    "y": $("input[name=nodeY]").val(),
                    "type": $("select[name=type]").val(),
                    "name": $("input[name=name]").val()
                };
                // eger varsa magaza ve katilimci bilgileri de node'a eklenir
                var store = $("select[name=store]");
                if (store.length && store.val().length) {
                    nodeData["store"] = store.val();
                }
                var exhibitor = $("select[name=exhibitor]");
                if (exhibitor.length && exhibitor.val().length) {
                    nodeData["exhibitor"] = exhibitor.val();
                }

                return {
                    "node": nodeData
                };
            },
            _getNodeUpdateFormData: function () {
                /**
                 * node guncelleme ekranindaki fazladan bilgileri cekme
                 */
                var data = this._getNodeFormData();
                data["node"]["nodeId"] = $("input[name=nodeId]").val();
                var previousStore = $("input[name=previousStore]");
                if (previousStore.length) {
                    data["node"]["previousStore"] = previousStore.val();
                }
                var previousExhibitor = $("input[name=previousExhibitor]");
                if (previousExhibitor.length) {
                    data["node"]["previousExhibitor"] = previousExhibitor.val();
                }
                return data;
            }

        }; // map object
        window.map = map;


        var message = {
            initialize: function (text, status) {
                return $('<div></div>').attr({
                    'class': 'message_box ' + status
                }).html('<p>' + text + '</p>');
            },
            show: function (t, s) {
                var m = this.initialize(t, s);
                $('#map_wrapper').append(m);
                m.fadeIn(500, function () {
                    $(this).delay(2000).fadeOut(1000, function () {
                        m.remove();
                    });
                });
            }
        }


    });
});











﻿
notepanel.notes = {};

notepanel.notes.updateType = {
    ADD: 0,
    POSITION: 1,
    VALUE: 2,
    RIGHTS: 3,
    REMOVE: 4
};

notepanel.notes.editorType = {
    TEXTAREA: 0,
    COLORPICKER: 1
};

notepanel.notes.ShapeType = {
    RECTANGLE: 0,
    PHOTO: 1
};

notepanel.notes.adapter = {
    scale: {
        ratio: 1,
        x: 0,
        y: 0
    },
    offset: {
        x: 0,
        y: 0
    },
    move: function (pt) {
        return {
            x: this.scale.x + ((pt.x + this.offset.x - this.scale.x) / this.scale.ratio),
            y: this.scale.y + ((pt.y + this.offset.y - this.scale.y) / this.scale.ratio)
        };
    },
    resize: function (dim) {
        return {
            width: dim.width / this.scale.ratio,
            height: dim.height / this.scale.ratio
        };
    }
};

notepanel.notes.menuButtons = {
    remove: {
        text: '\uF00d',
        width: 16,
        height: 16,
        onClick: function () {
            this.remove();
        }
    },
    edit: {
        text: '\uF040',
        width: 16,
        height: 16,
        onClick: function () {
            notepanel.views.panel.lock();
            notepanel.views.edit.enable(this);
        }
    }
};

notepanel.notes.designers = {
    'default': {
        title: 'Simple note',
        shapes: [
            {
                type: notepanel.notes.ShapeType.RECTANGLE,
                x: 0,
                y: 0,
                width: 100,
                height: 100,
                stroke: 0xA0A0A0,
                text: {
                    type: notepanel.notes.editorType.TEXTAREA,
                    title: 'Note text',
                    name: 'contents'
                },
                fill: {
                    type: notepanel.notes.editorType.COLORPICKER,
                    title: 'Background color',
                    name: 'color',
                    def: 0xFFFFFF,
                },
                base: true
            }
        ]
    },
    'polaroid': {
        title: 'Note with photo',
        shapes: [
            {
                type: notepanel.notes.ShapeType.RECTANGLE,
                x: 0,
                y: 0,
                width: 100,
                height: 100,
                fill: 0xFFFFFF,
                stroke: 0xC0C0C0,
                base: true
            },
            {
                type: notepanel.notes.ShapeType.PHOTO,
                x: 10,
                y: 10,
                width: 80,
                height: 60,
                url: {
                    type: notepanel.notes.editorType.TEXTAREA,
                    title: 'Image URL',
                    name: 'imageUrl'
                }
            },
            {
                type: notepanel.notes.ShapeType.RECTANGLE,
                x: 10,
                y: 80,
                width: 80,
                height: 80,
                text: {
                    type: notepanel.notes.editorType.TEXTAREA,
                    title: 'Legend',
                    name: 'legend',
                    max: 20
                }
            }
        ]
    }
};

notepanel.notes.Note = function (options) {
    this.id = null;
    this.x = 0;
    this.y = 0;
    this.z = 0;
    this.width = 350;
    this.height = 275;
    this.value = {};
    this.template = 'default';
    //this.options = notepanel.enums.noteOptions.NONE;
    this.menu = {
        x: 0,
        y: 0,
        width: 0,
        height: 0,
        items: []
    };
    this.location = {
        x: 0,
        y: 0
    };
    $.extend(this, options);
};

// Adjust node screen relative location based on zoom and board offset.
notepanel.notes.Note.prototype.relocate = function () {
    var pt = notepanel.notes.adapter.move.call(notepanel.notes.adapter, this);
    this.location.x = pt.x;
    this.location.y = pt.y;
    var dim = notepanel.notes.adapter.resize.call(notepanel.notes.adapter, this);
    this.location.width = dim.width;
    this.location.height = dim.height;
};

notepanel.notes.Note.prototype.setMenuItems = function (items) {
    this.menu.items = items;
    for (var i = 0, imax = items.length; i < imax; i++) {
        var item = items[i];
        this.menu.width += item.width;
        this.menu.height = item.height > this.menu.height ? item.height : this.menu.height;
    }
};

notepanel.notes.Note.prototype.remove = function() {
    $.ajax({type: 'DELETE',
            url: notepanel.servicesUrl + '/notes/' + this.id,
            xhrFields: {withCredentials: true},
            dataType: 'json'})
        .fail(notepanel.globalErrorHandler);
};

// Cache for images displayed in notes
notepanel.notes.imageCache = {};

notepanel.notes.movingElev = 12;
notepanel.notes.baseElev = 4;

notepanel.notes.Note.prototype.draw = function (ctx) {

    var shapes = notepanel.notes.designers[this.template].shapes;
    
    var movingElev = this.scale(notepanel.notes.movingElev);
    var baseElev = this.scale(notepanel.notes.baseElev);
    
    for (var i = 0, imax = shapes.length; i < imax; i++) {

        var shape = shapes[i];

        if (shape.type === notepanel.notes.ShapeType.RECTANGLE
                || shape.type === notepanel.notes.ShapeType.PHOTO) {

            var x1 = this.location.x + (this.location.width * shape.x / 100);
            var w = (this.location.width * shape.width / 100);
            var x2 = x1 + w;
            var y1 = this.location.y + (this.location.height * shape.y / 100);
            var h = (this.location.height * shape.height / 100);
            var y2 = y1 + h;

            if (this.moving) {
                x1 -= movingElev;
                x2 -= movingElev;
                y1 -= movingElev;
                y2 -= movingElev;
            }

            if (shape.base) {
                var dist = baseElev;
                if (this.moving) {
                    dist += movingElev;
                }
                ctx.beginPath();
                ctx.moveTo(x1 + dist, y1 + dist);
                ctx.lineTo(x2 + dist, y1 + dist);
                ctx.lineTo(x2 + dist, y2 + dist);
                ctx.lineTo(x1 + dist, y2 + dist);
                ctx.closePath();
                ctx.fillStyle = notepanel.colors.toCssString({r: 0, g: 0, b: 0, a: 64});
                ctx.fill();
            }

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y1);
            ctx.lineTo(x2, y2);
            ctx.lineTo(x1, y2);
            ctx.closePath();
        }

        if ('stroke' in shape) {
            var col = null;
            switch (typeof shape.stroke) {
                case 'object':
                    if (typeof this.value[shape.stroke.name] === 'number') {
                        col = this.value[shape.stroke.name];
                    } else if (typeof shape.stroke.def === 'number') {
                        col = shape.stroke.def;
                    }
                    break;
                case 'number':
                    col = shape.stroke;
                    break;
            }
            if (col) {
                var c = notepanel.colors.fromRgbInt(col);
                if (this.hovered) {
                    notepanel.colors.darken(c, 64);
                }
                ctx.strokeStyle = notepanel.colors.toCssString(c);
                ctx.stroke();
            }
        }

        if ('fill' in shape) {
            var col = null;
            switch (typeof shape.fill) {
                case 'object':
                    if (typeof this.value[shape.fill.name] === 'number') {
                        col = this.value[shape.fill.name];
                    } else if (typeof shape.fill.def === 'number') {
                        col = shape.fill.def;
                    }
                    break;
                case 'number':
                    col = shape.fill;
                    break;
            }
            if (col) {
                var c = notepanel.colors.fromRgbInt(col);
                if (this.hovered) {
                    notepanel.colors.lighten(c, 16);
                }
                ctx.fillStyle = notepanel.colors.toCssString(c);
                ctx.fill();
            }
        }

        if (shape.type === notepanel.notes.ShapeType.PHOTO) {
            var url;
            switch (typeof shape.url) {
                case 'object':
                    if (typeof this.value[shape.url.name] === 'string') {
                        url = this.value[shape.url.name];
                    }
                    break;
                case 'string':
                    url = shape.url;
                    break;
            }
            if (url) {
                if (url in notepanel.notes.imageCache) {
                    if (notepanel.notes.imageCache[url].loaded) {
                        ctx.drawImage(notepanel.notes.imageCache[url].image, x1, y1, w, h);
                    }
                } else {
                    var img = new Image();
                    notepanel.notes.imageCache[url] = {
                        loaded: false,
                        image: img
                    }
                    img.onload = function () {
                        notepanel.notes.imageCache[url].loaded = true;
                    };
                    img.src = url;
                }
            }
        }

        if ('text' in shape) {
            var lh = this.scale(32);
            notepanel.template.canvasText.lineHeight = lh + 'px';
            notepanel.template.canvasText.fontSize = this.scale(36) + 'px';
            var options = {
                x: x1,
                y: y1 + lh,
                boxWidth: w
            };
            switch (typeof shape.text) {
                case 'object':
                    if (typeof this.value[shape.text.name] === 'string') {
                        options.text = this.value[shape.text.name];
                    }
                    break;
                case 'string':
                    options.text = shape.text;
                    break;
            }
            if (options.text) {
                notepanel.template.canvasText.drawText(options);
            }
        }
    }
    
    if (this.hovered) {
        // draw note menu on the hovered note
        ctx.font = '14 px "FontAwesome"';
        ctx.fillStyle = "#000000";
        ctx.textBaseline = 'bottom';
        ctx.textAlign = 'start';
        // TODO : manage template with menu starting either from left and right
        var startX = this.location.x + this.location.width;
        if (this.moving) {
            startX -= movingElev;
        }
        this.menu.x = startX - this.menu.width;
        //this.menu.items.reverse();
        // menu starting from left
        //startX = boardX + this.x
        //menu.x = startX
        // drawing menu from left
        this.menu.y = this.location.y - this.menu.height;
        if (this.moving) {
            this.menu.y -= movingElev;
        }
        for (var i = 0, imax = this.menu.items.length; i < imax; i++) {
            var item = this.menu.items[i];
            item.y = this.menu.y;
            item.x = this.menu.x + (i * item.width);
            ctx.fillText(item.text, item.x, item.y + this.menu.height);
        }
    }
};

notepanel.notes.Note.prototype.isMouseOver = function (pt) {
    return notepanel.utils.isInRectangle(pt, this.location) || notepanel.utils.isInRectangle(pt, this.menu);
};

notepanel.notes.Note.prototype.scale = function (len) {
    return len / notepanel.notes.adapter.scale.ratio;
};

notepanel.notes.Note.prototype.activateMenu = function (pt) {
    if (notepanel.utils.isInRectangle(pt, this.menu)) {
        for (var i = 0, imax = this.menu.items.length; i < imax; i++) {
            var item = this.menu.items[i];
            if (notepanel.utils.isInRectangle(pt, item)) {
                item.onClick.apply(this);
                return true;
            }
        }
    }
    return false;
};

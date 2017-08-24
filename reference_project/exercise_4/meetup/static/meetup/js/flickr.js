$(function () {
    'use strict';
    var button = $("#flickr-button"),
        input = $("#flickr-input"),
        view = $("#flickr-view"),
        activityImageInput = $("#id_image"),
        imageClass = "flickr-image",
        markedClass = "flickr-marked";

    function createImage(link) {
        var img = $("<img>");
        img.attr("src", link);
        img.attr("class", imageClass);
        img.attr("height", "150px");
        img.attr("width", "150px");
        img.click(function () {
            var isMarked = img.hasClass(markedClass);
            activityImageInput.val(link);
            $("." + markedClass).removeClass(markedClass);
            if (!isMarked) {
                img.addClass(markedClass);
            }
        });
        return img;
    }

    function fillView(data) {
        var i;
        view.empty();
        for (i = 0; i < data.length; i += 1) {
            view.append(createImage(data[i]));
        }
    }

    button.click(function () {
        var query = input.val();
        $.get("/api/flickr/" + query, fillView);
    });
});


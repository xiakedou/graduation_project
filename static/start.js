$.StartScreen = function(){
    var plugin = this;
    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;

    plugin.init = function(){
        setTilesAreaSize();
        if (width >= 768) addMouseWheel();
    };

    var setTilesAreaSize = function(){
        var groups = $(".tiles-group");
        var tileAreaWidth = 80;
        $.each(groups, function(i, t){
            if (width <= 768) {
                tileAreaWidth = width;
            } else {
                tileAreaWidth += $(t).outerWidth() + 80;
            }
        });
        $(".tiles-area").css({
            width: tileAreaWidth
        });
    };

    var addMouseWheel = function (){
        $("body").mousewheel(function(event, delta, deltaX, deltaY){
            var page = $(".start-screen");
            var scroll_value = delta * 50;
            page.scrollLeft(page.scrollLeft() - scroll_value);
            return false;
        });
    };

    plugin.init();
};

$.StartScreen();

$.each($('[class*=tile-]'), function(){
    var tile = $(this);
    setTimeout(function(){
        tile.css({
            opacity: 1,
            "transform": "scale(1)",
            "transition": ".3s"
        }).css("transform", false);

    }, Math.floor(Math.random()*500));
});

$(".tiles-group").animate({
    left: 0
});

$(window).on(Metro.events.resize + "-start-screen-resize", function(){
    $.StartScreen();
});

function aboutme_dialog(){
    Metro.dialog.create({
        title: "About Me",
        content: "<div>何轲的本科毕业设计项目</div>",
        actions: [
            {
                caption: "OK",
                cls: "js-dialog-close"
            }
        ]
    });
}

function help_dialog(){
    Metro.dialog.create({
        title: "Help",
        content: "<div>默认用户名：test,密码：test</div>",
        actions: [
            {
                caption: "OK",
                cls: "js-dialog-close"
            }
        ]
    });
}

function author_dialog(){
    Metro.dialog.create({
        title: "Author Information",
        content: "<div><p>学校：华中科技大学</p><p>院系：计算机科学与技术学院</p><p>班级：计卓1401</p><p>姓名：何轲</p></div>",
        actions: [
            {
                caption: "OK",
                cls: "js-dialog-close"
            }
        ]
    });
}

function contact_dialog(){
    Metro.dialog.create({
        title: "Contact",
        content: "<div><p>QQ：1316192254</p><p>Email：xiakedou123456@outlook.com</p></div>",
        actions: [
            {
                caption: "OK",
                cls: "js-dialog-close"
            }
        ]
    });
}
SLIDES.push({
    id: "math",
    onjump: function(self){
        // Splash in background
        self.add({ id:"splash", type:"Splash" });
    },

    onstart:function (self) {
        // Circular Wordbox
        self.add({
            id:"title", type:"TextBox",
            x:230, y:-60, width:500,
            size:50, lineHeight:0.9, align:"center",
            text_id:"title"
        });

        self.add({
            id:"math_text", type:"TextBox",
            x:150, y:90, width:700,
            size: 30, lineHeight:0.7, align:"center",
            text_id:"math_text",
        });

        self.add({
            id:"math_date", type:"TextBox",
            x:220, y: 130, width:500,
            size: 30, lineHeight:0.9, align:"center",
            text_id:"math_date",
        });

        self.add({
            id:"math_regformlink", type:"Button", size:"long",
            x:310, y:320,
            text_id:"math_regformlink",
            // url: "https://github.com",
        });
    },

    onend: function (self) {

    }
});

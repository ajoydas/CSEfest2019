SLIDES.push({
	id: "ideacontest",

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
			id:"idea_text", type:"TextBox",
			x:150, y:90, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"idea_text",
		});

		self.add({
			id:"idea_date", type:"TextBox",
			x:220, y: 100, width:500,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"idea_date",
		});

		self.add({
			id:"idea_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"idea_regformlink",
			// url: "https://github.com",
		});
	},

	onend: function (self) {

	}
});


SLIDES.push({
	id: "picpuzzle",

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
			id:"picpuzzle_text", type:"TextBox",
			x:150, y:230, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"picpuzzle_text",
		});

		self.add({
			id:"picpuzzle_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"picpuzzle_regformlink",
			url: "https://punzzle.csefest2019.com",
		});
	},

	onend: function (self) {

	}
});

SLIDES.push({
	id: "gamefest",

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
			id:"gamefest_text", type:"TextBox",
			x:150, y:90, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"gamefest_text",
		});

		self.add({
			id:"gamefest_date", type:"TextBox",
			x:220, y: 100, width:500,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"gamefest_date",
		});

		self.add({
			id:"gamefest_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"gamefest_regformlink",
			url: "https://www.startech.com.bd/form/event_register/",
		});

		self.add({
			id:"gamefest_regdeadline", type:"TextBox",
			x:130, y:370, width:700,
			size: 20, lineHeight:0.9, align:"center",
			text_id:"gamefest_regdeadline"
		});

		self.add({
			id:"gamefest_eventlink", type:"Button", size:"long",
			x:310, y:430,
			text_id:"gamefest_eventlink",
			url: "https://www.facebook.com/events/2011644332265641",
		});
	},

	onend: function (self) {

	}
});

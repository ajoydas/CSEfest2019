SLIDES.push({
	id: "hackathon",

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
			id:"hackathon_text", type:"TextBox",
			x:150, y:90, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"hackathon_text",
		});

		self.add({
			id:"hackthon_date", type:"TextBox",
			x:220, y: 100, width:500,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"hackthon_date",
		});

		self.add({
			id:"hackathon_details", type:"TextBox",
			x:130, y:210, width:700,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"hackathon_details"
		});

		self.add({
			id:"hackathon_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"hackathon_regformlink",
			url: "https://goo.gl/QrmE9w",
		});

		self.add({
			id:"hackathon_regdeadline", type:"TextBox",
			x:130, y:370, width:700,
			size: 20, lineHeight:0.9, align:"center",
			text_id:"hackathon_regdeadline"
		});

		self.add({
			id:"hackathon_eventlink", type:"Button", size:"long",
			x:310, y:430,
			text_id:"hackathon_eventlink",
			url: "https://www.facebook.com/events/577607186020008/",
		});
	},

	onend: function (self) {

	}
});

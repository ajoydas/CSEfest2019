SLIDES.push({
	id: "iupc",
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
			id:"iupc_text", type:"TextBox",
			x:150, y:90, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"iupc_text",
		});

		self.add({
			id:"iupc_date", type:"TextBox",
			x:220, y: 100, width:500,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"iupc_date",
		});

		self.add({
			id:"iupc_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"iupc_regformlink",
			url: "https://goo.gl/GyZQ1K",
		});

		self.add({
			id:"iupc_regdeadline", type:"TextBox",
			x:130, y:370, width:700,
			size: 20, lineHeight:0.9, align:"center",
			text_id:"iupc_regdeadline"
		});

		self.add({
			id:"iupc_eventlink", type:"Button", size:"long",
			x:310, y:430,
			text_id:"iupc_eventlink",
			url: "https://www.facebook.com/events/2272788946291379/",
		});
	},

	onend: function (self) {

	}
});



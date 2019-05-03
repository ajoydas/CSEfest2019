SLIDES.push({
	id: "job",

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
			id:"job_text", type:"TextBox",
			x:150, y:90, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"job_text",
		});

		self.add({
			id:"job_date", type:"TextBox",
			x:220, y: 100, width:500,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"job_date",
		});

		self.add({
			id:"job_details", type:"TextBox",
			x:130, y:210, width:700,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"job_details"
		});

		self.add({
			id:"job_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"job_regformlink",
			// url: "https://github.com",
		});

		self.add({
			id:"job_regdeadline", type:"TextBox",
			x:130, y:370, width:700,
			size: 20, lineHeight:0.9, align:"center",
			text_id:"job_regdeadline"
		});

		self.add({
			id:"job_eventlink", type:"Button", size:"long",
			x:310, y:430,
			text_id:"job_eventlink",
			// url: "https://github.com",
		});
	},

	onend: function (self) {

	}
});

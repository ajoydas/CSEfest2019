SLIDES.push({
	id: "poster",

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
			id:"poster_text", type:"TextBox",
			x:150, y:90, width:700,
			size: 30, lineHeight:0.7, align:"center",
			text_id:"poster_text",
		});

		self.add({
			id:"poster_date", type:"TextBox",
			x:220, y: 100, width:500,
			size: 30, lineHeight:0.9, align:"center",
			text_id:"poster_date",
		});

		self.add({
			id:"poster_regformlink", type:"Button", size:"long",
			x:310, y:320,
			text_id:"poster_regformlink",
			url: "https://docs.google.com/forms/d/e/1FAIpQLSfBew-WfKvY1bvWilJvZFFn843kv7EKHUB9dZGqtLNOx_kHHw/viewform?vc=0&c=0&w=1&pli=1&fbclid=IwAR1vMrZ1KqsFQ9uhQ48SqOTKHCPnyZO5pvJ0JKJUske01s2TcUO4pAUK0HE",
		});

		self.add({
			id:"poster_regdeadline", type:"TextBox",
			x:130, y:370, width:700,
			size: 20, lineHeight:0.9, align:"center",
			text_id:"poster_regdeadline"
		});

		self.add({
			id:"poster_eventlink", type:"Button", size:"long",
			x:310, y:430,
			text_id:"poster_eventlink",
			url: "https://www.facebook.com/events/349455679240434/",
		});
	},

	onend: function (self) {

	}
});

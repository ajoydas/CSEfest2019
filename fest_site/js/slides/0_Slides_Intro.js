Loader.addToManifest(Loader.manifest,{

	// CSS ASSETS
	cssAsset0: "assets/ui/button.png",
	cssAsset1: "assets/ui/button_short.png",
	cssAsset2: "assets/ui/button_long.png",
	cssAsset8: "assets/ui/scratch.png",
});


// =================================
// This is the first page.
// The progress is loaded here.
// =================================

SLIDES.push({

	//id: "preloader",
	onstart: function(self){

		let o = self.objects;

		// Splash in background
		self.add({ id:"splash", type:"Splash" });

		// // TITLE TEXT : CSE Fest 2019
		// self.add({
		// 	id:"title", type:"TextBox",
		// 	x:130, y:80, width:700,
		// 	size:100, lineHeight:0.9, align:"center",
		// 	text_id:"title"
		// });

		self.add({
			id:"img_logo_back", type:"RotatingImageBox",
			src: "assets/logo/outer_circle.png",
			x:340, y:110, width:300, height:300
		});
		self.add({
			id:"img_logo_back2", type:"RotatingImageBox",
			src: "assets/logo/outer_circle_2.png",
			x:340, y:50, width:300, height:300
		});

		self.add({
			id:"img_logo", type:"ImageBox",
			src: "assets/logo/logoG.png",
			x:340, y:80, width:300, height:300
		});

		// Button
		self.add({
			id:"loading_button", type:"Button", x:382, y:410,
			text_id:"loading",
			active:false
		});
		let _loadingWords = function(ratio){
			ratio = Math.round(ratio*100);
			o.loading_button.setText2(Words.get("loading")+" "+ratio+"%");
		};

		// PRELOADER
		listen(self,"preloader/progress", function(ratio){
			_loadingWords(ratio);
		});
		listen(self,"preloader/done", function(){
			o.loading_button.setText("loading_done");
			o.loading_button.activate();
			o.loading_button.config.onclick = function(){
				publish("start/game");
			};
		});

	},
	onend: function(self){
		unlisten(self);
		self.remove("loading_button");
		self.remove("img_logo");
		self.remove("img_logo_back2");
		self.remove("img_logo_back");
	}

});


// =================================
// After clicking the "Enter Fest"
// button, this page gets loaded.
// =================================

SLIDES.push({
	id: "intro",
	onjump: function(self){
		// Splash in background
		self.add({ id:"splash", type:"Splash" });
	},
	onstart: function(self){

		let o = self.objects;

		// Circular Word box
		// self.add({
		// 	id:"intro_text", type:"TextBox",
		// 	x:130, y:10, width:700, height:500, align:"center",
		// 	text_id:"intro"
		// });

		// Button
		self.add({
			id:"iupc_button", type:"Button", x:270, y:15, size:"long",
			text_id:"iupc_button",
			message:"slideshow/goto",
			_id: "iupc",
		});

		self.add({
			id:"matholympiad_button", type:"Button", x:360, y:70, size:"long",
			text_id:"matholympiad_button",
			message:"slideshow/goto",
			_id: "math",
		});

		self.add({
			id:"hackathon_button", type:"Button", x:210, y:130, size:"long",
			text_id:"hackathon_button",
			message:"slideshow/goto",
			_id: "hackathon",
		});

		self.add({
			id:"robotics_button", type:"Button", x:360, y:190, size:"long",
			text_id:"robotics_button",
			message:"slideshow/goto",
			_id: "robotics",
		});

		self.add({
			id:"ai_button", type:"Button", x:210, y:250, size:"long",
			text_id:"ai_button",
			message:"slideshow/goto",
			_id: "aicontest",
		});

		// ------------------------ //
		self.add({
			id:"idea_button", type:"Button", x:360, y:310, size:"long",
			text_id:"idea_button",
			message:"slideshow/goto",
			_id: "ideacontest",
		});

		self.add({
			id:"poster_button", type:"Button", x:210, y:370, size:"long",
			text_id:"poster_button",
			message:"slideshow/goto",
			_id: "poster",
		});

		self.add({
			id:"pcipuzzle_button", type:"Button", x:360, y:430, size:"long",
			text_id:"pcipuzzle_button",
			message:"slideshow/goto",
			_id: "picpuzzle",
		});

		self.add({
			id:"gamefest_button", type:"Button", x:210, y:490, size:"long",
			text_id:"gamefest_button",
			message:"slideshow/goto",
			_id: "gamefest",
		});

		// _hide(o.intro_text); _fadeIn(o.intro_text, 200);
		_hide(o.iupc_button); _fadeIn(o.iupc_button, 200);
		_hide(o.matholympiad_button); _fadeIn(o.matholympiad_button, 400);
		_hide(o.hackathon_button); _fadeIn(o.hackathon_button, 600);
		_hide(o.robotics_button); _fadeIn(o.robotics_button, 800);
		_hide(o.ai_button); _fadeIn(o.ai_button, 1000);
		_hide(o.idea_button); _fadeIn(o.idea_button, 1200);
		_hide(o.poster_button); _fadeIn(o.poster_button, 1400);
		_hide(o.pcipuzzle_button); _fadeIn(o.pcipuzzle_button, 1600);
		_hide(o.gamefest_button); _fadeIn(o.gamefest_button, 1800);

	},
	onend: function(self){
		self.clear();
	}

});
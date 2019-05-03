Loader.addToManifest(Loader.manifestPreload,{
	splash_peep: "assets/splash/splash_peep.json",
	brain: "assets/splash/brain.json",
	python: "assets/splash/python.json",
	ubuntu: "assets/splash/software.json",
	java: "assets/splash/java.json",
	bin: "assets/splash/binary.json",
	music: "assets/splash/music.json",
	dance: "assets/splash/dance.json",
	restaurant: "assets/splash/restaurant.json",
	celeb: "assets/splash/celeb.json",
	stack: "assets/splash/stack.json",
	chip: "assets/splash/chip.json",
	game_pad: "assets/splash/console.json",
	// wifi: "assets/splash/wifi.json",
	kora: "assets/splash/kora.json",
	quora: "assets/splash/quora.json",
	facebook: "assets/splash/facebook.json",
	youtube: "assets/splash/youtube.json",
	linkedin: "assets/splash/linkedin.json",
	github: "assets/splash/github.json",
	reddit: "assets/splash/reddit.json",
	drive: "assets/splash/google-drive.json",
	web: "assets/splash/web.json",
	idea: "assets/splash/idea.json",
	robot: "assets/splash/robot.json",
	connection: "assets/splash/connection.json",
});

function Splash(config){

	let self = this;
	self.id = config.id;

	// Dimensions, yo
	let width = $("#main").clientWidth;
	let height = $("#main").clientHeight;
	let x = -(width-960)/2;
	let y = -(height-540)/2;
	// DOM
	self.dom = document.createElement("div");
	self.dom.className = "object";
	self.dom.style.left = x+"px";
	self.dom.style.top = y+"px";
	
	// APP
	let app = new PIXI.Application(width, height, {transparent:true, resolution:2});
	app.view.style.width = width;
	app.view.style.height = height;
	self.dom.appendChild(app.view);

	// CONTAINERS
	let edgesContainer = new PIXI.Container();
	let peepsContainer = new PIXI.Container();
	app.stage.addChild(edgesContainer);
	app.stage.addChild(peepsContainer);

	// PEEPS
	let peeps = [];
	self.addPeep = function(x, y, idx){
		let icon = ["brain", "python", "ubuntu", "java", "stack", "quora", "kora","facebook",
					"youtube", "linkedin", "github", "reddit", "drive", "web", "idea", "robot",
					"chip", "game_pad", "bin", "music", "dance", "celeb", "restaurant"];
		console.log("idx after call " + idx);

		let peep = new SplashPeep({ x:x, y:y, app:app, blush:config.blush, sprite: icon[idx%22]});


		peeps.push(peep);
		peepsContainer.addChild(peep.graphics);
	};

	// EDGES
	let edges = [];
	self.addEdge = function(from, to){
		let edge = new SplashEdge({ from:from, to:to });
		edges.push(edge);
		edgesContainer.addChild(edge.graphics);
	};

	// Create RINGS
	let _createRing = function(xRadius, count){
		yRadius = xRadius*(350/400);
		let idx = 0;
		let increment = (Math.TAU/count)+0.0001;
		for(let angle=0; angle<Math.TAU; angle+=increment){
			let a = angle-(Math.TAU/4);
			let x = width/2 + Math.cos(a)*xRadius;
			let y = height/2 + Math.sin(a)*yRadius;
			self.addPeep(x,y, idx);
			console.log("idx before call "+idx);
			idx++;
		}
	};
	_createRing(400, 20);
	_createRing(520, 35);
	_createRing(640, 45);
	_createRing(760, 65);

	// Connect all within a radius
	let _connectAllWithinRadius = function(radius){
		
		let r2 = radius*radius;

		for(let i=0;i<peeps.length;i++){
			let peep1 = peeps[i];

			for(let j=i+1;j<peeps.length;j++){
				let peep2 = peeps[j];

				// Are they close enough?
				let dx = peep2.x-peep1.x;
				let dy = peep2.y-peep1.y;
				if(dx*dx+dy*dy < r2){
					self.addEdge(peep1, peep2);
				}

			}
		}
	};
	_connectAllWithinRadius(250);

	// Animiniminimination
	let update = function(delta){
		Tween.tick();
		for(let i=0;i<peeps.length;i++) peeps[i].update(delta);
		for(let i=0;i<edges.length;i++) edges[i].update(delta);
	};
	app.ticker.add(update);
	update(0);

	///////////////////////////////////////////////
	///////////// ADD, REMOVE, KILL ///////////////
	///////////////////////////////////////////////

	// Add...
	self.add = function(){
		_add(self);
	};

	// Remove...
	self.remove = function(){
		app.destroy();
		_remove(self);
	};

}

function SplashPeep(config){

	let self = this;
	self.config = config;

	// Graphics!
	console.log("clip "+config.sprite);
	let g = _makeMovieClip(config.sprite, {scale:0.3});
	self.graphics = g;
	if(config.blush) g.gotoAndStop(1);
	if(Math.random()<0.5) g.scale.x*=-1; // Flip?

	// Them letiables...
	self.app = config.app;
	self.x = config.x;
	self.y = config.y;
	let initX = config.x;
	let initY = config.y;
	let initRotation = (Math.random()-0.5)*(Math.PI-0.4);
	let radius = 5+Math.random()*20;
	let swing = 0.05+Math.random()*0.45;
	let angle = Math.random()*Math.TAU;
	let speed = (0.05+Math.random()*0.95)/60;

	self.update = function(delta){
		
		// Them letiables...
		angle += speed*delta;
		let x = initX + Math.cos(angle)*radius;
		let y = initY + Math.sin(angle)*radius;
		let r = initRotation + Math.cos(angle)*swing;

		// NEAR MOUSE?
		let Mouse = self.app.renderer.plugins.interaction.mouse.global;
		let dx = Mouse.x-x;
		let dy = Mouse.y-y;
		let rad = 200;
		let bulgeX = 0;
		let bulgeY = 0;
		let dist2 = dx*dx+dy*dy;
		if(dist2 < rad*rad){
			let bulge = Math.sin(((rad-Math.sqrt(dist2))/rad)*Math.TAU/4)*50;
			let bulgeAngle = Math.atan2(-dy,-dx);
			bulgeX = Math.cos(bulgeAngle)*bulge;
			bulgeY = Math.sin(bulgeAngle)*bulge;
		}

		// Graphics!
		g.x = x + bulgeX;
		g.y = y + bulgeY;
		g.rotation = r;


	};

}

function SplashEdge(config){

	let self = this;
	self.config = config;

	// Graphics!
	let g = _makeMovieClip("connection");
	g.anchor.x = 0;
	g.anchor.y = 0.5;
	g.height = 1;
	self.graphics = g;

	// Them letiables...
	self.from = config.from;
	self.to = config.to;

	self.update = function(delta){
		
		// Just update graphics!
		let f = self.from.graphics;
		let t = self.to.graphics;
		let dx = t.x-f.x;
		let dy = t.y-f.y;
		let a = Math.atan2(dy,dx);
		let dist = Math.sqrt(dx*dx+dy*dy);

		g.x = f.x; 
		g.y = f.y;
		g.rotation = a;

		g.width = dist;

	};

}
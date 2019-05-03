function SlideSelect(config){
	var self = this;
	self.config = config;

	// DOM
	self.dom = config.dom;

	// Slides
	self.slides = config.slides;

	// Create a dot, and onclick
	self.addDot = function(slide){
		var dot = new SlideSelectDot(slide);
		self.dom.appendChild(dot.dom);
	};

	// Populate dots
	for(var i=0; i<self.slides.length; i++){
		var slide = self.slides[i];
		console.log("slide id "+slide.id);
		if(slide.id){
			self.addDot(slide);
		}
	}

}

// function for buttons in footer
// those small circles in the
// footer are dot
function SlideSelectDot(slide){

	var self = this;
	self.slide = slide;

	// DOM
	self.dom = document.createElement("div");

	var dotOb=document.createElement("img");

	self.dom.className = "dot";
	self.dom.classList.add("animated");

	//x:0, y:0, width:30, height:30
	console.log(slide.id);
	self.dom.setAttribute("data-balloon", Words.get("chapter_"+slide.id));

	dotOb.setAttribute("src", Words.get("icon_"+slide.id));
	dotOb.setAttribute("data-balloon-pos", "up");
	dotOb.setAttribute("width", "30");
	dotOb.setAttribute("height", "30");




	//self.dom.setAttribute("value","test");
	self.dom.appendChild(dotOb);

	//$('.data-balloon').after('some text')




	// On Click
	self.dom.onclick = function(){
		publish("slideshow/scratch", [slide.id]);
	};

	// Listen to when the slide changes
	subscribe("slideshow/slideChange", function(id){
		if(!id) return; // nah
		if(id==slide.id){
			self.dom.setAttribute("selected","yes");
		}else{
			self.dom.removeAttribute("selected");
		}
	});

}
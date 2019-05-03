/**********************

Convert a word.html to a JSON containing innerHTMLs

**********************/

window.Words = {};
Words.text = null;

Words.get = function(id){
	return Words.text[id];
};

Words.convert = function(filepath){

	// Promise
	let deferred = Q.defer();

	// Get dat stuff
	let request = pegasus(filepath);
	request.then(
		
		// success handler
		function(data, xhr) {

			// Convert HTML...
			let words = document.createElement("div");
			words.innerHTML = xhr.response;
			let paragraphs = words.querySelectorAll("p");

			// ...to a JSON
			Words.text = {}; // new one!
			for(let i=0;i<paragraphs.length;i++){
				let p = paragraphs[i];
				let id = p.id;
				let html = p.innerHTML;
				Words.text[id] = html;
			}

			// Fulfil promise!
			deferred.resolve(Words.text);

		},

		// error handler (optional)
		function(data, xhr) {
			alert("AHHHHHHHHHHHH, PROBLEM LOADING WORDS");
			console.error(data, xhr.status)
		}

	);

	// Return Promise
	return deferred.promise;

};
$(document).ready( function() {

	let greeting = "Hello,";
	let hr = new Date().getHours();

	if(hr >= 6 && hr < 12) {
		/*Morning 6a->12p*/
		greeting = "Good Morning,";
	} else if (hr == 12) {
		/*12pm*/
		let mins = new Date().getMinutes();
		if (mins == 0) {
			/*Noon Case Check*/
			/*Don't change anything*/
			greeting = "Hello,";
		}
		greeting = "Good Afternoon,";
	} else if (hr > 12 && hr < 18) {
		/*Afternoon 1p->6p*/
		greeting = "Good Afternoon,";
	} else if (hr >= 18 && hr < 21) {
		/*Evening 6p->9p*/
		greeting = "Good Evening,";
	} else if (hr >= 21 || hr < 6) {
		/*Night 9p->6a*/
		greeting = "Welcome,";
	} else {
		/*Unknown*/
		/*Leave Default*/
	}
	document.getElementById('greeting').innerHTML = greeting;
});
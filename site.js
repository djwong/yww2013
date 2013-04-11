function crib_toggle(id)
{
	var x = document.getElementById(id);
	var y = document.getElementById(id + "_ctl");
	if (x.style.display == "") {
		/* work around a bug in ie6/7. */
		try {
			x.style.display = "table-row";
		} catch(e) {
			x.style.display = "block";
		}
		y.innerHTML = "&#9660;";
	} else {
		x.style.display = "";
		y.innerHTML = "&#9654;";
	}
}

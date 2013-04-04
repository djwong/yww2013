function crib_toggle(id)
{
	var x = document.getElementById(id);
	var y = document.getElementById(id + "_ctl");
	if (x.style.display == "") {
		x.style.display = "table-row";
		y.innerHTML = "&#9660;";
	} else {
		x.style.display = "";
		y.innerHTML = "&#9654;";
	}
}

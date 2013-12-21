function crib_toggle(id)
{
	var x = $('#' + id);
	var y = $('#' + id + "_ctl");
	if (x.css('display') == 'none') {
		x.css('display', 'table-row');
		y.text('▼');
	} else {
		x.css('display', '');
		y.text('▶');
	}
}

function crib_ready()
{
	var x = location.hash;
	x = x.replace(/^#dance_/, "crib_");
	if ($('#' + x).length)
		crib_toggle(x);
}

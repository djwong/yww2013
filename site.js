function crib_toggle(id, show)
{
	var x = $('#' + id);
	if (typeof(show) === 'undefined')
		show = (x.css('display') == 'none');
	var y = $('#' + id + "_ctl");
	if (show) {
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

function crib_toggle_all(show)
{
	$('tr[id ^= "crib_"]').each(function(a,b) {crib_toggle(b.id, show);});
}

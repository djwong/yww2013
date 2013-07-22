function crib_toggle(id)
{
	var x = $('#' + id);
	var y = $('#' + id + "_ctl");
	if (x.css('display') == 'none') {
		x.css('display', 'table-row');
		y.text('▼');
	} else {
		x.css('display', 'none');
		y.text('▶');
	}
}

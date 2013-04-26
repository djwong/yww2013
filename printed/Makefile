OUTPUT=yww_booklet.pdf yww_booklet_cover.pdf packet.pdf

all: $(OUTPUT)
	@echo Outputs $(OUTPUT) have been generated. ENJOY.

clean:;
	rm -rf $(OUTPUT) tmp yww_booklet.ps yww_crib.ps yww_booklet_cover.ps yww_crib_cover.ps

distclean: clean
	rm -rf yww_crib.pdf yww_crib_cover.pdf

yww_booklet.pdf: yww_booklet.ps
	ps2pdf $^

yww_booklet.ps: yww_crib.ps
	./ps2booklet $^ $@

yww_crib.ps: yww_crib.pdf
	pdf2ps $^

yww_booklet_cover.pdf: yww_booklet_cover.ps
	ps2pdf $^

yww_booklet_cover.ps: yww_crib_cover.ps
	./ps2booklet $^ $@

yww_crib_cover.ps: yww_crib_cover.pdf
	pdf2ps $^

packet.pdf: schedule.ps afterparty.ps feedback.ps
	psjoin $^ | ps2pdf - - > $@

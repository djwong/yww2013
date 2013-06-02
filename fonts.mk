FONTFORGE=fontforge
OTF_FONTS=\
LinBiolinum_RB.otf \
LinBiolinum_RI.otf \
LinBiolinum_R.otf \
LinLibertine_RBI.otf \
LinLibertine_RB.otf \
LinLibertine_RI.otf \
LinLibertine_R.otf
WOFF_FROM_OTF_FONTS=$(subst otf,woff,$(OTF_FONTS))

CLEAN += $(WOFF_FROM_OTF_FONTS) fonts.css

fonts.css: $(WOFF_FROM_OTF_FONTS)
	echo '/*' > $@
	echo ' * Font loading clauses auto-generated.' >> $@
	echo ' * Get the Linux Libertine/Linux Biolinum fonts at http://linuxlibertine.sourceforge.net/' >> $@
	echo ' */' >> $@
	for fon in $(WOFF_FROM_OTF_FONTS); do ./woff2css $$fon; done >> $@

%.woff: %.otf
	$(FONTFORGE) -script otf2woff.pe $<

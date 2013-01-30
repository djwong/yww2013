TARGETS=index.html schedule.html classes.html ball.html register.html staff.html contact.html history.html
DESTDIR=output/
INSTALL=install

all: $(TARGETS)

install: $(TARGETS) $(FILES)
	$(INSTALL) -d $(DESTDIR)
	$(INSTALL) -m 0644 $(TARGETS) $(DESTDIR)
	$(INSTALL) -m 0644 $(FILES) $(DESTDIR)

.PHONY: install upload

upload: install
	./send-to-server

%.html: %.html.in footer files generate_header
	./generate_header $@
	cat $< >> $@
	cat footer >> $@

clean:
	rm -rf $(TARGETS) $(DESTDIR)

FILES=\
LinBiolinum_Bd.otf \
LinBiolinum_Bd.ttf \
LinBiolinum_It.otf \
LinBiolinum_It.ttf \
LinBiolinum_Re.otf \
LinBiolinum_Re.ttf \
LinLibertine_Bd.otf \
LinLibertine_Bd.ttf \
LinLibertine_BI.otf \
LinLibertine_BI.ttf \
LinLibertine_It.otf \
LinLibertine_It.ttf \
LinLibertine_Re.otf \
LinLibertine_Re.ttf \
fonts.css \
style.css \
classes.jpg \
contact.jpg \
header.jpg \
history.jpg \
musicians.jpg \
schedule.jpg \
register.jpg \
lindamae.jpg \
lindy.jpg

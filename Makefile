TARGETS=index.html schedule.html classes.html ball.html register.html staff.html contact.html history.html analytics.html travel.html ceilidh.html afterparty.html feedback.html fonts.css
DESTDIR=output/
INSTALL=install

all: $(TARGETS)

install: $(TARGETS) $(FILES)
	$(INSTALL) -d $(DESTDIR)
	$(INSTALL) -p -m 0644 $(TARGETS) $(DESTDIR)
	$(INSTALL) -p -m 0644 $(FILES) $(DESTDIR)

.PHONY: install upload

upload: install
	./send-to-server

%.html: %.html.in footer files generate_header
	./generate_header $@
	cat $< >> $@
	cat footer >> $@

.PHONY: registration.csv

include fonts.mk

registration.csv:
	wget 'http://docs.google.com/spreadsheet/ccc?key=0AtDnBlSkyNjodGNXaEJWUzYxcVV3cG9FUmllS1RUaHc&output=csv&usp=sharing' -O $@

analytics.html.in: registration.csv analytics.py
	./analytics.py $< --html > $@

include ceilidh.html.in.d
ceilidh.html.in.d: ceilidh.html.in.in ceilidh.txt crib_deps.py
	./crib_deps.py $< $@ ceilidh.html.in

ceilidh.html.in: ceilidh.html.in.in ceilidh.txt crib.py
	./crib.py -i $< $@

include ball.html.in.d
ball.html.in.d: ball.html.in.in ball.txt crib_deps.py
	./crib_deps.py $< $@ ball.html.in

ball.html.in: ball.html.in.in ball.txt crib.py
	./crib.py -i $< $@

clean:
	rm -rf $(TARGETS) $(DESTDIR) registration.csv ceilidh.html.in.d ball.html.in.d $(CLEAN) ceilidh.html.in ball.html.in analytics.html.in

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
style.css \
classes.jpg \
contact.jpg \
header.jpg \
history.jpg \
musicians.jpg \
schedule.jpg \
register.jpg \
lindamae.jpg \
lindy.jpg \
lea_maiolo.jpg \
cribs.pdf \
travel.jpg \
you.jpg \
bike.kml \
art/yww-144.png art/yww-128.png art/yww-64.png art/yww-32.png art/yww-16.png art/yww.svg \
site.js \
ceilidh.jpg \
cynthia.jpg \
group_pic.jpg

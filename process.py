from bs4 import BeautifulSoup
soup = BeautifulSoup(open('bookmarks.html'))


class Bookmark():
    """docstring for Bookmark"""
    def __init__(self, title, content, url, tag):
        self.title = title
        self.url = url
        self.tag = tag
        self.content = content

    def printAsEnex(self):
        output = """
            <note>
                <title>%(title)s</title>
                <content>
                    <![CDATA[<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">

                    <en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">
                        %(content)s
                    </en-note>
                    ]]>
                </content>
                <created>20121104T154829Z</created>
                <updated>20121104T154845Z</updated>
                <tag>%(tag)s</tag>
                <note-attributes>
                    <source-url>%(url)s</source-url>
                </note-attributes>
            </note>
        """ % {'title': self.title, 'content': self.content, 'tag': self.tag, 'url': self.url}
        return output.encode('utf-8')

    def __str__(self):
        return unicode(self.title + " " + self.url + " " + self.tag).encode('utf-8')

html_tags = soup.findAll(['h3', 'a'])

en_tag = ''

bookmarks = []

for tag in html_tags:
    if tag.name == 'h3':
        en_tag = tag.string
    if tag.name == 'a':
        new_bm = Bookmark(tag.string, "", tag['href'], en_tag)
        bookmarks.append(new_bm)

out = open('output.enex', 'w')

out.write("""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export.dtd">
        <en-export export-date="20121104T154912Z" application="Evernote/Windows" version="4.x">
    """)
for n in bookmarks:
    out.write(n.printAsEnex())

out.write("</en-export>")
out.close()

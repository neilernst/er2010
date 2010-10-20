from appscript import *

__graffle = app('OmniGraffle Professional 5')
__doc = __graffle.documents[1] # the top document, note 1-indexed array
# __s = __doc.canvases['Edits for RE2010'].get()
__s = __doc.canvases['Canvas 1'].get()
__shapes = __s.graphics.get()

for element in __shapes:
    id = element.id.get()
    # print id
    try:
        text = element.text.get()
        # print text
    except:
        pass
    data = element.user_data.get()
    if data != None:
        # print data
        if 'rel_type' in data.keys():
            if data['rel_type'] == 'AND' if id == 27:
                print 'and rel'
                element.labels[0].make(new=k.text, with_properties={k.text:u'AND'})
            if data['rel_type'] == 'OR':
                print 'or rel'

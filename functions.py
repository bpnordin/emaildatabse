

from webbrowser import get


def findType(messagePart):
    """
    takes a messagePart object https://developers.google.com/gmail/api/reference/rest/v1/users.messages#messagepart
    returns a dict with the structure of the message part
    head : mimeType
    parts : [A,B...] where A,B are dicts with the same structure
    """
    mime = messagePart['mimeType']
    mime_dict = {'head': messagePart, 
        'children' : []}
    if 'parts' in messagePart.keys():
        #then we dig down deeper
        parts_list = messagePart['parts']
        for part in parts_list:
            mime = findType(part)
            mime_dict['children'].append(mime)
        return mime_dict
    else:
        #this is the end
        return mime_dict

def gethtml(tree):
    if tree['head']['mimeType'] == 'text/html':
        #we are done
        return tree['head']
    elif len(tree['children']) > 0:
        for part in tree['children']:
            mes = gethtml(part)
            if mes:
                return mes
    else:
        #we have reached a leaf that is not 'text/html'
        pass 


def getMessage(messagePart):
    tree = findType(messagePart)
    if tree['head'] == 'mulitpart/mixed':
        #should contain an attactment and then the message part
        pass
    elif tree['head'] == 'multipart/related':
        #should have the multipart/alternative(html)
        #and then the other parts will relate to the html
        pass
    elif tree['head'] == 'multipart/alternative':
        #should just get the html part of the message
        pass
    else:
        print (f"No rule for {tree['head']}")



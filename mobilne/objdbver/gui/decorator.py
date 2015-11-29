from listentry import ListEntry

def RawToGuiLists(listsDict):
    """ Converts lists dicrionary into ListEntry GUI obj
        listsDict - dictionary of id - name pairs
    returns: list of ListEntry objects
    """
    guiLists = []
    for l_pair in listsDict.viewitems():
        # guiLists.append(ListEntry(name = 'zadanie', list_id = '0'))
        guiLists.append(ListEntry(l_pair[0], l_pair[1]))
    return guiLists

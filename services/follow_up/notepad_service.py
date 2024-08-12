
from follow_up.models import Notepad
from django.core.exceptions import ObjectDoesNotExist
def createOrUpdateNotepad(auth_id, note):
    try:
        notepad = Notepad.objects.get(authID=auth_id)
        notepad.note = note
        notepad.save()
        return notepad, True
    except ObjectDoesNotExist:
        notepad = Notepad.objects.create(authID_id=auth_id, note=note)
        return notepad, False
    
def getNotepadByAuthid(auth_id):
    try:
        notepad = Notepad.objects.get(authID=auth_id)
        return notepad
    except ObjectDoesNotExist:
        return None
import sqlite3
from django.conf import settings
from io import StringIO
from django.dispatch import receiver
from django.db.backends.signals import connection_created

# load default (memory) db from file db on EVERY new connection to default db

strDbDump = None

@receiver(connection_created)
def onDbConnectionCreate( connection, **kwargs ):

    global strDbDump
    if ( strDbDump is None ):
        # Read a file DB into string
        connectionDbFile = sqlite3.connect( settings.DATABASES['dbfile']['NAME'] )
        stringIoDbDump = StringIO()
        for lineDbDump in connectionDbFile.iterdump():
            stringIoDbDump.write( '%s\n' % lineDbDump )
        connectionDbFile.close()
        stringIoDbDump.seek( 0 )
        strDbDump = stringIoDbDump.read()

    # Write string into memory DB
    with connection.cursor() as cursor:
        cursor.executescript( strDbDump )
        connection.commit()

    return
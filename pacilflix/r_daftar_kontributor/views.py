from django.shortcuts import render
from django.db import connection
from collections import defaultdict

def get_kontributor_tipe():
    contributors = defaultdict(lambda: {
        'nama': '',
        'jenis_kelamin': '',
        'kewarganegaraan': '',
        'kontribusi': []
    })

    with connection.cursor() as cursor:
        query_contributors = """
        SELECT id, nama, jenis_kelamin, kewarganegaraan
        FROM CONTRIBUTORS
        """
        cursor.execute(query_contributors)
        contributor_rows = cursor.fetchall()

        for row in contributor_rows:
            id, nama, jenis_kelamin, kewarganegaraan = row
            contributors[id]['nama'] = nama
            contributors[id]['jenis_kelamin'] = jenis_kelamin
            contributors[id]['kewarganegaraan'] = kewarganegaraan

        query_sutradara = """
        SELECT id
        FROM SUTRADARA
        """
        cursor.execute(query_sutradara)
        sutradara_rows = cursor.fetchall()

        for row in sutradara_rows:
            id, = row
            if id in contributors:
                contributors[id]['kontribusi'].append('Sutradara')

        query_penulis_skenario = """
        SELECT id
        FROM PENULIS_SKENARIO
        """
        cursor.execute(query_penulis_skenario)
        penulis_skenario_rows = cursor.fetchall()

        for row in penulis_skenario_rows:
            id, = row
            if id in contributors:
                contributors[id]['kontribusi'].append('Penulis Skenario')

        query_pemain = """
        SELECT id
        FROM PEMAIN
        """
        cursor.execute(query_pemain)
        pemain_rows = cursor.fetchall()

        for row in pemain_rows:
            id, = row
            if id in contributors:
                contributors[id]['kontribusi'].append('Pemain')

    contributors = dict(contributors)
    return contributors

def kontributor(request):
    contributors = get_kontributor_tipe()
    return render(request, 'kontributor.html', {'contributors': contributors})

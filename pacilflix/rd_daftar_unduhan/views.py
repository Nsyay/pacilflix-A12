from django.shortcuts import redirect, render
from django.db import connection
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def daftar_unduhan(request):
    username = request.COOKIES.get('username')
    records_daftar_unduhan = []

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM TAYANGAN_TERUNDUH WHERE username = %s', [username])
        records_daftar_unduhan = cursor.fetchall()
        for i in range(len(records_daftar_unduhan)):
            cursor.execute(
                f'SELECT judul FROM TAYANGAN WHERE id = \'{records_daftar_unduhan[i][0]}\'' )
            records_daftar_unduhan[i] = records_daftar_unduhan[i] + cursor.fetchone()

    context = {
        'status': 'success',
        'records_daftar_unduhan': records_daftar_unduhan,
    }
    response = render(request, 'daftar_unduhan.html', context)
    return response

def hapus_unduhan(request):
    id_tayangan = request.GET.get('id_tayangan')
    username = request.COOKIES.get('username')
    timestamp = request.GET.get('timestamp')

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f'DELETE FROM TAYANGAN_TERUNDUH WHERE id_tayangan = \'{id_tayangan}\' AND username = \'{username}\' \
                    AND timestamp = \'{timestamp}\'')
        connection.commit()
        return JsonResponse({'message': 'Deletion successful.'}, status=200)
    except Exception as e:
            return JsonResponse({'message': f'Deletion failed: {str(e)}'}, status=400)
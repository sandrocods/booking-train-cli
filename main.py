from src.RequestCollection import RequestCollection
from consolemenu import *
from InquirerPy import inquirer
from consolemenu.items import *
from prettytable import PrettyTable
import datetime
from dateutil.relativedelta import relativedelta
import time
import random
import string

data_bayar = []


def GetTrainStations():
    keyword = input("Enter Location ex : Purwokerto\nLocation : ")
    Screen.clear()
    rc = RequestCollection()
    result = rc.get_TrainStations(keywords=keyword)
    if result['status'] == 'success':
        print(" =======================================")
        print("      Train Stations in " + keyword + "   ")
        print(" =======================================")
        t = PrettyTable(['No', 'Code Station', 'Label Station'])
        tmp = 0
        for item in result['data']:
            t.add_row([tmp, item['code'], item['label']])
            tmp += 1
        Screen.println(t)
        Screen.flush()
    else:
        print("{}".format(result['message']))

    Screen().input('Press [Enter] to continue')


def CheckTrainSchedule(data_bayar):
    global station_array, originStation, destinationStation, t

    current_date = datetime.datetime.now()
    plus_one_month = current_date + relativedelta(months=+1)

    validation = True
    while validation:
        try:
            date = input("? Masukan Tanggal Berangkat (YYYY-MM-DD) : ").split('-')
            # Jika date[0] dan date[1] dan date[2] kosong
            if len(date[0]) == 0 or len(date[1]) == 0 or len(date[2]) == 0:
                Screen().println("Date must be filled")
                time.sleep(1)
                Screen().clear()
                validation = True

            # Validasi tanggal
            if int(date[0]) > int(current_date.strftime("%Y")) or int(date[0]) < int(
                    current_date.strftime("%Y")) or int(date[1]) > int(plus_one_month.strftime("%m")) or int(
                date[1]) < int(current_date.strftime("%m")):
                Screen().println("Error : Date not valid")
                time.sleep(1)
                Screen().clear()
            else:
                validation = False
        except Exception:
            pass

    # Origin Station
    valid_station = True
    while valid_station:

        originStation = input("? Masukan Lokasi Keberangkatan : ")
        print("\n")
        rc = RequestCollection()
        result = rc.get_TrainStations(keywords=originStation)
        if result['status'] == 'success':
            print(" =======================================")
            print("      Train Stations in " + originStation + "   ")
            print(" =======================================")
            t = PrettyTable(['No', 'Code Station', 'Label Station'])
            tmp = 0

            station_array = []

            for item in result['data']:
                t.add_row([tmp, item['code'], item['label']])
                station_array.append(item['code'] + "-" + item['label'])
                tmp += 1
            Screen.println(t)
            Screen.flush()
        else:
            print("{}".format(result['message']))

        print("\n")
        originStation = inquirer.select(
            message="Pilih Station Keberangkatan : ",
            choices=station_array,
        ).execute()

        confirm = inquirer.confirm(message="Yakin data sudah benar ?").execute()
        if confirm:
            del station_array
            valid_station = False

    # Origin Station
    valid_station = True
    while valid_station:

        destinationStation = input("? Masukan Lokasi Tujuan : ")
        print("\n")
        rc = RequestCollection()
        result = rc.get_TrainStations(keywords=destinationStation)
        if result['status'] == 'success':
            print(" =======================================")
            print("      Train Stations in " + destinationStation + "   ")
            print(" =======================================")
            t = PrettyTable(['No', 'Code Station', 'Label Station'])
            tmp = 0

            station_array = []

            for item in result['data']:
                t.add_row([tmp, item['code'], item['label']])
                station_array.append(item['code'] + "-" + item['label'])
                tmp += 1
            Screen.println(t)
            Screen.flush()
        else:
            print("{}".format(result['message']))

        print("\n")
        destinationStation = inquirer.select(
            message="Pilih Station Tujuan : ",
            choices=station_array,
        ).execute()

        confirm = inquirer.confirm(message="Yakin data sudah benar ?").execute()
        if confirm:
            del station_array
            valid_station = False

    numPerson = input("? Masukan Jumlah Orang : ")

    # clean data
    date = '{}{}{}'.format(date[0], date[1], date[2])
    originStation = originStation.split('-')[0]
    destinationStation = destinationStation.split('-')[0]

    # screen
    Screen.clear()
    rc = RequestCollection()

    print("Please wait...")

    # request API
    result = rc.get_ScheduleTrain(date, originStation, destinationStation, numPerson)
    if result['status'] == 'success':
        print(" =======================================")
        print("      Train Schedule in " + date + "   ")
        print(" =======================================")
        t = PrettyTable(['No', 'Train Name', 'Class', 'Price Train', 'Duration', 'Seat Available'])
        tmp = 0

        list_train = []
        for item in result['data']:

            # handling error seat
            if item['availableSeats'] == 0:
                continue

            t.add_row([tmp, item['trainName'], item['classDisplay'], item['fareDisplay'], item['durationDisplay'],
                       item['availableSeats']])
            list_train.append(item['trainName'] + "-" + item['classDisplay'] + "-" + item['fareDisplay'] + "-" + item[
                'durationDisplay'] + "-" + str(item['availableSeats']))
            tmp += 1
        Screen.println(t)
        Screen.flush()

        confirm = inquirer.confirm(message="Sort data ? ").execute()
        if confirm:
            stop_sort = True

            while stop_sort:

                sort_option = inquirer.select(
                    message="Sortir berdasarkan : ",
                    choices=['Class', 'Price Train', 'Duration', 'Seat Available'],
                ).execute()

                if sort_option == 'Class':
                    Screen.println(t.get_string(sortby="Class"))

                    confirm_stop_sort = inquirer.confirm(message="Selesai Sorting ").execute()
                    if confirm_stop_sort:
                        stop_sort = False


                elif sort_option == 'Price Train':
                    Screen.println(t.get_string(sortby="Price Train"))

                    confirm_stop_sort = inquirer.confirm(message="Selesai Sorting ").execute()
                    if confirm_stop_sort:
                        stop_sort = False

                elif sort_option == 'Duration':
                    Screen.println(t.get_string(sortby="Duration"))

                    confirm_stop_sort = inquirer.confirm(message="Selesai Sorting ").execute()
                    if confirm_stop_sort:
                        stop_sort = False

                elif sort_option == 'Seat Available':
                    Screen.println(t.get_string(sortby="Seat Available"))

                    confirm_stop_sort = inquirer.confirm(message="Selesai Sorting ").execute()
                    if confirm_stop_sort:
                        stop_sort = False

        else:
            pass

        pesan_sekarang = inquirer.confirm(message="Pesan Sekarang ? ").execute()
        if pesan_sekarang:
            pilihan_kereta = inquirer.select(
                message="Pilih Kereta : ",
                choices=list_train,
            ).execute()

            kode_unik_pesanan = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            nama_pemesan = input("? Masukan Nama Pemesan : ")

            list_random_seat = [random.choice(["A", "B"]) + str(random.randint(1, int(pilihan_kereta.split('-')[4])))
                                for _ in range(int(pilihan_kereta.split('-')[4]))]

            pilih_kursi = inquirer.select(
                message="Pilih nomor kursi yang tersedia : ",
                choices=list_random_seat,
            ).execute()

            print("\n" * 2)
            print(" =========== Information Pemesan ===========")
            date_now = datetime.datetime.now()
            print(" Kode Unik Pemesan : " + kode_unik_pesanan)
            print(" Tanggal Pemesanan : " + str(date_now.strftime("%Y-%m-%d %H:%M:%S")))
            print(" Nama Pemesan : " + nama_pemesan)
            print(" Kereta : " + pilihan_kereta.split('-')[0])
            print(" Class : " + pilihan_kereta.split('-')[1])
            print(" Harga Kereta : " + pilihan_kereta.split('-')[2])
            print(" Durasi : " + pilihan_kereta.split('-')[3])
            print(" Kursi Nomor : " + str(pilih_kursi))
            print(" ============================================")

            # simpan pesanan
            with open('pesanan_kereta.txt', 'a') as file:
                file.write("Tanggal Pemesanan : " + str(date_now.strftime("%Y-%m-%d %H:%M:%S")) + "\n")
                file.write("Kode Unik Pemesan : " + kode_unik_pesanan + "\n")
                file.write("Nama Pemesan : " + nama_pemesan + "\n")
                file.write("Kereta : " + pilihan_kereta.split('-')[0] + "\n")
                file.write("Class : " + pilihan_kereta.split('-')[1] + "\n")
                file.write("Harga Kereta : " + pilihan_kereta.split('-')[2] + "\n")
                file.write("Durasi : " + pilihan_kereta.split('-')[3] + "\n")
                file.write("Kursi Nomor : " + str(pilih_kursi) + "\n")
                file.write("==========================================\n")
                file.close()

            bayar_sekarang = inquirer.confirm(message="Bayar Sekarang ").execute()
            if bayar_sekarang:
                print(" Total Pembayaran : " + pilihan_kereta.split('Rp ')[1].split('-')[0])
                nominal = input("? Masukan Nominal Pembayaran : ")
                if nominal == pilihan_kereta.split('Rp ')[1].split('-')[0].replace('.', ''):
                    print(" Pembayaran Berhasil ")
                    data_bayar.append({
                        'tanggal_pemesanan': date_now.strftime("%Y-%m-%d %H:%M:%S"),
                        'kode_unik_pesanan': kode_unik_pesanan,
                        'nama_pemesan': nama_pemesan,
                        'kode_kereta': pilihan_kereta.split('-')[0],
                        'class': pilihan_kereta.split('-')[1],
                        'harga_kereta': pilihan_kereta.split('-')[2],
                        'durasi': pilihan_kereta.split('-')[3],
                        'kursi_nomor': str(pilih_kursi),
                        'total_bayar': pilihan_kereta.split('Rp ')[1].split('-')[0],
                        'nominal_bayar': nominal,
                        'status_bayar': 'Berhasil'
                    })
                elif nominal > pilihan_kereta.split('Rp ')[1].split('-')[0].replace('.', ''):
                    print(" Pembayaran Berhasil ")
                    data_bayar.append({
                        'tanggal_pemesanan': date_now.strftime("%Y-%m-%d %H:%M:%S"),
                        'kode_unik_pesanan': kode_unik_pesanan,
                        'nama_pemesan': nama_pemesan,
                        'kode_kereta': pilihan_kereta.split('-')[0],
                        'class': pilihan_kereta.split('-')[1],
                        'harga_kereta': pilihan_kereta.split('-')[2],
                        'durasi': pilihan_kereta.split('-')[3],
                        'kursi_nomor': str(pilih_kursi),
                        'total_bayar': pilihan_kereta.split('Rp ')[1].split('-')[0],
                        'nominal_bayar': nominal,
                        'status_bayar': 'Berhasil'
                    })

                else:
                    print(" Pembayaran Gagal ")
                    data_bayar.append({
                        'tanggal_pemesanan': date_now.strftime("%Y-%m-%d %H:%M:%S"),
                        'kode_unik_pesanan': kode_unik_pesanan,
                        'nama_pemesan': nama_pemesan,
                        'kode_kereta': pilihan_kereta.split('-')[0],
                        'class': pilihan_kereta.split('-')[1],
                        'harga_kereta': pilihan_kereta.split('-')[2],
                        'durasi': pilihan_kereta.split('-')[3],
                        'kursi_nomor': str(pilih_kursi),
                        'total_bayar': pilihan_kereta.split('Rp ')[1].split('-')[0],
                        'nominal_bayar': nominal,
                        'status_bayar': 'Gagal'
                    })


            else:
                data_bayar.append({
                    'tanggal_pemesanan': date_now.strftime("%Y-%m-%d %H:%M:%S"),
                    'kode_unik_pesanan': kode_unik_pesanan,
                    'nama_pemesan': nama_pemesan,
                    'kode_kereta': pilihan_kereta.split('-')[0],
                    'class': pilihan_kereta.split('-')[1],
                    'harga_kereta': pilihan_kereta.split('-')[2],
                    'durasi': pilihan_kereta.split('-')[3],
                    'kursi_nomor': str(pilih_kursi),
                    'total_bayar': pilihan_kereta.split('Rp ')[1].split('-')[0],
                    'nominal_bayar': '',
                    'status_bayar': 'Gagal'
                })

            Screen().input('Press [Enter] to continue')




    else:
        print("{}".format(result['message']))


def history_pemesanan(data_bayar):
    itterator = 1
    for item_bayar in data_bayar:
        print("==============Pesanan ke " + str(itterator) + "====================")
        print(" Tanggal Pemesanan : " + item_bayar['tanggal_pemesanan'])
        print(" Kode Unik Pemesan : " + item_bayar['kode_unik_pesanan'])
        print(" Nama Pemesan : " + item_bayar['nama_pemesan'])
        print(" Kereta : " + item_bayar['kode_kereta'])
        print(" Class : " + item_bayar['class'])
        print(" Harga Kereta : " + item_bayar['harga_kereta'])
        print(" Durasi : " + item_bayar['durasi'])
        print(" Kursi Nomor : " + item_bayar['kursi_nomor'])
        print(" Total Pembayaran : " + item_bayar['total_bayar'])
        print(" Nominal Pembayaran : " + item_bayar['nominal_bayar'])
        print(" Status Pembayaran : " + item_bayar['status_bayar'])
        print("===========================================\n")
        itterator += 1

    Screen().input('Press [Enter] to continue')


def bayar_pemesanan(data_bayar):
    for item_bayar in data_bayar:
        if item_bayar['status_bayar'] == 'Gagal':
            print("==============Pesanan " + item_bayar['kode_unik_pesanan'] + "====================")
            print(" Tanggal Pemesanan : " + item_bayar['tanggal_pemesanan'])
            print(" Kode Unik Pemesan : " + item_bayar['kode_unik_pesanan'])
            print(" Nama Pemesan : " + item_bayar['nama_pemesan'])
            print(" Kereta : " + item_bayar['kode_kereta'])
            print(" Class : " + item_bayar['class'])
            print(" Harga Kereta : " + item_bayar['harga_kereta'])
            print(" Durasi : " + item_bayar['durasi'])
            print(" Kursi Nomor : " + item_bayar['kursi_nomor'])
            print(" Total Pembayaran : " + item_bayar['total_bayar'])
            print(" Nominal Pembayaran : " + item_bayar['nominal_bayar'])
            print(" Status Pembayaran : " + item_bayar['status_bayar'])
            print("===========================================\n")

            confirm = inquirer.confirm(message="Bayar Sekarang").execute()
            if confirm:
                nominal = input("Masukkan Nominal Pembayaran : ")
                if nominal.isdigit():
                    if int(nominal) >= int(item_bayar['total_bayar'].replace('.', '')):
                        print(" Pembayaran Berhasil ")
                        item_bayar['nominal_bayar'] = nominal
                        item_bayar['status_bayar'] = 'Berhasil'
                    else:
                        print(" Pembayaran Gagal ")
                        item_bayar['nominal_bayar'] = nominal
                        item_bayar['status_bayar'] = 'Gagal'
                else:
                    print(" Nominal Pembayaran Salah ")
                    item_bayar['nominal_bayar'] = nominal
                    item_bayar['status_bayar'] = 'Gagal'

    Screen().input('Press [Enter] to continue')


menu_format = MenuFormatBuilder().set_prompt('>>')

menu = ConsoleMenu("Booking Train Ticket", "Code by: sandrocods", formatter=menu_format)
menu_item_1 = MenuItem("Cek Stasiun Kereta")
menu_item_2 = MenuItem("Cek Jadwal Kereta")
menu_item_3 = MenuItem("Cek History Pemesanan")
menu_item_4 = MenuItem("Bayar Pemesanan")

menu.append_item(FunctionItem("Cek Jadwal Kereta", CheckTrainSchedule, args=[data_bayar]))
menu.append_item(FunctionItem("Cek Stasiun Kereta", GetTrainStations, args=[data_bayar]))
menu.append_item(FunctionItem("Cek History Pemesanan", history_pemesanan, args=[data_bayar]))
menu.append_item(FunctionItem("Bayar Pemesanan", bayar_pemesanan, args=[data_bayar]))

if __name__ == '__main__':
    try:
        menu.show()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit()

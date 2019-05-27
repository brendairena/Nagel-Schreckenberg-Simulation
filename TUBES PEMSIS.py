import numpy.random as random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from copy import copy, deepcopy


# Inisialisasi parameter
M = 100 #panjang lintasan
p = 0.3 #probabilitas
v0 = 0 #kecepatan awal
N = 10 #jumlah kendaraan
t_max = 100 #waktu maksimum
v_max = 5 #kecepatan maksimum
batas = [0,M] #panjang jalan
bawah = [30,30] #batas bawah jalan
atas = [70,70] #batas atas jalan
interval_1 = [80,80] #lintasan pada interval 80
interval_2 = [90,90] #lintasan pada interval 90
l = [30,70] #lebar jalan

# Main program
v = v0
t0 = 0
waktu = []
perpindahan = []
kendaraan = np.array(sorted([[random.randint(1,M), 5] for i in range(1,N+1)]))
susunan_kendaraan = [i for i in range(N)] #semua mobil

print("")
print("      SUSUNAN KENDARAAN      ")
print("=============================")
print(susunan_kendaraan)

for t in range(t_max): #sampai waktu maksimum akan terus berjalan
    x_row = [] #array posisi
    for i in susunan_kendaraan: #posisi mobil
        car = kendaraan[i]
        next_car = kendaraan[i+1 if i+1 < N else 0] #posisi mobil maju jika posisi maju yang baru tersebut < N
        #mengupdate kecepatan masing-masing kendaraan secara sekuensial
        # v pertama 
        v = np.min([v+1, v_max]) #v akan diupdate menjadi nilai minimum dari v+1 dan v_max
        
        # v kedua 
        if (next_car[0] < car[0]):
            d = M - next_car[0] #jarak antar kendaraan yaitu panjang lintasan - next_car[0]
        else: 
            d = (next_car[0]-car[0]) #jaraknya yaitu hasil pengurangan mobil yang didepan dengan mobil yang diposisi itu
        v = np.min([v, d-1]) #mencari yang paling minimum antara kecepatan dengan jarak antar mobil dikurang 1

        # v ketiga
        prob = random.rand() #mengupdate dengan probabilitas
        if (prob < p):
            v = np.max([0, v-1])
        
        # update posisi
        x = copy(car[0])
        x = x + v #mobil maju dengan menambahkan posisi dengan kecepatan
        # mengecek kondisi batas
        if (x >= M): #jika posisinya sudah lebih dari/sama dengan panjang lintasan
            temp = [] #array untuk menampung mobilnya
            for i in range(N):
                susunan = susunan_kendaraan[i] + N-1
                if (susunan + N-1 > N):
                    susunan = susunan - N
                temp.append(susunan)
            susunan_kendaraan = deepcopy(temp)
            x = x - M
            
            waktu.append(t-t0)
            t0 = t
            
        x_row.append(copy([x,car[1]]))

    kendaraan = deepcopy(x_row)
    perpindahan.append(deepcopy(x_row))
    
kepadatan = N/M
print("")
print(" KEPADATAN LINTASAN [X80; X90] ")
print("===============================")
print(kepadatan)

#showing average time
print("       WAKTU RATA-RATA        ")
print("==============================")
print(sum(waktu)/len(waktu))


# animating
fig = plt.figure()
ax = plt.axes(ylim=(0,100), xlim=(0,M))
plt.plot(batas,atas,color='black')
plt.plot(interval_1,l,color='red')
plt.plot(interval_2,l,color='red')
plt.plot(batas,bawah,color='black')
car_marker = ax.scatter([], [], marker="_")

def animate(i):
    posisi_kendaraan = perpindahan[i]
    car_marker.set_offsets(posisi_kendaraan)
    return car_marker


anim = animation.FuncAnimation(fig, animate, frames=len(perpindahan), interval=50)
plt.show()
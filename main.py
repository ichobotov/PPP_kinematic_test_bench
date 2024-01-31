import math
import numpy as np

ACC = 0.300
path = 'C:/Users/apisarenko.IPS/PycharmProjects/Itelma/tests/ppp'
file = open(path + '/pvtPlayer.A.result.log', 'w')


with open(path + '/pvtPlayer.A.log', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '$NAV,13,' in line:
            string = line.split(',')
            if math.sqrt((float(string[9]) ** 2) + (float(string[10]) ** 2)) <= ACC:
            #if string[9] <= ACC_LAT and string[10] <= ACC_LON:
                file.write(line)
        else:
            continue

file.close()

def file_reader(file):
    for line in file:
        yield line


difference = []

with open('reftrajectory.result.log', 'w') as result:
    with open('pvtPlayer.A.result.log') as source1:
        source2 = open('NAVrtk_ref_from_DK.log')
        ref_file = file_reader(source2)
        for line1 in source1:
            while True:
                try:
                    ref = next(ref_file)
                    if line1.split(',')[3] == ref.split(',')[3]:

                        line1_lat = line1.split(',')[4]
                        line1_lat_deg = int(line1_lat[0:2]) + float(float(line1_lat[2:]) / 60)
                        line1_lon = line1.split(',')[6]
                        line1_lon_deg = int(line1_lon[0:3]) + float(float(line1_lon[3:]) / 60)

                        ref_lat = ref.split(',')[4]
                        ref_lat_deg = int(ref_lat[0:2]) + float(float(ref_lat[2:]) / 60)
                        ref_lon = ref.split(',')[6]
                        ref_lon_deg = int(ref_lon[0:3]) + float(float(ref_lon[3:]) / 60)

                        delta_lat = abs(ref_lat_deg - line1_lat_deg)
                        delta_lon = abs(ref_lon_deg - line1_lon_deg)
                        # print(f'{delta_lat} /// {delta_lon}')
                        delta_lat_m = delta_lat * 111134.8611
                        delta_lon_m = math.cos(math.radians(ref_lat_deg)) * 111321.3778 * delta_lon

                        # delta_lon_m = math.cos(ref_lat_deg) * 111321.3778 * delta_lon
                        print(f'{delta_lat_m} / {delta_lon_m} /'+line1.split(',')[3])
                        hor_delta_m = math.sqrt(delta_lat_m ** 2 + delta_lon_m ** 2)
                        difference.append(hor_delta_m)
                        break
                except StopIteration:
                    source2.close()
                    source2 = open('NAVrtk_ref_from_DK.log')
                    ref_file = file_reader(source2)
                    break

    array = np.array(difference)
    subtract_diff = array - array.mean()
    result.write(
        f"""Total trials = {len(difference)}
    Average = {round(np.mean(difference), 2)}
    Min = {min(difference)}
    Max = {max(difference)}
    P50 = {np.percentile(np.array(difference), 50)}
    P90 = {np.percentile(np.array(difference), 90)}
    Stdev = {round(np.std(np.array(difference)), 2)}
    Trials = {difference}
    ******************
    Subtract_diff = {subtract_diff}
    Stdev = {round(np.std(subtract_diff), 2)}"""
    )



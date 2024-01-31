PvtPlayer_2023_12V11.exe -atl f_001.log -cmd sc2 > nul 2>nul

4) Для упрощения статистических вычислений рекомендую всегда оперировать с 1Гц данными независимо от герцовки оригинальных данных 
(тем более что реф траектории обычно доступны 1Гц - NAVrtk_ref_from_DK.log)
5) Как всегда оперируем только с позициями NAV независимо от исследуемого режима (pvtPlayer.A.log)
6) Добавляем РРР и начинаем со следующего
- отбираем только позиции с  рапортуемой HRMS<30cm
- вычитаем реф траект (только для кин - NAVrtk_ref_from_DK.log)
- убираем среднее
- вычисляем HRMS и (в дальнейшем) строим CDF (только гор ошибка)
7) основные показатели РРР сейчас это % хороших Эпох и HRMS



************************************************************************************
$GPGGA,071640.00,5540.4311749,N,03730.3194152,E,1,27,,224.374,M,13.887,M,,*45
$GPGST,071640.00,4.947,,,,2.300,1.816,3.986*78
$NAV,1,27,071640.00,5540.4311749,N,03730.3194152,E,224.374,2.300,1.816,3.986,+0.016,-0.010,+0.004,0.032,0.032,0.032,,,Uni,14566,13209*01

HRMS is 2-sigma horizontal RMS, derived from the latitude and longitude sigmas in fields 6 & 7 of the GST message
VRMS is actually another term for the 1-sigma altitude error which is already present in the GST message field 8

GST message fields
Field	Meaning
0	Message ID $GPGST
1	UTC of position fix
2	RMS value of the pseudorange residuals; includes carrier phase residuals during periods of RTK (float) and RTK (fixed) processing
3	Error ellipse semi-major axis 1-sigma error, in meters
4	Error ellipse semi-minor axis 1-sigma error, in meters
5	Error ellipse orientation, degrees from true north
6	Latitude 1-sigma error, in meters
7	Longitude 1-sigma error, in meters
8	Height 1-sigma error, in meters
9	The checksum data, always begins with *

************************************************************************************
statLog.exe -NATEST -FB0 -FINAV -RC -KS0.1 pvtPlayer.A.log >>stat8d 2>nul

1. StatLog предназдачен для посчёта статистики именно RTK-тестов.
Все остальные позиции в расчёт не берутся.
Поэтому ничего не считается.
2. Требование ввести "координаты базы" - это некоторая формальность, связанная с тем, что все оценки позиции происходят в терминах "базовой линии".
3. Да, для большинства файлов "координаты базы" не нужны. Оцененная "средняя" позиция принимается за координаты базы, а базовая лининя считается нулевой.
4. Для того, чтобы в РРР режиме завставить утилиту считать "среднюю" позицию, требуется указать доволнительный флаг -FB0 перед флагом -FINAV
5. Поскольку точно РРР решения невелика, то есть большая вероятность того, что "средняя" позиция будет далека от середины "пятна". 
Это связано с тем, что усредняются не все поизции, а только те, что попадают в самую большую "кучку" с довольно маленьким радиусом (кажется, 1-2 см). Для РРР решений я бы рекомендовал это радиус величить командой -KS0.1 (увеличить радиус до 1 дм)
Разумеется, при обработке РРР данных естественным будет наличие большого количества решений вылетающих за пределы "Кучкек Козлова или Шинво". 
К тому же, с обработку попадёт не только сошедшееся решение, но и начальный интервал сходимости, который может длиться полчаса и дольше.

FILE  : TEST
FileType: I  prefix: NAV
Warning: Unable to retrive base-coord from log-file
ResetInformation: 0.0 (startTime: -1.0)


Baseline: 0.000 0.000 0.000  (0.000 meters)
BaseCoord: 2845741.865 2188060.052 5254606.607
PhaseOffset    : 0.0000
SvUsed         : 8 19.5 42 (min/mean/max)

Trials       :   6523
Fixed        :   6523   (100.00%)
WrongK       :   5621   ( 86.17%)
WrongX       :   5620   ( 86.16%)
WrongX2      :   5619   ( 86.14%)
WrongX4      :   5618   ( 86.13%)
WrongX8      :   5615   ( 86.08%)
WrongX16     :   5611   ( 86.02%)
AccHor [cm]  :      2.15 (h50:      1.91   h95:      3.40)
AccVert[cm]  :      3.47 (v50:      2.56   v95:      6.34)
Resets       :     -1


************************************************************************************
- вычисляем HRMS

My original calculation of the 3DRMS was wrong because the RMS should take the arithmetic mean of the squares.

My conclusion is that :

VRMS is actually another term for the 1-sigma altitude error which is already present in the GST message field 8
HRMS is 2-sigma horizontal RMS, derived from the latitude and longitude sigmas in fields 6 & 7 of the GST message.
In pseudo-code:

LatErr = GST[6]
LonErr = GST[7]
AltErr = GST[8]

VRMS = AltErr
HRMS = 2* Math.sqrt(((Math.pow(LatErr, 2) + Math.pow(LonErr, 2))/2));
3DRMS = 3* Math.sqrt(((Math.pow(LatErr, 2) + Math.pow(LonErr, 2))/2));
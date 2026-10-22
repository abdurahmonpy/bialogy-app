

const CLASSES_LIST = [
  { id: "5", name: "5-sinf", label: "Biologiya kirish", color: "from-green-500 to-emerald-600", textLight: "text-emerald-500 bg-emerald-50", themeColor: "emerald" },
  { id: "6", name: "6-sinf", label: "Botanika darsligi", color: "from-emerald-500 to-teal-600", textLight: "text-teal-500 bg-teal-50", themeColor: "teal" },
  { id: "7", name: "7-sinf", label: "Zoologiya darsligi", color: "from-lime-500 to-yellow-600", textLight: "text-lime-650 bg-lime-50", themeColor: "lime" },
  { id: "8", name: "8-sinf", label: "Odam va uning salomatligi", color: "from-rose-500 to-pink-600", textLight: "text-rose-500 bg-rose-50", themeColor: "rose" },
  { id: "9", name: "9-sinf", label: "Sitologiya va genetika", color: "from-blue-500 to-indigo-600", textLight: "text-blue-500 bg-blue-50", themeColor: "blue" },
  { id: "10-11", name: "10-11-sinf", label: "Umumiy biologiya va ekologiya", color: "from-purple-500 to-violet-600", textLight: "text-purple-500 bg-purple-50", themeColor: "purple" },
];

const SYLLABUS = [
  // ----------------------------------------------------
  // 5-SINF: BIOLOGIYA KIRISH
  // ----------------------------------------------------
  {
    id: "5-1",
    classId: "5",
    title: "Hujayra – Hayotning G'ishti",
    topic: "Umumiy Biologiya",
    shortDesc: "Tirik organizmlarning eng kichik strukturaviy birligi bo'lgan hujayra tuzilishini sodda tushunish.",
    difficulty: "Oson",
    diagramType: "cell",
    analogies: [
      "Hujayra qobig'i bu - xonadonimizning mustahkam devorlari va eshigi. U uyga begonalarni kiritmaydi va uyni asraydi.",
      "Sitozola bu - jele kabi suyuqlik. Unda o'yinchoqlar kabi hujayra organoidlari suzib yuradi.",
      "Yadro bu - maktab direktori yoki shaharning hokimiyati. U barcha ishlarni boshqaradi, DNT kodi esa hokimiyatdagi muhim qonunlardir."
    ],
    keyTerms: [
      { term: "Hujayra", meaning: "Barcha tirik organizmlarning eng kichik tuzilish va faoliyat birligi." },
      { term: "Sitozola (Sitoplazma)", meaning: "Hujayra ichidagi yarim suyuq shaffof modda bo'lib, unda organoidlar joylashadi." },
      { term: "Yadro", meaning: "Hujayraning markaziy qismi bo'lib, irsiy ma'lumotni (DNT) saqlaydi va barcha jarayonlarni boshqaradi." }
    ],
    content: `Salom, yosh biolog! Bugun hayotingizdagi eng muhim sirni ochamiz – biz va atrofimizdagi barcha tirik mavjudotlar nimadan tuzilganmiz?

Atrofingizdagi eng katta uyni ko'rganmisiz? U kichkina g'ishtlardan terilgan. Xuddi shunday, tabiatdagi eng ulkan daraxtlar yoki eng katta fillar ham mikroskopik mikrog'ishtchalardan tashkil topgan. Bu g'ishtchalar **HUJAYRALAR** deb ataladi!

### Hujayra o'zi nima qiladi?
Hujayra – tirik. U nafas oladi, oziqlanadi, o'sadi, xuddi biz kabi ko'payadi. Agar hujayra bo'lmasa, hayot ham bo'lmaydi.

### Hujayraning 3 ta asosiy qismi:
1. **Hujayra qobig'i (Membrana)**: U juda aqlli devor! U hujayraga nima kerak bo'lsa (suv, ozuqa, kislorod) ichkariga kiritadi, zararli narsalarni esa tashqarida qoldiradi.
2. **Sitoplazma**: Hujayraning ichidagi shirin jelega o'xshash suyuqlik. Unda hujayraning yashashiga yordam beradigan kichik 'organlar' (organoidlar) suzadi.
3. **Yadro**: Hujayraning miyasi! U hujayraning qachon bo'linishi, qachon ovqatlanishini o'ylab, buyrug' berib turadi.`
  },
  {
    id: "5-2",
    classId: "5",
    title: "Mikroskop Olamiga Sayohat",
    topic: "Umumiy Biologiya",
    shortDesc: "Mikroskop nima va u orqali mikrobiyologiya olamini qanday ko'rish mumkinligini o'rganish.",
    difficulty: "Oson",
    diagramType: "microscope",
    analogies: [
      "Mikroskop ob'ektivi bu - oddiy ko'zoynakning super-versiyasi bo'lib, narsalarning eng mayda detallarini ming barobar katta qilib ko'rsata oladi.",
      "Mikrob bu - biz ko'ra olmaydigan super-mitti hasharotcha kabidir, u har bir joyda yashaydi."
    ],
    keyTerms: [
      { term: "Mikroskop", meaning: "Ko'z bilan ko'rib bo'lmaydigan juda mitti ob'ektlarni bir necha yuz va ming marta kattalashtirib beruvchi optik asbob." },
      { term: "Bakteriya", meaning: "Bir hujayrali sodda mikroorganizm bo'lib, tabiatda eng keng tarqalgan hayot shakllaridan biridir." }
    ],
    content: `Biz ko'zimiz bilan dunyodagi juda ko'p narsalarni ko'ra olamiz: qushlarni, gullarni, uylarni. Ammo yer yuzida shunday sirli bir dunyo borki, uni ko'rish uchun mo'jizaviy asbob – **MIKROSKOP** kerak!

### Mikroskop qanday tuzilgan?
Unda maxsus kattalashtirib beruvchi **linzalar** (shishalar) bor. Ular mitti buyumni 40 marta, 100 marta, hatto 1000 martalab kattalashtiradi.

### Mikroskop ostida nimalar bor?
Agar tomchi suvni mikroskop ostiga qo'ysangiz, u yerda quvnoq sakrab yurgan, bir-biri bilan urishayotgan mitti jonzotlarni ko'rasiz! Bular:
- **Bakteriyalar**: Ba'zilari bizga qatiq yoki pishloq tayyorlashda yordam beradi (foydali bakteriyalar), ba'zilari esa kasal qiladi (shuning uchun qo'limizni sovunlab yuvishimiz shart!).
- **Mikroskopik suvo'tlar**: Okeanlarda yashab bizga nafas olish uchun kislorod tayyorlaydi.`
  },
  {
    id: "5-3",
    classId: "5",
    title: "Tiriklikning Asosiy Xossalari",
    topic: "Umumiy Biologiya",
    shortDesc: "Tirik organizmlarni jonsiz tabiat jinslaridan ajratib turuvchi asosiy hayotiy belgilar bilan tanishish.",
    difficulty: "Oson",
    diagramType: "cell",
    analogies: [
      "Nafas olish - bu hujayra pechkasiga ko'mir (oziq) solib, unga olov (kislorod) purkab, issiqlik (energiya) olish jarayonidir.",
      "Ko'payish - bu kelajak avlod qoldirish orqali tabiat zanjirining uzilib ketmasligini ta'minlovchi biologik nusxa ko'chirishdir."
    ],
    keyTerms: [
      { term: "Nafas olish", meaning: "Hujayralarda organik moddalarning parchalanishi natijasida hayot uchun zarur bo'lgan energiya hosil qilish jarayoni." },
      { term: "Moddalar almashinuvi", meaning: "Organizmga oziq moddalarning kirishi, o'zlashtirilishi hamda parchalanish mahsulotlarining tashqariga chiqishi." },
      { term: "Ta'sirchanlik", meaning: "Tirik organizm yoki hujayraning tashqi muhitdan kelayotgan ta'sirlarga (yorug'lik, issiq, xavf) javob qaytarish xususiyati." }
    ],
    content: `Jonsiz tosh bilan mitti mushukchaning qanday farqi bor? Tosh o'smaydi, ovqat yemaydi va ko'paymaydi. Mushukcha esa xuddi shu ishlarning barchasini bajaradi! 

Tirik mavjudotlarni o'lik narsalardan ajratib turadigan maxsus qoidalar **TIRIKLIKNING ASOSIY XOSSALARI** deb ataladi. Ulardan asosiylari bilan tanishamiz:

### 1. Kimyoviy tarkibning birligi va Tuzilishi
Barcha tirik darsliklar murakkab oqsillar, yog'lar va uglevodlardan tashkil topgan hamda ularning barchasi hujayraviy tuzilishga ega (viruslardan tashqari).

### 2. Moddalar va energiya almashinuvi (Metabolizm)
Tirik organizm tashqi muhitdan oziq-ovqat va kislorod oladi, ularni hazm qiladi va parchalab tashlaydi. Keraksiz chiqindilarni esa tanasidan tashqariga chiqarib yuboradi.

### 3. Nafas olish, Oziqlanish va Ajratish
Tiriklik - quvvat bilan tirik! Nafas olayotganimizda kislorod yordamida olingan ozuqalar parchalanib, hayotiy quvvat (energiya) hosil bo'ladi.

### 4. O'sish, Rivojlanish va Ko'payish
Tirik mavjudotlar hayoti davomida hajmi va og'irligi bo'yicha kattalashadi (o'sadi). Shuningdek, ular o'zidan keyin bola (avlod) qoldiradi (ko'payadi).`
  },
  {
    id: "5-4",
    classId: "5",
    title: "Tirik va O'lik Tabiat Bog'liqligi",
    topic: "Umumiy Biologiya",
    shortDesc: "Organik dunyo va anorganik dunyoning o'zaro bog'liqligi hamda biologik muhitlar.",
    difficulty: "Oson",
    diagramType: "root",
    analogies: [
      "Tuproq va suv - bu tirik daraxtning eng mustahkam poydevori. Ularsiz daraxt oziqlana olmaydi.",
      "Atmosfera - zaminni yopib turuvchi ulkan himoya ko'rpasi bo'lib, hayot uchun kislorod va karbonat gazlari bilan bo'lishadi."
    ],
    keyTerms: [
      { term: "Litosfera (Tuproq)", meaning: "Yerning qattiq qobig'i va tog' jinslari qatlami bo'lib, o'simliklar unib chiqadigan zamin." },
      { term: "Gidrosfera", meaning: "Yerdagi barcha suv manbalari (okeanlar, dengizlar, daryolar), qaysiki suvsiz hujayra qurib qoladi." },
      { term: "Atmosfera", meaning: "Yerni o'rab turgan va tiriklikni zararli kosmik nurlardan asrovchi gaz ko'rpasi." }
    ],
    content: `Dunyodagi barcha narsalar ikki katta guruhga bo'linadi: **Tirik tabiat** (o'simliklar, hayvonlar, zamburug'lar, bakteriyalar) va **O'lik tabiat** (tosh, suv, tuproq, havo, quyosh nuri).

Hech o'ylab ko'rganmisiz, tirik tabiat o'lik tabiatsiz yashay oladimi? Yo'q, aslo! Ular bir-biri bilan mahkam zanjirdek bog'langan.

### Tabiat bizga nima beradi?
1. **Quyosh**: Sayyoramizdagi yagona issiqlik va yorug'lik manbai. Quyoshsiz o'simliklar yashil bo'la olmaydi, hayot muzlab qoladi.
2. **Havo (Atmosfera)**: Biz nafas oladigan kislorod mana shu havoda joylashgan. O'simliklar esa havodagi karbonat angidriddan ovqat tayyorlashda foydalanadi.
3. **Suv (Gidrosfera)**: Hujayraning 70-80% qismi suvdan iborat. Suvsiz organizmlar qurib, tezda halok bo'ladi.
4. **Tuproq (Litosfera)**: O'simliklar o'z ildizlari bilan tuproqni mahkam ushlaydi va undan mineral ozuqalarni shimib oladi.

Tabiatdagi har bir narsa o'zaro ta'sir qiladi! Agar biz suvni bulg'asak yoki havoni zaharlasak, tirik organizmlarga bevosita ziyon yetkazgan bo'lamiz.`
  },
  {
    id: "5-5",
    classId: "5",
    title: "Organizm va Tana A'zolari",
    topic: "Umumiy Biologiya",
    shortDesc: "Tiriklikning hujayradan boshlab butun organizmgacha bo'lgan murakkab tuzilish zanjiri.",
    difficulty: "Oson",
    diagramType: "heart",
    analogies: [
      "Hujayra - bu mitti g'isht, To'qima - devor, Organ - bitta to'la xona, Organizm - butun boshli ulkan shohona imoratdir."
    ],
    keyTerms: [
      { term: "To'qima", meaning: "Tuzilishi, kelib chiqishi va bajaradigan vazifasiga ko'ra o'xshash bo'lgan hujayralar va hujayralararo moddalar yig'indisi." },
      { term: "Organ (A'zo)", meaning: "Muayyan shakl va tuzilishga ega bo'lib, organizmda ma'lum bir hayotiy ishni bajaradigan tana qismi." },
      { term: "A'zolar tizimi", meaning: "Birgalikda umumiy bir hayotiy vazifani (masalan nafas olish yoki qon aylanish) bajaradigan organlar birligi." }
    ],
    content: `Bizning tanamiz naqadar mukammal ishlaydigan ulkan zavodga o'xshaydi! Bu zavod qanday qurilgan? Kelajakda biologiyaning eng muhim bo'g'inlarini zanjir bo'yicha tushunamiz.

### Tuzilish pog'onalari:

1. **Hujayra**: Tanamizning eng mitti bo'lagi.
2. **To'qima**: Bir xil vazifani bajaradigan va bir-biriga juda o'xshash bo'lgan hujayralar to'пламиdir. Masalan, terimizni qoplovchi epiteliy to'qimasi yoki harakatlanishni ta'minlovchi mushak to'qimasi.
3. **Organ (A'zo)**: Bir nechta to'qimalar birlashib, ma'lum bir organni hosil qiladi. Masalan, yurak, o'pka, jigar yoki oshqozon. Har bir organning o'z ishi bor!
4. **A'zolar tizimi**: Ma'lum bir maqsad yo'lida birlashgan organlar jamoasidir. Masalan: og'iz, qizilo'ngach, oshqozon va ichaklar birlashib – **Ovqat hazm qilish tizimi**ni hosil qiladi.
5. **Butun Organizm**: Barcha a'zolar va ularning tizimlari birlashsa – bir butun tirik inson, hayvon yoki daraxt paydo bo'ladi.`
  },

  // ----------------------------------------------------
  // 6-SINF: BOTANIKA DARSLIGI
  // ----------------------------------------------------
  {
    id: "6-1",
    classId: "6",
    title: "Barg va Fotosintez Sirlari",
    topic: "Botanika",
    shortDesc: "O'simliklarning qanday qilib yorug'likdan quyosh energiyasini yutib, oziq-ovqat va kislorod ishlab chiqarishini o'rganish.",
    difficulty: "O'rtacha",
    diagramType: "leaf",
    analogies: [
      "Fotosintez - quyosh energiyasi yordamida oshxonada ovqat pishirish jarayonidir. Quyosh - bu gaz plitasi, barg - tovadan iborat.",
      "Xlorofill - bu o'simlikning yashil quyosh panellaridir. U yorug'likni tutib, kimyoviy quvvat ishlab chiqaradi."
    ],
    keyTerms: [
      { term: "Fotosintez", meaning: "Xloroplastlarda quyosh nuri energiyasi ishtirokida karbonat angidrid va suvdan organik moddalar va kislorod hosil bo'lish jarayoni." },
      { term: "Xloroplast", meaning: "O'simlik hujayrasining fotosintezni amalga oshiruvchi yashil rangli organoidi." },
      { term: "Xlorofill", meaning: "O'simlik barglariga yashil rang beruvchi va quyosh nuri energiyasini yutuvchi pigment." }
    ],
    content: `Hech o'ylab ko'rganmisiz: o'simliklar non yemaydi, osh yemaydi, qanday qilib ulkan daraxt bo'lib o'sadi? Javob: Ular o'z ovqatini o'zlari **pishirib olishadi**!

O'simlikning haqiqiy 'sehrli oshxonasi' bu uning **Yashil barglaridir**. Bu oshxonada ovqat pishirish jarayoni **FOTOSINTEZ** deb ataladi.

### Oshxonada taom tayyorlash uchun nimalar kerak?
1. **Masalliqlar**: Suv (ildiz orqali yer tagidan olinadi) va Karbonat angidrid (gaz - biz nafas chiqaradigan havodan olinadi).
2. **Gaz o'chog'i (Energiya)**: **Quyosh nurlari**!
3. **Oshpaz**: **Xlorofill** (Bargning ichidagi yashil rang beruvchi mitti quyosh panellari).

Quyosh bargga tushganda, xlorofill uni yutib, suv va gazni aralashtiradi. Natijada **GLYUKOZA** (o'simlik yeydigan shirinlik) va eng muhimi – biz nafas oladigan toza **KISLOROD** ajraladi! Shuning uchun o'simliklarni asrashimiz kerak.`
  },
  {
    id: "6-2",
    classId: "6",
    title: "Ildiz va uning sirli kuchlari",
    topic: "Botanika",
    shortDesc: "Ildiz tizimlari, ularning o'simlik hayotidagi suv emish va yerga mustahkamlash vazifalari.",
    difficulty: "O'rtacha",
    diagramType: "root",
    analogies: [
      "Ildiz tukchalari bu - millionlab mitti kokteyl ichadigan ichimlik naychalari (trubochka) bo'lik, tuproq orasidagi suv tomchilarini so'rib oladi.",
      "Popuk ildiz - bu ko'plab mitti iplar to'plamiga o'xshaydi, o'q ildiz esa bitta qat'iy baquvvat ustundir."
    ],
    keyTerms: [
      { term: "Ildiz", meaning: "O'simlikning yer ostidagi vegetativ organi bo'lib, uni tuproqqa mahkamlaydi, suv va mineral oziqlarni emadi." },
      { term: "O'q ildiz tizimi", meaning: "Asosiy ildiz yaqqol rivojlangan va uning atrofidan yon ildizlar chiqqan ildiz tizimi (masalan, beda, lola)." }
    ],
    content: `Agar kuchli shamol bo'lsa, daraxtlar nega yiqilib ketmaydi? Ularni yer ostida qaysidir maxsus bog'ich saqlab turgandek, to'g'rimi? Ana o'sha qudratli narsa – **ILDIZ**!

Ildiz nafaqat daraxtni yerda qat'iy saqlab turadi, balki u o'simlikning eng faol 'nasosi' (suv emuvchi tizimi) hisoblanadi.

### Ildiz qanday vazifalarni bajaradi?
1. **Suv va tuz so'rish**: Tuproqning chuqur qatlamlaridagi mineral tuzlar erigan suvni barglarga etkazib beradi.
2. **Tirik langar**: Daraxtni yiqitmasdan mustahkam ushlab turadi.
3. **Zaxira ombori**: Ba'zi o'simliklar (masalan, sabzi, sholg'om) o'z ovqatini aynan ildizida saqlaydi yo'g'onlashib ketadi (tugnak ildizlar).`
  },
  {
    id: "6-3",
    classId: "6",
    title: "Gulning Tuzilishi va Changlanish",
    topic: "Botanika",
    shortDesc: "Gulli o'simliklarning jinsiy ko'payish organi hisoblanuvchi gulning ichki qismlari va ajoyib changlanish turlari.",
    difficulty: "O'rtacha",
    diagramType: "flower",
    analogies: [
      "Changchi va Urug'chi - bu xuddi mitti davlatdagi shoh va malikadek gap. Changchi mitti oltin changlarni tayyorlasa, urug'chi ularni qabul qilib murtak asraydi.",
      "Hasharotlar orqali changlanish - gullarning mitti asalarilarga nektar sovg'a qilib, uning bo'yniga changlarini yuklab yuborishidir."
    ],
    keyTerms: [
      { term: "Urug'chi (Pistil)", meaning: "Gulning o'rtasidagi asosiy urg'ochilik a'zosi bo'lib, u tuguncha, ustuncha va tumshuqchadan iborat." },
      { term: "Changchi (Stamen)", meaning: "Gulning ko'payishidagi erkaklik organi bo'lib, u changdon va changchi ipidan tuzilgan." },
      { term: "Nektar (Shirin sharbat)", meaning: "Gullar hasharotlarni changlantirish uchun jalb etish maqsadida ajratadigan o'ta xushbo'y va shirin suyuqlik." }
    ],
    content: `Tabiatdagi eng jozibali narsa nima? Albatta, fanning go'zal gullari! Gullar shunchaki chiroyli emas, ular o'simliklarning oila qurishi va yangi urug' tayyorlashi uchun xizmat qiladigan **KOPAYISH ORGANI**dir.

### Gul qismlari bilan yaqindan tanishamiz:
1. **Gultojbarglar**: Gullarning rang-barang varaqchalari. Ular asalarilar va kapalaklarni o'zining go'zalligi bilan chaqirib turish vazifasini bajaradi.
2. **Changchi**: Gulning erkaki. Undan mitti oltinsimon changlar chiqadi.
3. **Urug'chi**: Gulning markazidagi silliq idishcha (urg'ochisi). Uning eng pastida mitti yumaloq tuguncha bor – mana shu yerda kelajakdagi urug' va meva pishadi!

### Changlanish qanday sodir bo'ladi?
Changchidagi changlarning urug'chi tumshuqchasiga kelib tushishi **CHANGLANISH** deyiladi.
- **Hasharotlar yordamida**: Ari yoki kapalak gulga nektar ichish uchun qo'nganda, uning oyog'iga changlar yopishadi. Boshqa gulga borganda esa o'sha changni o'sha gulning urug'chisiga qoldiradi.
- **Shamol orqali**: Terak yoki bug'doy guli chiroyli bo'lmasligi mumkin, shuning uchun shamol esganda changlar havoda uchib urug'chiga tushadi.`
  },
  {
    id: "6-4",
    classId: "6",
    title: "Meva va Uruglarning Tarqalishi",
    topic: "Botanika",
    shortDesc: "Meva va urug'larning shakllanishi, turlari va mitti urug'larning dunyo bo'ylab sayohat qilish sirlari.",
    difficulty: "O'rtacha",
    diagramType: "leaf",
    analogies: [
      "Urug' - bu kelajak daraxtining mitti 'chizmasi' (dasturi). Meva esa bu chizmani sovuqdan yoki hayvonlar tishidan asrovchi 'qobiq'dir.",
      "Mitti parachute shaklidagi qoqi-o't urug'lari - havoda sekin qulovchi kichik vertolyotchalardir."
    ],
    keyTerms: [
      { term: "Murtak (Embryo)", meaning: "Urug' ichidagi mitti boshlang'ich bo'lib, qulay nam va issiq sharoit tushganda unib chiqa boshlaydi." },
      { term: "Quruq mevalar", meaning: "Pishganda suvi qochib quriydigan va bir yoki ko'p urug'li bo'ladigan mevalar (masalan: yong'oq, no'xat dukkagi)." },
      { term: "Ho'l mevalar", meaning: "Tarkibida ko'p miqdorda suv va shirinlik saqlaydigan meva turi (masalan: olma, shaftoli, qovun)." }
    ],
    content: `Gullash tugagach, gul tojlari to'kilib ketadi va uning o'rnida hayratlanarli narsa – **MEVA** paydo bo'ladi. Meva ichida esa kelajak daraxtlarining urug'lari saqlanadi.

### Urug'ning tuzilishi:
Urug'ni qo'lingizga oling, uning tashqarisida qattiq qobig'i bor. Ichini ochsangiz ikkita katta palla va ularning o'rtasida mitti oqimtir boshda – **Murtak**ni ko'rasiz. Murtakda mitti ildizcha va bargchalar bor! U go'yo uxlab yotgan mitti bolakay.

### Urug'lar qanday tarqaladi?
Daraxtlar uzoqroq qishloqlarga o'z bolalarini qanday yuborishadi? Ular turli xildagi yo'llo'ychalardan foydalanadi:
1. **Shamol orqali**: Qoqio't va chinor urug'larining parashutchalari va qanotchalari bo'lib, shamol ularni kilometrlarga uchirib ketadi.
2. **Suv orqali**: Palma yong'og'i suzishni biladi, u dengiz to'lqinida oylab suzib, chekka orollarga borib unadi.
3. **Hayvonlar va odamlar orqali**: Qushqo'nmas kabi yopishqoq tikanli urug'lar shimingizga yoki itning juniga ilashib sayohat qiladi. Shirin mevalarni esa hayvonlar yeb, keyin uzoqroqda axlati bilan tashlaydi va o'sha yerda urug' unib chiqadi.`
  },
  {
    id: "6-5",
    classId: "6",
    title: "O'simliklar Dunyosining Xilma-xilligi",
    topic: "Botanika",
    shortDesc: "Yashil suvo'tlardan tortib, murakkab gulli o'simliklargacha bo'lgan o'simliklar olami evolutsiyasi.",
    difficulty: "O'rtacha",
    diagramType: "root",
    analogies: [
      "Suvo'tlar - poyasi va ildizi bo'lmagan eng sodda suv kashshoflari.",
      "Ochiq urug'lilar (Qarag'ay) - qishin-yozin yam-yashil kiyingan va urg'ochi qubbalarida urug' asraydigan jafokorlar."
    ],
    keyTerms: [
      { term: "Yuksak o'simliklar", meaning: "Tanasi poya, barg va ildizga (haqiqiy vegetativ organlarga) aniq bo'lingan o'simliklar guruhi." },
      { term: "Spora", meaning: "Sodda va sporali o'simliklarning (yo'sinlar, qirqbo'g'imlar) jinsiz ko'payishiga xizmat qiladigan o'ta mitti changsimon hujayrasi." },
      { term: "Ochiq urug'lilar (Gymnosperms)", meaning: "Guli bo'lmagan, lekin urug'i qubba (shishka) sirtida ochiq holda yetishadigan qarag'aydoshlar oilasi." }
    ],
    content: `Yer yuzida 350 mingdan ortiq o'simlik turi bor! Ular hammasi ham bir xil emas. Biologlar ularni ikki guruhga ajratadi:

### 1. Quyi o'simliklar (Sodda o'simliklar)
Bularga **Suvo'tlar** kiradi. Ularning tanasi juda sodda yassi plastinka – **tallom**dan iborat. Ularda na ildiz, na poya bor. Ular suv muhitining mitti asiridir.

### 2. Yuksak o'simliklar (Murakkab o'simliklar)
Ularning poya va barglari bor:
- **Yo'sinlar va Qirqbo'g'imlar**: Ular urug' o'rniga mikroskopik **spora**lar yordamida ko'payadi va namlikni juda yaxshi ko'radi.
- **Ochiq urug'lilar**: Qarag'ay, archa, tilog'och kabi ignabargli daraxtlar. Ularning mevalari va gullari yo'q. Qubbalarining (shishka) ichida urug'lar ochiq holda o'tiradi.
- **Yopiq urug'lilar (Gulli o'simliklar)**: Sayyoramizning haqiqiy qirollari! Ularda gul va urug'lar bor, urug'lar meva ichida xavfsiz himoyalangan. Biz yeydigan qovun, shaftsli, gilos – barchasi mana shu guruhdan!`
  },

  // ----------------------------------------------------
  // 7-SINF: ZOOLOGIYA DARSLIGI
  // ----------------------------------------------------
  {
    id: "7-1",
    classId: "7",
    title: "Sodda Hayvonlar: Bir Hujayrali Olam",
    topic: "Zoologiya",
    shortDesc: "Ameba va Infuzoriya tufelkaning ko'zsiz, oyoqsiz harakatlanishi va yashash sirlari.",
    difficulty: "O'rtacha",
    diagramType: "cell",
    analogies: [
      "Ameba - bu o'zgaruvchan shaklli loyga o'xshash mitti tirik organizm. Uning oyoqlari loy kabi oqib chiqadi.",
      "Infuzoriya tufelka - bu mitti shippakka juda o'xshaydi, uning kipriklari eshkak kabi suvni eshib suzishini ta'minlaydi."
    ],
    keyTerms: [
      { term: "Sodda hayvonlar", meaning: "Inson ko'ziga ko'rinmaydigan, tanasi faqat bitta hujayradan iborat bo'lgan hayvonot guruhi." },
      { term: "Soxta oyoqlar", meaning: "Amebaning harakatlanishi va oziqasini o'rab olishiga xizmat qiladigan vaqtinchalik sitoplazmatik o'simtalar." }
    ],
    content: `Biz hayvon deganda ayiq, yo'lbars, kuchukchani tushunamiz. Ammo ulardan tashqari bitta hujayradan tuzilgan, ko'zsiz, quloqsiz yashayotgan hayvonlar ham bor! Bular **Sodda hayvonlar** deb ataladi.

Kelajakda eng mashhur bo'lgan ikki do'st bilan tanishamiz:

### 1. Ameba (O'zgaruvchan shakl)
Uning doimi shakli yo'q, xamirdek cho'zilib yuradi. Oldinda ovqat ko'rsa, o'sha tomonga tanasini cho'zib, 'soxta oyoq' hosil qiladi va ovqatni yutib yuboradi. Harakatlanishi va ovqatlanishi bitta a'zoda!

### 2. Infuzoriya-Tufelka (Shippakcha)
Uning shakli biz kiyadigan shippakka (tufelka) o'xshab qat'iy bo'ladi. Tanasida mayda tukchalar bo'lib, suvda ularni qimirlatib eshkak eshayotgandek tez suzib yuradi.`
  },
  {
    id: "7-2",
    classId: "7",
    title: "Hasharotlar Olamining Tuzilishi",
    topic: "Zoologiya",
    shortDesc: "Hasharotlarning tashqi skeletlari, ochiq qon aylanishi va metamorfoz (o'zgarish) bosqichlari haqida.",
    difficulty: "Qiyin",
    diagramType: "insect",
    analogies: [
      "Hasharotning tashqi skeleti - bu ritsarlar kiyadigan temir zirh (bronya). Tana a'zolari zirh ichida xavfsiz turadi.",
      "Lichinkaning kapalakka aylanishi - dumsiz cho'michsimon qushchaning shohona uchuvchi samolyotga aylanishiga o'xshaydi."
    ],
    keyTerms: [
      { term: "Metamorfoz", meaning: "Hayvonlarning rivojlanish davomida lichinka bosqichidan voyaga yetgan shaklga keskin o'zgarib o'tishi (masalan: g'umbak -> kapalak)." },
      { term: "Traxeyalar", meaning: "Hasharotlarning butun tanasiga havo olib kiruvchi mitti nafas yo'llari." }
    ],
    content: `Hasharotlar sayyoramizning eng ko'p sonli aholisi hisoblanadi. Chumoli, ari, chigirtka va go'zal kapalaklar... Ularning barchasining tuzilishlari umurtqalilardan tubdan farq qiladi.

### Ularning qanday xususiyatlari bor?
1. **Zirh-Skelet**: Ularning suyaklari tanasining ichida emas, aksincha sirtida bo'ladi! Bu xitindan iborat qattiq po'stloq bo'lib, ichki nozik organlarni himoyalaydi.
2. **Ochiq qon tizimi**: Ularning qoni qizil emas, balki rangsiz yoki sarg'ish rangda bo'lib, ochiq bo'shliqda a'zolar atrofida bemalol oqib yuradi.
3. **Metamorfoz siri**: Kapalaklar bevosita kapalak bo'lib tug'ilmaydi. Avval mitti tuxum, keyin barg yeydigan qora qurt (lichinka), keyin muzlab qotgan g'umbak bo'ladi, keyin ise sehrli tarzda qanotli kapalakka aylanadi!`
  },
  {
    id: "7-3",
    classId: "7",
    title: "Umurtqasizlar: Chuvalchang va Bo'g'imoyoqlilar",
    topic: "Zoologiya",
    shortDesc: "Skelet suyagi yo'q bo'lgan eng mitti, ammo ekotizim uchun eng muhim hayvon guruhlari.",
    difficulty: "O'rtacha",
    diagramType: "insect",
    analogies: [
      "Ustritsalar va Salyangozlar - o'zlarining ohak uychalarini belida ko'tarib yuruvchi tinchliksevar sayyohlar.",
      "Gidra - dushman yaqinlashganda tanasidagi mitti zaharlangan nayzachalarni otadigan haqiqiy biologik kamonchidir."
    ],
    keyTerms: [
      { term: "Umurtqasizlar", meaning: "Tanasida ichki suyakli o'q (umurtqa) ustuni bo'lmagan hayvonlarning ulkan va xilma-xil sinflari." },
      { term: "Bo'g'imoyoqlilar", meaning: "Oyog'i alohida bo'g'imlardan iborat bo'lgan, tanasini qattiq xitin zirhi qoplagan tiriklik guruhi (qisqichbaqa, hasharot, o'rgimchak)." },
      { term: "Regeneratsiya", meaning: "Hayvonning shikastlangan yoki kesib tashlangan tana a'zolarini o'zidan o'stirib qayta tiklash xususiyati (masalan gidra yoki yomg'ir chuvalchangi)." }
    ],
    content: `Dunyodagi barcha hayvonlarni ikki katta davlatga ajratish mumkin: **Umurtqalilar** (suyakli poydevori bor) va **Umurtqasizlar** (suyakli poydevori yo'q). Yer yuzidagi barcha hayvonlarning taxminan 95 % i einan umurtqasizlardir!

### Umurtqasizlarning eng mashhur guruhlari:

1. **Bo'shliqichlilar (Gidralar, Meduzalar)**: Suv tubida yashaydi. Ularda miya yoki yurak yo'q, lekin ular mitti zaharlangan sensorli hujayralari orqali barcha mayda o'ljasini tuta olgan o'ta xavfli jonzotlardir.
2. **Chuvalchanglar (Yassi, Dumaloq, Halqali)**: Ularning orasida yomg'ir chuvalchangi eng qadrli do'stimizdir. U tuproqni kavlab, biz uchun yer osti kanallari ochib yuradi, yerni kislorodga to'yintiradi va oziqlantiradi.
3. **Mollyuskalar (Shilliqqurtlar)**: Ularning tanasi juda yumshoq bo'ladi, lekin ko'pchiligi o'zini qattiq chig'anoqlar ostiga yashiradi.
4. **Bo'g'imoyoqlilar**: Bunga qisqichbaqasimonlar, zaharli o'rgimchaklar va biz yaxshi taniydigan hasharotlar kiradi. Ularning har biri qattiq po'stloqli zirh kiyadi.`
  },
  {
    id: "7-4",
    classId: "7",
    title: "Baliqlar va Ikki Olam Chegarasi (Baqalar)",
    topic: "Zoologiya",
    shortDesc: "Suv hayotiga moslashgan baliqlar va ikki olam chegarasida nafas oluvchi amfibiyalar anatomiyasi.",
    difficulty: "O'rtacha",
    diagramType: "heart",
    analogies: [
      "Yosh amfibiya (itbaliq) dumli mitti baliqchadir, voyaga yetganda esa to'rt oyoqli quruqlik ovchisiga aylanadi.",
      "Baliqning yon chizig'i - bu uzoqdagi suv siljishini va suzayotgan boshqa jonzotlarni ko'rsatadigan biologik radardir."
    ],
    keyTerms: [
      { term: "Jabra (Gills)", meaning: "Baliqlarning suvda erigan gaz yoki kislorodni shimib, nafas olishiga xizmat qiladigan nozik qon tomir simmetrik devorchalari." },
      { term: "Yon chiziq", meaning: "Baliqlar tanasining yon tomonida joylashgan, suv oqimining tezligi va yo'nalishini sezadigan ajoyib his a'zosi." },
      { term: "Ikkiyoqlama hayotlilar (Amfibiyalar)", meaning: "Yoshlik davri suvda jabra orqali, voyaga yetganda quruqlikda teri va o'pka orqali nafas oluvchi sovuqqon hayvonlar." }
    ],
    content: `Bugun biz umurtqali hayvonlarning ilk kashshoflari bilan tanishamiz: suvning tubida yashovchi baquvvat **Baliqlar** va suvdan quruqlikka chiqishni boshlagan jasur **Andiz baqalari** (Amfibiyalar).

### Baliqlar: Suvning haqiqiy egalari
Ularda nafas olish uchun o'pka yo'q, shuning uchun ular suvni yutib, uning tarkibidagi erigan kislorodni **jabra (gils)** orqali qonga shimib oladi.
Baliqlarning yuragi atigi **ikki kamerali** (1 ta bo'lmacha va 1 ta qorinchadan iborat). Shuningdek, ularning tanasining o'rtasida mitti radarlar zanjiri bor, buni – **Yon chiziq** deymiz. Ular yordamida baliq ko'r bo'lsa ham qorong'i suvda toshlarga urilmasdan bemalol suza oladi.

### Amfibiyalar (Suvda va quruqlikda yashovchilar)
Baqalarni eslang: ular nafas olganda ham o'pka, ham doimiy nam bo'lib turuvchi **terisi** orqali havo yutadi. Agar baqaning terisi qurib qolsa, u nafas ololmay halok bo'ladi!
Ular metamorfoz (o'zgarish) orqali hayot kechiradi: suvga qo'yilgan urug'lardan uchi dumli mitti itbaliq chiqib keladi, vaqt o'tishi bilan uning dumi qisqarib oyoqlari o'sib chiqadi va u go'zal baqaga aylanadi.`
  },
  {
    id: "7-5",
    classId: "7",
    title: "Issiqqonlilar: Qushlar va Sutemizuvchilar",
    topic: "Zoologiya",
    shortDesc: "Tana haroratini doimiy saqlaydigan, rivojlangan nerv tizimi va uchish dairesiga ega hayvonlar.",
    difficulty: "Qiyin",
    diagramType: "heart",
    analogies: [
      "Issiqqonlilik - bu hayvonning ichki avtomatik isitish tizimidir (pechkasidir). Atrof bo'ronda qolsa ham uning ichi doimiy iliq turadi.",
      "Qushning suyaklari ichi g'ovak pufaklangan havo yo'llaridir, bu uchi yengil bo'lishi va balandga oson ko'tarilishi uchun ajoyib dizayndir."
    ],
    keyTerms: [
      { term: "Homoyotermiya (Issiqqonlilik)", meaning: "Tashqi muhit harorati o'zgarishidan qat'i nazar, tana haroratini bir xil iliq holatda saqlay olish xususiyati." },
      { term: "Sutemizuvchilar (Mammalia)", meaning: "Bolasini tirik tug'ib, o'z suti bilan boquvchi, jun qoplamining himoyasiga ega oliy umurtqalilar." },
      { term: "Havo xaltachalari", meaning: "Qushlarning uchishida o'pkalariga yordam beruvchi va tana zichligini kamaytiruvchi maxsus ichki pufaklar." }
    ],
    content: `Nima uchun kaltakesaklar qishda qotib ko'rinmay qoladi, lekin kichkina chumchuqlar qor yoqqanda ham daraxtda sayrab yuribdi? Chunki kaltakesaklar – sovuqqon, chumchuqlar va insonlar esa – **ISSIQQONLI** jonzotdir!

### Qushlar: Havoning mo'jizalari
Qushlar uchishi uchun juda ko'p xususiyatlarni shakllantirgan:
1. **Yengil skelet**: Ularning suyaklari ichi bo'sh, havo bilan liq to'la bo'ladi, bu ularni yengil uchuvchi samolyotga aylantiradi.
2. **Ikkiyoqlama nafas olish**: Ularda **Havo xaltachalari** bo'lib, o'zi ham nafas olganda, ham chiqarganda o'pka doimiy toza kislorod bilan to'lib turadi.
3. **Yurak 4 kamerali**: Toza kislorodli qizil qon bilan karbonat kislotali ko'k qon umuman aralashmaydi.

### Sutemizuvchilar: Tabiatning eng rivojlangan egalari
Ularni dunyoning barcha burchagida uchratasiz, hatto ko'k kitlar okeanlarda, ko'rshapalak esa havoda yashaydi. Ularning asosiy belgilari:
- Badanlari isituvchi **jun** bilan qoplangan.
- Ularning bosh miyasi, ayniqsa **Katta miya yarimsharlari po'stlog'i** juda yaxshi rivojlangan (ular o'rganadi, xotirlaydi va fikrlaydi).
- Ular o'z bolalarini tirik tug'ib, onaning shifobaxsh **suti** bilan parvarishlaydi.`
  },

  // ----------------------------------------------------
  // 8-SINF: ODAM VA UNING SALOMATLIGI
  // ----------------------------------------------------
  {
    id: "8-1",
    classId: "8",
    title: "Qon Aylanishi: Yurak va Nasoslar",
    topic: "Odam anatomiyasi",
    shortDesc: "Inson yuragining 4 kamerali tuzilishi, kichik va katta qon aylanish doiralari qonuniyatlari.",
    difficulty: "Qiyin",
    diagramType: "heart",
    analogies: [
      "Yurak - bu uyingizdagi suv motori (nasos). U bir sekund ham o'chmasdan kecha-kunduz tinimsiz qon haydab turadi.",
      "Arteriya - yuk mashinalari toza mahsulot va kislorod tashiyotgan keng shohko'chalar. Vena - chiqindilarni olib ketuvchi yo'llar."
    ],
    keyTerms: [
      { term: "Arteriya", meaning: "Yurakdan a'zolarga kislorodga to'yingan qizil toza qonni olib ketuvchi qon tomirlar." },
      { term: "Vena", meaning: "A'zolardan yoki to'qimalardan karbonat angidrid saqlovchi karbonatli to'q qonni yurakka olib keluvchi tomirlar." },
      { term: "Katta qon aylanish doirasi", meaning: "Chap qorinchadan boshlanib, butun tana a'zolarini kislorod bilan ta'minlab, o'ng bo'lmachada tugaydigan qon aylanish yo'li." }
    ],
    content: `Hozir kaftingizni musht qiling. Mana shu kichkina mushtingiz hajmidagi a'zo sizning butun hayotingizni ushlab turibdi! Bu – **YURAK**.

Yurak – inson organizmidagi eng baquvvat mushak. U daqiqasiga o'rtacha 70-80 marta urib, to'xtovsiz qon haydaydi.

### Yurakning ichki xonalari (Kameralari):
Bizning yuragimiz **4 ta xonali**:
- Tepada **2 ta bo'lmacha** (qonni qabul qiladi).
- Pastda **2 ta qorinsta** (qonni uzoqqa haydaydi).

### Ikki xil qon aylanish doirasi:
1. **Kichik doira (O'pka doirasi)**: Qon yurakdan o'pkaga borib, u yerdagi kislorodni o'ziga yuklab oladi va yurakka qaytadi.
2. **Katta doira (Tana doirasi)**: Kislorodga liq to'la bo'lgan qizil toza qon butun tanamizga – soch tolasidan tortib oyoq tirnog'igacha borib, barcha hujayralarni oziqlantiradi.`
  },
  {
    id: "8-2",
    classId: "8",
    title: "Miya va Nerv Tizimining Boshqaruvi",
    topic: "Odam anatomiyasi",
    shortDesc: "Miya qobiqlari, neyronlararo elektrik signallar va odam organizmining markaziy boshqaruv pulti.",
    difficulty: "Qiyin",
    diagramType: "dna",
    analogies: [
      "Neyronlar - bir-biriga elektrik simlar orqali ulangan kompyuter tarmoqlari kabidir.",
      "Refleks - issiq narsani ushlab olganda qo'lingizni o'ylab o'tirmasdan tezda tortib olishingiz (markaziy miya ruxsatisiz sodir bo'ladigan himoya tizimi)."
    ],
    keyTerms: [
      { term: "Neyron", meaning: "Nerv tizimining signallarni uzatishga ixtisoslashgan jami asosiy strukturaviy-funksional hujayrasi." },
      { term: "Refleks", meaning: "Markaziy nerv tizimi ishtirokida tashqi yoki ichki ta'sirlarga javob qaytarish reaksiyasi." }
    ],
    content: `Agar tasodifan issiq choynakka qo'lingiz tegsa nima qilasiz? Sekunddan tezroq muddatda qo'lingizni tortib olasiz, to'g'rimi? Ana o'sha xabarni kim soniyaning mingdan bir ulushida yetkazdi? Albatta, **NERV TIZIMI** va uning qiroli – **MIYA**!

### Markaziy boshqaruv tizimi qanday ishlaydi?
Butun badanimizda millionlab mitti **neyronlar** degan nerv hujayralari yashaydi. Ular bir-biri bilan elektrik simlar kabi bog'langan bo'lib, miyadan kelgan buyruqlarni yuboradi.

### Miyaning qismlari:
- **Katta miya yarimsharlari**: Siz dars yodlaganda, rasmlar chizganda, orzu qilganda faol ishlaydi (fikrlash markazi).
- **Miyacha**: Siz velosiped uchayotganingizda, muvozanatni saqlab yurishingizni nazorat qiluvchi muvozanat markazi.
- **Uzunchoq miya**: Hech o'ylab ko'rganmisiz: nega uxlayotganingizda ham nafas olasiz, yuragingiz urishdan to'xtamaydi? Chunki uzunchoq miya siz uxlaysizmi, uyg'oqmisiz, bu hayotiy jarayonlarni avtomatik boshqarib turadi.`
  },
  {
    id: "8-3",
    classId: "8",
    title: "Tayanch-Harakat Tizimi va Suyaklar",
    topic: "Odam anatomiyasi",
    shortDesc: "Inson karkasi bo'lmish suyaklarning kimyoviy tarkibi va bo'g'imlarning harakatlanish simfoniyasi.",
    difficulty: "Qiyin",
    diagramType: "root",
    analogies: [
      "Suyakning organik tarkibi uning kauchuk kabi egiluvchanligini, mineral tarkibi esa marmar kabi baquvvat mo'rtligini ta'minlaydi.",
      "Skelet - yangi imorat binosining qat'iy temir devor karkasidir."
    ],
    keyTerms: [
      { term: "Bo'g'im (Joint)", meaning: "Suyaklarning bir-biri bilan o'zaro harakatchan tutashgan qismi o'ram paylar bilan himoyalangan." },
      { term: "Osteotsit (Bone cell)", meaning: "Suyak to'qimasining asosi bo'lgan va kalsiy minerallarini asraydigan mustahkam hujayra." },
      { term: "Gipodinamiya", meaning: "Kam harakatlanish oqibatida mushaklar kuchsizlanishi va tana a'zolari faoliyati sustlashishi xavfi." }
    ],
    content: `Inson qanday tik qadam bosadi va yugura oladi? Tanamizda buni bajaradigan ajoyib jamoa bor: **Tayanch-harakat tizimi**. U **suyak (skelet)** va uni tortib turuvchi faol **mushaklar**dan iborat.

### Suyakning kimyoviy siri (Nega u sinmaydi?):
Agar biz faqat temir kabi qattiq bo'lganimizda, biror yerdan sakraganda suyaklarimiz parcha-parcha bo'lib ketgan bo'lardi. Bizda ikki turdagi modda bor:
1. **Organik moddalar (Kollagen, Ossein)**: Suyakka rezina kabi elastiklik va egiluvchanlik beradi. Yosh bolalarda u juda ko'p, shuning uchun ular ko'p yiqilsa ham suyaklari osonlikcha sinmaydi.
2. **Anorganik moddalar (Kalsiy, Fosfatlar)**: Suyakka toshdek qattiqlik beradi. Yoshi katta bobolarimizda bu moddalar juda ko'payib ketib, suyak poydevori mo'rt bo'lib qoladi va tez sinadi.

### Bo'g'imlar: Moy kabi sirpanuvchan zvenolar
Ikki suyak uchrashadigan joyda **Bo'g'im** paydo bo'ladi. Ularning o'rtasida maxsus moy suyaklarning bir-biriga ishqalanib yeyilib ketishini oldini oladi. Mushaklarimiz qisqarganda suyaklarni shu bo'g'im tirsagidan sim kabi tortib harakatga keltiradi.`
  },
  {
    id: "8-4",
    classId: "8",
    title: "Ovqat Hazm Qilish va Ozuqaning Yo'li",
    topic: "Odam anatomiyasi",
    shortDesc: "Yutgan oziq-ovqatingiz oshqozonda qanday parchalanishi va jigarning ajoyib filtrlik siri.",
    difficulty: "Qiyin",
    diagramType: "root",
    analogies: [
      "Fermentlar - bu oqsillar va yog'larni hujayra to'qiydigan mitti zarraga bo'lib tashlovchi biologik qaychilardir.",
      "Jigar - inson tanasidagi eng katta va aqlli tozalash zavodidir (suv va qon bio-filtri)."
    ],
    keyTerms: [
      { term: "Ferment", meaning: "Hujayralarda kimyoviy parchalanish reaksiyalarini millionlab marta tezlashtiruvchi biologik kuchli faol moddalar." },
      { term: "So'rilish", meaning: "Hazm bo'lgan ozuqa zarrachalarining ingichka ichak sirtidagi vorsinkalar orqali qonga va limfaga o'tishi." },
      { term: "Safro (Bile)", meaning: "Jigar tomonidan ajratilib, 12 barmoqli ichakda yog'larni mitti tomchilarga bo'lib beruvchi yashil-sariq suyuqlik." }
    ],
    content: `Biz kuniga uch mahal yaxshi ovqatlanamiz. Oshqozonimiz o'sha lagandagi guruchni qanday qilib bizga kerak bo'lgan kalsiy, oqsil va energiyaga aylantira oladi? Bu yerda dunyodagi eng murakkab konveyer – **Ovqat hazm qilish tizimi** ishlaydi.

### Taomning mitti sarguzashtlari:

1. **Og'iz bo'shlig'i**: Tishlarimiz bilan ovqatni mexanik ravishda maydalaymiz, so'lak tarkibidagi birinchi fermentlar uglevodlarni (shirinliklarni) parchalashni boshlaydi.
2. **Oshqozon (Blender)**: Ovqat qizilo'ngach orqali o'tib, mushakli qopga – oshqozonga tushadi. Oshqozonda kuchli **kislota (HCl)** va **Pepsin** degan oqsil kesuvchi ferment uchrashib ovqatni suyuq bo'tqaga aylantiradi.
3. **Ingichka ichak (Oziqlanish zali)**: Eng uzun ichagimiz! Bu yerda qolgan barcha oqsillar, yog'lar va uglevodlar mitti molekulagacha bo'linadi va ichak devoridagi vorsinkalar (tukchalar) orqali to'g'ridan-to'g'ri qonimizga **so'riladi**.
4. **Jigar (Bojxona ombori)**: Ingichka ichakdan chiqqan qon jigar bojxonasidan o'tadi. Jigar qondagi barcha zaharli moddalarni va dorilarni filtrlash orqali tozalaydi va o't pufagi yordamida yog'larni parchalovchi **Safro** ajratadi.`
  },
  {
    id: "8-5",
    classId: "8",
    title: "Nafas Olish va Siydik Ajratish",
    topic: "Odam anatomiyasi",
    shortDesc: "O'pkalardagi gazlar almashinuvi siri va buyraklarning butun qonimizni ajoyib tozalash kuchi.",
    difficulty: "Qiyin",
    diagramType: "heart",
    analogies: [
      "Alveolalar - o'pkadagi uzum shingillaridek osilgan mitti pufakchalar bo'lib, ular qonga kislorod yuklab beradi.",
      "Nefron - har daqiqa qonni suzib turadigan mitti nano-tozalovchi elakchalardir."
    ],
    keyTerms: [
      { term: "Alveola", meaning: "O'pkaning oxiridagi mitti havo pufakchalari bo'lib, uning yupqa qobig'ida kapillyar tomirlar bilan gaz almashinuvi sodir bo'ladi." },
      { term: "Nefron", meaning: "Buyraklarning siydik hosil qiluvchi va qonni filtrlovchi eng mitti asosiy ishchi strukturaviy zvenosi." },
      { term: "Diafragma", meaning: "Ko'krak bo'shlig'ini qorindan ajratuvchi va o'pkalarni kengaytirib-toraytirib nafas olishni boshqaradigan kuchli yassi mushak." }
    ],
    content: `Biz nafas olayotganda havodagi kislorod o'pkamizga tushadi. Ammo u qanday qilib qo'l va oyoqlarimizga yetib boradi? Va tanamizdagi yig'ilib qolgan ortiqcha badbo'y chiqindi va namlar qanday yo'qoladi? Bularni ikki hayotiy tizim boshqaradi:

### 1. Nafas olish tizimi (Kislorod yuklash stansasii)
Havo burundan o'tib, traxeya, bronxlar orqali o'pkaning uchidagi salkam 300 million dona **Alveolalar**ga boradi.
Bu mitti pufakchalar yuzasidan o'tayotgan qon tomirlariga kislorod sakrab kiradi, qondagi karbonat angidrid (chiqindi gaz) esa alveolalar ichiga sakrab o'tib tashqariga nafas sifatida chiqarib yuboriladi.

### 2. Siydik ajratish tizimi (Buyrak filtrlar jamoasi)
Orqamizda loviyaga o'xshash mitti ikki dona **Buyrak** bor. Ular oddiy narsa emas, ular super-biologik filtrlardir!
Sutkasiga barcha qonimiz buyrakdan taxminan 300 marta o'tib, tozalanadi. Buyrakning mitti elaklari – **Nefronlar** qondagi barcha zararli kislotalar, ortiqcha tuzlar va suvlarni ajratib olib, siydik pufagiga yuboradi (bu siydik bo'lib tashqariga chiqadi).`
  },

  // ----------------------------------------------------
  // 9-SINF: SITOLOGIYA VA GENETIKA
  // ----------------------------------------------------
  {
    id: "9-1",
    classId: "9",
    title: "DNT va Irsiyat Sirlari",
    topic: "Sitologiya",
    shortDesc: "DNT qo'sh spiral zanjiri, nukleotidlar zanjiri va genetic ma'lumotlarning nasldan naslga o'tishi.",
    difficulty: "Qiyin",
    diagramType: "dna",
    analogies: [
      "DNT degani bu - biologik oshpazlik retseptlar kitobi. Unda ko'zlaringiz qora bo'ladimi yoki ko'k, sochingiz tekis bo'ladimi yoki jingalak - hammasi yozilgan.",
      "Komplementarlik qonuni - xuddi qulf va kalitdek bir-biriga mos keluvchi kiyimlardir (Adeninga faqat Timin, Guaninna esa faqat Sitosin tushadi)."
    ],
    keyTerms: [
      { term: "DNT (Dezoksiribonuklein kislota)", meaning: "Hujayralarda irsiy ma'lumotni saqlash, nasldan-naslga uzatish va uni amalga oshirish vazifasini bajaruvchi polimer organik molekula." },
      { term: "Gen", meaning: "DNT zanjirining muayyan bir oqsil strukturasini belgilaydigan irsiy bo'lagi." },
      { term: "Komplementarlik qonuni", meaning: "DNT qo'sh zanjirida nukleotidlarning qat'iy juft hosil qilib birikishi: A-T, G-S." }
    ],
    content: `Siz nega otangizga yoki onangizga o'xshaysiz? Nega ba'zi odamlarning sochlari sarg'ish, ba'zilariniki qora bo'ladi? Bu borada tabiatning eng katta kompyuter kodi – **DNT** aybdor!

### DNT nima o'zi?
DNT – bu qo'sh spiral shaklidagi mitti narvonga o'xshash zanjir. Bu zanjirning har bir pog'onasi maxsus mitti harflar – **Nukleotidlar**dan iborat:
- **A** (Adenin)
- **T** (Timin)
- **G** (Guanin)
- **S** (Sitosin)

Bular har doim qat'iy qoidaga bo'ysunadi (Komplementarlik): **A** faqat **T** bilan gaplashadi, **G** faqat **S** bilan qo'l berib ko'rishadi.

Miyangiz, jigaringiz, ko'zingiz qanday tuzilishi lozimligi haqidagi ma'lumotlar aynan mana shu 4 ta harfning ketma-ket joylashishida (kodida) yozib qo'yilgan. Bir dona genda sizning ko'z rangiz, bo'yingiz kabi belgilar kodlangan bo'ladi.`
  },
  {
    id: "9-2",
    classId: "9",
    title: "Hujayraning Bo'linishi: Mitoz va Meyoz",
    topic: "Sitologiya",
    shortDesc: "Tana hujayralarining mitoz yo'li bilan va jinsiy hujayralarning meyoz yo'li bilan bo'linishi farqlari.",
    difficulty: "Qiyin",
    diagramType: "cell",
    analogies: [
      "Mitoz - bu kserof nusxalash asbobi (Kseroks). U hujayraning aynan bir xil 100% nusxasini ko'paytirib beradi.",
      "Meyoz - bu xromosomalar kartalarini aralashtirib, yarmini yangi o'yinchiga ulashish jarayonidir."
    ],
    keyTerms: [
      { term: "Mitoz", meaning: "Somatik (tana) hujayralarining bo'linish usuli bo'lib, xromosomalar to'plami o'zgarmaydi (2n -> 2n)." },
      { term: "Meyoz", meaning: "Jinsiy hujayralarning shakllanishidagi bo'linish turi, bunda xromosoma to'plami ikki barobar qisqaradi (2n -> 1n)." }
    ],
    content: `Agar siz yiqilib tizzangizni tirnab olsangiz, bir necha kundan keyin u yerda yangi teri paydo bo'ladi. Bu qanday sodir bo'ladi? Javob: qolgan tirik teri hujayralari bo'linib o'z xonadoshini ko'paytirdi!

Hujayralar ikki xil uslubda ko'payadi:

### 1. MITOZ (Tana hujayralari bo'linishi)
Bu usulda ona hujayra o'zidan aynan bir xil bo'lgan ikkita qiz hujayra hosil qiladi. Ulardagi xromosomalar soni aynan ona hujayradagidek bir xil (diploidal, 2n) holatda bo'ladi. Bu bo'linish tufayli tirnay olgan terimiz tiklanadi, bo'yimiz o'sadi.

### 2. MEYOZ (Jinsiy hujayralar shakllanishi)
Bu sehrli bo'linish bo'lib, unda xromosomalar soni ikki barobar qisqaradi. Masalan, odamda tana hujayrasida 46 ta xromosoma bor, ammo jinsiy hujayralarda meyozdan so'ng atigi 23 ta qoladi. Negaligini bilasizmi?
Chunki kelajakda ota tomondan 23 ta va ona tomondan 23 ta xromosoma birlashib, yana to'laqonli 46 ta xromosomaga ega bo'lgan yangi chaqaloq shakllanishi kerak!`
  },
  {
    id: "9-3",
    classId: "9",
    title: "Gregor Mendel va Genetika Qonunlari",
    topic: "Sitologiya",
    shortDesc: "Monastir bog'ida boshlangan buyuk kashfiyot: mitti no'xatlar yordamida irsiyat qonuniyatlarini o'rganish.",
    difficulty: "Qiyin",
    diagramType: "dna",
    analogies: [
      "Dominant gen - bu hamma gapni o'zi gapiradigan polvon kurashchidir. Retsessiv gen esa uning soyasidagi uyatchan bolakaydir.",
      "Gomozigota - bu xuddi bir xil rangdagi ikki poy poyabzalga o'xshaydi (AA yoki aa)."
    ],
    keyTerms: [
      { term: "Allellar", meaning: "Gomologik xromosomalarning bir xil sohasida joylashgan va bitta belgining turli ko'rinishlarini (masalan, sarg'ish yoki yashil) belgilovchi juft genlar." },
      { term: "Dominant belgi", meaning: "Gibrid avlodda chatishtirilayotgan belgilardan ustun kelib, birinchi bo'lib o'zini yuzaga chiqaradigan belgi (masalan, 'A')." },
      { term: "Retsessiv belgi", meaning: "Dominant gen bo'lganda yashirin qoladigan va faqat gomozigota (aa) holatdagina ko'rinadigan kuchsiz belgi." }
    ],
    content: `XIX asrda avstriyalik rohib **Gregor Mendel** monastir bog'ida oddiy **no'xatlar** bilan ajoyib tajribalar o'tkazdi. U bilmagan holda biologiyada eng ulug' fanlardan biri – **GENETIKA**ga poydevor qo'ydi!

### Mendel nima qildi?
U sarg'ish no'xat bilan yashil no'xatni o'zaro chatishtirdi (changlatdi). Qiziqarli tomoni, birinchi avloddagi barcha no'xat bolalar **yuz foiz sarg'ish** bo'lib tug'ildi! Yashil rang qayoqqa yo'qoldi?

Mana shu yerda Mendel birinchi biologik qonunni kashf etdi:
1. **Mendelning I Qonuni (Bir xillik qonuni)**: Birinchi avlodda belgilar aralashib ketmaydi, ulardan bittasi ustun – **Dominant (A)**, ikkinchisi esa yashirin – **Retsessiv (a)** bo'ladi.
2. **Mendelning II Qonuni (Ajralish qonuni)**: Birinchi avloddagi sarg'ish gibrid no'xatlarni (Aa) o'zaro chatishtirganda, ikkinchi avlodda (F2) kutilmaganda yana yashil no'xatlar paydo bo'ldi! Tajribada sarg'ish va yashil no'xatlar soni **3:1** nisbatda (75% sarg'ish, 25% yashil) namoyon bo'ldi.`
  },
  {
    id: "9-4",
    classId: "9",
    title: "Plastik va Energetik Almashinuv (Metabolizm)",
    topic: "Sitologiya",
    shortDesc: "Hujayra ichidagi to'xtovsiz biologik zavod: moddalar hosil bo'lishi va ATF energiya batareyalari parchalanishi.",
    difficulty: "Qiyin",
    diagramType: "cell",
    analogies: [
      "Assimilyatsiya (Anabolizm) - bu bino qurish uchun g'isht terishdir (moddalar hosil qilinadi, quvvat sarflanadi).",
      "ATF - bu hujayraning mitti quvvat batareyasidir. U zaryadlangan holatda ATF, zaryadi tugaganda ADF deb ataladi."
    ],
    keyTerms: [
      { term: "Metabolizm (Moddalar almashinuvi)", meaning: "Hujayra ichida sodir bo'ladigan barcha kimyoviy sintez va parchalanish reaksiyalarining yig'indisi." },
      { term: "Dissimilyatsiya (Katabolizm)", meaning: "Murakkab organik moddalarni parchalash orqali ularning tarkibidagi energiyani (ATF) biologik ozod qilish jarayoni." },
      { term: "Mitoxondriya", meaning: "Hujayraning haqiqiy elektrostansiyasi! Aynan shu yerda moddalar parchalanib, ATF batareyalari zaryad oladi." }
    ],
    content: `Siz uxlayotganingizda ham hujayralaringiz soniyasiga millionlab kimyoviy ishlarni bajaradi. Bu jarayonlar **METABOLIZM** yoki moddalar almashinuvi deb ataladi. U ikki qarama-qarshi oqimdan iborat:

### 1. Plastik almashinuv (Assimilyatsiya / Anabolizm):
Bu - qurilish jarayoni! Hujayra o'ziga kirgan mitti aminokislotalardan oqsillar, glyukozadan kraxmal yasaydi. Bu jarayonda **energiya sarflanadi**. Xuddi g'ishtdan imorat qurganda usta kuch sarflagandek.

### 2. Energetik almashinuv (Dissimilyatsiya / Katabolizm):
Bu - parchalash jarayoni! Hujayra siz yegan taomlarni (masalan glyukozani) kislorod yordamida mitoxondriya ichida parchalab yuboradi. Natijada sizga harakat qilish va gapirish uchun o'ta zarur bo'lgan **ATF (Adenozintrifosfat)** energiya molekulalari tayyorlanadi.

Aynan bir molekula glyukoza to'liq parchalansa, hujayrada naqd **38 molekula ATF** batareyasi quvvat oladi! Bu energiya hisobiga biz yashaymiz.`
  },
  {
    id: "9-5",
    classId: "9",
    title: "Mutatsiyalar va O'zgaruvchanlik",
    topic: "Sitologiya",
    shortDesc: "DNT kodi nusxalanishidagi kichik imlo xatolaridan kelib chiqadigan qiziqarli mutatsiyalar va ularning turlari.",
    difficulty: "Qiyin",
    diagramType: "dna",
    analogies: [
      "Mutatsiya - kitob chop etganda tasodifan 'TUZ' o'rniga 'MUSHUK' deb bosilib ketishidek mitti biologik xatodir.",
      "Modifikatsiya - quyoshda tursangiz teringiz qorayishi, lekin sharoit o'zgarganda yana o'z holiga qaytishi (irsiyatsiz o'zgarish)."
    ],
    keyTerms: [
      { term: "Irsiy o'zgaruvchanlik (Mutatsion)", meaning: "DNT tuzilishining mutatsiyalar ta'sirida to'satdan va qaytmas o'zgarishi va bu o'zgarishning bolalarga o'tishi." },
      { term: "Modifikatsion o'zgaruvchanlik", meaning: "Genlar o'zgarmasdan, faqat tashqi muhit (quyosh, oziq) tasirida belgi shaklining vaqtincha o'zgarishi." },
      { term: "Mutagen omillar", meaning: "Mutatsiyani sun'iy tezlashtiruvchi zararli omillar: radiatsiya, nikotin zaharli moddalari yoki sarg'ish ultrabinafsha nurlar." }
    ],
    content: `Nima uchun tabiatda ba'zan ko'zlari butunlay ko'k rangli oppoq mushuklar (albinoslar) yoki to'rt bargli bedalar paydo bo'lib qoladi? Bunga biologiyaning eng sirli xodisasi – **MUTATSIYA** sababchi!

Biologlar o'zgarishlarni ikki guruhga ajratadi:

### 1. Irsiy bo'lmagan o'zgaruvchanlik (Modifikatsiya)
Siz har kuni tosh ko'tarsangiz, mushaklaringiz baquvvat bo'lib shishadi. Lekin kelajakda tug'iladigan chaqalog'ingiz mushakdor bo'lib tug'ilmaydi. Chunki bu o'zgarish geningizga yozilmagan, u shunchaki tashqi sharoitga tana moslashuvidir.

### 2. Irsiy o'zgaruvchanlik (Mutatsiyalar)
Bu yerda xato to'g'ridan-to'g'ri DNT zanjirida sodir bo'ladi!
- **Gen mutatsiyalari**: DNT dagi bitta mitti harfning joyi almashib qolishi.
- **Xromosoma mutatsiyalari**: Xromosoma bo'laklarining sinishi yoki yo'qolishi.
- **Genom mutatsiyalari**: Xromosomalar sonining o'zgarishi. Masalan, odamda odatda 46 ta xromosoma bo'lishi kerak, lekin ba'zida adashib 47 dona bo'lib qolsa – bu Daun sindromiga sabab bo'ladi.`
  },

  // ----------------------------------------------------
  // 10-11-SINF: UMUMIY BIOLOGIYA VA EKOLOGIYA
  // ----------------------------------------------------
  {
    id: "10-1",
    classId: "10-11",
    title: "Ekotizim: Ekologik Zanjirlar",
    topic: "Evolutsiya",
    shortDesc: "Energiya piramidasi, produtsent va konsumentlar, hamda tabiatdagi oziq zanjiri muvozanati.",
    difficulty: "Qiyin",
    diagramType: "pyramid",
    analogies: [
      "Oziq zanjiri - bu o'zaro bir-biriga ulangan parovoz vagonlaridir. Agar bitta vagon (masalan, hasharotlar) tushib qolsa, butun poezd (ekotizim) halokatga uchraydi.",
      "10 foiz qoidasi - bu xuddi cho'ntagingizdagi pullarning har bir navbatdagi do'konga borganda 90% qismini soliq sifatida to'lab ketishingizga o'xshaydi."
    ],
    keyTerms: [
      { term: "Produtsentlar", meaning: "Noorganik moddalardan foydalanib o'zi uchun organik modda sintezlaydigan organizmlar (masalan, yashil o'simliklar)." },
      { term: "Konsumentlar", meaning: "Tayyor organik moddalar bilan oziqlanuvchi iste'molchilar (o'txo'rlar, yirtqichlar)." },
      { term: "Ekologik piramida sharti (10% qoidasi)", meaning: "Zanjirning bir bo'g'inidan ikkinchisiga o'tayotganda energiyaning bor-yo'g'i 10% qismi saqlanib o'tishi haqidagi qonuniyat." }
    ],
    content: `Sayyoramizdagi barcha jonzotlar bir-biri bilan ko'rinmas iplar orqali bog'langan. Hech bir hayvon yoki o'simlik yolg'iz o'zi yashay olmaydi. Buni o'rganadigan fan **EKOLOGIYA** deb ataladi.

Kelajakda tabiatning 'oziq-ovqat piramidasi' bilan tanishamiz:

### Piramidaning boshqaruv qatlamlari:
1. **Produtsentlar (Yaratuvchilar)**: O'simliklar. Ular quyoshdan bepul energiya olib, oziq tayyorlashadi.
2. **I-darajali Konsumentlar**: O'txorlar (masalan, quyon, sigir). Ular o'tlarni yeyishadi.
3. **II-darajali Konsumentlar**: Yirtqichlar (masalan, tulki, bo'ri). Ular o'txorlarni ovlashadi.
4. **Destruktorlar (Chituvchilar)**: Zamburug'lar va bakteriyalar. Ular chigan o'simlik yoki hayvonlarni chirityib, tuproqqa mineral qiladi va o'simlikka yana ozuqa bo'ladi.

### Ekologik piramida qonuni (10 foiz qoidasi):
O'simlik yeyayotgan quyon o'simlikning bor-yo'g'i **10% energiyasini** o'z tanasiga aylantiradi, qolgan 90% isiib ketadi. Quyonni yegan tulki ham quyonning bor-yo'g'i 10% kaloriyasini o me'lashtiradi. Shuning uchun tabiatda har doim o'simliklar yirtqichlarga qaraganda ancha ko'p bo'ladi!`
  },
  {
    id: "10-2",
    classId: "10-11",
    title: "Evolutsion Rivojlanish va Darvin Nazariyasi",
    topic: "Evolutsiya",
    shortDesc: "Tabiiy tanlanish, yashash uchun kurash va har xil moslashuvchanliklar evolutsiyasi qonunlari.",
    difficulty: "Qiyin",
    diagramType: "dna",
    analogies: [
      "Tabiiy tanlanish - tabiat degan super-murabbiyning (trener) faqat eng chidamli va aqlli sportchilarni keyingi o'yinga saralab olishidir.",
      "Yashash uchun kurash - oziq va dushmanlardan omon qolish uchun tabiat olimpiadasidagi shafqatsiz kurash."
    ],
    keyTerms: [
      { term: "Tabiiy tanlanish", meaning: "Yashash sharoitlariga yaxshiroq moslashgan organizmlarning saqlanib qolib, moslashmaganlarining yo'qolib ketish jarayoni." },
      { term: "Yashash uchun kurash", meaning: "Organizmlarning tashqi muhit noqulay omillari, dushmanlari va o‘zaro oziq-hudud uchun olib boradigan murakkab munosabatlari." }
    ],
    content: `Nima uchun cho'lda yashaydigan kaktuslarning barglari o'rnida tikanlar bor? Nima uchun Jirafaning bo'yni uzun bo'lib qolgan? Bu mo'jizalarni biologiyaning eng ulug' qonuni – **EVOLUTSIYA** tushuntiradi.

Evolutsiyaning harakatlantiruvchi kuchi **Charles Darwin** tomonidan kashf etilgan bo'lib, 3 ta ustunga tayanadi:

### 1. Irsiy o'zgaruvchanlik
Hamma organizmlar o'z avvalgilaridan biroz g'ayritabiiy yoki yangi belgilar bilan tug'iladi. Masalan, jirafalar orasida bo'yni boshqalardan biroz uzunroq bo'lgan mitti jirafachalar tug'ilgan.

### 2. Yashash uchun kurash
Ozuqa kam, dushmanlar ko'p bo'lgani uchun hayvonlar tirik qolishga intiladi. Jirafalar daraxt barglarini yeyish uchun kurashgan.

### 3. Tabiiy tanlanish
Eng uzun bo'yinli jirafalar baland daraxtdagi barglarga osonlikcha yetib, ochlikdan omon qolgan. Qisqa bo'yinlilari esa ochlikdan halok bo'lgan. Omon qolgan uzun bo'yinli jirafalar ko'payib, o'z bolalariga o'sha genlarni topshirgan. Ming yillar davomida bu jarayon takrorlanib, hozirgi uzun bo'yinli jirafalar paydo bo'lgan.`
  },
  {
    id: "10-3",
    classId: "10-11",
    title: "Hayotning Kelib Chiqishi va Eralar",
    topic: "Evolutsiya",
    shortDesc: "Zaminimizda hayot qanday boshlandi? Miller tajribasi, birlamchi okean sirlari va geoxronologik xarita.",
    difficulty: "Qiyin",
    diagramType: "pyramid",
    analogies: [
      "Koatservat - suvdagi oqsillar aralashib hosil qilgan, hujayra qobig'ini eslatuvchi mitti shaffof tomchilardir.",
      "Geoxronologik jadval - bu yer sayyorasining 4.6 milliard yillik ulug' kitobidir."
    ],
    keyTerms: [
      { term: "Koatservat", meaning: "Birlamchi okean suvidagi murakkab oqsillarning konsentratsiyalashishi bilan hosil bo'lgan quyuq gidrofob molekulyar tomchilar." },
      { term: "Abiogen sintez", meaning: "Eski zamin tarixida noorganik gazlardan (metan, vodorod, suv bug'i) elektr uchquni yordamida hayotiy organik birikmalar paydo bo'lish nazariyasi." },
      { term: "Mezozoy", meaning: "Dinozavrlar qirolligi, ignabargli daraxtlar keng tarqalgan va ilk qushlar paydo bo'lgan uchinchi biologik buyuk era." }
    ],
    content: `Yer sayyorasi bundan taxminan 4.5 milliard yil muqaddam qup-quruq changli jazirama bo'lib yaralgan. Unda na suv, na havo, na bitta tirik hujayra bo'lgan. Xo'sh, hayot qanday boshlandi?

### Oparin-Xoldeyn Nazariyasi: Birlamchi okean va Koatservat sho'rvasi
Olimlarning fikricha, qadimgi osmonda kuchli chaqmoqlar chaqib, vulqonlar otilganda, havoda suzib yurgan noorganik gazlar o'zaro qo'shilib, yerga yomg'ir bo'lib yoqqan. Bu mitti tomchilar daryolar hosil qilib, birlamchi issiq okeanda yig'ilgan va biologik organik moldachalarni – **koatservat tomchilari**ni hosil qilgan. Bu tomchilar atrofdan ovqat shimib olib, birinchi hujayraga (bakteriyalarga) aylangan!

### Geoxronologik jadval (Yer boblari):
Yer yuzi o'z tarixini bir nechta bob ya'ni **Eralar**ga ajratadi:
1. **Arxey**: Eng birinchi mikroskopik hayot davri (bakteriyalar paydo bo'lishi).
2. **Proterozoy**: Oddiy hayvonlar, suvo'tlar va meduzalar davri.
3. **Paleozoy**: Baliqlar, o'simliklarning quruqlikka birinchi hujayralar bo'lib chiqishi va ulkan sudralib yuruvchilar shakllanishi.
4. **Mezozoy (Dinozavrlar asri)**: Yer yuzini ulkan kaltakesaklar bosib ketdi va qarag'aylar unib chiqdi.
5. **Kaynozoy (Hozirgi yangi era)**: Issiqqonlilar, sutemizuvchilar va bizning aqlli insoniyat hukmron bo'lgan davr.`
  },
  {
    id: "10-4",
    classId: "10-11",
    title: "Biosfera va Global Ekologiya",
    topic: "Evolutsiya",
    shortDesc: "Vernadskiy ta'limoti bo'yicha biosfera qatlamlari, ozon teshigi, Orol fojiasi va tabiatni asrash.",
    difficulty: "Qiyin",
    diagramType: "pyramid",
    analogies: [
      "Biosfera - bu sayyoramizning kiyimga o'xshash yashil jonli qobig'idir.",
      "Ozon qatlami - bu sayyoramiz kiygan quyosh nurlaridan asraydigan mitti ko'zoynakdir."
    ],
    keyTerms: [
      { term: "Biosfera", meaning: "Yer sayyorasining organizmlar yashaydigan va ularning faoliyati ta'sirida o'zgargan butun hayotiy qobig'i." },
      { term: "Noosfera (Aql qatlami)", meaning: "Biosferaning inson aqli va texnologiyalari ta'sirida boshqariladigan eng yuqori taraqqiy etgan yangi bosqichi." },
      { term: "Qizil kitob (Red Book)", meaning: "Butun dunyoda yoki alohida davlatda yo'qolib ketayotgan nodir jonzotlarni ro'yxatlarga oladigan rasmiy davlat hujjati." }
    ],
    content: `Biz butun koinotdagi mo'jizali yashil sayyorada yashaymiz. Bu yer hayotining barcha tarqalgan joyi rus olimi V.I. Vernadskiy tomonidan **BIOSFERA** deb nomlangan.

### Biosfera qismlari:
U uchta asosiy olam kesishmasida joylashgan:
- **Atmosferaning pastki qismi** (taxminan 20 km balandlikkacha).
- **Gidrosfera (okeanlar va dengizlar)** - butunlay hayot bilan to'la.
- **Litosferaning yuqori qismi** (tuproq osti salkam 3 km gacha).

### Insoniyat yaratgan muammolar:
Hozirda inson aqli kuchayib biosferadan **Noosfera** (ongli hayot muhiti) darajasiga o'tilmoqda. Ammo bizning noto'g'ri faoliyatimiz tabiatga ulkan ziyon qilmoqda:
1. **Global isish (Issiqxona effekti)**: Zavodlar tutuni havodagi issiq gazlarni tutib qolib, yer haroratini ko'tarmoqda, muzliklar erimoqda.
2. **Ozon darchasi**: Aerozollar havoga tarqalib, osmondagi bizni saraton qiluvchi ultrabinafsha nurlardan asrovchi ozon qatlamini yemirmoqda.
3. **Orol dengizi fojiasi**: O'zbekistonimizdagi eng katta daryolarni sug'orishga noto'g'ri ishlatish oqibatida ulkan dengiz qurib qoldi, yerlar tuzlandi va iqlim o'zgardi.

Shuning uchun biologiyani o'rganib, har birimiz bitta daraxt ekishimiz shart!`
  },
  {
    id: "10-5",
    classId: "10-11",
    title: "Antropogenez: Inson Evolutsiyasi",
    topic: "Evolutsiya",
    shortDesc: "Insoniyatning kelib chiqishi, uning shakllanish bosqichlari hamda biologik va ijtimoiy evolutsiya omillari.",
    difficulty: "Qiyin",
    diagramType: "dna",
    analogies: [
      "Mehnat va so'zlashuv - mitti maymunsifat ibtidoiy odamni haqiqiy aqlli koinot egasiga aylantirgan super kuchdir (Ijtimoiy omil)."
    ],
    keyTerms: [
      { term: "Antropogenez", meaning: "Insonning biologik tur sifatida vujudga kelishi va tarixiy shakllanish jarayoni." },
      { term: "Avstralopitek", meaning: "Odam evolutsiyasining eng birinchi bosqichi bo'lib, ikki oyog'ida tik yura boshlagan qadimgi odamsifat maymunlar." },
      { term: "Homo Sapiens (Aqlli odam)", meaning: "Insoniyat rivojlanishining eng oliy va yakuniy zamonaviy shakli." }
    ],
    content: `Biz yer yuzidagi eng yuksak jonzotmiz. Xo'sh, biologik tomondan inson qanday qilib yaralgan? Biz quruqlikda yashaydigan primat hayvonlar bilan qandoshmiz, buni – **ANTROPOGENEZ** bobi tushuntiradi.

### Inson evolutsiyasining xronologik zinapoyasi:

1. **Avstralopiteklar**: Bundan 4-5 million yil avval Afrikada yashagan, daraxtdan yerga tushib ikki oyoqlab yurishni boshlagan maymun-odamlar.
2. **Mohir odam (Homo habilis)**: Birinchi marta qo'liga tosh va kiyik suyagini olib, uni topshirish va oddiy qurol sifatida yo'nib ishlashni kashf qilgan.
3. **Tik yuruvchi odam (Homo erectus - Pitekantrop va Sinantrop)**: Olovdan foydalanishni boshlagan va ibtidoiy dasta-to'da bo'lib qishloqlarda g'orlarda yashagan.
4. **Neandertal odamlari**: Arxeologik qazilma bo'lib, ular sovuq asrlarda kiyim kiygan, murakkab qurollar yasagan va o'z yaqinlarini ko'mish odatitni shakllantirgan.
5. **Kromanyon odami (Homo sapiens - Aqlli odam)**: San'at (g'or rasmlari), madaniyat va o'zaro chiroyli so'zlashuvga ega bo'lgan ilk to'liq inson.

### Insonni yaratgan ikki buyuk kuch:
- **Biologik omillar**: Nasldan naslga o'tish (DNT), mutatsiyalar va tabiiy tanlanish. Bu tanamiz duralishini yaratdi.
- **Ijtimoiy omillar**: **Mehnat**, **So'zlashuv (Nutq)** va **Sotsium (Jamoa)**. Charles Darwin hamda Friedrich Engels yozganidek: 'Mehnat insonni inson qildi!'`
  }
];






const SUBJECTS_LIST = [
  {
    id: 'biologiya',
    name: 'Biologiya',
    shortDesc: 'Botanika, Zoologiya, Odam anatomiyasi, Sitologiya, Genetika va Evolutsiya',
    iconName: 'Dna',
    color: 'from-emerald-700 to-teal-800',
    bgLight: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    borderColor: 'hover:border-emerald-500',
    suggestedTopics: ['Botanika', 'Zoologiya', 'Odam anatomiyasi', 'Sitologiya', 'Genetika', 'Umumiy Biologiya', 'Fotosintez va nafas olish', 'Evolutsion nazariya'],
    grades: ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-11-sinf', 'Abituriyent']
  },
  {
    id: 'kimyo',
    name: 'Kimyo',
    shortDesc: 'Mendeleyev davriy qonuni, Anorganik va Organik kimyo, Reaksiyalar',
    iconName: 'FlaskConical',
    color: 'from-cyan-700 to-blue-800',
    bgLight: 'bg-cyan-50 text-cyan-800 border-cyan-200',
    borderColor: 'hover:border-cyan-500',
    suggestedTopics: ['Davriy jadval va elementlar', 'Anorganik moddalar sinflari', 'Eritmalar va konsentratsiya', 'Organik kimyo (Uglevodorodlar)', 'Kimyoviy reaksiyalar tezligi', 'Elektrolitik dissotsilanish'],
    grades: ['7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf', 'Abituriyent']
  },
  {
    id: 'fizika',
    name: 'Fizika',
    shortDesc: 'Mexanika, Dinamika, Termodinamika, Elektr va Optika',
    iconName: 'Zap',
    color: 'from-amber-600 to-orange-700',
    bgLight: 'bg-amber-50 text-amber-800 border-amber-200',
    borderColor: 'hover:border-amber-500',
    suggestedTopics: ['Nyuton qonunlari va Dinamika', 'Kinematika va to\'g\'ri chiziqli harakat', 'Molekulyar fizika va Issiqlik', 'Elektr toki va Om qonuni', 'Optika va yorug\'lik hodisalari', 'Atom va yadro fizikasi'],
    grades: ['6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf', 'Abituriyent']
  },
  {
    id: 'matematika',
    name: 'Matematika & Geometriya',
    shortDesc: 'Algebraik ifodalar, Tenglamalar, Funksiyalar va Geometrik figuralar',
    iconName: 'Calculator',
    color: 'from-indigo-700 to-violet-800',
    bgLight: 'bg-indigo-50 text-indigo-800 border-indigo-200',
    borderColor: 'hover:border-indigo-500',
    suggestedTopics: ['Kvadrat tenglamalar va Viyet teoremasi', 'Funksiyalar va ularning grafiklari', 'Trigonometriya asoslari', 'Uchburchaklar va Pifagor teoremasi', 'Hosilalar va integrallar', 'Stereometriya (Fazoviy shakllar)'],
    grades: ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf', 'Abituriyent']
  },
  {
    id: 'tarix',
    name: 'Tarix',
    shortDesc: 'O\'zbekiston tarixi, Qadimgi dunyo, Amir Temur davlati va Jahon tarixi',
    iconName: 'Landmark',
    color: 'from-stone-700 to-stone-900',
    bgLight: 'bg-stone-100 text-stone-800 border-stone-300',
    borderColor: 'hover:border-stone-500',
    suggestedTopics: ['Qadimgi Baqtriya va So\'g\'diyona', 'Amir Temur va Temuriylar saltanati', 'Jadidchilik harakati', 'Mustaqil O\'zbekiston tarixi', 'Qadimgi Rim va Yunoniston', 'Birinchi va Ikkinchi Jahon urushlari'],
    grades: ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf', 'Abituriyent']
  },
  {
    id: 'ona-tili',
    name: 'Ona tili va Adabiyot',
    shortDesc: 'Fonetika, Morfologiya, Sintaksis, Imlo qoidalari va Mumtoz adabiyot',
    iconName: 'BookOpen',
    color: 'from-rose-700 to-pink-800',
    bgLight: 'bg-rose-50 text-rose-800 border-rose-200',
    borderColor: 'hover:border-rose-500',
    suggestedTopics: ['Morfologiya (So\'z turkumlari)', 'Sintaksis (Gap bo\'laklari)', 'Imlo qoidalari va punktuatsiya', 'Alisher Navoiy hayoti va ijodi', 'O\'zbek mumtoz adabiyoti', 'Zamonaviy o\'zbek adabiyoti'],
    grades: ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf', 'Abituriyent']
  },
  {
    id: 'ingliz-tili',
    name: 'Ingliz tili (English)',
    shortDesc: 'Grammar, Tenses, Vocabulary, Reading comprehension & CEFR',
    iconName: 'Languages',
    color: 'from-blue-700 to-indigo-800',
    bgLight: 'bg-blue-50 text-blue-800 border-blue-200',
    borderColor: 'hover:border-blue-500',
    suggestedTopics: ['English Verb Tenses', 'Prepositions & Phrasal Verbs', 'Conditional Sentences (If clauses)', 'Passive Voice', 'Vocabulary Builder (B1-B2)', 'Reading Comprehension'],
    grades: ['Boshlang\'ich (A1-A2)', 'O\'rta (B1-B2)', 'Ilg\'or (C1)', 'Maktab dasturi', 'IELTS / CEFR']
  },
  {
    id: 'geografiya',
    name: 'Geografiya',
    shortDesc: 'Tabiiy geografiya, Materiklar va okeanlar, O\'zbekiston iqtisodiyoti',
    iconName: 'Globe',
    color: 'from-teal-700 to-emerald-800',
    bgLight: 'bg-teal-50 text-teal-800 border-teal-200',
    borderColor: 'hover:border-teal-500',
    suggestedTopics: ['Yer sharining tuzilishi va litosfera', 'Atmosfera va iqlim zonalari', 'Materiklar va okeanlar tabiiyoti', 'O\'zbekiston tabiiy geografiyasi', 'Jahon mamlakatlari iqtisodiy geografiyasi'],
    grades: ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf']
  },
  {
    id: 'informatika',
    name: 'Informatika va IT',
    shortDesc: 'Algoritmlar, Dasturlash (Python), Kompyuter tuzilishi va Kiberxavfsizlik',
    iconName: 'Laptop',
    color: 'from-purple-700 to-violet-900',
    bgLight: 'bg-purple-50 text-purple-800 border-purple-200',
    borderColor: 'hover:border-purple-500',
    suggestedTopics: ['Algoritmlar nazariyasi va blok-sxemalar', 'Python dasturlash asoslari', 'Kompyuter apparat ta\'minoti', 'Axborot xavfsizligi va viruslar', 'Ma\'lumotlar bazasi va SQL asoslari', 'Internet va tarmoq texnologiyalari'],
    grades: ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf', 'IT kurs']
  }
];

// Curated starter tests for each subject
const INITIAL_PRESET_TESTS = [
  {
    id: 'preset-kimyo-1',
    subject: 'Kimyo',
    title: 'Mendeleyev davriy qonuni va atom tuzilishi',
    topic: 'Davriy jadval va elementlar',
    difficulty: 'O\'rtacha',
    classGrade: '8-sinf',
    createdAt: 1700000000000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-k1',
        question: "Mendeleyev davriy sistemasida tartib raqami (atom raqami) nimani bildiradi?",
        options: ["Atomdagi protonlar yoki elektronlar sonini", "Atomdagi neytronlar sonini", "Atomning nisbiy atom massasini", "Valent elektronlar sonini"],
        answerIndex: 0,
        explanation: "Elementning tartib raqami yadro zaryadiga, ya'ni yadrodagi protonlar soniga va betaraf atomdagi elektronlar soniga teng."
      },
      {
        id: 'q-k2',
        question: "Suv molekulasi (H2O) tarkibida vodorod va kislorodning valentligi qanday?",
        options: ["H - I, O - II", "H - II, O - I", "H - I, O - I", "H - II, O - II"],
        answerIndex: 0,
        explanation: "Suv molekulasida vodorod bir valentli (I), kislorod esa ikki valentli (II) bo'ladi."
      },
      {
        id: 'q-k3',
        question: "Qaysi gaz havoning asosiy qismini (taxminan 78%) tashkil qiladi?",
        options: ["Kislorod (O2)", "Azot (N2)", "Karbonat angidrid (CO2)", "Argon (Ar)"],
        answerIndex: 1,
        explanation: "Yer atmosferasidagi havoning hajmiy jihatdan taxminan 78 foizini azot gazi tashkil qiladi."
      },
      {
        id: 'q-k4',
        question: "Lakmus qog'ozi kislotali muhitda qanday rangga kiradi?",
        options: ["Ko'k", "Qizil", "Sariq", "Binafsha"],
        answerIndex: 1,
        explanation: "Kislotali eritmada indikator lakmus o'z rangini qizil rangga o'zgartiradi (ishqoriy muhitda esa ko'k rangga kiradi)."
      }
    ]
  },
  {
    id: 'preset-fizika-1',
    subject: 'Fizika',
    title: 'Klassik mexanika va Nyuton qonunlari',
    topic: 'Nyuton qonunlari va Dinamika',
    difficulty: 'O\'rtacha',
    classGrade: '7-9 sinf',
    createdAt: 1700000001000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-f1',
        question: "Inersiya hodisasining mohiyati nimadan iborat?",
        options: ["Jismning o'z tezligini tashqi kuch ta'sir qilmaguncha saqlash xossasi", "Jismning doim to'xtashga intilishi", "Gravitatsiya ta'sirida tezlashishi", "Og'irlik kuchining yo'qolishi"],
        answerIndex: 0,
        explanation: "Inersiya - bu jismga boshqa jismlar ta'sir etmaganda o'zining tinch holatini yoki to'g'ri chiziqli tekis harakatini saqlash hodisasi (Nyutonning 1-qonuni)."
      },
      {
        id: 'q-f2',
        question: "SI xalqaro birliklar sistemasida kuch birligi nima?",
        options: ["Joul (J)", "Paskal (Pa)", "Nyuton (N)", "Vatt (W)"],
        answerIndex: 2,
        explanation: "Kuchning o'lchov birligi mashhur ingliz olimi Isaak Nyuton sharafiga Nyuton (N) deb nomlangan. 1 N = 1 kg*m/s^2."
      },
      {
        id: 'q-f3',
        question: "Yer yuzidagi erkin tushish tezlanishi (g) ning o'rtacha qiymati qancha?",
        options: ["9.8 m/s^2", "5.4 m/s^2", "12.2 m/s^2", "300 000 m/s"],
        answerIndex: 0,
        explanation: "Yer sathida erkin tushish tezlanishi o'rtacha g ≈ 9.8 m/s^2 (masalalar yechishda odatda 10 m/s^2 deb yaxlitlanadi)."
      },
      {
        id: 'q-f4',
        question: "Termodinamikada absolyut nol harorat Selsiy shkalasi bo'yicha necha gradusga teng?",
        options: ["-273.15 °C", "-100 °C", "0 °C", "-373.15 °C"],
        answerIndex: 0,
        explanation: "Absolyut nol harorat (0 Kelvin) atom va molekulalarning issiqlik harakati to'xtaydigan eng past harorat bo'lib, -273.15 °C ga to'g'ri keladi."
      }
    ]
  },
  {
    id: 'preset-matematika-1',
    subject: 'Matematika & Geometriya',
    title: 'Algebraik qoidalar va tenglamalar',
    topic: 'Kvadrat tenglamalar va Viyet teoremasi',
    difficulty: 'O\'rtacha',
    classGrade: '8-sinf',
    createdAt: 1700000002000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-m1',
        question: "x^2 - 5x + 6 = 0 kvadrat tenglamaning ildizlarini aniqlang:",
        options: ["x1 = 2, x2 = 3", "x1 = -2, x2 = -3", "x1 = 1, x2 = 6", "x1 = -1, x2 = 5"],
        answerIndex: 0,
        explanation: "Viyet teoremasiga ko'ra: x1 + x2 = 5 va x1 * x2 = 6. Bu shartni x1 = 2 va x2 = 3 sonlari qanoatlantiradi."
      },
      {
        id: 'q-m2',
        question: "To'g'ri burchakli uchburchakning katetlari 3 sm va 4 sm bo'lsa, gipotenuzasi necha sm?",
        options: ["5 sm", "6 sm", "7 sm", "25 sm"],
        answerIndex: 0,
        explanation: "Pifagor teoremasiga ko'ra: c^2 = a^2 + b^2 = 3^2 + 4^2 = 9 + 16 = 25. Demak, c = 5 sm."
      },
      {
        id: 'q-m3',
        question: "2 ning 8-darajasi (2^8) qanchaga teng?",
        options: ["128", "256", "512", "64"],
        answerIndex: 1,
        explanation: "2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 = 256."
      },
      {
        id: 'q-m4',
        question: "Doiraning yuzini hisoblash formulasi qaysi?",
        options: ["S = π * r^2", "S = 2 * π * r", "S = 4/3 * π * r^3", "S = a * b"],
        answerIndex: 0,
        explanation: "Doira yuzi radiusi kvadratining pi (π ≈ 3.14) soniga ko'paytmasiga teng: S = π * r^2."
      }
    ]
  },
  {
    id: 'preset-tarix-1',
    subject: 'Tarix',
    title: 'O\'zbekiston va Jahon tarixi sinovi',
    topic: 'Amir Temur va Temuriylar saltanati',
    difficulty: 'O\'rtacha',
    classGrade: '7-sinf',
    createdAt: 1700000003000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-t1',
        question: "Amir Temur davlatining poytaxti qaysi shahar bo'lgan?",
        options: ["Samarqand", "Buxoro", "Shahrisabz", "Toshkent"],
        answerIndex: 0,
        explanation: "Sohibqiron Amir Temur Samarqand shahrini o'z saltanatining poytaxti etib belgilagan va uni dunyoning eng go'zal shahriga aylantirgan."
      },
      {
        id: 'q-t2',
        question: "Mirzo Ulug'bek tomonidan Samarqandda qurilgan mashhur rasadxona qaysi fanni rivojlantirishga xizmat qilgan?",
        options: ["Astronomiya va Matematika", "Tibbiyot", "Geologiya", "Adabiyot"],
        answerIndex: 0,
        explanation: "Ulug'bek rasadxonasida yulduzlar harakati o'rganilgan va 1018 ta yulduzning jadvali tuzilgan mashhur 'Ziji jadidi Ko'ragoniy' asari yaratilgan."
      },
      {
        id: 'q-t3',
        question: "Qadimgi Misr piramidalaridan eng kattasi qaysi fir'avnga tegishli?",
        options: ["Xeops (Xufu)", "Xafra", "Tutanxamon", "Ramses II"],
        answerIndex: 0,
        explanation: "Giza maydonidagi eng buyuk piramida miloddan avvalgi XXVI asrda fir'avn Xeops (Xufu) uchun qurilgan."
      }
    ]
  },
  {
    id: 'preset-ona-tili-1',
    subject: 'Ona tili va Adabiyot',
    title: 'O\'zbek tili grammatikasi va adabiyot',
    topic: 'Morfologiya (So\'z turkumlari)',
    difficulty: 'O\'rtacha',
    classGrade: '5-9 sinf',
    createdAt: 1700000004000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-ot1',
        question: "Qaysi qatordagi barcha so'zlar sifat so'z turkumiga tegishli?",
        options: ["Chiroyli, aqlli, shirin", "Kitob, qalam, daftar", "Yugurdi, o'qidi, yozdi", "Tez, sekin, ko'p"],
        answerIndex: 0,
        explanation: "Belgi, xususiyat va xislatni bildirib 'qanday?', 'qanaqa?' so'rog'iga javob bo'lgan 'chiroyli', 'aqlli', 'shirin' so'zlari sifatdir."
      },
      {
        id: 'q-ot2',
        question: "Alisher Navoiy qaysi asarlar to'plami bilan turkiy tilda 'Xamsa' yaratgan birinchi ijodkor hisoblanadi?",
        options: ["Xamsa (Besh doston)", "Xazoyinul maoniy", "Lisonut-tayr", "Mahbubul qulub"],
        answerIndex: 0,
        explanation: "Buyuk mutafakkir Alisher Navoiy 1483-1485 yillarda 5 ta dostondan iborat o'lmas 'Xamsa' asarini turkiy tilda yaratgan."
      },
      {
        id: 'q-ot3',
        question: "Gapda harakatni bajaruvchi bosh bo'lak nima deb ataladi?",
        options: ["Ega", "Kesim", "To'ldiruvchi", "Hol"],
        answerIndex: 0,
        explanation: "Ega bosh kelishikdagi (kim? nima? qayer?) so'roqlariga javob bo'lib, gapning markaziy grammatik asosi hisoblanadi."
      }
    ]
  },
  {
    id: 'preset-ingliz-tili-1',
    subject: 'Ingliz tili (English)',
    title: 'English Grammar & Vocabulary Fundamentals',
    topic: 'English Verb Tenses',
    difficulty: 'O\'rtacha',
    classGrade: 'B1 Daraja',
    createdAt: 1700000005000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-en1',
        question: "Select the correct sentence:",
        options: ["She doesn't like apples.", "She don't likes apples.", "She not like apples.", "She isn't like apples."],
        answerIndex: 0,
        explanation: "In Present Simple, third-person singular (he, she, it) uses 'does not' + base verb: 'She doesn't like apples.'"
      },
      {
        id: 'q-en2',
        question: "I have been living in Tashkent ___ 2018.",
        options: ["since", "for", "in", "from"],
        answerIndex: 0,
        explanation: "We use 'since' to refer to a specific starting point in time in the past with Present Perfect Continuous."
      },
      {
        id: 'q-en3',
        question: "What is the synonym of the word 'rapid'?",
        options: ["fast", "slow", "heavy", "quiet"],
        answerIndex: 0,
        explanation: "'Rapid' means happening in a short time or at a fast pace (synonym: quick, fast)."
      }
    ]
  },
  {
    id: 'preset-informatika-1',
    subject: 'Informatika va IT',
    title: 'Dasturlash va kompyuter savodxonligi',
    topic: 'Python dasturlash asoslari',
    difficulty: 'O\'rtacha',
    classGrade: '7-11 sinf',
    createdAt: 1700000006000,
    isUserCreated: false,
    questions: [
      {
        id: 'q-inf1',
        question: "Python tilida o'zgaruvchi turini aniqlash uchun qaysi funksiya ishlatiladi?",
        options: ["type()", "typeof()", "kind()", "class()"],
        answerIndex: 0,
        explanation: "Python tilida istalgan obyekt yoki o'zgaruvchining ma'lumot turini (int, str, list va h.k.) bilish uchun type() funksiyasi qo'llaniladi."
      },
      {
        id: 'q-inf2',
        question: "Kompyuterning asosiy 'miyasi' hisoblangan qurilma nima?",
        options: ["Markaziy protsessor (CPU)", "Qattiq disk (HDD/SSD)", "Tezkor xotira (RAM)", "Videokarta (GPU)"],
        answerIndex: 0,
        explanation: "CPU (Central Processing Unit) barcha hisoblash amallari va dasturiy buyruqlarni bajaruvchi asosiy hisoblash organi hisoblanadi."
      },
      {
        id: 'q-inf3',
        question: "1 Megabayt (MB) necha Kilobaytga (KB) teng?",
        options: ["1024 KB", "1000 KB", "512 KB", "2048 KB"],
        answerIndex: 0,
        explanation: "Ikkilik sanoq sistemasiga asosan 1 MB = 1024 KB, 1 KB = 1024 Bayt bo'ladi."
      }
    ]
  }
];

// Helper to load all quizzes (built-in presets + custom user created)
export function getSavedSubjectQuizzes() {
  try {
    const raw = localStorage.getItem('user_custom_quizzes_v2');
    if (!raw) return INITIAL_PRESET_TESTS;
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return INITIAL_PRESET_TESTS;
    return parsed;
  } catch (e) {
    console.error('Failed to parse saved subject quizzes', e);
    return INITIAL_PRESET_TESTS;
  }
}

// Helper to save a new quiz
export function saveCustomQuiz(newQuiz: CustomSubjectQuiz) {
  const current = getSavedSubjectQuizzes();
  // prepend new quiz so it shows on top
  const updated = [newQuiz, ...current.filter(q => q.id !== newQuiz.id)];
  localStorage.setItem('user_custom_quizzes_v2', JSON.stringify(updated));
  return updated;
}

// Helper to remove a quiz
export function deleteCustomQuiz(quizId: string) {
  const current = getSavedSubjectQuizzes();
  const updated = current.filter(q => q.id !== quizId);
  localStorage.setItem('user_custom_quizzes_v2', JSON.stringify(updated));
  return updated;
}


window.APP_DATA = { CLASSES_LIST, SYLLABUS, SUBJECTS_LIST, INITIAL_PRESET_TESTS };
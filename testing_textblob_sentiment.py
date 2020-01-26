from nltk.tokenize import word_tokenize
from textblob import TextBlob
from translate import Translator

# pos_count = 0
# pos_correct = 0
# with open("positivas.txt", "r") as f:
#     for line in f.read().split('\n'):
#         analysis = TextBlob(line)
#         # print(line)
#         try:
#             eng = analysis.translate(to='en')
#             if eng.sentiment.polarity > 0:
#                 pos_correct += 1
#             pos_count += 1
#         except:
#             # Mostramos este mensaje en caso de que se presente algún problema
#             print("El elemento no está presente")
# neg_count = 0
# neg_correct = 0
# with open("negativas.txt", "r") as f:
#     for line in f.read().split('\n'):
#         analysis = TextBlob(line)
#         # print(line)
#         try:
#             eng = analysis.translate(to='en')
#             if eng.sentiment.polarity <= 0:
#                 neg_correct += 1
#             neg_count += 1
#         except:
#             print('el elemento no esta presente')
# print("Precisión positiva = {}% via {} ejemplos".format(pos_correct / pos_count * 100.0, pos_count))
# print("Precisión negativa = {}% via {} ejemplos".format(neg_correct / neg_count * 100.0, neg_count))

respuestas = "no _s_ ale 24918294 ale@gmail.com _s_ derecho derecho _n_ _s_ sofía costadinoff _s_ 33791036 " \
             "sofiacnoff@gmail.com franco budini _s_ _s_ _s_ 39122227 campana, bueno aires alejandro fernández " \
             "eugenia cruz francobudini1@gmail.com diseño gráfico 36493528 32289656 _s_ no eugeniacruz.ros@gmail.com " \
             "escuela superior de diseño alejandrofernandez440@gmail.com _s_ diseño gráfico _s_ si escuela de arte " \
             "ricardo carpani escuela provincial de artes visuales _s_ fabián romero _s_ diseño gráfico técnico en " \
             "diseño gráfico y comunicación visual 33735104 no dg.fabianromero@gmail.com oriana magalí di yorio _s_ " \
             "37675615 itec 3 misiones oriana.diyorio@gmail.com _s_ diseño gráfico digital _s_ celeste peñalba son " \
             "geniales!!! si 44231725 _s_ celestepenalba@hotmail.com _s_ selene paulin escuela de arte n1 ricardo " \
             "carpani - campana 39366186 _s_ juan martín avila cerdá sele-paulin@hotmail.com diseño gráfico " \
             "secundario en la escuela madre cabrini 40115674 _s_ no juanmartin-avila@hotmail.com en fadu unl santa " \
             "fe _s_ licenciatura en diseño de la comunicación visual facultad de arquitectura, diseño y urbanismo (" \
             "fadu - unl) no comunicación visual no _s_ federico valle 35704302 federicovalle91@gmail.com _s_ la " \
             "vigil diseño gráfico y comunicación visual sii _s_ _s_ luciano zarza 41822849 zarzaluciano9@gmail.com " \
             "_s_ instituto tecnológico numero 3,  posadas misiones tecnicatura superior en diseño gráfico digital no " \
             "_s_ mi nombre es cecilia perez 41206107 cecip998@gmail.com _s_ _s_ juan martín birrittella 37159256 " \
             "dg.jmartinb@gmail.com no si _s_ miguela gamero 37450902 miguelagamero@hotmail.com nono si _s_ matías " \
             "rinaldi 36742402 matiasgrinaldi@hotmail.com _s_ escuela de artes visuales vigil díseño gráfico y " \
             "comunicación visual no _s_ fabián romero 33735104 dg.fabianromero@gmail.com _s_ itec3 diseño gráfico si " \
             "_s_ fabián romero 33735104 dg.fabianromero@gmail.com _s_ itec3 diseño gráfico digital si _s_ eugenia " \
             "buero 38723193 euge.buero@hotmail.com _s_ uai diseño gráfico si _s_ leandro lamolla _s_ ignacio " \
             "sternari 31960107 sternaridroid@gmail.com _s_ escuela superior de diseño diseño gráfico no _s_ nahir " \
             "deschamps maguid 43380401 nahirmaguid@gmail.com _s_ esd escuela superior de diseño diseño gráfico si " \
             "_s_ maría magdalena estrada 38897503 _s_ ma.magdalenaestrada@gmail.com yanet vignatti _s_ 38288787 " \
             "yanevignatti@gmail.com universidad nacional del litoral _s_ lic. en diseño de la comunicación " \
             "universidad nacional del litoral no licenciatura en diseño de la comunicación visual no no _s_ eliana " \
             "martin 39049739 elimartint@gmail.com _s_ en la facultad  de arquitectura, planeamiento y diseño (unr) " \
             "licenciatura en comunicación visual no _s_ juan martín birrittella 37159256 dg.jmartinb@gmail.com nop " \
             "si! _s_ _s_ juan martín birrittella 37159256 catalina sol martínez prieto dg.jmartinb@gmail.com " \
             "41161354 nop si! cata.martinez.prieto@gmail.com _s_ me recibí este año florencia fernández _s_ si " \
             "40645891 santiago de cleene 42609167 sdcleene00@gmail.com _s_ _s_ instituto superior de comunicación " \
             "visual _s_ constanza bianchi diseño grafico e ilustración maría azul napolitano 42325294 no 39950457 " \
             "constanza.bianchi.1027@gmail.com _s_ azulnapolitano2@gmail.com uai lic. en diseño gráfico _s_ siiii!!!! " \
             "_s_ _s_ sebastián fernando grillo lloret priscila lizaso instituto súper isa cepec 28942711 " \
             "grilo.contacto@gmail.com 42129311 _s_ tecnicatura en diseño integral no escuela de arte ricardo " \
             "carpani, campana buenos aires diseño gráfico _s_ _s_ camila gambini 44025245 " \
             "camilagambini6toatm@gmail.com agustín encina florfdez17@gmail.com 40449968 no _s_ " \
             "agustin98encina@gmail.com _n_ fadu unl lizaso.nahir@yahoo.com _s_ uai _s_ _s_ licenciatura en diseño de " \
             "la comunicación visual no lic. diseño gráfico victor hugo barrios martin alvarez nono 40858708 29455764 " \
             "chucucan@gmail.com no _s_ _s_ neural@hotmail.es _s_ luciano zarza nombre: constanza apellidos: yezzi " \
             "morales no escuela superior de diseño _s_ 41822849 41655303 si ayelen arguello zarzaluciano9 @ " \
             "gmail.com constanzaym @ hotmail.com que? jaja _s_ _s_ diseño gráfico en la escuela superior de diseño(" \
             "esd) no instituto tecnológico numero 3 posadas misiones diseño gráfico _s_ tecnicatura superior en " \
             "diseño gráfico digital no _s_ lucia kondratavicius fermo no 38901219 lkf.dg95 @ gmail.com escuela " \
             "superior de diseño _s_ _s_ en la unr _s_ luna a.moran licenciatura en comunicacion visual ernesto david " \
             "sánchez 40.057 .586 sisi 34889447 ernestodavidsanchez @ gmail.com _s_ lun9704 @ gmail.com diseño de " \
             "interiores! unr - facultad de ciencia política y relaciones internacionales no licenciatura en " \
             "comunicación social _s_ _s_ en uai valeria morales guerra _s_ no lic.en diseño gráfico 95025894 matías " \
             "bonfiglio si valestramesi01 @ gmail.com 42.325 .312 _s_ universidad abierta interamericana " \
             "matiasbonfiglio1722000 @ gmail.com _s_ licenciatura en diseño gráfico rosario sí diseño gráfico _s_ por " \
             "publicidad renzo polichiso 37154344 renzo.polichiso @ hotmail.com _s_ laburo si sergio uliambre " \
             "29681073 sergiouliambre @ hotmail.com _s_ escuela de arte ricardo carpani, ciudad de campana diseño " \
             "gráfico, estoy en el último año no _s_ nicolás molina 40578117 nicomolina202 @ gmail.com _s_ escuela de " \
             "arte ricardo carpani _s_ diseño gráfico maría emilia olmedo no 38338473 _s_ lucia ferraris emiliadigraf " \
             "@ gmail.com 39455095 no estudio ahora _s_ luciaferraris24 @ gmail.com no jonathan ledesma _s_ _s_ " \
             "36140983 universidad nacional del litoral anabella elias jonhi1404 @ gmail.com licenciatura en diseño " \
             "de la comunicación visual 38509034 no ani.elias09 @ gmail.com ok _s_ _s_ complejo belgrano macarena " \
             "fernández diseño digital 38427128 si cinthiamacarena @ outlook.com _s_ escuela de arte ricardo carpani, " \
             "campana, bs as _n_ diseño gráfico si _s_ _s_ _s_ _s_ _s_ maximo valente luana dapino florencia müller " \
             "miguela gamero 39505011 40823570 valentina lanari 39.950 .458 37450902 luanadapino @ gmail.com " \
             "flor.muller @ outlook.com miguelagamero @ hotmail.com _s_ 43285297 _s_ ya me gradué, pero nunca vienen " \
             "mal libros nuevos ort belgrano valentinavlanari @ gmail.com en la escuela superior de diseño sisi " \
             "diseño gráfico _s_ diseño gráfico no escuela superior de diseño de rosario _s_ maximorvalente @ " \
             "gmail.com muy poco, de haberlo visto alguna vez en redes sociales _s_ lucrecia olivé prieto diseño " \
             "gráfico sí 43167686 lucreciaoliveprieto @ gmail.com _n_ _n_ _s_ si adios si okey saludo quiero maestría " \
             "si saludo si okey adios maestría si dale si okey saludo maestría si dale si si dale si okey curso " \
             "maestría si especialización si metele saludo maestría saludo terminamos terminamos saludo hola! ㋡  mi " \
             "nombre es pad y soy el asistente virtual de funpei para la carrera del ciclo de licenciatura en gestión " \
             "de recursos humanos. te proponemos responder una pequeña encuesta de 4 preguntas. - envía si para " \
             "continuar. - envía terminar para finalizar la encuesta.perfecto! ⓵  ¿cuál es para vos, el seminario del " \
             "ciclo de licenciatura en gestión de rr.hh.que otorga mayores herramientas para tu desempeño laboral y " \
             "cuál es el que no otorga nada? ok, gracias saludo saludo terminamos terminamos saludo saludo si saludo " \
             "si terminamos si si perfecto okey si si terminamos terminamos si si si metele adios maestría terminamos " \
             "terminamos si si ok ok si ok dale si no _s_ ale 24918294 ale @ gmail.com _s_ derecho derecho _n_ _s_ " \
             "sofía costadinoff _s_ 33791036 sofiacnoff @ gmail.com franco budini _s_ _s_ _s_ 39122227 campana, " \
             "bueno aires alejandro fernández eugenia cruz francobudini1 @ gmail.com diseño gráfico 36493528 32289656 " \
             "_s_ no eugeniacruz.ros @ gmail.com escuela superior de diseño alejandrofernandez440 @ gmail.com _s_ " \
             "diseño gráfico _s_ si escuela de arte ricardo carpani escuela provincial de artes visuales _s_ fabián " \
             "romero _s_ diseño gráfico técnico en diseño gráfico y comunicación visual 33735104 no dg.fabianromero @ " \
             "gmail.com oriana magalí di yorio _s_ 37675615 itec 3 misiones oriana.diyorio @ gmail.com _s_ diseño " \
             "gráfico digital _s_ celeste peñalba son geniales!!! si 44231725 _s_ celestepenalba @ hotmail.com _s_ " \
             "selene paulin escuela de arte n1 ricardo carpani - campana 39366186 _s_ juan martín avila cerdá sele - " \
             "paulin @ hotmail.com diseño gráfico secundario en la escuela madre cabrini 40115674 _s_ no juanmartin - " \
             "avila @ hotmail.com en fadu unl santa fe _s_ licenciatura en diseño de la comunicación visual facultad " \
             "de arquitectura, diseño y urbanismo(fadu - unl) no comunicación visual no _s_ federico valle 35704302 " \
             "federicovalle91 @ gmail.com _s_ la vigil diseño gráfico y comunicación visual sii _s_ _s_ luciano zarza " \
             "41822849 zarzaluciano9 @ gmail.com _s_ instituto tecnológico numero 3, posadas misiones tecnicatura " \
             "superior en diseño gráfico digital no _s_ mi nombre es cecilia perez 41206107 cecip998 @ gmail.com _s_ " \
             "_s_ juan martín birrittella 37159256 dg.jmartinb @ gmail.com no si _s_ miguela gamero 37450902 " \
             "miguelagamero @ hotmail.com nono si _s_ matías rinaldi 36742402 matiasgrinaldi @ hotmail.com _s_ " \
             "escuela de artes visuales vigil díseño gráfico y comunicación visual no _s_ fabián romero 33735104 " \
             "dg.fabianromero @ gmail.com _s_ itec3 diseño gráfico si _s_ fabián romero 33735104 dg.fabianromero @ " \
             "gmail.com _s_ itec3 diseño gráfico digital si _s_ eugenia buero 38723193 euge.buero @ hotmail.com _s_ " \
             "uai diseño gráfico si _s_ leandro lamolla _s_ ignacio sternari 31960107 sternaridroid @ gmail.com _s_ " \
             "escuela superior de diseño diseño gráfico no _s_ nahir deschamps maguid 43380401 nahirmaguid @ " \
             "gmail.com _s_ esd escuela superior de diseño diseño gráfico si _s_ maría magdalena estrada 38897503 _s_ " \
             "ma.magdalenaestrada @ gmail.com yanet vignatti _s_ 38288787 yanevignatti @ gmail.com universidad " \
             "nacional del litoral _s_ lic.en diseño de la comunicación universidad nacional del litoral no " \
             "licenciatura en diseño de la comunicación visual no no _s_ eliana martin 39049739 elimartint @ " \
             "gmail.com _s_ en la facultad de arquitectura, planeamiento y diseño(unr) licenciatura en comunicación " \
             "visual no _s_ juan martín birrittella 37159256 dg.jmartinb @ gmail.com nop si! _s_ _s_ juan martín " \
             "birrittella 37159256 catalina sol martínez prieto dg.jmartinb @ gmail.com 41161354 nop si! " \
             "cata.martinez.prieto @ gmail.com _s_ me recibí este año florencia fernández _s_ si 40645891 santiago de " \
             "cleene 42609167 sdcleene00 @ gmail.com _s_ _s_ instituto superior de comunicación visual _s_ constanza " \
             "bianchi diseño grafico e ilustración maría azul napolitano 42325294 no 39950457 constanza.bianchi .1027 " \
             "@ gmail.com _s_ azulnapolitano2 @ gmail.com uai lic.en diseño gráfico _s_ siiii!!!! _s_ _s_ sebastián " \
             "fernando grillo lloret priscila lizaso instituto súper isa cepec 28942711 grilo.contacto @ gmail.com " \
             "42129311 _s_ tecnicatura en diseño integral no escuela de arte ricardo carpani, campana buenos aires " \
             "diseño gráfico _s_ _s_ camila gambini 44025245 camilagambini6toatm @ gmail.com agustín encina " \
             "florfdez17 @ gmail.com 40449968 no _s_ agustin98encina @ gmail.com _n_ fadu unl lizaso.nahir @ " \
             "yahoo.com _s_ uai _s_ _s_ licenciatura en diseño de la comunicación visual no lic.diseño gráfico victor " \
             "hugo barrios martin alvarez nono 40858708 29455764 chucucan @ gmail.com no _s_ _s_ neural @ hotmail.es " \
             "_s_ luciano zarza nombre: constanza apellidos: yezzi morales no escuela superior de diseño _s_ 41822849 " \
             "41655303 si ayelen arguello zarzaluciano9 @ gmail.com constanzaym @ hotmail.com que? jaja _s_ _s_ " \
             "diseño gráfico en la escuela superior de diseño(esd) no instituto tecnológico numero 3 posadas misiones " \
             "diseño gráfico _s_ tecnicatura superior en diseño gráfico digital no _s_ lucia kondratavicius fermo no " \
             "38901219 lkf.dg95 @ gmail.com escuela superior de diseño _s_ _s_ en la unr _s_ luna a.moran " \
             "licenciatura en comunicacion visual ernesto david sánchez 40.057 .586 sisi 34889447 ernestodavidsanchez " \
             "@ gmail.com _s_ lun9704 @ gmail.com diseño de interiores! unr - facultad de ciencia política y " \
             "relaciones internacionales no licenciatura en comunicación social _s_ _s_ en uai valeria morales guerra " \
             "_s_ no lic.en diseño gráfico 95025894 matías bonfiglio si valestramesi01 @ gmail.com 42.325 .312 _s_ " \
             "universidad abierta interamericana matiasbonfiglio1722000 @ gmail.com _s_ licenciatura en diseño " \
             "gráfico rosario sí diseño gráfico _s_ por publicidad renzo polichiso 37154344 renzo.polichiso @ " \
             "hotmail.com _s_ laburo si sergio uliambre 29681073 sergiouliambre @ hotmail.com _s_ escuela de arte " \
             "ricardo carpani, ciudad de campana diseño gráfico, estoy en el último año no _s_ nicolás molina " \
             "40578117 nicomolina202 @ gmail.com _s_ escuela de arte ricardo carpani _s_ diseño gráfico maría emilia " \
             "olmedo no 38338473 _s_ lucia ferraris emiliadigraf @ gmail.com 39455095 no estudio ahora _s_ " \
             "luciaferraris24 @ gmail.com no jonathan ledesma _s_ _s_ 36140983 universidad nacional del litoral " \
             "anabella elias jonhi1404 @ gmail.com licenciatura en diseño de la comunicación visual 38509034 no " \
             "ani.elias09 @ gmail.com ok _s_ _s_ complejo belgrano macarena fernández diseño digital 38427128 si " \
             "cinthiamacarena @ outlook.com _s_ escuela de arte ricardo carpani, campana, bs as _n_ diseño gráfico si " \
             "_s_ _s_ _s_ _s_ _s_ maximo valente luana dapino florencia müller miguela gamero 39505011 40823570 " \
             "valentina lanari 39.950 .458 37450902 luanadapino @ gmail.com flor.muller @ outlook.com miguelagamero @ " \
             "hotmail.com _s_ 43285297 _s_ ya me gradué, pero nunca vienen mal libros nuevos ort belgrano " \
             "valentinavlanari @ gmail.com en la escuela superior de diseño sisi diseño gráfico _s_ diseño gráfico no " \
             "escuela superior de diseño de rosario _s_ maximorvalente @ gmail.com muy poco, de haberlo visto alguna " \
             "vez en redes sociales _s_ lucrecia olivé prieto diseño gráfico sí 43167686 lucreciaoliveprieto @ " \
             "gmail.com _n_ _n_ _s_ ¡Chau! "
stopwords = list(
    "de la que el en y a los del se las por un para con no una su al lo como más pero sus le ya o este sí porque esta "
    "entre cuando muy sin sobre también me hasta hay donde quien desde todo nos durante todos uno les ni contra otros "
    "ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto esa estos mucho quienes nada "
    "muchos cual poco ella estar estas algunas algo nosotros mi mis tú te ti tu tus ellas nosotras vosostros "
    "vosostras os mío mía míos mías tuyo tuya tuyos tuyas suyo suya suyos suyas nuestro nuestra nuestros nuestras "
    "vuestro vuestra vuestros vuestras esos esas estoy estás está estamos estáis están esté estés estemos estéis "
    "estén estaré estarás estará estaremos estaréis estarán estaría estarías estaríamos estaríais estarían estaba "
    "estabas estábamos estabais estaban estuve estuviste estuvo estuvimos estuvisteis estuvieron estuviera estuvieras "
    "estuviéramos estuvierais estuvieran estuviese estuvieses estuviésemos estuvieseis estuviesen estando estado "
    "estada estados estadas estad he has ha hemos habéis han haya hayas hayamos hayáis hayan habré habrás habrá "
    "habremos habréis habrán habría habrías habríamos habríais habrían había habías habíamos habíais habían hube "
    "hubiste hubo hubimos hubisteis hubieron hubiera hubieras hubiéramos hubierais hubieran hubiese hubieses "
    "hubiésemos hubieseis hubiesen habiendo habido habida habidos habidas soy eres es somos sois son sea seas seamos "
    "seáis sean seré serás será seremos seréis serán sería serías seríamos seríais serían era eras éramos erais eran "
    "fui fuiste fue fuimos fuisteis fueron fuera fueras fuéramos fuerais fueran fuese fueses fuésemos fueseis fuesen "
    "sintiendo sentido sentida sentidos sentidas siente sentid tengo tienes tiene tenemos tenéis tienen tenga tengas "
    "tengamos tengáis tengan tendré tendrás tendrá tendremos tendréis tendrán tendría tendrías tendríamos tendríais "
    "tendrían tenía tenías teníamos teníais tenían tuve tuviste tuvo tuvimos tuvisteis tuvieron tuviera tuvieras "
    "tuviéramos tuvierais tuvieran tuviese tuvieses tuviésemos tuvieseis tuviesen teniendo tenido tenida tenidos "
    "tenidas tened")
neg_count = 0
pos_count = 0
secret = '<your secret from Microsoft>'
translator = Translator(provider="microsoft", to_lang="en",secret_access_key=secret)

for x in word_tokenize(respuestas):
    if x not in stopwords:
        try:
            x = translator.translate(x)
            print(x)
            x = TextBlob(x)
            if x.sentiment.polarity <= 0:
                neg_count += 1
                print("Negativa:", x, "con polaridad de {}".format(round(x.sentiment.polarity, 2)))
            else:
                pos_count += 1
                print("************************")
                print("Positiva:", x, "con polaridad de {}".format(round(x.sentiment.polarity, 2)))
                print("************************")
        except Exception as e:
            print(str(e))
pos_ptg = round(((pos_count / len(word_tokenize(respuestas))) * 100), 2)
neg_ptg = round(((neg_count / len(word_tokenize(respuestas))) * 100), 2)
print("El porcentaje de palabras positivas es {}% y el de negativas es {}%".format(pos_ptg, neg_ptg))

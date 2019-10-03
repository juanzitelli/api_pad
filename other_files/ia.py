from textblob.classifiers import NaiveBayesClassifier


def intention(vtexto):
    # Let's create a FAQ for my stream

    zoes =                  ('puto de ',
                             'trolo de ', 'comilon de ', 'hijo de puta',
                             'hdp de', 'trolón de ', 'sorete de', 'chupame la pija', 'orto,estúpido', 'imbécil', 'destestable', 'nazi', 'te')

    aceptacion =             ('si por supuesto',
                              'ok',
                              'dale',
                              'puede ser',
                              'por supuesto',
                              'metele',
                              'quiero',
                              'yes',
                              'yeha',
                              'positivo'
                              'claro si')


    negacion =              ('no',
                             'negativo no quiero',
                             'ni loco',
                             'no quiero',
                             'de ninguna manera',
                             'no por esta vez')

    saludo_hola              = ('hola como',
                             'quiero preguntar',
                             'i want to',
                             'quiero saber mas',
                             'los contacto para',
                             'que tal', 'como les va','estimados')

    saludo_chau             = ('chau','adio','hasta luego','nos vemos','es todo')


    agradecimientos =       ('gracias por ', 'muchas gracias por ','regio me sirver', 'espectacular esto', 'impresionante esto', 'maravilloso', 'cool', 'espectacular'
                             ,'es lo que necesecitaba','necesitaba eso', 'perfecto', 'excelente ', 'brillante')


    i1 = [(x, 'zoes') for x in zoes]
    i2 = [(x, 'aceptacion') for x in aceptacion]
    i3 = [(x, 'negacion') for x in negacion]
    i4 = [(x, 'saludo_hola') for x in saludo_hola]
    i5 = [(x, 'saludo_chau') for x in saludo_chau]
    i6 = [(x, 'agradecimientos') for x in agradecimientos]



    # FIXME: find better way to flatten lists together
    training_set = []

    training_set.extend(i2)
    training_set.extend(i3)
    training_set.extend(i4)
    training_set.extend(i5)
    training_set.extend(i6)
    training_set.extend(i1)

    classifier = NaiveBayesClassifier(training_set)

    prob_dist = classifier.prob_classify(vtexto)



    if prob_dist.prob(prob_dist.max()) < 0.5:
        r= vtexto
    else:
        r= prob_dist.max()

    return r


print(intention('siiii'))


"""
print(intention('sip'))

print(intention('por supuesto'))

print(intention('ok'))

print(intention('dale'))

print(intention('claro'))

print("---")

print(intention('no'))

print(intention('ni loco'))

print(intention('ninguna manera'))

print(intention('no por esta vez'))



print("---")
print(intention('quiero preguntar'))
print(intention('hola como'))


print("---")
print(intention('pija'))
print(intention('trolo'))


print("---")
print(intention('gracias muy'))
print(intention('gracias'))
print(intention('realmente'))

print("---opciones ")
print(intention('a'))
print(intention('b'))
print(intention('horario'))

print(intention('1'))
print(intention('1212 1212'))
print(intention('3333'))

"""
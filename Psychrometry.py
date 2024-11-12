from Utils import mereni
from time import sleep

while True:
    event = input('Vitejte!\n Co chcete udělat?\n 1 - Měřit\n 2 - podat OZNUK (OZNámení UKončení studia)\n 3 - Být milionářem\n 4 - Ukončit aplikaci\n\n')

    match event:
        case "1":
            cas = input('Jak dlouhy usek chcete měřit\n')
            try:
                cas = int(cas)
            except ValueError:
                print('tak tohle neni cislo')
                continue
            nazev = input('jak se ma jmenovat vysledny soubor\n')
            try:
                mereni(cas, nazev)
            except Exception:
                print('No neco je blbe')
            continue
        case "2":
            jmeno = input('Zadejte VUT cislo\n')
            sleep(2)
            print(f'OZNUK na cislo {jmeno} byl odeslan')
            continue
        case "3":
            x = input("Kdo nebo co je Herpes:\n a) Přezdívka Vlastimila Harapese\n b) Německy Pan pes\n c) Odborný výraz pro hárajícího psa\n d) Pásový opar\n")
            match x:
                case 'd':
                    print('Vyborne!')
                    sleep(2)
                    continue
                case _:
                    print('Blbeeeeeee')
                    sleep(2)
                    continue
        case "4":
            print('Děkuji vám za pozornost a zatím nashle.')
            break

        case _:
            print('Zadejte validni vstup')

# Reflektion – ORM med SQLAlchemy

Skriv vad du förväntade dig före körningen och vad du faktiskt såg. Använd labbets testdata.

| Testfall | Förväntat resultat | Faktiskt resultat |
| --- | --- | --- |
| 1. Läs kund 1 och jämför med DBeaver | | |
| 1. Läs kund 999 | | |
| 2. Spara ett giltigt namn och läs igen | | |
| 2. Prova ett namn med bara mellanslag och läs igen | | |
| 3. Skapa och läs en egen testkund | | |
| 3. Prova samma test-ID igen | | |
| 3. Ta bort din testkund och läs igen | | |
| 4. Jämför före, efter flush och efter rollback | | |
| 5. Läs order för kund 1, 2, 3 och 999 | | |

## Rita och förklara

- Mina klasser, tabeller, nycklar och antal på varje sida
- Vad `order.customer_id` innehåller och vad `order.customer` ger
- Vilken regel `Customer.rename()` kontrollerar

## Förklara med egna ord

1. Vilket steg tog SQLAlchemy över från måndagens `find_customer()`?
2. Vilken observation visar att ett namn sparades? Vilken visar att rollback ångrade skrivningen?
3. Vad skiljer en befintlig kund utan order från en kund som saknas?

## I mitt kursprojekt

- Tabell, primärnyckel och två fält jag mappade
- Fungerande läsning, saknat ID och en kontrollerad skrivning
- Sambandet jag provade och var jag sparade min kod och körinstruktion

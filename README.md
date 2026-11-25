# Dag 8 – Från egen SQL till ORM

I måndags skrev du SQL själv, hämtade en rad med `fetchone()` och byggde ett `Customer`-objekt. I dag läser och ändrar du samma typ av kund med SQLAlchemy. Du kontrollerar vad som faktiskt sparas i MySQL och följer ett samband mellan en kund och kundens order.

Arbeta i ordning. Gör steg 1–5 först. I steg 6 ritar du sambandet och i steg 7 använder du samma arbetssätt i ditt kursprojekt. Skriv förväntat och faktiskt resultat i [REFLECTION.md](REFLECTION.md) medan du jobbar.

| Steg | Vad du gör | Fil |
| --- | --- | --- |
| 1 | Starta labbet och läs ett befintligt och ett saknat ID | [main.py](main.py), [models.py](models.py) |
| 2 | Byt en kunds namn och verifiera att det sparades | [tasks.py](tasks.py) |
| 3 | Skapa och ta bort en egen testkund | [tasks.py](tasks.py) |
| 4 | Följ en ändring som skickas till MySQL och sedan ångras | [rollback_demo.py](rollback_demo.py) |
| 5 | Läs kundens order med SQL och ORM | [relations.py](relations.py) |
| 6 | Rita och förklara sambandet | [REFLECTION.md](REFLECTION.md) |
| 7 | Prova ORM på en tabell och en relation i ditt projekt | Ditt kursprojekt |

## 1. Starta labbet och läs en kund

**Mål**  
Visa samma kund i DBeaver och med ORM. Jämför med vad som händer när kunden saknas.

1. Öppna lärarens mall på GitHub och välj **Use this template → Create a new repository**. Skapa ett eget privat repo. Kopiera klonlänken från ditt eget repos **Code**-meny, kör `git clone` följt av länken och öppna den klonade mappen i VS Code.
2. Öppna labbets [setup.sql](setup.sql) i DBeaver och kör hela skriptet mot din lokala MySQL-server. Det använder **`course_storage`** från måndagen. Kund 1 och 2 läggs till när de saknas. Ett namn du sparade i måndags finns kvar.
3. Skapa en virtuell miljö i det nya repot. I VS Code väljer du **Git Bash** i terminalens meny vid **+**. Kör kommandona från mappen där README och `requirements.txt` ligger.

   **Windows · Git Bash**

   ```bash
   python --version
   python -m venv .venv
   source .venv/Scripts/activate
   python -m pip install -r requirements.txt
   ```

   Använd Python 3.11 eller senare. `(.venv)` visar att labbets miljö är aktiv. När du öppnar en ny Git Bash-terminal aktiverar du miljön igen.

   <details>
   <summary>Om du använder PowerShell eller macOS/Linux</summary>

   **Windows · PowerShell**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

   Ersätt `python` i resten av labbets kommandon med `.\.venv\Scripts\python.exe`.

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

   </details>

4. Kör programmet med två olika ID:n. Använd samma MySQL-uppgifter som i DBeaver när terminalen frågar. Lösenordet visas inte medan du skriver.

   ```bash
   python main.py 1 --sql
   python main.py 999
   ```

5. Jämför med den här frågan i DBeaver. Byt sedan från `1` till `999` och kör igen.

   ```sql
   SELECT customer_id, name
   FROM course_storage.customers
   WHERE customer_id = 1;
   ```

6. Läs `read_customer()` i [main.py](main.py) och `Customer` i [models.py](models.py). Peka ut `__tablename__`, mappningen av `customer_id` och kontrollen av `None`.

**Varför?**  
`Engine` tillhandahåller databasanslutningar. `Session` hämtar och följer mappade objekt. Med `session.get(Customer, customer_id)` hämtar du med tabellens primärnyckel. SQLAlchemy bygger objektet från raden, vilket du gjorde själv efter `fetchone()` i måndags. Flaggan `--sql` visar SQL som programmet skickar till MySQL.

**Kontroll**  
ID 1 visar samma kund i programmet och i DBeaver. ID 999 ger `None` i Python och meddelandet **Kunden saknas** i terminalen. I DBeaver får du noll rader.

## 2. Byt namn och läs sedan på nytt

**Mål**  
Implementera `rename_customer()` i [tasks.py](tasks.py). Visa att ett giltigt namn sparas och att ett ogiltigt namn avvisas.

1. Öppna `rename_customer()` och ersätt den tillfälliga `NotImplementedError` med din kod. Använd en session och ett transaktionsblock kring uppslaget och namnbytet.

   ```python
   with Session(engine) as session, session.begin():
       ...  # Hämta kunden och gör namnbytet här.
   ```

2. Hämta kunden via `session.get(Customer, customer_id)`. Om kunden saknas, signalera det med `LookupError` och ett begripligt meddelande.
3. Anropa `customer.rename(new_name)`. Läs metoden i [models.py](models.py). Den tar bort omgivande mellanslag och avvisar tomma namn och namn längre än 100 tecken.
4. Prova kommandona nedan. Mellanslagen i det andra kommandot är avsiktliga.

   ```bash
   python tasks.py rename 1 "  Ada ORM  " --sql
   python tasks.py rename 1 "   "
   python tasks.py rename 999 "Okänd kund"
   python main.py 1
   ```

**Varför?**  
I måndags skrev du `UPDATE` och anropade `connection.commit()`. Nu följer sessionen ändringen av det mappade objektet och skickar uppdateringen. När transaktionsblocket avslutas normalt bekräftas ändringen. Ett undantag som lämnar blocket gör rollback. Terminalverktyget läser sedan kunden i en ny session.

**Kontroll**  
Efter första kommandot står `Ada ORM` utan omgivande mellanslag på raden **Ny läsning**. Tomt namn och saknat ID ger var sitt felmeddelande. Sista läsningen visar fortfarande `Ada ORM`.

## 3. Skapa och ta bort din egen testkund

**Mål**  
Implementera `create_customer()` och `delete_test_customer()` i [tasks.py](tasks.py).

1. Kontrollera att test-ID 9001 är ledigt med `python main.py 9001`. Om det finns en kund där, välj ett annat ledigt ID från 9000 och uppåt och byt i alla kommandon nedan.
2. För skapandet, avvisa ID under 9000 och validera namnet med `normalize_name()`. Använd ett transaktionsblock. Kontrollera om ID:t redan finns och ge i så fall ett begripligt fel med `ValueError`. Skapa annars en `Customer` med ID och namn. Registrera objektet med `session.add()`.
3. För borttagningen, behåll kontrollen i startkoden som stoppar ID under 9000. Hämta din egen testkund i ett transaktionsblock. Om posten saknas, signalera det med `LookupError`. Ta annars bort det hämtade objektet med `session.delete()`.
4. Prova att skapa, läsa, försöka skapa samma ID igen och till sist ta bort testkunden du själv skapade.

   ```bash
   python tasks.py create 9001 "Min testkund"
   python main.py 9001
   python tasks.py create 9001 "Försök med samma ID"
   python main.py 9001
   python tasks.py delete 9001
   python main.py 9001
   python main.py 1
   ```

**Varför?**  
`session.add()` förbereder en `INSERT` och `session.delete()` förbereder en `DELETE`. Transaktionen bekräftar ändringen när blocket avslutas normalt. Primärnyckeln i MySQL ser till att varje kund har ett unikt ID.

**Kontroll**  
Kundens namn syns efter skapandet, dubblettförsöket lämnar namnet oförändrat och testkunden saknas efter borttagningen. Kund 1 ska fortfarande gå att läsa.

## 4. Följ flush och rollback

1. Läs först kund 1 med `python main.py 1`. Skriv vilket namn du förväntar dig att en ny session läser efter en rollback.
2. Öppna [rollback_demo.py](rollback_demo.py) och följ `rename()`, `flush()` och `rollback()`. Kör sedan den färdiga demon.

   ```bash
   python rollback_demo.py
   python main.py 1
   ```

3. Skriv ned de tre raderna **Före**, **Efter flush** och **Ny session efter rollback**.

**Varför?**  
`flush()` skickar uppdateringen till MySQL inom den pågående transaktionen. `rollback()` ångrar den. En ny session ger dig ett sätt att kontrollera vad som faktiskt finns sparat.

**Kontroll**  
`Tillfälligt ORM-namn` syns efter flush. Efter rollback går det tidigare sparade namnet att läsa igen, även när du startar ett nytt program.

**Spara ditt arbete i labbrepot**

```bash
git add tasks.py REFLECTION.md
git commit -m "Verify ORM reads, writes and rollback"
```

## 5. Hämta kundens order

1. Öppna [setup_relations.sql](setup_relations.sql) i DBeaver och kör hela skriptet. Det skapar **`orm_relations_lab`**, en separat databas med `customers` och `orders`. Välj den databasen i DBeaver innan du jämför med SQL nedan.
2. Kör de fyra fallen. Titta särskilt på utskrifterna **Inga orders** och **Kunden saknas**.

   ```bash
   python relations.py 1 --sql
   python relations.py 2
   python relations.py 3
   python relations.py 999
   ```

3. Kör SQL-frågan nedan. Jämför med ORM-utskriften för kund 1. Byt sedan till 3, och därefter 999.

   ```sql
   SELECT c.customer_id, c.name, o.order_id
   FROM customers AS c
   LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
   WHERE c.customer_id = 1
   ORDER BY o.order_id;
   ```

4. Hitta `ForeignKey("customers.customer_id")`, `Customer.orders` och `Order.customer` i [relations.py](relations.py). Peka också ut var programmet läser `customer.orders` medan sessionen är öppen.

**Varför?**  
Orderradens `customer_id` är en främmande nyckel som pekar på kundens primärnyckel. Med `relationship()` kan du följa sambandet som Pythonobjekt. `customer.orders` ger kundens order och `order.customer` leder tillbaka till kunden. SQLAlchemy kan hämta orderraderna med en separat `SELECT` när du läser relationen.

**Kontroll**

| Kund-ID | Resultat i ORM på startdata |
| --- | --- |
| 1 | Order 11 och 12 |
| 2 | Order 13 |
| 3 | Kunden finns och ordersamlingen är tom |
| 999 | Kunden saknas |

Observera även att `LEFT JOIN` för kund 3 ger en kundrad med `NULL` på ordersidan. För 999 blir det noll rader.

## 6. Rita relationen och förklara vad den gör

1. Rita `Customer` och `Order` i [REFLECTION.md](REFLECTION.md). En textskiss räcker. Skriv tabellerna under klasserna och markera primärnyckel och främmande nyckel.
2. Visa på skissen hur många order en kund kan ha och hur många kunder en order hör till.
3. Förklara med en mening vad som skiljer värdet `order.customer_id` från `order.customer`. Visa också ett beteende hos kundobjektet genom att förklara vad `rename()` kontrollerar.

**Varför?**  
Skissen gör det lätt att se vilka fält som lagras i MySQL och vilka attribut Python använder för att följa en relation.

## 7. Överför arbetssättet till ditt kursprojekt

1. Välj en befintlig tabell i projektdatabasen. Jämför tabellnamn, primärnyckel och två kolumner med den Pythonklass du vill mappa.
2. Prova att läsa en befintlig rad och ett ID som saknas. Jämför med DBeaver.
3. Prova en kontrollerad ändring på egen testdata. Läs objektet i en ny session för att kontrollera att ändringen sparades. Prova sedan ett avvisat värde och kontrollera att det sparade värdet finns kvar.
4. Utgå från två tabeller med ett verkligt 1:N-samband. Mappa sambandet och visa hur du hämtar de relaterade objekten. Rita kopplingen i din klassbild.
5. Spara kod, klassbild, två testfall och körinstruktioner i ditt befintliga kursprojekt. Spara också [REFLECTION.md](REFLECTION.md) i detta labbrepo. Det här är ett arbetssteg i kursprojektet.

**Varför?**  
Du kan använda en ORM-mappning på en tabell som redan finns. MySQLs primärnycklar, främmande nycklar och övriga regler gäller fortfarande.

## Om något strular

| Det du ser | Börja här |
| --- | --- |
| `ModuleNotFoundError` | Kontrollera att du kör med labbets Python. Kör `python -m pip install -r requirements.txt` i samma miljö. |
| Du kommer inte in i MySQL | Prova anslutningen i DBeaver. Standard i startkoden är lokal server på port 3306. Använd din lokala MySQL-inloggning i terminalen. |
| Tabellen saknas | Kontrollera vilken databas programmet använder. Kör hela `setup.sql` för kundövningen eller `setup_relations.sql` för relationsövningen. |
| `Fyll i rename_customer` eller motsvarande | Du körde en skrivuppgift som fortfarande har kvar sin startfunktion. Arbeta klart den funktionen i `tasks.py` och prova igen. |
| DBeaver visar ett tidigare namn | Jämför databas och ID. Kontrollera att transaktionen har bekräftats och gör en ny läsning. |

Spara dina ändringar med `git status`, `git add` för de filer du har ändrat och en tydlig `git commit`. Använd `git push` när du vill spara dem i ditt eget repo på GitHub. Håll lösenord utanför kod och anteckningar.

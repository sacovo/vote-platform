# E-Vote Platform

Diese Plattform ermöglicht es, Wahlen und Abstimmungen online abzuhalten. Die Wahlen sind dabei nicht anonym, sondern nur [_pseudonym_](https://de.wikipedia.org/wiki/Pseudonym). Für Aussenstehende ist es praktisch unmöglich herauszufinden, wer wie abgestimmt hat. Auch für Personen mit Zugang zur internen Datenbank ist es mit Zeit und Mühe verbunden, dasselbe herauszufinden. Echte Anonymität kann auf dieser technischen Basis allerdings nicht gewährleistet werden. Die Wahrung der Pseudonymität basiert auf dem Vertrauen gegenüber den Betreiber\*innen der Plattform, da diese theoretisch – auch unbemerkt – zusätzliche Operationen im Hintergrund ausführen könnten, um Stimmen mit Stimmenden zu verknüpfen.

Die Plattform generiert für alle Wahlberechtigten einen Teilnahmecode, verschickt diesen per E-Mail, speichert beides zusammen als [Hash-Wert](https://de.wikipedia.org/wiki/Kryptographische_Hashfunktion) in der internen Datenbank und löscht die Verknüpfung zwischen E-Mail-Adressen und Teilnahmecodes unwiderruflich. Wahlberechtigte können mit dem Teilnahmecode und ihrer E-Mail-Adresse abstimmen. Passen Teilnahmecode und E-Mail-Adresse zusammen, wird die Stimme akzeptiert und in die Datenbank aufgenommen. Ebenfalls wird der Teilnahmecode selbst abgespeichert, was eine spätere _individuelle Verifikation_ durch die Stimmenden ermöglicht: Alle abgegebenen Stimmen sind öffentlich einsehbar, wobei ein zur Überprüfung ausreichend grosser Teil des Codes zusammen mit der jeweiligen abgegebenen Stimme angezeigt wird.

Um zu verhindern, dass von den Betreiber\*innen zusätzliche Teilnahmecodes generiert werden, erhalten die Sektionen eine Übersicht über die Codes, die für die Delegierten ihrer Sektion ausgestellt wurden. Sie erhalten dabei ebenfalls nur einen Teil jedes Teilnahmecodes. Für jede abgebene Stimme wird auch die Sektion der Wahlberechtigten gespeichert und öffentlich angezeigt. Aufgabe der Sektionsverantwortlichen ist also zum einen zu überprüfen, dass ihre Delegierten tatsächlich die angegeben Codes erhalten haben und andererseits, dass für ihre Sektion nur mit den angegebenen Codes abgestimmt wurde.

## Setup

Clone repository

```
docker-compose up -d 
```

# E-Vote Platform

Diese Plattform ermöglicht es, Wahlen und Abstimmungen Online abzuhalten. Die Wahlen sind dabei nicht 100% anonym, für aussenstehende soll es aber möglichst mühsam sein herauszufinden, wer wie abgestimmt hat. Auch für Personen mit Zugang zur internen Datenbank ist es mit Zeit und Mühe verbunden, herauszufinden, wer wie abgestimmt hat. Aber die Anonymität kann aber nicht technisch gewährleistet werden und basiert auf dem Vertrauen gegenüber den Betreiber\*innen, da diese auch unbemerkt zusätzliche Operationen im Hintergrund ablaufen könnten um Stimmen mit Stimmenden zu verknüpfen.

Die Platform generiert für alle Wahlberechtigten einen Code, verschickt diesen per E-Mail und speichert einen Hash des Codes in der Datenbank. Wahlberechtigte können mit dem Code und ihrer E-Mail Adresse abstimmen. Stimmt der Code und die E-Mail Adresse wird die Stimme in der Datenbank gespeichert. Ebenfalls wird der Code mit der abgebenen Stimme gespeichert. Die abgegebenen Stimmen können öffentlich überprüft werden, dabei wird ein Teil des Codes und die abgebene Stimme angezeigt. Das heisst, das Wahlberechtigte überprüfen können, ob mit ihrem Code tatsächlich so abgestimmt wurde, wie sie das vorhatten.

Um zu verhindern, dass von den Betreiber\*innen zusätzliche Code generiert werden erhalten die Sektionen eine Übersicht über die Codes, die für die Delegierten ihrer Sektion ausgestellt wurden.  Die Sektionen  Sie erhalten dabei ebenfalls nur einen Teil jedes Codes. Für jede abgebene Stimme wird auch die Sektion der Wahlberechtigten gespeichert und öffentlich angezeigt. Aufgabe der Sektionsverantwortlichen ist also zum einen, zu überprüfen, dass ihre Delegierten tatsächlich die angegeben Codes erhalten haben und andererseits, dass für ihre Sektion nur mit den angebenen Codes abgestimmt wurde.

## Setup

Clone repository

```
docker-compose up -d 
```

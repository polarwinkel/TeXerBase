<h1>Neue Aufgabe</h1>
<form action="/saveNewExercise" method="POST" accept-charset="utf-8">
    <label>Titel: </label><input type="text" name="title"></input><br />
    <label>Thema: </label><select type="text" name="topicId">
    {% for topic in topics %}
        <option value="{{ topic[0] }}">{{ topic[2] }}</option>
    {% endfor %}
    </select><br />
    <label>Schwierigkeitsgrad: </label><select name="difficulty">
        <option value="">-</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
    </select><br />
    Aufgabe im mdTeX-Format:<br />
    <textarea name="exercise" rows="20" cols="72"></textarea><br />
    Lösung:<br />
    <textarea name="solution" rows="20" cols="72"></textarea><br />
    <label>Quelle: </label><input type="text" name="origin"></input><br />
    <label>Autor: </label><input type="text" name="author"></input><br />
    <label>Jahr: </label><input type="text" name="year"></input><br />
    <label>Lizenz: </label><select name="licenseId">
    {% for license in licenses %}
        <option value="{{ license[0] }}">{{ license[1] }}</option>
    {% endfor %}
    </select><br />
    Kommentar:<br />
    <textarea name="comment" rows="5" cols="72"></textarea><br />
    <label>zIndex (Sortierung): </label><input type="text" name="zOrder"></input><br />
    <input type="submit" value="Speichern">
</form> 

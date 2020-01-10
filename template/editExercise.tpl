<h1>Aufgabe bearbeiten:</h1>
<form action="/saveExercise" method="POST" accept-charset="utf-8">
    <input type="hidden" name="eid" value="{{ exercise[0] }}">
    <label>Titel: </label><input type="text" name="title" value="{{ exercise[1] }}" /><br />
    <label>Thema: </label><select type="text" name="topicId">
        {% for topic in topics %}
            {% if topic[0] == exercise[2] %}
                <option value="{{ topic[0] }}" selected="selected">{{ topic[2] }}</option>
            {% else %}
                <option value="{{ topic[0] }}">{{ topic[2] }}</option>
            {% endif %}
        {% endfor %}
    </select><br />
    <label>Schwierigkeitsgrad: </label><select name="difficulty">
        <option value="">-</option>
        {% for i in range(1, 5) %}
            {% if i == exercise[3] %}
                <option value="{{ i }}" selected="selected">{{ i }}</option>
            {% else %}
                <option value="{{ i }}">{{ i }}</option>
            {% endif %}
        {% endfor %}
    </select><br />
    Aufgabe im mdTeX-Format:<br />
    <textarea name="exercise" id="exercise" rows="20" cols="72">{{ exercise[4] }}</textarea><br />
    <button type="button" onclick="previewExercise()">Vorschau</button>
    <div id="previewExercise"></div>
    Lösung:<br />
    <textarea name="solution" id="solution" rows="20" cols="72">{{ exercise[5] }}</textarea><br />
    <button type="button" onclick="previewSolution()">Vorschau</button>
    <div id="previewSolution"></div>
    <label>Quelle: </label><input type="text" name="origin" value="{{ exercise[6] }}" /><br />
    <label>Autor: </label><input type="text" name="author" value="{{ exercise[7] }}"></input><br />
    <label>Jahr: </label><input type="text" name="year" value="{{ exercise[8] }}"></input><br />
    <label>Lizenz: </label><select name="licenseId">
        {% for license in licenses %}
            {% if license[0] == exercise[9] %}
                <option value="{{ license[0] }}" selected="selected">{{ license[1] }}</option>
            {% else %}
                <option value="{{ license[0] }}">{{ license[1] }}</option>
            {% endif %}
        {% endfor %}
    </select><br />
    Kommentar:<br />
    <textarea name="comment" id="comment" rows="5" cols="72">{{ exercise[10] }}</textarea><br />
    <button type="button" onclick="previewComment()">Vorschau</button>
    <div id="previewComment"></div>
    <label>zIndex (Sortierung): </label><input type="text" name="zOrder" value="{{ exercise[11] }}"></input><br />
    <input type="submit" value="Speichern">
</form>
<script>
    function mdtex2html(mdtex) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "../mdtex2html", false);
        xhr.setRequestHeader("Content-Type", "application/mdtex");
        xhr.send(mdtex);
        return xhr.responseText;
    }
    function previewExercise() {
        mdtex = document.getElementById("exercise").value;
        html = mdtex2html(mdtex);
        document.getElementById("previewExercise").innerHTML = html;
    }
    function previewSolution() {
        mdtex = document.getElementById("solution").value;
        html = mdtex2html(mdtex);
        document.getElementById("previewSolution").innerHTML = html;
    }
    function previewComment() {
        mdtex = document.getElementById("comment").value;
        html = mdtex2html(mdtex);
        document.getElementById("previewComment").innerHTML = html;
    }
</script>

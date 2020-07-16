<h1 id="title">{{ e['title'] }}</h1></h1>
<div id="content">
    <form id="form" accept-charset="utf-8">
        <input type="hidden" name="id" class="formdata" value="{{ e['id'] }}">
        <label>Titel: </label><input type="text" name="title" class="formdata" value="{{ e['title'] }}" /><br />
        <label>Thema: </label><select type="text" name="topicId" class="formdata">
            {% for topic in topics %}
                {% if topic['id'] == exercise['topicId'] %}
                    <option value="{{ topic['id'] }}" selected="selected">{{ topic['topic'] }}</option>
                {% else %}
                    <option value="{{ topic['id'] }}">{{ topic['topic'] }}</option>
                {% endif %}
            {% endfor %}
        </select><br />
        <label>Schwierigkeitsgrad: </label><select name="difficulty" class="formdata">
            <option value="">-</option>
            {% for i in range(1, 5) %}
                {% if i == e['difficulty'] %}
                    <option value="{{ i }}" selected="selected">{{ i }}</option>
                {% else %}
                    <option value="{{ i }}">{{ i }}</option>
                {% endif %}
            {% endfor %}
        </select><br />
        Aufgabe im mdTeX-Format:<br />
        <textarea name="exercise" id="exercise" class="formdata" rows="20" cols="72">{{ e['exercise'] }}</textarea><br />
        <button type="button" onclick="preview('exercise')">Vorschau</button>
        <div id="previewexercise"></div>
        Lösung:<br />
        <textarea name="solution" id="solution" class="formdata" rows="20" cols="72">{{ e['solution'] }}</textarea><br />
        <button type="button" onclick="preview('solution')">Vorschau</button>
        <div id="previewsolution"></div>
        <label>Quelle: </label><input type="text" name="origin" class="formdata" value="{{ e['origin'] }}" /><br />
        <label>Autor: </label><input type="text" name="author" class="formdata" value="{{ e['author'] }}"></input><br />
        <label>Jahr: </label><input type="text" name="year" class="formdata" value="{{ e['year'] }}"></input><br />
        <label>Lizenz: </label><select name="licenseId" class="formdata">
            {% for license in licenses %}
                {% if license[0] == e['licenseId'] %}
                    <option value="{{ license[0] }}" selected="selected">{{ license[1] }}</option>
                {% else %}
                    <option value="{{ license[0] }}">{{ license[1] }}</option>
                {% endif %}
            {% endfor %}
        </select><br />
        Kommentar:<br />
        <textarea name="comment" id="comment" class="formdata" rows="5" cols="72">{{ e['comment'] }}</textarea><br />
        <button type="button" onclick="preview('comment')">Vorschau</button>
        <div id="previewcomment"></div>
        <label>zIndex (Sortierung): </label><input type="text" name="zOrder" class="formdata" value="{{ e['zOrder'] }}"></input><br />
        <button type="button"  onclick="save()">Speichern</button>
    </form>
</div>
<script src="{{ relroot }}static/getFormJson.js"></script> 
<script>
    function mdtex2html(mdtex, element) {
        // gets html for a given mdTeX from the server and outputs in in the 'element' when received
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "../mdtex2html");
        xhr.setRequestHeader("Content-Type", "application/mdtex");
        xhr.send(mdtex);
        xhr.onreadystatechange = function() {
            html = xhr.responseText;
            document.getElementById(element).innerHTML = html;
        }
    }
    function preview(item) {
        mdtex = document.getElementById(item).value;
        html = mdtex2html(mdtex, 'preview'+item);
    }
    function save() {
        var xhr = new XMLHttpRequest();
        formJson = getFormJson();
        console.log(formJson);
        if (formJson.id=='') {
            xhr.open('POST', '{{ relroot }}TODO');
        } else {
            xhr.open('POST', '{{ relroot }}saveExercise');
        }
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(formJson));
        xhr.onreadystatechange = function() {
            //if (xhr.responseText.id.isNumeric) {
            //    window.location = '';
            //} else {
                document.getElementById('content').innerHTML = xhr.responseText;
            //}
        }
    }
</script>

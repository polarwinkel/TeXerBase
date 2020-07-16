<script>
function buildUrl() {
    var title = document.getElementById('title').value;
    if (document.getElementById('solutions').checked==true) {
        var type = 'solutions';
    } 
    else if (document.getElementById('source').checked==true) {
        var type = 'source';
    } 
    else {var type='exercises';}
    var exercises = '';
    var exerChecks = document.getElementsByClassName('exerCheck');
    for (var i=0; i<exerChecks.length; i++) {
        if (exerChecks.item(i).checked == true) {
            exercises = exercises+exerChecks[i].value+',';
        }
    }
    url = '/sheet/' + title + ';'+ exercises+';'+type+';';
    document.getElementById('sheetUrl').value = url;
    document.getElementById('sheetLink').href = url;
}
</script>

<h1>Aufgabenblatt erstellen</h1>
<label for="title">Titel: </label><input name="title" id="title" onchange="buildUrl()" /><br />
<label for="exercises">Aufgaben </label><input type="radio" name="type" id="exercises" value="exercises" onchange="buildUrl()" checked><br />
<label for="solutions">Lösungen </label><input type="radio" name="type" id="solutions" value="solutions" onchange="buildUrl()" /><br />
<label for="source">mdTeX-Quelltext </label><input type="radio" name="type" id="source" value="source" onchange="buildUrl()" /><br />
<label for="sheetUrl">URL: </label><input name="sheetUrl" id="sheetUrl" disabled />
<p><a href="" id="sheetLink">zum Aufgabenblatt</a></p>
<h2>Vorhandene Aufgaben</h2>
{% for topic in topics %}
    <h3>{{ topic['topic'] }}</h3>
    <table>
        <tr>
            <th>Id</th>
            <th style="width:70%">Titel</th>
            <th>Schwierigkeit</th>
        </tr>
        {% for exe in exerlist %}
            {% if exe['topicId']==topic['id'] %}
                <tr>
                    <td><input type="checkbox" class="exerCheck" value="{{ exe['id'] }}" onchange="buildUrl()" />{{ exe['id'] }}</td>
                    <td><a href="../viewExercise/{{ exe['id'] }}">{{ exe['title'] }}</a></td>
                    <td>{{ exe['difficulty'] }}</td>
                </tr>
            {% endif %}
        {% endfor %}
    </table>
{% endfor %}

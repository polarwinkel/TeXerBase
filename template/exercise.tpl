{% if e['id'] == '' %}
    <h1 id="title">Neue Aufgabe</h1></h1>
{% else %}
    <h1 id="title">{{ e['title'] }}</h1></h1>
{% endif %}
    <div id="content">
    </div>

<script src="{{ relroot }}static/getFormJson.js"></script> 
<script>
    var eJson = {{ eJson }};
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
    function show(eJson) {
        html = '<div id="exercise"></div>\n';
        mdtex2html(eJson.exercise, 'exercise');
        if (eJson.solution != '') {
            html += '<hr />\n';
            html += '<h2>Lösung</h2>\n';
            html += '<div id="solution"></div>\n';
            mdtex2html(eJson.solution, 'solution');
        }
        if (eJson.origin != '') {
            html += '<p style="text-align:right;">Quelle:'+eJson.origin+'</p>\n';
        }
        if (eJson.comment != '') {
            html += '<hr />\n';
            html += '<h2>Bemerkungen</h2>\n';
            html += '<div id="comment"></div>\n';
            mdtex2html(eJson.comment, 'comment');
        }
        html += '<p style="text-align:right;" class="no-print" onclick="edit()"><a>Aufgabe bearbeiten</a></p>\n';
        document.getElementById('content').innerHTML = html;
    }
    function edit() {
        html = '<input type="hidden" name="id" class="formdata" value="'+eJson.id+'">\n';
        html += '<label>Titel: </label><input type="text" name="title" class="formdata" value="'+eJson.title+'" /><br />\n';
        html += '<label>Thema: </label><select type="text" id="topicId" name="topicId" class="formdata">\n';
        html += '</select><br />\n';
        loadTopics(eJson.topicId);
        html += '<label for="difficulty" id="labelDifficulty">Schwierigkeitsgrad: </label>';
        html += '<input type="range" id="difficulty" name="difficulty" class="formdata" min="0" max="3" value="'+eJson.difficulty+'" oninput="styleDifficulty(this.value)"><br />\n';
        html += 'Aufgabe im mdTeX-Format:<br />\n';
        html += '<textarea name="exercise" id="exercise" class="formdata" rows="20" cols="72">'+eJson.exercise+'</textarea><br />\n';
        html += '<button type="button" onclick="preview(\'exercise\')">Vorschau</button>\n';
        html += '<div id="previewexercise"></div>\n';
        html += 'Lösung:<br />\n';
        html += '<textarea name="solution" id="solution" class="formdata" rows="20" cols="72">'+eJson.solution+'</textarea><br />\n';
        html += '<button type="button" onclick="preview(\'solution\')">Vorschau</button>\n';
        html += '<div id="previewsolution"></div>\n';
        html += '<label>Quelle: </label><input type="text" name="origin" class="formdata" value="'+eJson.origin+'" /><br />\n';
        html += '<label>Autor: </label><input type="text" name="author" class="formdata" value="'+eJson.author+'"></input><br />\n';
        html += '<label>Jahr: </label><input type="text" name="year" class="formdata" value="'+eJson.year+'"></input><br />\n';
        html += '<label>Lizenz: </label><select type="text" id="licenseId" name="licenseId" class="formdata">\n';
        html += '</select><br />\n';
        loadLicenses(eJson.licenseId);
        html += 'Kommentar:<br />\n';
        html += '<textarea name="comment" id="comment" class="formdata" rows="5" cols="72">'+eJson.comment+'</textarea><br />\n';
        html += '<button type="button" onclick="preview(\'comment\')">Vorschau</button>\n';
        html += '<div id="previewcomment"></div>\n';
        html += '<label for="zOrder">zIndex (Sortierung): </label>\n';
        html += '<input type="range" id="zOrder" name="zOrder" class="formdata" min="0" max="1000" value="'+eJson.zOrder+'"><br />\n';
        html += '<button type="button" onclick="save()">Speichern</button>\n';
        document.getElementById('content').innerHTML = html;
    }
    function reloadExercise(id) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{{ relroot }}getExerciseJson');
        xhr.setRequestHeader("Content-Type", "text/text");
        xhr.onreadystatechange = function() {
            eJson = JSON.parse(xhr.responseText);
            show(eHtmlJson);
        }
        xhr.send(id);
    }
    function loadTopics(idActive) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{{ relroot }}getTopicsJson');
        xhr.setRequestHeader("Content-Type", "text/text");
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 0 || (xhr.status >= 200 && status < 400)) {
                    Json = JSON.parse(xhr.responseText);
                    optionsHtml = '';
                    for (var item of Json) {
                        if (idActive == item.id) {
                            optionsHtml += '<option value="'+item.id+'" selected="selected">'+item.topic+'</option>';
                        } else {
                            optionsHtml += '<option value="'+item.id+'">'+item.topic+'</option>';
                        }
                    }
                } else {
                    optionsHtml = 'ERROR '+xhr.status+'while processing ajax-request'
                }
                document.getElementById('topicId').innerHTML = optionsHtml;
            }
        };
    }
    function loadLicenses(idActive) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{{ relroot }}getLicensesJson');
        xhr.setRequestHeader("Content-Type", "text/text");
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 0 || (xhr.status >= 200 && status < 400)) {
                    Json = JSON.parse(xhr.responseText);
                    optionsHtml = '';
                    for (var item of Json) {
                        if (idActive == item.id) {
                            optionsHtml += '<option value="'+item.id+'" selected="selected">'+item.name+'</option>';
                        } else {
                            optionsHtml += '<option value="'+item.id+'">'+item.name+'</option>';
                        }
                    }
                } else {
                    optionsHtml = 'ERROR '+xhr.status+'while processing ajax-request'
                }
                document.getElementById('licenseId').innerHTML = optionsHtml;
            }
        };
    }
    function preview(item) {
        mdtex = document.getElementById(item).value;
        html = mdtex2html(mdtex, 'preview'+item);
    }
    function save() {
        var xhr = new XMLHttpRequest();
        formJson = getFormJson();
        xhr.open('POST', '{{ relroot }}saveExercise');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(formJson));
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (isNaN(xhr.responseText)) {
                    alert(xhr.responseText);
                    console.log(xhr.responseText);
                } else {
                    window.location = '{{ relroot }}exercise/'+xhr.responseText;
                }
            }
        }
    }
    function styleDifficulty(n) {
        if (n==0) {
            document.getElementById('labelDifficulty').style.background = 'blue';
        } else if (n==1) {
            document.getElementById('labelDifficulty').style.background = 'green';
        } else if (n==2) {
            document.getElementById('labelDifficulty').style.background = 'yellow';
        } else if (n==3) {
            document.getElementById('labelDifficulty').style.background = 'red';
        }
    }
    if (eJson.id == '') {
        edit(eJson);
    } else {
        show(eJson);
    }
</script>

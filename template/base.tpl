<!doctype html>
<html>
    <head>
        <title>TeXerBase Exercise Database</title>
        <meta charset="utf-8" />
        <script>
            function request() {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "./", false);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.send(JSON.stringify({
                    echo: 'Hallo Welt'
                }));
                var box = document.getElementById('requestbox');
                box.innerHTML = xhr.responseText;
            }
        </script>
        <style>
            html {
                margin: 1em;
                background-color: #040;
                font-family: "latin modern roman", Garamond, Georgia, "Times New Roman", Times, sans-serif;
                color: black;
            }
            body {
                max-width: 30cm;
                margin: auto;
                background-color: white;
                padding: 4em;
                padding-top: 1em;
                padding-bottom: 3em;
                font-size: 1.6em;
            }
            math {
                font-size: 1.1em;
            }
            label{
                display: inline-block;
                float: left;
                clear: left;
                width: 250px;
                text-align: right;
                margin-right: 0.5em;
            }
            input {
                display: inline-block;
                float: left;
            }
            @media print
            {    
                body {
                    padding: 1em;
                    font-size: 1em;
                }
                .no-print, .no-print *
                {
                    display: none !important;
                }
            }
        </style>
    </head>
    <body>
        <p class="no-print" style="width:100%; background-color:080; text-align:right;">
            <a href="/" style="font-size:0.6em;">Home</a> | 
            <a href="/cheatsheetMdTeX" style="font-size:0.6em;">cheatsheetMdTeX</a> | 
            <a href="/cheatsheetSvg" style="font-size:0.6em;">cheatsheetSvg</a>
        </p>
        {{ content }}
    </body>
</html>

<!doctype html>
<html id="html">
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
            function printView() {
                document.getElementById('html').style.fontSize = '16px';
                document.getElementById('html').style.backgroundColor = '#aaa';
                document.getElementById('body').style.width = '21.0cm';
                document.getElementById('body').style.paddingRight = '1.5cm';
                document.getElementById('body').style.paddingLeft = '1.5cm';
                document.getElementById('nav').style.display = 'none';
            }
        </script>
        <style>
            html {
                margin: 1em;
                background-color: #040;
                font-family: "latin modern roman", Garamond, Georgia, "Times New Roman", Times, sans-serif;
                color: black;
                font-size: 1.6em;
            }
            body {
                max-width: 30cm;
                margin: auto;
                margin-top: 1em;
                margin-bottom: 1em;
                background-color: white;
                padding: 4em;
                padding-top: 1em;
                padding-bottom: 1em;
            }
            math {
                font-size: 1rem;
            }
            label{
                display: inline-block;
                float: left;
                clear: left;
                width: 250px;
                text-align: right;
                margin-right: 0.5em;
                font-size: 1rem;
            }
            input {
                font-size: 1rem;
            }
            select {
                font-size: 1rem;
            }
            textarea {
                display: inline-block;
                float: left;
                font-size: 1rem;
            }
            button {
                font-size: 1rem;
            }
            p {
                page-break-inside: avoid;
            }
            @page {
                size: A4;
                margin: 0;
                margin-bottom: 1cm;
            }
            @page :first {
                margin-top: 0;
            }
            @media print {
                html, body {
                    width: 21cm;
                    height: 29.7cm;
                }
                .no-print, .no-print
                {
                    display: none !important;
                }
            }
        </style>
    </head>
    <body id="body">
        {{ nav }}
        {{ content }}
    </body>
</html>

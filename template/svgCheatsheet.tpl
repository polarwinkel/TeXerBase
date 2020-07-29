<h1>Cheatsheet <code>svg</code> coden</h1> 
<h2>Sandbox</h1>
<textarea oninput="preview()" id="svgCode"" rows="5" cols="72">
<svg x="0px" y="0px" width="250px" height="250px" viewBox="0 0 250 250">
    <circle cx="100" cy="100" r="30" fill="red" />
</svg>
</textarea>
<h3>Live-Preview:</h3>
<div id="svgView"></div>
<h2>Snippets</h2>
<table style="border:1px solid black;">
    <tr>
        <th style="width:20%">Objekt</th>
        <th style="width:20%">Beispiel</th>
        <th style="width:60%">Code</th>
    </tr>
    <tr>
        <td>Kreis</td>
        <td><svg><circle cx="100" cy="100" r="30" fill="red" /></svg></td>
        <td><code>&lt;circle cx="100" cy="100" r="30" fill="red" /&gt;</code></td>
    </tr>
    <tr>
        <td>Ellipse</td>
        <td><svg><ellipse cx="100" cy="50" rx="60" ry="30" fill="green"/></svg></td>
        <td><code>&lt;ellipse cx="100" cy="50" rx="60" ry="30" fill="green"/&gt;</code></td>
    </tr>
    <tr>
        <td>Rechteck</td>
        <td><svg><rect x="50" y="50" width="150" height="75" fill="#FF0" stroke="#000" stroke-width="10" /></svg></td>
        <td><code>&lt;rect x="50" y="50" width="150" height="75" fill="#FF0" stroke="#000" stroke-width="10" /&gt;</code></td>
    </tr>
    <tr>
        <td>Linie</td>
        <td><svg><line x1="10" y1="10" x2="100" y2="100" stroke="#00F"/></svg></td>
        <td><code>&lt;line x1="10" y1="10" x2="100" y2="100" stroke="#00F"/&gt;</code></td>
    </tr>
    <tr>
        <td>Pfad</td>
        <td><svg><path d="M 10,100 L 50,50 v 50 h 100" fill="none" stroke="rgb(255,153,102)" stroke-width="2"/></svg></td>
        <td><code>&lt;path d="M 10,100 L 50,50 v 50 h 100" fill="none" stroke="rgb(255,153,102)" stroke-width="2"/&gt;</code></td>
    </tr>
    <tr>
        <td>Polygon</td>
        <td><svg><polygon points="50,120 100,25 200,100" fill="purple" stroke="#000" stroke-width="5" stroke-dasharray="40 10"/></svg></td>
        <td><code>&lt;polygon points="50,120 100,25 200,100" fill="purple" stroke="#000" stroke-width="5" stroke-dasharray="40 10"/&gt;</code></td>
    </tr>
    <tr>
        <td>Bezier-Pfad (quadratisch)</td>
        <td><svg>
            <path d="M 100,10 Q 10,50 200,150" fill="none" stroke="blue"/>
            <path d="M 100,10 10,50 200,150" fill="none" stroke="gray"/>
        </svg></td>
        <td><code>
            &lt;path d="M 100,10 Q 10,50 200,150" fill="none" stroke="blue"/&gt;<br />
            &lt;path d="M 100,10 10,50 200,150" fill="none" stroke="gray"/&gt;
        </code></td>
    </tr>
</table>
<h3>Beispiel</h3>
<img src="/img/test.svg" alt="svg-testbild" width="800" height="600" />

<script>
    function preview() {
        svg = document.getElementById("svgCode").value;
        document.getElementById("svgView").innerHTML = svg;
    }
    preview();
</script>

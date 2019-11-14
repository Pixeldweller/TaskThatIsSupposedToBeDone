    ## coding: utf-8
<!DOCTYPE html>
    <html lang="DE">
    <head>
        <title>
            <%block name="title">
                Homepage
            </%block>
        </title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/content/base.css" type="text/css">
        <script type="text/javascript" src="/content/selectionUtil.js"></script>
    </head>
    <body>
    <h1>
        Projekte & Co.
    </h1>

    <div id='nav'>
        <!-- NAVIGATION -->
        <div>
            <a tabindex="1" href="/report" class="linkButton">Auswertung</a>
            <a tabindex="2" href="/projects" class="linkButton">Projekte</a>
            <a tabindex="3" href="/employees" class="linkButton">Mitarbeiter</a>
            <a tabindex="4" href="/customers" class="linkButton">Kunden</a>
        </div>
        <br><br>
    </div>

        <%block name="feedbackPanel">

        </%block>

    <div id='main'>
        <%block name="content">

            </%block>
    </div>

        <%block name="block_0">

        </%block>

    <div class="elemtentContainer">
        <a style="font-size: 55%" onclick="window.history.back();" class="linkButton"> Zurück </a>
    </div>

    <footer>Ein Projekt von Pixeldweller WS18/19</footer>
    </body>
    </html>
    ## EOF

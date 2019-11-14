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
    </head>
    <body>
        <h1>
            Projekte & Co.
        </h1>

        <div id='nav'>
          <!-- NAVIGATION -->
          <div>
              <!-- <a href="/report" class="linkButton">Auswertung</a> -->
              <a href="/projects" class="linkButton">Projekte</a>
              <a href="/employees" class="linkButton">Mitarbeiter</a>
              <a href="/customers" class="linkButton">Kunden</a>
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

        <br>
        <a style="font-size: 85%" onclick="window.history.back();" class="linkButton"> Zurück </a>

    </body>
</html>
## EOF

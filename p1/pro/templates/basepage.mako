## coding: utf-8
<!DOCTYPE html>
<html lang="DE">
    <head>
        <title>
            Homepage
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
              <a href="/projects" class="linkButton">Projekte</a>
              <a href="/employees" class="linkButton">Mitarbeiter</a>
              <a href="/customers" class="linkButton">Kunden</a>
          </div>
          <br><br>
        </div>

        <div id='main'>
             <%block name="content">
                ${page.default_view()}
             </%block>
        </div>

        <footer>
            During your current session, you've viewed this page ${page.getPageCount()} times! Your life is a patio of fun!
        </footer>


    </body>
</html>
## EOF

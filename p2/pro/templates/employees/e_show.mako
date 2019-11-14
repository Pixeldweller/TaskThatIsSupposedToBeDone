## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%block name="content">
    <form>
        <div>
             <h2>Mitarbeiter ID: ${data_o['id']}</h2>
        </div>
        <div>
            <h3>Vorname:</h3>
            <p>${data_o['firstname']}</p>
        </div>
        <div>
            <h3>Nachname:</h3>
            <p>${data_o['lastname']}</p>
        </div>
        <div>
            <h3>Adresse:</h3>
            <p>${data_o['address']}</p>
        </div>
        <div>
            <h3>E-Mail:</h3>
            <p>${data_o['email']}</p>
        </div>
        <div>
            <h3>Rollen:</h3>
            <p>${data_o['role']}</p>
        </div>

        <br>
        <br>

    </form>
</%block>

<!---->

##EOF

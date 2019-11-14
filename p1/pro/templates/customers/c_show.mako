## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%block name="content">
    <form>
        <div>
             <h2>Kunden ID: ${data_o['id']}</h2>
        </div>
        <div>
            <h3>Kunden Nummer:</h3> <p>${data_o['number']}</p>
        </div>
        <div>
            <h3>Name:</h3> <p>${data_o['name']}</p>
        </div>
        <div>
            <h3>Ansprechpartner:</h3> <p>${data_o['contact']}</p>
        </div>
         <div>
            <h3>Adresse:</h3> <p>${data_o['address']}</p>
        </div>
         <div>
            <h3>Telefon:</h3> <p>${data_o['phn']}</p>
        </div>
        <div>
            <h3>E-Mail:</h3> <p>${data_o['email']}</p>
        </div>

        <br>
        <br>
    </form>
</%block>

<!---->

##EOF

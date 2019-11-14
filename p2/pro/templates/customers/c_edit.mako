## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%block name="content">
    <form id="addForm" action ="/customers/add/" method="GET" >
        <div>
             <p>Kunden ID: ${data_o['id']}</p>
             <input style="display:none" type="text" name="id" required value="${data_o['id']}"/>
        </div>
        <div>
            Kunden Nummer: <input type="text" name="number" required value="${data_o['number']}"/>
        </div>
        <div>
            Name: <input type="text" name="name" required value="${data_o['name']}"/>
        </div>
        <div>
            Ansprechpartner: <input type="text" name="contact" required value="${data_o['contact']}"/>
        </div>
         <div>
            Adresse: <textarea name="address" form="addForm" required>${data_o['address']}</textarea>
        </div>
         <div>
            Telefon: <input type="tel" name="phn" required value="${data_o['phn']}"/>
        </div>
        <div>
            E-Mail: <input type="email" name="email" required value="${data_o['email']}"/>
        </div>

        <br>
        <br>
        <input class="button" type="submit" value="Übernehmen">
    </form>
</%block>

<!---->

##EOF

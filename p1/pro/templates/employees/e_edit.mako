## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%block name="content">
    <form id="addForm" action ="/employees/add/" method="GET" >
        <div>
             <p>Mitarbeiter ID: ${data_o['id']}</p>
             <input style="display:none" type="text" name="id" required value="${data_o['id']}"/>
        </div>
        <div>
            Vorname: <input type="text" name="firstname" required value="${data_o['firstname']}"/>
        </div>
        <div>
            Nachname: <input type="text" name="lastname" required value="${data_o['lastname']}"/>
        </div>
        <div>
            Adresse: <textarea type="text" name="address" form="addForm" required>${data_o['address']}</textarea>
        </div>
        <div>
            E-Mail: <input type="email" name="email" required value="${data_o['email']}"/>
        </div>
        <div>
            Rollen: <input type="text" name="role" required value="${data_o['role']}"/>
        </div>

        <br>

        <br>
        <input class="button" type="submit" value="Übernehmen">
    </form>
</%block>

<!---->

##EOF

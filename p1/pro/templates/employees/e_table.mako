## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%
    highest_id = 0
%>
<%block name="content">
    <table id="idList">
      <tr>
          <th> Nummer </th>
          <th> Vorname </th>
          <th> Nachname </th>
          <th> Adresse </th>
          <th> E-Mail </th>
          <th> Role </th>
          <th> Aktion </th>
      </tr>

      % for key_s in data_o['data']:
      <tr id="r${key_s['id']}">
          <%
              highest_id = key_s['id']
          %>
           <td>${key_s['id']}</td>
           <td>${key_s['firstname']}</td>
           <td>${key_s['lastname']}</td>
           <td>${key_s['address']}</td>
           <td>${key_s['email']}</td>
           <td>${key_s['role']}</td>

            <td>
                <a href='/employees/show/${key_s['id']}'>Details</a>
                <br>
                <a href='/employees/edit/${key_s['id']}'>Bearbeiten</a>
                <br>
                <a href='/employees/delete/${key_s['id']}'>Löschen</a>
            </td>
      </tr>
      % endfor
    </table>

    <br>
    <h2><a href="/employees/edit/${highest_id+1}" class="linkButton">Neuer Mitarbeiter</a></h2>
</%block>


##EOF

## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%
    highest_id = 0
%>

<%block name="content">
    <table id="idList">
      <tr>
          <th> Nummer </th>
          <th> Name </th>
          <th> Ansprechpartner </th>
          <th> Adresse </th>
          <th> Telefon </th>
          <th> E-Mail </th>
          <th> Aktion </th>
      </tr>

      % for key_s in data_o['data']:
      <tr id="r${key_s['id']}">
           <%
              highest_id = key_s['id']
           %>
           <td>${key_s['number']}</td>
           <td>${key_s['name']}</td>
           <td>${key_s['contact']}</td>
           <td>${key_s['address']}</td>
           <td>${key_s['phn']}</td>
           <td>${key_s['email']}</td>

            <td>
                <a href='/customers/show/${key_s['id']}'>Details</a>
                <br>
                <a href='/customers/edit/${key_s['id']}'>Bearbeiten</a>
                <br>
                <a href='/customers/delete/${key_s['id']}'>Löschen</a>
            </td>
      </tr>
      % endfor
    </table>

    <br>
    <h2><a href="/customers/edit/${highest_id+1}" class="linkButton">Neuer Kunde</a></h2>
</%block>


##EOF

## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%
    highest_id = 0
%>

<%block name="feedbackPanel">
    % if data_o['msg'] is not '':
    <div id="main" style="background-color: lightsalmon;">
        <p>${data_o['msg']}</p>
    </div>
    % endif
</%block>

<%block name="content">
    <table id="idList" onkeydown="selectNext(e)">
      <tr>
          <th> Nummer </th>
          <th> Vorname </th>
          <th> Nachname </th>
          <th> Adresse </th>
          <th> E-Mail </th>
          <th> Role </th>
      </tr>

      % for key_s in data_o['data']:
      <tr class="selectable" onfocus="setSelectedRow(this,${key_s['id']})" onclick="checkDeselect(this,${key_s['id']});" id="r${key_s['id']}" tabindex="${key_s['id']+3}">
          <%
              highest_id = key_s['id']
          %>
           <td>#${key_s['id']}</td>
           <td>${key_s['firstname']}</td>
           <td>${key_s['lastname']}</td>
           <td>${key_s['address']}</td>
           <td>${key_s['email']}</td>
           <td>${key_s['role']}</td>
      </tr>
      % endfor
    </table>

    <br>
    <h4>
        <button onclick="openDetailPage('employees')" class="button needsSelection" disabled>Details</button>
        <button onclick="openEditPage('employees')" class="button needsSelection" disabled>Bearbeiten</button>
        <button onclick="openDeletePage('employees')" class="button needsSelection" disabled>Löschen</button>
        <a href="/employees/edit/${highest_id+1}" class="linkButton">Neuer Mitarbeiter</a>

    </h4>
</%block>


##EOF

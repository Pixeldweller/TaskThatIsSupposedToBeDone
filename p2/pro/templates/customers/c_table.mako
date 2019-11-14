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
    <table id="idList">
      <tr>
          <th> Nummer </th>
          <th> Name </th>
          <th> Ansprechpartner </th>
          <th> Adresse </th>
          <th> Telefon </th>
          <th> E-Mail </th>
      </tr>

      % for key_s in data_o['data']:
      <tr id="r${key_s['id']}" class="selectable" onclick="checkDeselect(this,${key_s['id']});" onfocus="setSelectedRow(this,${key_s['id']})"  tabindex="${key_s['id']+3}">
           <%
              highest_id = key_s['id']
           %>
           <td>#${key_s['number']}</td>
           <td>${key_s['name']}</td>
           <td>${key_s['contact']}</td>
           <td>${key_s['address']}</td>
           <td>${key_s['phn']}</td>
           <td>${key_s['email']}</td>
      </tr>
      % endfor
    </table>

    <br>
    <h4>
        <button onclick="openDetailPage('customers')" class="button needsSelection" disabled>Details</button>
        <button onclick="openEditPage('customers')" class="button needsSelection" disabled>Bearbeiten</button>
        <button onclick="openDeletePage('customers')" class="button needsSelection" disabled>Löschen</button>
        <a href="/customers/edit/${highest_id+1}" class="linkButton">Neuer Kunde</a>
    </h4>
</%block>


##EOF

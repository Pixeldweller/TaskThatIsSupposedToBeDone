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
          <th> Title </th>
          <th> Beschreibung </th>
          <th> Startdatum </th>
          <th> Laufzeit (in Wochen) </th>
          <th> Budget </th>
          <th> Kunde </th>
          <th> Mitarbeiter </th>
      </tr>

      % for key_s in data_o['data']:
      <tr class="selectable" onfocus="setSelectedRow(this,${key_s['id']})" onclick="checkDeselect(this,${key_s['id']});" id="r${key_s['id']}" tabindex="${key_s['id']+3}">
          <%
              highest_id = key_s['id']
          %>
           <td>#${key_s['id']}</td>
           <td>${key_s['title']}</td>
           <td>${key_s['desc']}</td>
           <td>${key_s['startdate']}</td>
           <td>${key_s['duration']}</td>
           <td>${key_s['budget']}€</td>
           <td>
                <%
                        def get_cust_name(id):
                            for entry in data_o['possible_customers']:
                                if entry['id'] == id:
                                    return entry['name']
                            return "KUNDE NICHT MEHR VORHANDEN"
                   %>
               <p>
                   ${get_cust_name(key_s['customer'])}
                   <a style="right: 80%; font-size:75%;" href="/customers/show/${key_s['customer']}">Link</a>
               </p>
           </td>

           <td>
             % for entry in key_s['employee']:
                 <p style="text-align: center;"><a style="right: 80%; font-size:75%;" href="/employees/show/${entry['employee_id']}">${entry['name']}</a></p>
             %endfor
           </td>

      </tr>
      % endfor
    </table>
    <a href="/projects/table_view"> Wechsel zur Kachelansicht </a>
    <br>
    <div class="miscContainer fadeInObject">
        <h4 style="position: relative; top: -50px;">
            <button tabindex=${highest_id+2} onclick="openDetailPage('projects')" class="button needsSelection" disabled>Details</button>
            <button tabindex=${highest_id+3} onclick="openEditPage('projects')" class="button needsSelection" disabled>Bearbeiten</button>
            <button tabindex=${highest_id+4} onclick="openDeletePage('projects')" class="button needsSelection" disabled>Löschen</button>
            <a tabindex=${highest_id+5} href="/projects/edit/${highest_id+1}" class="linkButton">Neues Projekt</a>
        </h4>
    </div>
</%block>


##EOF

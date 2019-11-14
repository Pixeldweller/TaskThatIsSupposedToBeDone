## coding: utf-8

<%
    highest_id = 0
%>

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
      <th> Aktion </th>
  </tr>

  % for key_s in data_o:
  <tr id="r${key_s['id']}">
      <%
          highest_id = key_s['id']
      %>
       <td>${key_s['id']}</td>
       <td>${key_s['title']}</td>
       <td>${key_s['desc']}</td>
       <td>${key_s['startdate']}</td>
       <td>${key_s['duration']}</td>
       <td>${key_s['budget']}€</td>
       <td>
           <iframe src="/customers/show/${key_s['customer']}"></iframe>
           <a style="right: 80%; font-size:75%;" href="/customers/edit/${key_s['customer']}">Link</a>
       </td>

       <td>
         % for empl in key_s['employee']:
         <!--<a href="employees/edit/${empl['id']}">${empl['id']}</a>-->
             <div>
                 <iframe src="/employees/show/${empl['id']}/${empl['time']}"></iframe>
             </div>
         % endfor
       </td>
        <td>
            <a href='/project_detail/show/${key_s['id']}'>Details</a>
            <br>
            <a href='/projects/edit/${key_s['id']}'>Bearbeiten</a>
            <br>
            <a href='/projects/delete/${key_s['id']}'>Löschen</a>
        </td>
  </tr>
  % endfor
</table>

<br>
<h2><a href="/projects/edit/${highest_id+1}" class="linkButton">Neues Projekt</a></h2>



##EOF

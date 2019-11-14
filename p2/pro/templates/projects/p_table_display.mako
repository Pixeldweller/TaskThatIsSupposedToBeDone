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
      % for key_s in data_o['data']:
          <div class="box selectable" id="r${key_s['id']}" onclick="checkDeselect(this,${key_s['id']});" onfocus="setSelectedRow(this,${key_s['id']})" tabindex="${key_s['id']+3}">
          <%
              highest_id = key_s['id']
          %>
           <!--<td>${key_s['id']}</td>-->
           <h2>${key_s['title']} (#${key_s['number']})</h2>
           <h3>Beschreibung</h3>
               <p>${key_s['desc']}</p>
          <div class="floating">
              <h3>Startdatum</h3>
               <p>${key_s['startdate']}</p>
              <h3>Dauer</h3>
               <p>${key_s['duration']} Wochen</p>
          </div>
          <div class="floating">
              <h3>Budget (in EUR)</h3>
               <p>${key_s['budget']}€</p>

              <h3>Kunde</h3>
               <div>
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

               </div>
          </div>



            <div>
                 <table class="roundTable">
                    <tr>
                        <th>Mitarbeiter Einsatz</th>
                        <!-- KWs -->
                        <%
                            from datetime import datetime, timedelta

                            detail = key_s['employee']
                            wochen = int(key_s['duration'])

                            def safe_get(val, employee_id):
                                for data in detail:
                                    if data['employee_id'] == employee_id :
                                        try:
                                            if data[val] is None :
                                                return 0
                                            else:
                                                return int(data[val])
                                        except:
                                            return 0

                            def get_week_dates(weekoffset):
                                try:
                                    if key_s['startdate'] is None:
                                        return 'Projektwoche '+weekoffset
                                    part = key_s['startdate'].split('-')
                                    dt = datetime(int(part[0]),int(part[1]),int(part[2])) + timedelta(weeks=weekoffset)

                                    start = dt - timedelta(days=dt.weekday())
                                    end = start + timedelta(days=4) # MO to FRI
                                    return (start.strftime('%d.%m.%Y'))+ ' - ' + (end.strftime('%d.%m.%Y'))
                                except Exception as e:
                                    return 'Projektwoche '+weekoffset
                        %>
                        %for i in range(wochen):
                            <th>${get_week_dates(i)}</th>
                        %endfor
                    </tr>
                 % for entry in key_s['employee']:
                    % if safe_get("pw"+str(i), entry['employee_id']) is not None:
                        <tr>

                        <td><a style="right: 80%; font-size:75%;" href="/employees/show/${entry['employee_id']}">${entry['name']}</a></td>
                        %for i in range(wochen):
                            <td>
                                <p style="text-align: center;">${safe_get("pw"+str(i), entry['employee_id'])} std.</p>
                            </td>
                        %endfor
                    </tr>
                    % endif

                 %endfor
                </table>
            </div>

          <br>

      </div>
      % endfor
    <br>

    <div style="width: 100%; float:left;">
    <a href="/projects/table_view/True"> Wechsel zur Tabellenansicht </a>
    <div class="miscContainer fadeInObject">
        <h4 style="position: relative; top: -50px;">
            <button tabindex="${highest_id+3}" onclick="openDetailPage('projects')" class="button needsSelection" disabled>Details</button>
            <button tabindex="${highest_id+4}" onclick="openEditPage('projects')" class="button needsSelection" disabled>Bearbeiten</button>
            <button tabindex="${highest_id+5}" onclick="openDeletePage('projects')" class="button needsSelection" disabled>Löschen</button>
            <a tabindex=${highest_id+5} href="/projects/edit/${highest_id+1}" class="linkButton">Neues Projekt</a>
        </h4>
    </div>

    </div>
</%block>


##EOF

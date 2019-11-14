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
      <div class="box" id="r${key_s['id']}">
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
          <div class="miscContainer">
                <!--<a href='/project_detail/show/${key_s['id']}'>Details</a>-->
                <a class="linkButton" href='/projects/show/${key_s['id']}'>Details</a>
                <a class="linkButton" href='/projects/edit/${key_s['id']}'>Bearbeiten</a>
                <a class="linkButton" href='/projects/delete/${key_s['id']}'>Löschen</a>
           </div>
      </div>
      % endfor
    <br>
    <div style="width: 100%; float:left;">
     <h2><a href="/projects/edit/${highest_id+1}" class="linkButton">Neues Projekt</a></h2>
    </div>
</%block>


##EOF

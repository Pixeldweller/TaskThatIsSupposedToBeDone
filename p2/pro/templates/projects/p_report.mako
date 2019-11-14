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
          <div class="reportBox" id="r${key_s['id']}" tabindex="${key_s['id']+3}">

          <div style="float:left;">
               <h2>${key_s['title']} (#<a style="right: 80%; font-size:75%;" href="/projects/show/${key_s['id']}">${key_s['number']}</a>)</h2>
               <p>${key_s['desc']}</p>

               <%
                        def get_cust_name(id):
                            for entry in data_o['possible_customers']:
                                if entry['id'] == id:
                                    return entry['name']
                            return "KUNDE NICHT MEHR VORHANDEN"
               %>
               <p><b>Kunde:</b> ${get_cust_name(key_s['customer'])}  <a style="right: 80%; font-size:75%;" href="/customers/show/${key_s['customer']}">Link</a></p>
               <p><b>Budget:</b> ${key_s['budget']}€ </p>
               <p><b>Zeitraum:</b> ${key_s['startdate']} + ${key_s['duration']} Wochen</p>

          </div>
          <div style="width: 70%;float:right;">
             <table class="roundTable">
                <tr>
                    <th>Mitarbeiter Einsatz</th>
                    <!-- KWs -->
                    <%
                        from datetime import datetime, timedelta

                        detail = key_s['employee']
                        wochen = int(key_s['duration'])
                        summe = []

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

                        def get_sum(val, employee_id):
                            for data in detail:
                                if data['employee_id'] == employee_id :
                                    try:
                                        summe = 0
                                        for i in range(val):
                                            summe += int(data['pw'+str(i)])
                                        return summe
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
                    <th><i>Summe</i></th>
                </tr>
             % for entry in key_s['employee']:
                % if safe_get("pw"+str(i), entry['employee_id']) is not None:
                    <tr>

                    <td><a style="right: 80%; font-size:75%;" href="/employees/show/${entry['employee_id']}">${entry['lastname']} , ${entry['firstname']}</a></td>
                    %for i in range(wochen):
                        <td>
                            <p style="text-align: center;">${safe_get("pw"+str(i), entry['employee_id'])} std.</p>
                        </td>
                    %endfor
                        <td><b><p style="text-align: center;">${get_sum(wochen,entry['employee_id'])} std.</p></b></td>
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
    </div>
</%block>


##EOF

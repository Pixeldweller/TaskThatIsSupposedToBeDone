## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%block name="title">
    Projekt bearbeiten: ${data_o['title']}
</%block>


<%block name="content">
    <script>
        function getValue(inputID){
            if(document.getElementById(inputID).value == ''){
                return 0;
            }
            return escapeHtml(document.getElementById(inputID).value);
        }

        function escapeHtml(unsafe) {
            return unsafe
                 .replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#039;");
         }

         function resetTimesFor(empl_id) {
             for(var i = 0; i< getValue('duration'); i++){
                 document.getElementsByName(empl_id+"-pw"+i)[0].value = undefined;
             }
         }
    </script>

    <form id="addForm" action ="/projects/add/" method="GET" >
        <div>
             <p>Projekt ID: ${data_o['id']}</p>
             <input id="p_id" style="display:none" type="text" name="id" required value="${data_o['id']}"/>
        </div>
        <div>
            Projekt Nummer: <input id="p_num" type="number" name="number" required value="${data_o['number']}"/>
        </div>
        <div>
            Projekttitel: <input id="title" type="text" name="title" required value="${data_o['title']}"/>
        </div>
        <div>
            Beschreibung: <textarea id="desc" name="desc" form="addForm" required>${data_o['desc']}</textarea>
        </div>
        <div>
            Startdatum: <input id="startdate" type="date" name="startdate" required value="${data_o['startdate']}"/>
        </div>
        <div>
            Laufzeit in Wochen: <input id="duration" onchange="window.location = '/projects/edit/'+getValue('p_id')+'/TRUE/'+getValue('p_num')+'/'+getValue('title')+'/'+getValue('desc')+'/'+getValue('startdate')+'/'+getValue('duration')+'/'+getValue('budget')+'/'+getValue('customer')" type="number" min="0.00" name="duration" required value="${data_o['duration']}"/>
        </div>
        <div>
            Budget: <input id="budget" type="number" min="0.00" max="10000.00" step="any" name="budget" onchange="this.value = parseFloat(this.value).toFixed(2);" value="${data_o['budget']}"/>
        </div>
        <div>
            Mitarbeiter:
        </div>
        <div>
            <!--<input style="display: none" type="number" name="employee_id" value="..."/>-->
            <table>
                <tr>
                    <th>Mitarbeiter Zeiten in Projektwoche</th>
                    <!-- KWs -->
                    <%
                        from datetime import datetime, timedelta

                        wochen = int(data_o['duration'])

                        def safe_get(val, employee_id):
                            for data in data_o['employee']:
                                if data['employee_id'] == employee_id :
                                    try:
                                        if data[val] is None :
                                            return 0
                                        else:
                                            return int(data[val])
                                    except Exception as e:
                                        return 0
                            return ''

                        def get_week_dates(weekoffset):
                            try:
                                part = data_o['startdate'].split('-')
                                dt = datetime(int(part[0]),int(part[1]),int(part[2])) + timedelta(weeks=weekoffset)

                                start = dt - timedelta(days=dt.weekday())
                                end = start + timedelta(days=4) # MO to FRI
                                return (start.strftime('%d.%m.%Y'))+ ' - ' + (end.strftime('%d.%m.%Y'))
                            except Exception as e:
                                return 'Projektwoche '+ str(weekoffset)
                    %>
                    %for i in range(wochen):
                        <th>${get_week_dates(i)}</th>
                    %endfor
                    <th>Aktion</th>
                </tr>
                % for entry in data_o['possible_employees']:
                <tr>
                    <td>${entry['lastname']}</td>
                    %for i in range(wochen):
                        <td>
                            <input name="${entry['id']}-pw${i}" type="number" value="${safe_get("pw"+str(i), entry['id'])}"/>
                        </td>
                    %endfor
                    <td><p class="action" onclick="resetTimesFor(${entry['id']})">Zurücksetzen</p></td>
                </tr>
                % endfor
            </table>
        </div>

        <br>

        <div>
            Kunden:
             <select id="customer" name="customer">
                  %for entry in data_o['possible_customers']:
                       %if entry['id'] == data_o['customer']:
                             <option value="${entry['id']}" selected>${entry['name']}</option>
                       %else:
                             <option value="${entry['id']}">${entry['name']}</option>
                       %endif
                  %endfor
            </select>
        </div>

        <br>
        <input class="button" type="submit" value="Übernehmen">
    </form>
</%block>

<!---->

##EOF

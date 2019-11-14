## coding: utf-8

<%inherit file="/basepage_include.mako"/>

<%inherit file="/projects/p_detail.mako"/>

<%block name="block_0">

    <div id="container">
            <table class="roundTable">
                    <tr>
                        <th>Mitarbeiter Einsatz</th>
                        <!-- KWs -->
                        <%
                            from datetime import datetime, timedelta

                            detail = data_o['employee']
                            wochen = int(data_o['duration'])

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
                                    if data_o['startdate'] is None:
                                        return 'Projektwoche '+weekoffset
                                    part = data_o['startdate'].split('-')
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
                 % for entry in data_o['employee']:
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

</%block>

<!---->

##EOF

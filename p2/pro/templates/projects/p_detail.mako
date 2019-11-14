## coding: utf-8

<%inherit file="/basepage_include.mako"/>


<%block name="title">
    Projekt: ${data_o['title']}
</%block>

<%block name="content">

    <div>
        <h2>Projektübersicht zu: ${data_o['title']} (#${data_o['number']})</h2>

        <blockquote>${data_o['desc']}</blockquote>

         <%
            def get_cust_name(id):
                for entry in data_o['possible_customers']:
                    if entry['id'] == id:
                        return entry['name']
                return "KUNDE NICHT MEHR VORHANDEN"
        %>
       <p>
          - Für Kunden: ${get_cust_name(data_o['customer'])}
           <a style="right: 80%; font-size:75%;" href="/customers/show/${data_o['customer']}">Link</a> -
       </p>


        <p>- Budget: ${data_o['budget']}€ -</p>


        <p> Zeitraum: ${data_o['startdate']} + ${data_o['duration']} Wochen</p>
    </div>

    <%block name="timetable">

    </%block>

</%block>

<!---->

##EOF

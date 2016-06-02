# -*- coding: cp1252 -*-
class HTMLErrorPrinter:
    
    def no_timetables(self):
        return """\
<html>
  <head>
    <link rel='stylesheet' type='text/css' media='screen' href='http://fenix.ist.utl.pt/CSS/istPublicPagesStyles.css' />
    <style type="text/css">
    body {
        background-color: #F8F8F8;
        font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
        font-size: 13px;
        color: #444;
        margin: 0px;
    }
    </style>
  </head>
  <body style="margin:15px">
    <div class="mtop1 coutput2" style="line-height: 1.5em;font-family:'Verdana';font-size:12px;color:#DD0000">
      N&atilde;o h&aacute; nenhum hor&aacute;rio compat&iacute;vel com todas as disciplinas que seleccionou.<br> Experimente remover um tipo de aula ou uma disciplina.
    </div>
  </body>
<html>"""

    def print_no_timetables(self):
        print self.no_timetables()
        return
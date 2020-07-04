// Grammar for parsing Yahoo quota page http://finance.yahoo.com/quote.
grammar YAHOOQUOTE;

import JSON;		// include all rules from JSON.g4

yahoo_quote
		: line+ eol
		;

line: root_app_main_line
		| any_line
		;

root_app_main_line: ROOT_APP_MAIN '=' json ';'
		;

any_line
		: ANYCHAR+
		;

eol :  NEWLINE
  	|  EOF
  	;

ROOT_APP_MAIN: 'root.App.main' ;
ANYCHAR: . ;
NEWLINE: '\r'? '\n' ;			// return newlines to parser
WS  : [ \t]+ -> skip ;	// toss out whitespace

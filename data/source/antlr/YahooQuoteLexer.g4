// Lexer grammar for parsing Yahoo quota page http://finance.yahoo.com/quote.
lexer grammar YahooQuoteLexer ;

ROOT_APP_MAIN: 'root.App.main' -> pushMode(JSON) ;

WORD:	~[ \t\n\r]+ ;

NEWLINE : '\r'? '\n' ;

WS
   : [ \t\r] + -> skip
   ;

// JSON mode tokens.
mode JSON ;

// Close the mode.
CLOSE
		: ';' -> popMode ;

STRING
		: '"' (ESC | SAFECODEPOINT)* '"'
   	;

fragment ESC
		: '\\' (["\\/bfnrt] | UNICODE)
   	;
fragment UNICODE
		: 'u' HEX HEX HEX HEX
		;
fragment HEX
		: [0-9a-fA-F]
		;
fragment SAFECODEPOINT
		: ~ ["\\\u0000-\u001F]
		;

NUMBER
		: '-'? INT ('.' [0-9] +)? EXP?
		;

fragment INT
		: '0' | [1-9] [0-9]*
		;

EQ	: '='
		;
LCB : '{'
		;
RCB : '}'
		;
LB	: '['
		;
RB	: ']'
		;
LP	: '('
		;
RP	: ')'
		;
COMMA
		: ','
		;
COLON
		: ':'
		;
TRUE: 'true'
		;
FALSE
		: 'false'
		;
NULL: 'null'
		;


// no leading zeros

fragment EXP
		: [Ee] [+\-]? INT
		;

// \- since - means "range" inside [...]
JSONWS
   : [ \t\r] + -> skip
   ;

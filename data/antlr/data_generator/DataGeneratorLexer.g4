// Lexer grammar for writting to data proto.
lexer grammar DataGeneratorLexer ;

DOLLAR
		: '$'
		;

COLON
		: ':'
		;

SEMICOLON
		:	';'
		;

LCB
		:	'{'
		;

RCB
		:	'}'
		;

LP
		:	'('
		;

RP
		:	')'
		;

EQ
		:	'='
		;

DOT
		:	'.'
		;

PLUS
		:	'+'
		;

MINUS
		:	'-'
		;

MULTI
		:	'*'
		;

DIV
		:	'/'
		;

NAME
		: [a-zA-Z][a-zA-Z0-9_]*
		;

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
// no leading zeros
fragment EXP
   : [Ee] [+\-]? INT
   ;


WS
    : [ \t\r\n] + -> skip
   	;

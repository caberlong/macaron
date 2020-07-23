// Parser grammar for writting to data proto.
parser grammar DataGeneratorParser ;

options { tokenVocab=DataGeneratorLexer; }

generateDataProto
		: assign+ EOF
 		;

assign
		: assignVariable
		| assignSubProto
		|	assignField
		;

assignVariable
		: NAME EQ expr SEMICOLON
		;

assignSubProto 
		: NAME LCB assign* RCB
		;

assignField
		:	protoPath COLON expr SEMICOLON
		;

protoPath
		:	NAME (DOT protoPath)?
		;

expr
		: refVar
		|	NUMBER
		| STRING
		| left=expr PLUS right=expr
		| left=expr MINUS right=expr
		| left=expr MULTI right=expr
		| left=expr DIV right=expr
		| LP expr RP
		; 

refVar
		: DOLLAR protoPath
		;

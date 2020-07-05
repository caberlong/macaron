// Parser grammar for parsing Yahoo quota page http://finance.yahoo.com/quote.
parser grammar YahooQuoteParser ;

options { tokenVocab=YahooQuoteLexer; }

yahoo_quote
		: line+ EOF
 		;

line
		: json_line | other_line
		;

json_line
		: ROOT_APP_MAIN EQ json CLOSE NEWLINE
		;

other_line
		: ~ROOT_APP_MAIN WORD* NEWLINE
		;

json
    : value
    ;

obj
    : LCB pair (COMMA pair)* RCB
    | LCB RCB
    ;

pair
    : STRING COLON value
    ;

arr
    : LB value (COMMA value)* RB
    | LB RB
    ;

value
    : STRING
    | NUMBER
    | obj
    | arr
    | TRUE
    | FALSE
    | NULL
    ;

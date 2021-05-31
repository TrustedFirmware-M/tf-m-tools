/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_PARSER_TF_FUZZ_GRAMMAR_TAB_HPP_INCLUDED
# define YY_YY_PARSER_TF_FUZZ_GRAMMAR_TAB_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    PURPOSE = 258,
    RAW_TEXT = 259,
    SET = 260,
    READ = 261,
    REMOVE = 262,
    SECURE = 263,
    DONE = 264,
    SST = 265,
    KEY = 266,
    POLICY = 267,
    NAME = 268,
    UID = 269,
    STAR = 270,
    ACTIVE = 271,
    DELETED = 272,
    EQUAL = 273,
    DATA = 274,
    DFNAME = 275,
    FLAG = 276,
    NONE = 277,
    WRITE_ONCE = 278,
    NO_RP = 279,
    NO_CONF = 280,
    OFFSET = 281,
    CHECK = 282,
    VAR = 283,
    HASH = 284,
    NEQ = 285,
    PRINT = 286,
    EXPECT = 287,
    PASS = 288,
    FAIL = 289,
    NOTHING = 290,
    ERROR = 291,
    IDENTIFIER_TOK = 292,
    LITERAL_TOK = 293,
    HEX_LIST = 294,
    FILE_PATH_TOK = 295,
    NUMBER_TOK = 296,
    SEMICOLON = 297,
    SHUFFLE = 298,
    TO = 299,
    OF = 300,
    OPEN_BRACE = 301,
    CLOSE_BRACE = 302,
    ATTR = 303,
    TYPE = 304,
    ALG = 305,
    EXPORT = 306,
    COPY = 307,
    ENCRYPT = 308,
    DECRYPT = 309,
    SIGN = 310,
    VERIFY = 311,
    DERIVE = 312,
    NOEXPORT = 313,
    NOCOPY = 314,
    NOENCRYPT = 315,
    NODECRYPT = 316,
    NOSIGN = 317,
    NOVERIFY = 318,
    NODERIVE = 319,
    PERSISTENT = 320,
    VOLATILE = 321,
    FROM = 322,
    WITH = 323
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 353 "parser/tf_fuzz_grammar.y" /* yacc.c:1909  */
int valueN; int tokenN; char *str;

#line 126 "parser/tf_fuzz_grammar.tab.hpp" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


extern YYSTYPE yylval;
extern YYLTYPE yylloc;
int yyparse (tf_fuzz_info *rsrc);

#endif /* !YY_YY_PARSER_TF_FUZZ_GRAMMAR_TAB_HPP_INCLUDED  */

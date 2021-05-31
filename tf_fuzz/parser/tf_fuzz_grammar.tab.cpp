/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* Copy the first part of user declarations.  */
#line 8 "parser/tf_fuzz_grammar.y" /* yacc.c:339  */

#include <iostream>
#include <vector>
#include <set>

#include "class_forwards.hpp"
#include "data_blocks.hpp"
#include "boilerplate.hpp"
#include "gibberish.hpp"
#include "compute.hpp"
#include "string_ops.hpp"
#include "psa_asset.hpp"
#include "find_or_create_asset.hpp"
#include "template_line.hpp"
#include "tf_fuzz.hpp"
#include "sst_asset.hpp"
#include "crypto_asset.hpp"
#include "psa_call.hpp"
#include "crypto_call.hpp"
#include "sst_call.hpp"
#include "security_call.hpp"
#include "secure_template_line.hpp"
#include "sst_template_line.hpp"
#include "crypto_template_line.hpp"

/* These items are defined in tf_fuzz_grammar.l.  Note, however that, because
   of "name mangling," defining them as extern "C" may or may not be ideal,
   depending upon which compiler -- gcc vs. g++, compiles the output from lex.
   So far, it seems best without the extern "C", including also compiling
   under Visual Studio. */
/* extern "C"
{ */
  extern int yylineno;
  int yywrap() {return 1;}
  extern char yytext[];
  extern int yyleng;
/* } */

int yylex (void);
void yyerror (tf_fuzz_info *, const char *);
    /* Sends the yyparse() argument to yyerror(), probably, to print incorrect
       text it parsed. */

/* A few consts just to make code more comprehensible: */
const bool yes_fill_in_template = true;
const bool dont_fill_in_template = false;
const bool yes_create_call = true;
const bool dont_create_call = false;

tf_fuzz_info *rsrc;

/* These are object pointers used to parse the template and create the test.  Ac-
   tually, probably only templateLin is used for now, but this is a good outline of
   of the template_line class hierarchy. */
template_line                   *templateLin = nullptr;
  sst_template_line             *sstTemplateLin = nullptr;
    set_sst_template_line       *setSstTemplateLin = nullptr;
    read_sst_template_line      *reaSstTemplateLin = nullptr;
    remove_sst_template_line    *remSstTemplateLin = nullptr;
  policy_template_line          *polTemplateLin = nullptr;
    set_policy_template_line    *setPolTemplateLin = nullptr;
    read_policy_template_line   *reaPolTemplateLin = nullptr;
  key_template_line             *keyTemplateLin = nullptr;
    set_key_template_line       *setKeyTemplateLin = nullptr;
    read_key_template_line      *reaKeyTemplateLin = nullptr;
    remove_key_template_line    *remKeyTemplateLin = nullptr;
  security_template_line        *secTemplateLin = nullptr;
    security_hash_template_line *secHasTemplateLin = nullptr;
/* Call and asset objects are presumably not immediately needed, because the objects
   of these types are within the resource object, *rsrc, but even if only just to
   show that class hierarchy: */
psa_call                        *psaCal = nullptr;
  sst_call                      *sstCal = nullptr;
    sst_set_call                *sstSetCal = nullptr;
    sst_get_call                *sstGetCal = nullptr;
    sst_remove_call             *sstRemCal = nullptr;
  crypto_call                   *cryCal = nullptr;
    policy_call                 *polCal = nullptr;
      init_policy_call          *iniPolCal = nullptr;
      reset_policy_call         *resPolCal = nullptr;
      add_policy_usage_call     *addPolUsaCal = nullptr;
      set_policy_lifetime_call  *setPolLifCal = nullptr;
      set_policy_type_call      *setPolTypCal = nullptr;
      set_policy_algorithm_call *setPolAlgCal = nullptr;
      set_policy_usage_call     *setPolUsaCal = nullptr;
      get_policy_lifetime_call  *getPolLifCal = nullptr;
      get_policy_type_call      *getPolTypCal = nullptr;
      get_policy_algorithm_call *getPolAlgCal = nullptr;
      get_policy_usage_call     *getPolUsaCal = nullptr;
      get_policy_size_call      *getPolSizCal = nullptr;
      get_key_policy_call       *getKeyPolCal = nullptr;
    key_call                    *keyCal = nullptr;
      generate_key_call         *genKeyCal = nullptr;
      create_key_call           *creKeyCal = nullptr;
      copy_key_call             *copKeyCal = nullptr;
      read_key_data_call        *reaKeyDatCal = nullptr;
      remove_key_call           *remKeyCal = nullptr;
psa_asset                       *psaAst = nullptr;
  sst_asset                     *sstAst = nullptr;
  crypto_asset                  *cryAst = nullptr;
    policy_asset                *polAst = nullptr;
    key_asset                   *keyAst = nullptr;

/* For generating random, but readable/memorable, data: */
gibberish gib;
char gib_buff[4096];  // spew gibberish into here
int rand_data_length = 0;

/* General-utility variables: */
bool purpose_defined = false;
psa_asset_usage random_asset = psa_asset_usage::all;
    /* to pick what type of asset at random */
bool random_name;  /* template didn't specify name, so it's generated randomly */
string literal_data;  /* literal data for an asset value */

/* Holders for state in read commands: */
expect_info expect;  /* everything about expected results and data */
set_data_info set_data;  /* everything about setting the value of PSA-asset data */
asset_name_id_info parsed_asset;  /* everything about identifying assets */
string target_barrier = "";  /* asset to set and search barrier when re-ordering PSA calls */
key_policy_info policy_info;  /* everything about key policies */
bool assign_data_var_specified = false;
string assign_data_var;
bool print_data = false;  /* true to just print asset data to the test log */
bool hash_data = false;  /* true to just print asset data to the test log */
bool literal_is_string = true;
    /* if true, literal value is character-string;  if false, is list of hex values */

/* The following are more tied to the template syntax than to the resulting PSA calls */
string literal;  /* temporary holder for all string literals */
string identifier;  /* temporary holder for strings representing identifiers */
string var_name;  /* a variable name */
string asset_name;  /* as parsed, not yet put into parsed_asset */
string aid;  /* string-typed holder for an asset ID in a list thereof */
int nid;  /* same idea as aid, but for asset ID# lists */
size_t strFind1, strFind2;  /* for searching through strings */

/* Because of the parsing order, psa_calls of the specific type have to be
   push_back()ed onto rsrc->calls before their expected results are known.  Therefore,
   must inject those results after parsing the expected results.  add_expect is a
   loop index to track where to add results. */
unsigned int add_expect = 0;

/* Temporaries: */
vector<psa_asset*>::iterator t_sst_asset;
vector<psa_asset*>::iterator t_key_asset;
vector<psa_asset*>::iterator t_policy_asset;
sst_call *t_sst_call = nullptr;
key_call *t_key_call = nullptr;
policy_call *t_policy_call = nullptr;
long number;  /* temporary holder for a number, e.g., sting form of UID */
int i, j, k;

/* Relating to template-statement blocks: */
vector<template_line*> template_block_vector;  /* (must be *pointers to* templates) */
vector<int> block_order;  /* "statisticalized" order of template lines in a block */
int nesting_level = 0;
    /* how many levels deep in { } nesting currently.  Initially only 0 or 1. */
bool shuffle_not_pick;
    /* true to shuffle statements in a block, rather than pick so-and-so
       number of them at random. */
int low_nmbr_lines = 1;  /* if picking so-and-so number of template lines from a ... */
int high_nmbr_lines = 1; /*    ... block at random, these are fewest and most lines. */
int exact_nmbr_lines = 1;

using namespace std;


void set_purp_str (
    char *raw_purpose,  /* the purpose C string from parser */
    tf_fuzz_info *rsrc  /* test resources containing the actual test-purpose string */
) {
    size_t l;  /* temporary of size_t type */
    string purp_str = raw_purpose;
    strFind1 = purp_str.find (" ");
    purp_str = purp_str.substr (strFind1, purp_str.length());
    purp_str.erase (0, 1);  // (extra space)
    strFind1 = purp_str.rfind (";");
    purp_str = purp_str.substr (0, strFind1);
    l = 0;
    do {  /* escape all " chars (if not already escaped) */
        l = purp_str.find ("\"", l);
        if (   l < purp_str.length()) {  /* did find a quote character */
            if (   l == 0  /* it's the first character in the string*/
                || purp_str[l-1] != '\\' /* or it's not already escaped */
               ) {
                purp_str.insert (l, "\\");  /* then escape the " char */
                l++;  /* point l to the " again */
            }
            l++;  /* point l past the " */
        }
    } while (l < purp_str.length());
    rsrc->test_purpose = purp_str;
}

/* randomize_template_lines() chooses a template-line order in cases where they are to
   be randomized -- shuffled or random picked. */
void randomize_template_lines (
    bool shuffle_not_pick,  /* true to perform a shuffle operation rather than pick */
    int &low_nmbr_lines, /* if picking so-and-so number of template lines from a ... */
    int &high_nmbr_lines, /*    ... block at random, these are fewest and most lines. */
    int &exact_nmbr_lines,
    vector<template_line*> &template_block_vector,
    vector<int> &block_order,
    tf_fuzz_info *rsrc  /* test resources containing the actual test-purpose string */
) {
    set<int> template_used;  /* used for shuffle */
    low_nmbr_lines = (low_nmbr_lines < 0)?  0 : low_nmbr_lines;
    high_nmbr_lines = (high_nmbr_lines < 0)?  0 : high_nmbr_lines;
    if (low_nmbr_lines > high_nmbr_lines) {
        int swap = low_nmbr_lines;
        low_nmbr_lines = high_nmbr_lines;
        high_nmbr_lines = swap;
    }
    template_used.clear();
    if (shuffle_not_pick) {
        /* Choose a random order in which to generate all of the
           template lines in the block: */
        while (template_used.size() < template_block_vector.size()) {
            i = rand() % template_block_vector.size();
            if (template_used.find (i) == template_used.end()) {
                /* This template not already shuffled in. */
                block_order.push_back (i);
                template_used.insert (i);
            }
        }
        /* Done shuffling;  empty out the set: */
    } else {
        if (high_nmbr_lines == low_nmbr_lines) {
            exact_nmbr_lines = low_nmbr_lines;
                /* just in case the template says "3 to 3 of"... */
        } else {
            exact_nmbr_lines =   low_nmbr_lines
                               + (rand() % (  high_nmbr_lines
                                            - low_nmbr_lines + 1  )  );
        }
        for (int j = 0;  j < exact_nmbr_lines;  ++j) {
            /* Repeatedly choose a random template line from the block: */
            i = rand() % template_block_vector.size();
            block_order.push_back (i);
        }
    }
    IVM(cout << "Order of lines in block:  " << flush;
        for (auto i : block_order) {
            cout << i << "  ";
        }
        cout << endl;
    )
}

/* interpret_template_line() fills in random data, locates PSA assets, (etc.) and
   conditionally creates PSA calls for a given template line.  Note that there needs
   to be a single place where all of this is done, so that statement blocks can be
   randomized and then dispatched from a single point. */
void interpret_template_line (
    template_line *templateLin,  /* the template line to process */
    tf_fuzz_info *rsrc,  /* program resources in general */
    set_data_info &set_data, psa_asset_usage random_asset,
    bool assign_data_var_specified, expect_info &expect, key_policy_info &policy_info,
    bool print_data, bool hash_data, string asset_name, string assign_data_var,
    asset_name_id_info &asset_info,  /* everything about the asset(s) involved */
    bool create_call_bool,  /* true to create the PSA call at this time */
    bool create_asset_bool,  /* true to create the PSA asset at this time */
    bool fill_in_template,  /* true to back-fill info into template */
    int instance
        /* if further differentiation to the names or IDs is needed, make instance >0 */
) {
    const bool yes_fill_in_template = true;  /* just to improve readability */
    vector<psa_asset*>::iterator t_psa_asset;

    if (fill_in_template) {
        /* Set basic parameters from the template line: */
        templateLin->set_data = set_data;
        templateLin->expect = expect;
        templateLin->policy_info = policy_info;
        templateLin->asset_info.id_n_not_name = asset_info.id_n_not_name;
        templateLin->asset_info.set_name (asset_name);
        /* Fill in state parsed from the template below: */
        templateLin->assign_data_var_specified = assign_data_var_specified;
        templateLin->assign_data_var.assign (assign_data_var);
        templateLin->print_data = print_data;
        templateLin->hash_data = hash_data;
        templateLin->random_asset = random_asset;
        if (   set_data.literal_data_not_file && !set_data.random_data
            && set_data.string_specified) {
            templateLin->set_data.set (literal_data);
        }
        /* Save names or IDs to the template-line tracker: */
        for (auto id_no : asset_info.asset_id_n_vector) {
             templateLin->asset_info.asset_id_n_vector.push_back (id_no);
        }
        asset_info.asset_id_n_vector.clear();
        for (auto as_name : asset_info.asset_name_vector) {
             templateLin->asset_info.asset_name_vector.push_back (as_name);
        }
        asset_info.asset_name_vector.clear();
    }

    /* Random asset choice (e.g., *active) case: */
    if (templateLin->random_asset != psa_asset_usage::all) {
        /* Just create the call tracker;  random name chosen in simulation stage: */
        templateLin->setup_call (set_data, templateLin->set_data.random_data,
                                 yes_fill_in_template, create_call_bool,
                                 templateLin, rsrc   );
    } else if (asset_info.id_n_not_name) {
        /* Not random asset;  asset(s) by ID rather than name.  Go through all
           specified asset IDs: */
        uint64_t id_no;
        for (auto id_n :  templateLin->asset_info.asset_id_n_vector) {
            id_no = id_n + (uint64_t) instance * 10000UL;
            templateLin->asset_info.set_id_n(id_no);  /* just a holder */
            asset_name = templateLin->asset_info.make_id_n_based_name (id_no);
            templateLin->asset_info.set_calc_name (asset_name);
            templateLin->expect.data_var = var_name;
            if (!set_data.literal_data_not_file) {
                templateLin->set_data.set_file (set_data.file_path);
            }
            templateLin->setup_call (set_data, templateLin->set_data.random_data,
                                     fill_in_template, create_call_bool,
                                     templateLin, rsrc   );
        }
    } else {
        /* Not random asset, asset(s) specified by name.  Go through all specified
           asset names: */
        for (auto as_name :  templateLin->asset_info.asset_name_vector) {
            /* Also copy into template line object's local vector: */
            if (instance > 0) {
                templateLin->asset_info.set_name (as_name + "_" + to_string (instance));
            } else {
                templateLin->asset_info.set_name (as_name);
            }
            /* Give each occurrence a different random ID: */
            templateLin->asset_info.set_id_n (100 + (rand() % 10000));
                /* TODO:  unlikely, but this *could* alias! */
            templateLin->setup_call (set_data, templateLin->set_data.random_data,
                                     yes_fill_in_template, create_call_bool,
                                     templateLin, rsrc   );
        }
    }
}


#line 409 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 1
#endif

/* In a future release of Bison, this section will be replaced
   by #include "tf_fuzz_grammar.tab.hpp".  */
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
#line 353 "parser/tf_fuzz_grammar.y" /* yacc.c:355  */
int valueN; int tokenN; char *str;

#line 521 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:355  */
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

/* Copy the second part of user declarations.  */

#line 552 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL \
             && defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
  YYLTYPE yyls_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE) + sizeof (YYLTYPE)) \
      + 2 * YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  34
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   159

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  69
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  82
/* YYNRULES -- Number of rules.  */
#define YYNRULES  155
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  212

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   323

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   378,   378,   379,   390,   409,   451,   475,   501,   504,
     507,   510,   513,   519,   524,   529,   534,   543,   555,   568,
     583,   595,   607,   622,   634,   649,   679,   691,   701,   712,
     713,   718,   726,   736,   737,   744,   745,   751,   751,   751,
     751,   753,   760,   767,   775,   784,   793,   799,   807,   816,
     826,   838,   851,   859,   860,   868,   868,   875,   883,   896,
     904,   908,   914,   923,   924,   932,   944,   951,   959,   967,
     974,   977,   978,   984,   990,   996,  1002,  1008,  1014,  1020,
    1026,  1032,  1038,  1044,  1050,  1056,  1062,  1068,  1074,  1081,
    1081,  1081,  1081,  1081,  1081,  1081,  1082,  1082,  1082,  1082,
    1082,  1082,  1083,  1083,  1083,  1083,  1089,  1098,  1107,  1108,
    1114,  1114,  1114,  1117,  1118,  1126,  1140,  1150,  1157,  1164,
    1176,  1182,  1188,  1189,  1196,  1200,  1210,  1211,  1218,  1224,
    1231,  1243,  1250,  1257,  1268,  1274,  1288,  1291,  1298,  1307,
    1317,  1320,  1321,  1324,  1337,  1340,  1341,  1344,  1353,  1361,
    1371,  1380,  1388,  1399,  1407,  1413
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 1
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "PURPOSE", "RAW_TEXT", "SET", "READ",
  "REMOVE", "SECURE", "DONE", "SST", "KEY", "POLICY", "NAME", "UID",
  "STAR", "ACTIVE", "DELETED", "EQUAL", "DATA", "DFNAME", "FLAG", "NONE",
  "WRITE_ONCE", "NO_RP", "NO_CONF", "OFFSET", "CHECK", "VAR", "HASH",
  "NEQ", "PRINT", "EXPECT", "PASS", "FAIL", "NOTHING", "ERROR",
  "IDENTIFIER_TOK", "LITERAL_TOK", "HEX_LIST", "FILE_PATH_TOK",
  "NUMBER_TOK", "SEMICOLON", "SHUFFLE", "TO", "OF", "OPEN_BRACE",
  "CLOSE_BRACE", "ATTR", "TYPE", "ALG", "EXPORT", "COPY", "ENCRYPT",
  "DECRYPT", "SIGN", "VERIFY", "DERIVE", "NOEXPORT", "NOCOPY", "NOENCRYPT",
  "NODECRYPT", "NOSIGN", "NOVERIFY", "NODERIVE", "PERSISTENT", "VOLATILE",
  "FROM", "WITH", "$accept", "lines", "line", "command", "expect",
  "set_command", "read_command", "remove_command", "secure_command",
  "done_command", "literal_or_random_data", "sst_set_base_args",
  "sst_set_extended_args", "sst_flags", "sst_flag", "none", "write_once",
  "no_rp", "no_conf", "sst_offset_spec", "sst_read_args", "read_args",
  "sst_read_extended_args", "sst_remove_args", "asset_designator",
  "single_existing_asset", "random_picked_asset", "sst_asset_name",
  "sst_asset_set_file_path", "read_args_var_name",
  "sst_asset_dump_file_path", "key_size", "policy_usage_list",
  "policy_usages", "export", "noexport", "copy", "nocopy", "encrypt",
  "noencrypt", "decrypt", "nodecrypt", "sign", "nosign", "verify",
  "noverify", "derive", "noderive", "persistent", "volatle",
  "policy_usage", "policy_type", "policy_algorithm", "policy_specs",
  "policy_spec", "policy_asset_spec", "policy_asset_name",
  "policy_set_args", "policy_read_args", "key_set_sources",
  "key_set_source", "key_data_or_not", "key_set_args", "key_remove_args",
  "key_read_args", "block", "block_content", "open_brace", "close_brace",
  "ASSET_NUMBER_LIST", "ASSET_NUMBERS", "ASSET_NUMBER",
  "ASSET_IDENTIFIER_LIST", "ASSET_IDENTIFIERS", "ASSET_IDENTIFIER",
  "IDENTIFIER", "FILE_PATH", "exact_sel_count", "low_sel_count",
  "high_sel_count", "NUMBER", "LITERAL", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323
};
# endif

#define YYPACT_NINF -102

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-102)))

#define YYTABLE_NINF -152

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
      35,  -102,    75,   104,    47,   -17,  -102,  -102,    20,    64,
      35,   -23,  -102,  -102,  -102,  -102,  -102,  -102,    30,    39,
      73,    37,    95,   112,    37,    95,     7,   106,    95,   103,
    -102,  -102,  -102,    35,  -102,  -102,    72,  -102,    92,    20,
      94,    32,    -2,   116,  -102,    -4,    -8,  -102,    33,    74,
    -102,  -102,    53,    53,  -102,    99,    99,   113,    53,  -102,
     115,  -102,  -102,  -102,  -102,  -102,   101,    93,  -102,  -102,
    -102,  -102,  -102,  -102,  -102,    96,  -102,  -102,  -102,  -102,
     101,  -102,  -102,  -102,    98,    88,  -102,    -7,   102,    99,
    -102,    99,    34,    76,  -102,     2,    77,  -102,  -102,    38,
      99,    99,  -102,  -102,  -102,  -102,    74,   102,    89,    99,
    -102,  -102,   117,  -102,  -102,  -102,  -102,  -102,  -102,  -102,
    -102,  -102,  -102,  -102,    20,  -102,   101,  -102,    98,  -102,
    -102,  -102,  -102,  -102,    88,  -102,  -102,  -102,  -102,  -102,
    -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,   134,  -102,
    -102,  -102,  -102,    74,  -102,  -102,  -102,  -102,  -102,  -102,
    -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,
    -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,
    -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,    38,  -102,
    -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,   107,  -102,
    -102,  -102,  -102,  -102,    99,  -102,  -102,    38,  -102,  -102,
    -102,  -102
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       2,     4,     0,     0,     0,     0,    26,   153,     0,     0,
       2,     0,     8,    10,     9,    11,    12,     5,     0,     0,
     150,     0,     0,   113,     0,     0,     0,     0,     0,     0,
     138,   137,   133,     2,     1,     3,     0,     6,     0,     0,
       0,     0,     0,    33,    63,    30,   122,    18,     0,   108,
      19,    20,     0,     0,    21,     0,     0,     0,     0,    22,
       0,    23,    56,    55,   131,    24,     0,     0,    13,    14,
      15,   148,    16,     7,   134,     0,   152,    58,   147,    57,
     145,    65,   143,    64,   141,    35,    17,     0,     0,     0,
      29,     0,     0,   124,   128,   122,     0,   115,   114,     0,
       0,     0,   110,   111,   112,   120,   108,     0,     0,     0,
      51,    50,    53,   132,   119,   116,   117,   118,   121,    61,
      62,    25,   139,   136,     0,   144,   145,   140,   141,    41,
      42,    43,    44,    34,    35,    37,    38,    39,    40,    28,
     154,   155,    27,   149,    32,    66,    31,   125,     0,    60,
      59,   124,   123,   108,    69,    73,    75,    77,    79,    81,
      83,    85,    74,    76,    78,    80,    82,    84,    86,    87,
      88,   105,    89,    96,    90,    97,    91,    98,    92,    99,
      93,   100,    94,   101,    95,   102,   103,   104,    71,   106,
     107,   109,    52,    68,    48,    67,    49,    47,     0,    46,
     135,   146,   142,    36,     0,   130,    70,    71,    45,    54,
     129,    72
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
    -102,    -3,    -6,  -102,  -102,  -102,  -102,  -102,  -102,  -102,
     -40,  -102,  -102,    13,  -102,  -102,  -102,  -102,  -102,  -102,
    -102,    14,  -102,  -102,    40,  -102,    58,    50,  -102,  -102,
    -102,  -102,  -102,   -56,  -102,  -102,  -102,  -102,  -102,  -102,
    -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,  -102,
      54,  -102,  -102,  -101,  -102,  -102,  -102,  -102,  -102,    57,
    -102,  -102,  -102,  -102,  -102,  -102,   -36,  -102,  -102,  -102,
      26,   114,   -31,    29,   -70,   -55,    51,  -102,  -102,  -102,
     119,    49
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     9,    10,    11,    38,    12,    13,    14,    15,    16,
      90,    43,    86,   133,   134,   135,   136,   137,   138,   209,
      51,   112,   199,    61,    44,   148,    62,    45,   144,   194,
     192,   171,   102,   206,   172,   173,   174,   175,   176,   177,
     178,   179,   180,   181,   182,   183,   184,   185,   186,   187,
     207,   103,   104,   105,   106,    49,    58,    50,    59,    94,
      95,    96,    47,    65,    54,    17,    32,    33,   123,    83,
     127,   128,    79,   125,    80,    72,   145,    18,    19,    75,
      20,   142
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
     114,   115,    31,    74,    91,   191,    93,    35,   139,    36,
     126,    87,    29,    81,    91,    87,    88,    98,    55,    37,
      56,    87,    57,     1,    89,     2,     3,     4,     5,     6,
      67,   140,   141,    31,   146,   121,   147,   150,     1,    82,
       2,     3,     4,     5,     6,   189,   190,    77,    97,    60,
      41,    42,   205,   195,   197,   151,   126,    27,    28,    92,
    -126,     7,    46,     8,    34,    53,    30,   113,    64,    78,
      78,    71,   118,   107,    52,    39,     7,    63,     8,   154,
     108,   109,   110,    40,   111,    21,    22,    23,   200,   155,
     156,   157,   158,   159,   160,   161,   162,   163,   164,   165,
     166,   167,   168,   169,   170,    68,    69,    70,    41,    71,
     129,   130,   131,   132,    24,    25,    26,  -151,    31,    41,
      42,    60,    99,   100,   101,    48,    71,   140,   141,   116,
     117,   119,   120,    66,    73,     7,    71,    85,    78,    82,
     122,   124,   143,   198,  -127,   153,   204,   203,   208,   210,
     149,   211,   152,   188,   202,   201,    84,   196,   193,    76
};

static const yytype_uint8 yycheck[] =
{
      55,    56,     8,    39,    12,   106,    46,    10,    15,    32,
      80,    19,    29,    15,    12,    19,    20,    48,    11,    42,
      13,    19,    15,     3,    28,     5,     6,     7,     8,     9,
      33,    38,    39,    39,    89,    66,    91,    92,     3,    41,
       5,     6,     7,     8,     9,   100,   101,    15,    15,    15,
      13,    14,   153,   108,   109,    95,   126,    10,    11,    67,
      68,    41,    22,    43,     0,    25,    46,    53,    28,    37,
      37,    37,    58,    20,    24,    45,    41,    27,    43,    41,
      27,    28,    29,    44,    31,    10,    11,    12,   124,    51,
      52,    53,    54,    55,    56,    57,    58,    59,    60,    61,
      62,    63,    64,    65,    66,    33,    34,    35,    13,    37,
      22,    23,    24,    25,    10,    11,    12,    44,   124,    13,
      14,    15,    48,    49,    50,    13,    37,    38,    39,    16,
      17,    16,    17,    30,    42,    41,    37,    21,    37,    41,
      47,    45,    40,    26,    68,    68,    12,   134,    41,   204,
      92,   207,    95,    99,   128,   126,    42,   108,   107,    40
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     3,     5,     6,     7,     8,     9,    41,    43,    70,
      71,    72,    74,    75,    76,    77,    78,   134,   146,   147,
     149,    10,    11,    12,    10,    11,    12,    10,    11,    29,
      46,    71,   135,   136,     0,    70,    32,    42,    73,    45,
      44,    13,    14,    80,    93,    96,    93,   131,    13,   124,
     126,    89,    96,    93,   133,    11,    13,    15,   125,   127,
      15,    92,    95,    96,    93,   132,    30,    70,    33,    34,
      35,    37,   144,    42,   135,   148,   149,    15,    37,   141,
     143,    15,    41,   138,   140,    21,    81,    19,    20,    28,
      79,    12,    67,    79,   128,   129,   130,    15,   141,    48,
      49,    50,   101,   120,   121,   122,   123,    20,    27,    28,
      29,    31,    90,    90,   144,   144,    16,    17,    90,    16,
      17,   141,    47,   137,    45,   142,   143,   139,   140,    22,
      23,    24,    25,    82,    83,    84,    85,    86,    87,    15,
      38,    39,   150,    40,    97,   145,   144,   144,    94,    95,
     144,    79,   128,    68,    41,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64,    65,
      66,   100,   103,   104,   105,   106,   107,   108,   109,   110,
     111,   112,   113,   114,   115,   116,   117,   118,   119,   144,
     144,   122,    99,   145,    98,   144,   150,   144,    26,    91,
     135,   142,   139,    82,    12,   122,   102,   119,    41,    88,
     144,   102
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    69,    70,    70,    71,    71,    71,    71,    72,    72,
      72,    72,    72,    73,    73,    73,    73,    74,    74,    74,
      75,    75,    75,    76,    76,    77,    78,    79,    79,    80,
      80,    80,    80,    81,    81,    82,    82,    83,    83,    83,
      83,    84,    85,    86,    87,    88,    89,    90,    90,    90,
      90,    90,    90,    91,    91,    92,    92,    93,    93,    94,
      94,    95,    95,    96,    96,    96,    97,    98,    99,   100,
     101,   102,   102,   103,   104,   105,   106,   107,   108,   109,
     110,   111,   112,   113,   114,   115,   116,   117,   118,   119,
     119,   119,   119,   119,   119,   119,   119,   119,   119,   119,
     119,   119,   119,   119,   119,   119,   120,   121,   122,   122,
     123,   123,   123,   124,   124,   124,   125,   125,   125,   125,
     126,   127,   128,   128,   129,   129,   130,   130,   131,   131,
     131,   132,   133,   134,   134,   134,   135,   135,   136,   137,
     138,   139,   139,   140,   141,   142,   142,   143,   144,   145,
     146,   147,   148,   149,   150,   150
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     0,     2,     1,     1,     2,     3,     1,     1,
       1,     1,     1,     2,     2,     2,     2,     4,     3,     3,
       3,     3,     3,     3,     3,     4,     1,     2,     2,     2,
       1,     3,     3,     0,     2,     0,     2,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     3,     2,     2,     2,
       1,     1,     2,     0,     2,     1,     1,     2,     2,     1,
       1,     2,     2,     1,     2,     2,     1,     1,     1,     1,
       3,     0,     2,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     2,     2,     0,     2,
       1,     1,     1,     0,     2,     2,     2,     2,     2,     2,
       2,     2,     0,     2,     1,     2,     0,     1,     2,     5,
       4,     1,     2,     2,     3,     5,     3,     1,     1,     1,
       2,     0,     2,     1,     2,     0,     2,     1,     1,     1,
       1,     1,     1,     1,     1,     1
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (rsrc, YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)                                \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;        \
          (Current).first_column = YYRHSLOC (Rhs, 1).first_column;      \
          (Current).last_line    = YYRHSLOC (Rhs, N).last_line;         \
          (Current).last_column  = YYRHSLOC (Rhs, N).last_column;       \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).first_line   = (Current).last_line   =              \
            YYRHSLOC (Rhs, 0).last_line;                                \
          (Current).first_column = (Current).last_column =              \
            YYRHSLOC (Rhs, 0).last_column;                              \
        }                                                               \
    while (0)
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K])


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL

/* Print *YYLOCP on YYO.  Private, do not rely on its existence. */

YY_ATTRIBUTE_UNUSED
static unsigned
yy_location_print_ (FILE *yyo, YYLTYPE const * const yylocp)
{
  unsigned res = 0;
  int end_col = 0 != yylocp->last_column ? yylocp->last_column - 1 : 0;
  if (0 <= yylocp->first_line)
    {
      res += YYFPRINTF (yyo, "%d", yylocp->first_line);
      if (0 <= yylocp->first_column)
        res += YYFPRINTF (yyo, ".%d", yylocp->first_column);
    }
  if (0 <= yylocp->last_line)
    {
      if (yylocp->first_line < yylocp->last_line)
        {
          res += YYFPRINTF (yyo, "-%d", yylocp->last_line);
          if (0 <= end_col)
            res += YYFPRINTF (yyo, ".%d", end_col);
        }
      else if (0 <= end_col && yylocp->first_column < end_col)
        res += YYFPRINTF (yyo, "-%d", end_col);
    }
  return res;
 }

#  define YY_LOCATION_PRINT(File, Loc)          \
  yy_location_print_ (File, &(Loc))

# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value, Location, rsrc); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, tf_fuzz_info *rsrc)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  YYUSE (yylocationp);
  YYUSE (rsrc);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, tf_fuzz_info *rsrc)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  YY_LOCATION_PRINT (yyoutput, *yylocationp);
  YYFPRINTF (yyoutput, ": ");
  yy_symbol_value_print (yyoutput, yytype, yyvaluep, yylocationp, rsrc);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, YYLTYPE *yylsp, int yyrule, tf_fuzz_info *rsrc)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                       , &(yylsp[(yyi + 1) - (yynrhs)])                       , rsrc);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, yylsp, Rule, rsrc); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep, YYLTYPE *yylocationp, tf_fuzz_info *rsrc)
{
  YYUSE (yyvaluep);
  YYUSE (yylocationp);
  YYUSE (rsrc);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Location data for the lookahead symbol.  */
YYLTYPE yylloc
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
  = { 1, 1, 1, 1 }
# endif
;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (tf_fuzz_info *rsrc)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.
       'yyls': related to locations.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    /* The location stack.  */
    YYLTYPE yylsa[YYINITDEPTH];
    YYLTYPE *yyls;
    YYLTYPE *yylsp;

    /* The locations where the error started and ended.  */
    YYLTYPE yyerror_range[3];

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;
  YYLTYPE yyloc;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N), yylsp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yylsp = yyls = yylsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  yylsp[0] = yylloc;
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;
        YYLTYPE *yyls1 = yyls;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yyls1, yysize * sizeof (*yylsp),
                    &yystacksize);

        yyls = yyls1;
        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
        YYSTACK_RELOCATE (yyls_alloc, yyls);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;
      yylsp = yyls + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END
  *++yylsp = yylloc;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];

  /* Default location.  */
  YYLLOC_DEFAULT (yyloc, (yylsp - yylen), yylen);
  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 3:
#line 379 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Lines:  Line number " << dec << yylineno << "." << endl;)
            /* Re-randomize objects we parse into: */
            expect = expect_info();
            set_data = set_data_info();
            parsed_asset = asset_name_id_info();
            policy_info = key_policy_info();
        }
#line 1917 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 4:
#line 390 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Purpose line:  " << flush;)
            set_purp_str (yytext, rsrc);
            IVM(cout << rsrc->test_purpose << endl;)
            /* TODO:  Is there much/any value in turning this back on?  The
                      constructor clear()s them out, and run-time errors observed
                      under Visual Studio...
               Just a precaution to make sure that these vectors start out empty.
               Should inherently be, but purpose is typically specified first:
            parsed_asset.asset_id_n_vector.clear();
            parsed_asset.asset_name_vector.clear(); */
            /* Re-randomize or re-initialize objects we parse into: */
            purpose_defined = true;
            expect = expect_info();
            set_data = set_data_info();
            parsed_asset = asset_name_id_info();
            policy_info = key_policy_info();
            target_barrier = "";
        }
#line 1941 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 5:
#line 409 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            /* TODO:  This code may not won't work with "secure hash neq ..." */
            IVM(cout << "Block of lines." << endl;)
            /* "Statisticalize" :-) the vector of template lines, then crank
               the selected lines in order here. */
            randomize_template_lines (shuffle_not_pick,
                low_nmbr_lines, high_nmbr_lines, exact_nmbr_lines,
                template_block_vector, block_order, rsrc
            );
            /* Vector block_order contains the sequence of template lines to be
               realized, in order.  Pop the indicated template line off the
               vector and generate code from it: */
            k = 0;  /* ID adder to at least help ensure uniqueness */
            for (int i : block_order) {
                templateLin = template_block_vector[i];
                /* Note that temLin will have its fields filled in already. */
                interpret_template_line (
                    templateLin, rsrc, set_data, random_asset,
                    assign_data_var_specified, expect, policy_info,
                    print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                    yes_create_call,  /* did not create call nor asset earlier */
                    yes_create_asset,
                    dont_fill_in_template,  /* but did fill it all in before */
                    0
                );
                k++;
                for (add_expect = 0;  add_expect < rsrc->calls.size();  ++add_expect) {
                    if (!(rsrc->calls[add_expect]->exp_data.expected_results_saved)) {
                        templateLin->expect.copy_expect_to_call (rsrc->calls[add_expect]);
                        templateLin->expect.expected_results_saved = true;
                    }
                }
            }
            templateLin->asset_info.asset_id_n_vector.clear();
            templateLin->asset_info.asset_name_vector.clear();
            /* Done.  Empty out the "statisticalization" vector: */
            block_order.clear();
            /* Empty out the vector of template lines; no longer needed. */
            template_block_vector.clear();
            --nesting_level;
            IVM(cout << "Finished coding block of lines." << endl;)
        }
#line 1988 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 6:
#line 451 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Command with no expect:  \"" << flush;)
            if (!purpose_defined) {
                cerr << endl << endl
                     << "Error:  Please begin your test with the \"purpose\" "
                     << "directive.  \n        For example, "
                     << "\"purpose to exercise crypto and SST...\"" << endl;
                exit (1024);
            }
            if (nesting_level == 0) {  /* if laying down the code now... */
                for (add_expect = 0;  add_expect < rsrc->calls.size();  ++add_expect) {
                    if (!(rsrc->calls[add_expect]->exp_data.expected_results_saved)) {
                        templateLin->expect.copy_expect_to_call (rsrc->calls[add_expect]);
                        templateLin->expect.expected_results_saved = true;
                    }
                }
                delete templateLin;  /* done with this template line */
            } else {
                /* The template line is now fully decoded, so stuff it onto
                   vector of lines to be "statisticalized": */
                template_block_vector.push_back (templateLin);
            }
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2017 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 7:
#line 475 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            /* (This is the same as for command SEMICOLON, other than the IVM.) */
            IVM(cout << "Command with expect:  \"" << flush;)
            if (!purpose_defined) {
                cerr << endl << endl
                     << "Error:  Please begin your test with the \"purpose\" "
                     << "directive.  \n        For example, "
                     << "\"purpose to exercise crypto and SST...\"" << endl;
                exit (1024);
            }
            if (nesting_level == 0) {
                for (add_expect = 0;  add_expect < rsrc->calls.size();  ++add_expect) {
                    if (!(rsrc->calls[add_expect]->exp_data.expected_results_saved)) {
                        templateLin->expect.copy_expect_to_call (rsrc->calls[add_expect]);
                        templateLin->expect.expected_results_saved = true;
                    }
                }
                delete templateLin;
            } else {
                template_block_vector.push_back (templateLin);
            }
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2045 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 8:
#line 501 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Set command:  \"" << yytext << "\"" << endl;)
        }
#line 2053 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 9:
#line 504 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Remove command:  \"" << yytext << "\"" << endl;)
        }
#line 2061 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 10:
#line 507 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Read command:  \"" << yytext << "\"" << endl;)
        }
#line 2069 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 11:
#line 510 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Security command:  \"" << yytext << "\"" << endl;)
        }
#line 2077 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 12:
#line 513 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Done command:  \"" << yytext << "\"" << endl;)
        }
#line 2085 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 13:
#line 519 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Expect pass clause:  \"" << flush;)
            templateLin->expect.set_pf_pass();
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2095 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 14:
#line 524 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Expect fail clause:  \"" << flush;)
            templateLin->expect.set_pf_fail();
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2105 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 15:
#line 529 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Expect nothing clause:  \"" << flush;)
            templateLin->expect.set_pf_nothing();
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2115 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 16:
#line 534 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Expect error clause:  \"" << flush;)
            templateLin->expect.set_pf_error (identifier);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2125 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 17:
#line 543 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Set SST command:  \"" << yytext << "\"" << endl;)
            templateLin = new set_sst_template_line (rsrc);
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                nesting_level == 0 /* similarly, create asset unless inside {} */,
                yes_fill_in_template, 0
            );
        }
#line 2142 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 18:
#line 555 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Set key command:  \"" << yytext << "\"" << endl;)
            templateLin = new set_key_template_line (rsrc);
            target_barrier = policy_info.asset_2_name;  /* policy */
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                nesting_level == 0 /* similarly, create asset unless inside {} */,
                yes_fill_in_template, 0
            );
        }
#line 2160 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 19:
#line 568 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Set policy command:  \"" << yytext << "\"" << endl;;)
            templateLin = new set_policy_template_line (rsrc);
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                nesting_level == 0 /* similarly, create asset unless inside {} */,
                yes_fill_in_template, 0
            );
        }
#line 2177 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 20:
#line 583 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Read SST command:  \"" << yytext << "\"" << endl;;)
            templateLin = new read_sst_template_line (rsrc);
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                dont_create_asset /* if no such asset exists, fail the call */,
                yes_fill_in_template, 0
            );
        }
#line 2194 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 21:
#line 595 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Read key command:  \"" << yytext << "\"" << endl;;)
            templateLin = new read_key_template_line (rsrc);
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                dont_create_asset /* if no such asset exists, fail the call */,
                yes_fill_in_template, 0
            );
        }
#line 2211 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 22:
#line 607 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Read policy command:  \"" << yytext << "\"" << endl;;)
            templateLin = new read_policy_template_line (rsrc);
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                dont_create_asset /* if no such asset exists, fail the call */,
                yes_fill_in_template, 0
            );
        }
#line 2228 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 23:
#line 622 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Remove SST command:  \"" << yytext << "\"" << endl;;)
            templateLin = new remove_sst_template_line (rsrc);
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                dont_create_asset /* don't create an asset being deleted */,
                yes_fill_in_template, 0
            );
        }
#line 2245 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 24:
#line 634 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Remove key command:  \"" << yytext << "\"" << endl;;)
            templateLin = new remove_key_template_line (rsrc);
            templateLin->asset_info.set_name (asset_name);  // set in key_asset_name, below
            interpret_template_line (
                templateLin, rsrc, set_data, random_asset,
                assign_data_var_specified, expect, policy_info,
                print_data, hash_data, asset_name, assign_data_var, parsed_asset,
                nesting_level == 0 /* create call unless inside {} */,
                dont_create_asset /* don't create an asset being deleted */,
                yes_fill_in_template, 0
            );
        }
#line 2263 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 25:
#line 649 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
  /* TODO:  This needs to allow not only SST assets, but mix and match with others
             (keys especially) as well. */
            IVM(cout << "Secure hash command:  \"" << yytext << "\"" << endl;)
            templateLin = new security_hash_template_line (rsrc);
            templateLin->asset_info.set_name (asset_name);
            templateLin->assign_data_var_specified = assign_data_var_specified;
            templateLin->assign_data_var.assign (assign_data_var);
            templateLin->expect = expect;
            templateLin->print_data = print_data;
            templateLin->hash_data = hash_data;
            templateLin->random_asset = random_asset;
            /* Hash checks are different from the rest in that there's a single
               "call" -- not a PSA call though -- for all of the assets cited in the
               template line.  In *other* cases, create a single call for *each*
               asset cited by the template line, but not in this case. */
            for (auto as_name : parsed_asset.asset_name_vector) {
                /* Also copy into template line object's local vector: */
                 templateLin->asset_info.asset_name_vector.push_back (as_name);
            }
            /* Don't need to locate the assets, so no searches required. */
            templateLin->expect.data_var = var_name;
            templateLin->setup_call (set_data, set_data.random_data, yes_fill_in_template,
                                     nesting_level == 0, templateLin, rsrc   );
            parsed_asset.asset_name_vector.clear();


        }
#line 2296 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 26:
#line 679 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            if (nesting_level != 0) {
                cerr << "\n\"done\" only available at outer-most { } nesting level."
                     << endl;
                exit (702);
            } else {
                YYACCEPT;
            }
        }
#line 2310 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 27:
#line 691 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Create from literal data:  \"" << flush;)
            set_data.random_data = false;
            set_data.string_specified = true;
            set_data.literal_data_not_file = true;
            literal.erase(0,1);  // zap the ""s
            literal.erase(literal.length()-1,1);
            literal_data.assign (literal);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2325 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 28:
#line 701 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* TF-Fuzz supplies random data */
            IVM(cout << "Create from random data" << endl;)
            set_data.randomize();
            literal.assign (set_data.get());  /* just in case something uses literal */
            set_data.random_data = true;
            set_data.string_specified = false;
        }
#line 2337 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 30:
#line 713 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-create from random data (no 'data *')" << endl;)
            set_data.randomize();
            literal.assign (set_data.get());  /* just in case something uses literal */
        }
#line 2347 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 31:
#line 718 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* set from variable */
            IVM(cout << "SST-set set from variable:  \"" << flush;)
            assign_data_var.assign (identifier);
            assign_data_var_specified = true;
            expect.data_specified = false;
            expect.data_var_specified = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2360 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 32:
#line 726 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            set_data.literal_data_not_file = set_data.random_data = false;
            IVM(cout << "SST-create from file:  " << yytext << "\"" << endl;)
            /* TODO:  Need to decide whether the concept of using files to set SST
                       asset values has meaning, and if so, write code to write code to
                       set data appropriately from the file. */
        }
#line 2372 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 34:
#line 737 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST creation flags" << endl;)
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2381 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 36:
#line 745 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST creation flag" << endl;)
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2390 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 41:
#line 753 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            set_data.flags_string = "PSA_STORAGE_FLAG_NONE";
                /* TODO:  grab from boilerplate */
            IVM(cout << "SST no storage flag:  " << yytext << "\"" << endl;)
        }
#line 2400 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 42:
#line 760 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            set_data.flags_string = "PSA_STORAGE_FLAG_WRITE_ONCE";
                /* TODO:  grab from boilerplate */
            IVM(cout << "SST write-once flag:  " << yytext << "\"" << endl;)
        }
#line 2410 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 43:
#line 767 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            set_data.flags_string = "PSA_STORAGE_FLAG_NO_REPLAY_PROTECTION";
                /* TODO:  grab from boilerplate */
            IVM(cout << "SST no-replay-protection flag:  "
                     << yytext << "\"" << endl;)
        }
#line 2421 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 44:
#line 775 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            set_data.flags_string = "PSA_STORAGE_FLAG_NO_CONFIDENTIALITY";
                /* TODO:  grab from boilerplate */
            IVM(cout << "SST no-confidentiality flag:  " << yytext
                     << "\"" << endl;)
        }
#line 2432 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 45:
#line 784 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-data offset:  \"" << flush;)
            set_data.data_offset = atol(yytext);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2442 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 46:
#line 793 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-read arguments:  " << yytext << "\"" << endl;)
        }
#line 2450 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 47:
#line 799 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* dump to variable */
            IVM(cout << "Read dump to variable:  \"" << flush;)
            assign_data_var.assign (identifier);
            assign_data_var_specified = true;
            expect.data_specified = false;
            expect.data_var_specified = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2463 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 48:
#line 807 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* check against variable */
            IVM(cout << "Read check against variable:  \""
                     << yytext << "\"" << endl;)
            set_data.set (literal);
            assign_data_var_specified = false;
            expect.data_specified = false;
            expect.data_var_specified = true;
            expect.data_var = identifier;
        }
#line 2477 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 49:
#line 816 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* check against literal */
            IVM(cout << "Read check against literal:  " << flush;)
            expect.data.assign (literal);
            expect.data.erase(0,1);    // zap the ""s
            expect.data.erase(expect.data.length()-1,1);
            assign_data_var_specified = false;  /* don't read variable */
            expect.data_specified = true;  /* check against literal data */
            expect.data_var_specified = false;  /* don't check against variable */
            IVM(cout << yytext << endl;)
        }
#line 2492 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 50:
#line 826 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* print out content in test log */
            IVM(cout << "Read log to test log:  \"" << flush;)
            /* TODO:  set_data content probably doesn't need to be set here;
                       constructor probably sets it fine. */
            set_data.random_data = false;
            set_data.literal_data_not_file = true;
            assign_data_var_specified = false;
            expect.data_specified = false;
            expect.data_var_specified = false;
            print_data = true;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2509 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 51:
#line 838 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* hash the data and save for later comparison */
            IVM(cout << "Read hash for future data-leak detection:  \"" << flush;)
            /* TODO:  set_data content probably doesn't need to be set here;
                       constructor probably sets it fine. */
            set_data.random_data = false;
            set_data.literal_data_not_file = true;
            assign_data_var_specified = false;
            expect.data_specified = false;
            expect.data_var_specified = false;
            hash_data = true;
            rsrc->include_hashing_code = true;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2527 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 52:
#line 851 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {  /* dump to file */
            IVM(cout << "Read dump to file:  \""
                     << yytext << "\"" << endl;)
            set_data.literal_data_not_file = set_data.random_data = false;
        }
#line 2537 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 54:
#line 860 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST data offset" << endl;)
            set_data.data_offset = atol(yytext);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2547 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 56:
#line 868 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-remove arguments:  \""
                     << yytext << "\"" << endl;)
        }
#line 2556 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 57:
#line 875 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Asset identifier list:  \"" << flush;)
            random_name = false;
            asset_name.assign (identifier);  /* TODO:  Not sure this ultimately has any effect... */
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2569 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 58:
#line 883 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Asset random identifier:  \"" << flush;)
            random_name = true;
            rand_data_length = 4 + (rand() % 5);
            gib.word (false, gib_buff, gib_buff + rand_data_length - 1);
            aid.assign (gib_buff);
            parsed_asset.asset_name_vector.push_back (aid);
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2585 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 59:
#line 896 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Single existing asset by name:  \"" << flush;)
            random_name = false;
            policy_info.asset_3_name.assign (identifier);
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2598 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 61:
#line 908 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Asset random active:  \"" << flush;)
            random_asset = psa_asset_usage::active;
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2609 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 62:
#line 914 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Asset random deleted:  \"" << flush;)
            random_asset = psa_asset_usage::deleted;
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2620 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 64:
#line 924 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-asset UID list:  \"" << flush;)
            random_name = false;
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = true;
            parsed_asset.id_n_specified = true;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2633 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 65:
#line 932 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-asset random UID:  \"" << flush;)
            parsed_asset.id_n_not_name = true;
            random_name = false;
            nid = 100 + (rand() % 10000);
            parsed_asset.asset_id_n_vector.push_back (nid);
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2647 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 66:
#line 944 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-asset-create file path:  \"" << flush;)
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2656 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 67:
#line 951 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Read-arguments variable name:  \"" << flush;)
            var_name = yytext;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2666 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 68:
#line 959 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "SST-asset dump-file path:  \"" << flush;)
            set_data.file_path = yytext;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2676 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 69:
#line 967 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key size:  \"" << flush;)
            policy_info.n_bits = atol(yytext);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2686 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 72:
#line 978 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-policy usages at line number " << dec << yylineno
                     << "." << endl;)
        }
#line 2695 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 73:
#line 984 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.exportable = true;
            IVM(cout << "Exportable key true:  " << yytext << "\"" << endl;)
        }
#line 2704 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 74:
#line 990 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.exportable = false;
            IVM(cout << "Non-exportable key:  " << yytext << "\"" << endl;)
        }
#line 2713 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 75:
#line 996 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.copyable = true;
            IVM(cout << "Copyable key true:  " << yytext << "\"" << endl;)
        }
#line 2722 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 76:
#line 1002 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.copyable = false;
            IVM(cout << "Non-copyable key:  " << yytext << "\"" << endl;)
        }
#line 2731 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 77:
#line 1008 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_encrypt = true;
            IVM(cout << "Encryption key true:  " << yytext << "\"" << endl;)
        }
#line 2740 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 78:
#line 1014 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_encrypt = false;
            IVM(cout << "Non-encryption key:  " << yytext << "\"" << endl;)
        }
#line 2749 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 79:
#line 1020 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_decrypt = true;
            IVM(cout << "Decryption key true:  " << yytext << "\"" << endl;)
        }
#line 2758 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 80:
#line 1026 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_decrypt = false;
            IVM(cout << "Non-decryption key:  " << yytext << "\"" << endl;)
        }
#line 2767 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 81:
#line 1032 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_sign = true;
            IVM(cout << "Signing key true:  " << yytext << "\"" << endl;)
        }
#line 2776 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 82:
#line 1038 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_sign = false;
            IVM(cout << "Non-signing key:  " << yytext << "\"" << endl;)
        }
#line 2785 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 83:
#line 1044 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_verify = true;
            IVM(cout << "Verify key true:  " << yytext << "\"" << endl;)
        }
#line 2794 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 84:
#line 1050 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.can_verify = false;
            IVM(cout << "Non-verify key:  " << yytext << "\"" << endl;)
        }
#line 2803 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 85:
#line 1056 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.derivable = true;
            IVM(cout << "Derivable key true:  " << yytext << "\"" << endl;)
        }
#line 2812 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 86:
#line 1062 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.derivable = false;
            IVM(cout << "Non-derivable key:  " << yytext << "\"" << endl;)
        }
#line 2821 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 87:
#line 1068 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.persistent = true;
            IVM(cout << "Persistent key:  " << yytext << "\"" << endl;)
        }
#line 2830 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 88:
#line 1074 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            policy_info.persistent = false;
            IVM(cout << "Volatile key:  " << yytext << "\"" << endl;)
        }
#line 2839 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 105:
#line 1083 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Policy usage:  " << yytext << "\"" << endl;)
        }
#line 2847 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 106:
#line 1089 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            // Change type identifier, e.g., from "raw_data" to PSA_KEY_TYPE_RAW_DATA:
            identifier = formalize (identifier, "PSA_KEY_TYPE_");
            policy_info.key_type = identifier;
            IVM(cout << "Policy type:  \""
                     << policy_info.key_type << "\"" << endl;)
      }
#line 2859 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 107:
#line 1098 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            // Change type identifier, e.g., from "sha_256" to PSA_ALG_SHA_256:
            identifier = formalize (identifier, "PSA_ALG_");
            policy_info.key_algorithm = identifier;
            IVM(cout << "Policy algorithm:  \""
                     << policy_info.key_algorithm << "\"" << endl;)
      }
#line 2871 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 109:
#line 1108 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-policy specs at line number " << dec << yylineno
                     << "." << endl;)
        }
#line 2880 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 114:
#line 1118 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "policy-asset identifier list:  \"" << flush;)
            random_name = false;
            asset_name.assign (identifier);  /* TODO:  Not sure this ultimately has any effect... */
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2893 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 115:
#line 1126 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "policy-asset random identifier:  \"" << flush;)
            random_name = true;
            rand_data_length = 2 + (rand() % 10);
            gib.word (false, gib_buff, gib_buff + rand_data_length - 1);
            aid.assign (gib_buff);
            parsed_asset.asset_name_vector.push_back (aid);
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2909 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 116:
#line 1140 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "policy-asset identifier list:  \"" << flush;)
            random_name = false;
            policy_info.get_policy_from_key = false;
            asset_name.assign (identifier);  /* TODO:  Not sure this ultimately has any effect... */
            parsed_asset.asset_name_vector.push_back (identifier);
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2924 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 117:
#line 1150 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "policy-asset random active:  \"" << flush;)
            policy_info.get_policy_from_key = false;
            random_asset = psa_asset_usage::active;
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2936 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 118:
#line 1157 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "policy-asset random deleted:  \"" << flush;)
            policy_info.get_policy_from_key = false;
            random_asset = psa_asset_usage::deleted;
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2948 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 119:
#line 1164 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "policy-asset specified by key:  \"" << flush;)
            policy_info.get_policy_from_key = true;
            random_name = false;
            asset_name.assign (identifier);  /* ask this key what it's policy is */
            random_asset = psa_asset_usage::all;  /* don't randomly choose existing asset */
            parsed_asset.id_n_not_name = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 2962 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 120:
#line 1176 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Policy-create arguments:  \"" << yytext << "\"" << endl;)
        }
#line 2970 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 121:
#line 1182 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Policy-read arguments:  " << yytext << "\"" << endl;)
        }
#line 2978 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 123:
#line 1189 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-set sources at Line number "
                     << yytext << "\"" << endl;)
        }
#line 2987 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 124:
#line 1196 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-set sources, literal or random data:  "
                     << yytext << "\"" << endl;)
        }
#line 2996 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 125:
#line 1200 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-set sources, explicitly-specified policy name:  "
                     << flush;)
            policy_info.asset_2_name = identifier;  /* policy */
            /* Make note that key data (key material) was not specified: */
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3008 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 127:
#line 1211 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key data, literal or random data:  "
                     << yytext << "\"" << endl;)
        }
#line 3017 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 128:
#line 1218 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-create from data, policy, or nothing (default):  \""
                     << yytext << "\"" << endl;)
            policy_info.copy_key = false;
            policy_info.implicit_policy = false;
        }
#line 3028 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 129:
#line 1224 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-copy from other key:  \"" << flush;)
            policy_info.asset_2_name = identifier;  /* policy */
            policy_info.copy_key = true;
            policy_info.implicit_policy = false;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3040 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 130:
#line 1231 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-create directly specifying policy attributes (implicit policy):  \""
                     << yytext << "\"" << endl;)
            policy_info.copy_key = false;
            policy_info.implicit_policy = true;
            cerr << "\nError:  Defining keys with implicit policies is not yet implemented."
                 << endl;
            exit (772);
        }
#line 3054 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 131:
#line 1243 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key-remove arguments:  \""
                     << yytext << "\"" << endl;)
        }
#line 3063 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 132:
#line 1250 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Key dump:  \"" << yytext << "\"" << endl;)
        }
#line 3071 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 133:
#line 1257 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Shuffled block:  \"" << flush;)
            if (nesting_level > 1) {
                cerr << "\nError:  Sorry, currently only one level of { } "
                     << "nesting is allowed." << endl;
                exit (500);
            }
            shuffle_not_pick = true;
            low_nmbr_lines = high_nmbr_lines = 0;  /* not used, but... */
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3087 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 134:
#line 1268 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Fixed number of lines from block:  \"" << flush;)
            shuffle_not_pick = false;
            /* low_nmbr_lines and high_nmbr_lines are set below. */
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3098 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 135:
#line 1274 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Range number of lines from block:  \"" << flush;)
            if (nesting_level > 1) {
                cerr << "\nError:  Sorry, currently only one level of { } "
                     << "nesting is allowed." << endl;
                exit (502);
            }
            shuffle_not_pick = false;
            /* low_nmbr_lines and high_nmbr_lines are set below. */
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3114 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 136:
#line 1288 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Block content:  \"" << yytext << "\"" << endl;)
        }
#line 3122 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 137:
#line 1291 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Single-line would-be-block content:  \"" << flush;)
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3131 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 138:
#line 1298 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Open brace:  \"" << flush;)
            template_block_vector.clear();  // clean slate of template lines
            nesting_level = 1;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3142 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 139:
#line 1307 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Close brace:  " << flush;)
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3151 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 143:
#line 1324 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "ASSET_NUMBER:  \"" << flush;)
            nid = atol(yytext);
            parsed_asset.asset_id_n_vector.push_back (nid);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3162 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 147:
#line 1344 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "ASSET_IDENTIFIER:  \"" << flush;)
            aid = identifier = yytext;
            parsed_asset.asset_name_vector.push_back (aid);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3173 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 148:
#line 1353 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "IDENTIFIER:  \"" << flush;)
            identifier = yytext;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3183 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 149:
#line 1361 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "FILE_PATH:  \"" << flush;)
            set_data.file_path = yytext;
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3193 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 150:
#line 1371 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Exact number of random template lines:  \"" << flush;)
            low_nmbr_lines = high_nmbr_lines = exact_nmbr_lines = number;
            ++nesting_level;
            IVM(cout << number << "\"" << endl;)
        }
#line 3204 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 151:
#line 1380 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Least number of random template lines:  \"" << flush;)
            low_nmbr_lines = number;
            IVM(cout << number << "\"" << endl;)
        }
#line 3214 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 152:
#line 1388 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "Most number of random template lines:  \"" << flush;)
            high_nmbr_lines = number;
            ++nesting_level;
            IVM(cout << number << "\"" << endl;)
        }
#line 3225 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 153:
#line 1399 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
            IVM(cout << "NUMBER:  \"" << flush;)
            number = atol(yytext);
            IVM(cout << yytext << "\"" << endl;)
        }
#line 3235 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 154:
#line 1407 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
          IVM(cout << "LITERAL string:  " << flush;)
          literal = yytext;
          literal_is_string = true;
          IVM(cout << yytext << endl;)
        }
#line 3246 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;

  case 155:
#line 1413 "parser/tf_fuzz_grammar.y" /* yacc.c:1646  */
    {
          IVM(cout << "LITERAL hex-value list:  " << flush;)
          literal = yytext;
          literal_is_string = false;
          IVM(cout << yytext << endl;)
        }
#line 3257 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
    break;


#line 3261 "parser/tf_fuzz_grammar.tab.cpp" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;
  *++yylsp = yyloc;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (rsrc, YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (rsrc, yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }

  yyerror_range[1] = yylloc;

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval, &yylloc, rsrc);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  yyerror_range[1] = yylsp[1-yylen];
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;

      yyerror_range[1] = *yylsp;
      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp, yylsp, rsrc);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  yyerror_range[2] = yylloc;
  /* Using YYLLOC is tempting, but would change the location of
     the lookahead.  YYLOC is available though.  */
  YYLLOC_DEFAULT (yyloc, yyerror_range, 2);
  *++yylsp = yyloc;

  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (rsrc, YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, &yylloc, rsrc);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp, yylsp, rsrc);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 1422 "parser/tf_fuzz_grammar.y" /* yacc.c:1906  */



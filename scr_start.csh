#!/bin/csh
#
#	Mike J. Hopkins
#	Genesis 2000 scr_start.csh
#	revision 1.4.1
#	
#	This version of the scr_start.csh script includes
#	support for the Python programming language, 
#	as well as Java and binary execuables...
#
#
if($?GENESIS_DIR)then
  set _genesis_root=$GENESIS_DIR
else
  set _genesis_root=/genesis
endif

if($?GENESIS_EDIR)then
  set _genesis_edir=$GENESIS_EDIR
else
  set _genesis_edir=e$GENESIS_VER
endif

if($_genesis_edir =~ /* || $_genesis_edir =~ ?:*)then
  set path=($_genesis_edir/all $path)
else
  set path=($_genesis_root/$_genesis_edir/all $path)
endif

set STATUS=0
set PROG=$1
if(! -e $PROG)then
  set PROG_STATUS=1
  goto end
endif

# define aliases
set DIR_PREFIX='@%#%@'

alias VON 'echo "${DIR_PREFIX}VON";'
alias VOF 'echo "${DIR_PREFIX}VOF";'

alias SU_ON  'echo "${DIR_PREFIX}SU_ON";'
alias SU_OFF 'echo "${DIR_PREFIX}SU_OFF";'

alias PAUSE 'echo "${DIR_PREFIX}PAUSE \!:*"; \\
   set STATUS=$<; set READANS=$<; set PAUSANS=$<; \\
   if ($PAUSANS != "OK") exit'
alias MOUSE 'echo "${DIR_PREFIX}MOUSE \!:*"; \\
   set STATUS=$<; set READANS=$<; set MOUSEANS="$<"'
alias COM 'echo "${DIR_PREFIX}COM \!:*"; \\
   set STATUS=$<; set READANS="$<"; set COMANS=($READANS)'
alias AUX 'echo "${DIR_PREFIX}AUX \!:*"; \\
   set STATUS=$<; set READANS="$<"; set COMANS=($READANS)'

set argv = ($2)

#executing hook script
if(-e $_genesis_root/sys/hooks/script_start.csh)then
   source $_genesis_root/sys/hooks/script_start.csh
endif

# check first line of program
set _HEAD=`head -1 $PROG`
set _EXT=`echo $PROG:e`

if("$_HEAD" =~ *perl*)then
   echo "Executing Perl Program $PROG $argv"
   perl $PROG $argv
   set PROG_STATUS=$status
else if("$_HEAD" =~ *python*)then
   echo "Executing Python Program $PROG $argv"
   python $PROG $argv
   set PROG_STATUS=$status
else if("$_HEAD" =~ *wish*)then
   setenv TCSHONLYSTARTEXES 1
   echo "Executing TCL Program $PROG $argv"
   $_genesis_root/sys/hooks/wish_start.tcl $PROG $argv
   set PROG_STATUS=$status
else if ("$_EXT" =~ [Cc][Ll][Aa][Ss][Ss]) then
   set JPATH  = `echo $PROG:h`
   set JPROG  = `echo $PROG:t`
   set JCLASS = `echo $JPROG:r`
   setenv CLASSPATH $JPATH
   echo "Set CLASSPATH to:  $CLASSPATH"
   echo "Executing JavaClass $JCLASS $argv"
   echo "..."
   java $JCLASS $argv
   set PROG_STATUS=$status
else if ("$_EXT" =~ [Ee][Xx][Ee]) then
   echo "Executing Compiled Program $PROG $argv"
   $PROG $argv
   set PROG_STATUS=$status
else
   echo "Executing C Shell Program $PROG"
   source $PROG
   set PROG_STATUS=$status
endif

end:
exit($PROG_STATUS)
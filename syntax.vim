" Just a sketch
" (suggested Jellybeans colorscheme)

syntax keyword pinealPrimitive polygon group layer window
syntax keyword pinealAttribute translate rotate scale
syntax keyword pinealAttribute line rotation radius position fill stroke
syntax keyword pinealFunction  color
syntax keyword pinealKeyword   alias draw


syntax match pinealBraces "\v[{}\()\[\]]"
syntax match pinealSplit  "\v:"

syntax match pinealComment ";.*$"

syntax match pinealNumber "\v<\d+>"
syntax match pinealNumber "\v<\d+\.\d+>"
syntax match pinealNumber "\v<\d*\.?\d+([Ee]-?)?\d+>"
syntax match pinealNumber "\v<0x\x+([Pp]-?)?\x+>"
syntax match pinealNumber "\v<0b[01]+>"
syntax match pinealNumber "\v<0o\o+>"

syntax match pinealOperator "\v\*"
syntax match pinealOperator "\v/"
syntax match pinealOperator "\v\+"
syntax match pinealOperator "\v-"
syntax match pinealOperator "\v\?"
syntax match pinealOperator "\v\*\="
syntax match pinealOperator "\v/\="
syntax match pinealOperator "\v\+\="
syntax match pinealOperator "\v-\="



highlight link pinealPrimitive SpecialChar
highlight link pinealKeyword   Keyword

highlight link pinealName      Function
highlight link pinealAttribute Identifier
highlight link pinealFunction  Function
highlight link pinealBraces    Delimiter
highlight link pinealSplit     Keyword
highlight link pinealComment   Comment

highlight link pinealNumber    Number
highlight link pinealOperator  Operator

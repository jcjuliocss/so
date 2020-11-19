#!/bin/bash

login_entrada="$1"
senha_entrada="$2"


while IFS='-' read -r linha || [[ -n "$linha" ]]; do
	login=`echo $linha | cut -f1 -d'-'`
	senha=`echo $linha | cut -f2 -d'-'`
	if [ "$login_entrada" == "$login" ]
	then
		if [ "$senha_entrada" = "$senha" ]
		then
			echo "aceito"
			exit 1
		fi
	fi
done < "usuarios.txt"

echo "rejeitado"
